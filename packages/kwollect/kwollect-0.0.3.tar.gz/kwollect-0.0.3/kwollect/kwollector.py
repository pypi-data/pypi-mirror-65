#!/usr/bin/python3

import sys
import time
import re
import random
import asyncio
import glob
import json
import traceback
import logging as log

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, unquote

import yaml
import aiopg
import psycopg2
import pysnmp.hlapi.asyncio as snmp
from pysnmp.proto.rfc1905 import NoSuchObject, NoSuchInstance
from pyonf import pyonf


config = """
metrics_dir: /etc/kwollect/metrics.d/
db_host: localhost
db_name: kwdb
db_user: kwuser
db_password: changeme
log_level: warning
"""
config = pyonf(config)

log.basicConfig(
    level=str.upper(config.get("log_level", "warning")),
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)


def main():
    # asyncio.run(main(), debug=config.get("log_level") == "debug")
    asyncio.run(async_main())


async def async_main():

    init_snmp()
    await init_psql()

    metrics = load_metric_descriptions(config["metrics_dir"])
    metrics_per_device = merge_metrics_per_device_and_protocol(metrics)
    metrics_per_device = await parse_snmp_iface_metrics(metrics_per_device)

    for device, metrics in metrics_per_device.items():
        if device.protocol == "snmp":
            process_method = process_snmp_host
        elif device.protocol == "ipmisensor":
            process_method = process_ipmisensor_host
        else:
            log.warning("Unsupported protocol for device %s", device)
            continue

        req_interval_ms = min(metric.update_every for metric in metrics)

        log.info(
            "Scheduling %s requests every %s milli-seconds", device, req_interval_ms
        )
        asyncio.create_task(
            schedule_every(
                req_interval_ms / 1000,
                process_method,
                (device, metrics),
                task_name=f"{device.protocol}@{device.hostname}",
            )
        )

    # Waiting for infinity, but catching failing tasks
    ended_task, _ = await asyncio.wait(
        asyncio.all_tasks(), return_when=asyncio.FIRST_COMPLETED
    )
    log.error("Scheduling task %s as ended, that should not happen", ended_task)
    sys.exit(1)


@dataclass(frozen=True)
class MetricDevice:
    """A device to be queried by some protocol"""

    hostname: str
    protocol: str
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class MetricDescription:
    """A metrics to fetch"""

    name: str
    device_id: str
    url: str
    path: str = ""
    update_every: int = 10000
    optional: bool = False
    device_alias: Optional[str] = None
    scale_factor: Optional[float] = None

    def __post_init__(self):
        _url = urlparse(self.url)
        self.device = MetricDevice(
            hostname=_url.hostname,
            protocol=_url.scheme,
            port=_url.port,
            username=unquote(_url.username) if _url.username else None,
            password=unquote(_url.password) if _url.password else None,
        )
        if _url.path:
            self.path = re.sub(r"^/", "", unquote(_url.path))


def load_metric_descriptions(metrics_dir):
    """Load metric descriptions from directory"""
    log.debug("Loading metric descriptions from %s", metrics_dir)
    metrics = []
    for description_file in glob.glob(metrics_dir + "/*"):
        with open(description_file) as f:
            try:
                ydata = yaml.safe_load(f.read())
                if isinstance(ydata, list):
                    metrics += [MetricDescription(**d) for d in ydata]
                elif isinstance(ydata, dict):
                    metrics.append(MetricDescription(**ydata))
                elif ydata is None:
                    pass
                else:
                    raise Exception("Unparsable metric description")
            except Exception as ex:
                log.error("Error when reading %s content", description_file)
                log.error("%s: %s", repr(ex), str(ex))
                log.error(traceback.format_exc())
                sys.exit(1)

    log.debug("\n  ".join((str(metric) for metric in metrics)))
    return metrics


def merge_metrics_per_device_and_protocol(metrics):
    """Merge list of metrics per involved device and returns a Dict[MetricDevice, MetricDescription]"""
    metrics_per_device = {}
    for metric in metrics:
        if metric.device not in metrics_per_device:
            metrics_per_device[metric.device] = []
        metrics_per_device[metric.device].append(metric)
    return metrics_per_device


async def schedule_every(
    period, func_name, args=[], kwargs={}, delayed_start=True, task_name=None
):
    """Schedule func_name to run every period"""

    TIMEOUT_MAX_COUNT = 5

    if not task_name:
        task_name = (
            f"{func_name}("
            + ", ".join(args)
            + ", "
            + ", ".join(f"{k}={v}" for k, v in kwargs.items())
        )

    if delayed_start and period > 1:
        await asyncio.sleep(random.randint(0, int(period * 1000)) / 1000)

    log.debug("Start task scheduler for %s", task_name)

    while True:

        task = asyncio.create_task(func_name(*args, **kwargs))
        task.task_name = task_name + "/" + str(int(time.time()))
        log.debug("Task created: %s", task.task_name)
        timeout_count = 0

        while True:
            await asyncio.sleep(period)
            if not task.done():
                timeout_count += 1
                if timeout_count >= TIMEOUT_MAX_COUNT:
                    log.warning(
                        "Cancelling task that did not finished after %s periods of %s sec: %s",
                        TIMEOUT_MAX_COUNT,
                        period,
                        task.task_name,
                    )
                    task.cancel()
                    break
                log.warning(
                    "Waiting for task that did not finish under its period of %s sec: %s",
                    period,
                    task.task_name,
                )
            elif task.exception():
                log.warning(
                    "Task had an exception %s, scheduling new one: %s",
                    task.exception(),
                    task.task_name,
                )
                task.print_stack()
                break
            else:
                log.debug("Task correctly finished: %s", task.task_name)
                break


async def process_snmp_host(device, metrics):
    """Process one query for metrics on a device using SNMP"""

    log.debug(
        "Starting process_snmp_host for task: %s", asyncio.current_task().task_name
    )

    metrics = await filter_optional_metrics(device, metrics)
    if not metrics:
        log.info(
            "Nothing to process after filtering optional metrics for SNMP host %s",
            device.hostname,
        )
        return

    # "oids" maps SNMP OID with the associated metric position in "metrics" list
    # (the OID must be stored as string, without heading "." as in PySNMP)
    oids = {metric.path: metric_idx for metric_idx, metric in enumerate(metrics)}

    # "results" stores SNMP request result and has same length and ordering than metrics
    # (None value is used if result is not available for a metric)
    results = [None] * len(metrics)

    timestamp = time.time()
    _results = await make_snmp_request(
        device.hostname, "get", oids.keys(), device.username
    )
    log.debug(
        "snmpget request executed in %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    for oid, value in _results.items():
        results[oids[oid]] = value

    if not any(results):
        log.warning("Nothing to process for SNMP host %s", device.hostname)
        return

    values = [(timestamp, result) for result in results]
    await insert_metrics_values(metrics, values)


async def process_ipmisensor_host(device, metrics):
    """Process one query for metrics on a device using IPMI"""

    log.debug(
        "Starting process_ipmisensor_host for task: %s",
        asyncio.current_task().task_name,
    )

    metrics = await filter_optional_metrics(device, metrics)
    if not metrics:
        log.info(
            "Nothing to process after filtering optional metrics for IPMI host %s",
            device.hostname,
        )
        return

    timestamp = time.time()

    command = f"/usr/sbin/ipmi-sensors -D LAN_2_0 -h {device.hostname}"
    if device.username:
        command += f" -u {device.username}"
    if device.password:
        command += f" -p {device.password}"
    # command += " -r " + ",".join(metric.path for metric in metrics)
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    log.debug(
        "ipmi-sensor command executed in %s for task: %s",
        time.time() - timestamp,
        asyncio.current_task().task_name,
    )

    if process.returncode != 0:
        log.warning(
            "ipmi-sensor command %s failed for task: %s (%s)",
            command,
            asyncio.current_task().task_name,
            stderr,
        )
        raise ChildProcessError(
            f"Error on ipmi-sensor command for {device.hostname}: {stderr}"
        )

    # parse ipmi-sensor stdout and store values by sensor name and sensor ID.
    # (both ipmi-sensor's ID and name fields may be used in the MetricDescription
    # URL path but some devices use identical names for different sensor, so ID is safer)
    ipmisensor_values = {}
    for ipmisensor_output in stdout.decode().strip().split("\n")[1:]:
        values = [value.strip() for value in ipmisensor_output.split("|")]
        sensor_id, sensor_name, sensor_value = values[0], values[1], values[3]
        ipmisensor_values[sensor_id] = sensor_value
        ipmisensor_values[sensor_name] = sensor_value

    # "results" stores IPMI result and has same length and ordering than metrics
    # (None value is used if result is not available for a metric)
    results = [None] * len(metrics)

    for metric_idx, sensor_name in enumerate(metric.path for metric in metrics):
        if sensor_name not in ipmisensor_values:
            log.warning(
                "Could not find IPMI sensor with name or ID %s on device %s",
                sensor_name,
                device.hostname,
            )
        elif ipmisensor_values[sensor_name] != "N/A":
            results[metric_idx] = ipmisensor_values[sensor_name]

    if not any(results):
        log.warning("Nothing to process for IPMI sensor host %s", device.hostname)
        return

    values = [(timestamp, result) for result in results]
    await insert_metrics_values(metrics, values)


promoted_device = None
promoted_device_lastupdate = -1


async def filter_optional_metrics(device, metrics):
    """Query DB to filter out optional metrics from metrics argument for a device"""
    global promoted_device, promoted_device_lastupdate
    cur_time = int(time.time())
    if cur_time - promoted_device_lastupdate > 0 or promoted_device is None:
        log.debug(
            "Prepare updating promoted devices for task: %s",
            asyncio.current_task().task_name,
        )
        promoted_device_lastupdate = cur_time
        promoted_device = [
            line[0]
            for line in await sql("SELECT device_id FROM promoted_metrics", fetch=True)
        ]
    return [
        metric
        for metric in metrics
        if not metric.optional
        or metric.device_id in promoted_device
        or (metric.device_alias and metric.device_alias in promoted_device)
    ]


async def insert_metrics_values(metrics, values):
    """Insert metrics and associated values into DB"""

    sql_insert = (
        "INSERT INTO metrics(timestamp, device_id, metric_id, value, labels) VALUES\n  "
    )
    sql_labels = {}

    for i, metric in enumerate(metrics):
        timestamp, value = values[i]
        if value:
            sql_insert += f"(to_timestamp({timestamp}), "
            sql_insert += f"'{metric.device_id}', "
            sql_insert += f"'{metric.name}', "
            try:
                value = float(value)
                if metric.scale_factor:
                    value = value * metric.scale_factor
                sql_insert += f"{value}, "
            except ValueError:
                sql_insert += "'NaN', "
                sql_labels.update({"str_value": value})
            if metric.device_alias:
                sql_labels.update({"_device_alias": metric.device_alias})

            if sql_labels:
                sql_insert += f"'{json.dumps(sql_labels)}'"
            else:
                sql_insert += "NULL"

            sql_insert += "),\n  "

    # Remove trailing '),\n  '
    sql_insert = sql_insert[:-4]

    log.debug(sql_insert)
    await sql(sql_insert)


async def parse_snmp_iface_metrics(metrics_per_device):
    """Find real OID of SNMP metrics that use {{ iface }} alias in their URLs"""

    parsed_metrics_per_device = {}

    # Parse metrics with SNMP {{iface}} URL
    for device, metrics in metrics_per_device.items():
        if device.protocol != "snmp":
            parsed_metrics_per_device[device] = metrics
        elif not any(
            metric for metric in metrics if re.findall(r"{{(.*)}}", metric.path)
        ):
            parsed_metrics_per_device[device] = metrics
        else:
            parsed_metrics_per_device[device] = await parse_device_snmp_iface_metrics(
                device, metrics
            )

    # Purge devices that don't have anymore metrics after iface parsing
    parsed_metrics_per_device = {
        device: metrics
        for device, metrics in parsed_metrics_per_device.items()
        if metrics
    }
    return parsed_metrics_per_device


async def parse_device_snmp_iface_metrics(device, metrics):
    """Send SNMP request to retrieve OID suffixes corresponding to metrics' {{ iface }}"""

    log.debug("Getting SNMP IF-MIB::ifDescr values on host %s", device.hostname)
    results = await make_snmp_request(
        device.hostname, "walk", "1.3.6.1.2.1.2.2.1.2", device.username
    )

    for oid, snmp_iface_descr in results.items():
        for metric in metrics:
            metric_iface = re.findall(r"{{(.*)}}", metric.path)
            if metric_iface:
                metric_iface = metric_iface[0].strip()

                if snmp_iface_descr == metric_iface:
                    iface_oid_suffix = oid.replace("1.3.6.1.2.1.2.2.1.2.", "")
                    metric.path = re.sub(r"{{.*}}", iface_oid_suffix, metric.path)
                    log.debug("  %s is %s", metric_iface, iface_oid_suffix)

    new_metrics = []
    for metric in metrics:
        if re.findall(r"{{(.*)}}", metric.path):
            log.warning(
                "SNMP iface %s for %s not converted, deleting metrics",
                metric.path,
                device.hostname,
            )
        else:
            new_metrics.append(metric)
    log.debug(new_metrics)
    return new_metrics


snmp_engine = None


def init_snmp():
    global snmp_engine
    snmp_engine = snmp.SnmpEngine()


psql_pool = None


async def init_psql():
    global psql_pool
    psql_pool = await aiopg.create_pool(
        database=config["db_name"],
        user=config["db_user"],
        password=config["db_password"],
        host=config["db_host"],
        maxsize=75,
    )


async def sql(cmd, fetch=False):
    ret = []
    qtime = time.time()
    try:
        async with psql_pool.acquire() as conn:
            async with conn.cursor() as cur:
                log.debug(cur)
                log.debug(
                    "Got SQL worker after %s (free %s/%s) for task: %s",
                    time.time() - qtime,
                    psql_pool.freesize,
                    psql_pool.size,
                    asyncio.current_task().task_name,
                )
                qtime = time.time()
                await cur.execute(cmd)
                if fetch:
                    ret = await cur.fetchall()
    except psycopg2.ProgrammingError as ex:
        log.warning("Error when performing SQL request %s", cmd)
        log.warning("%s: %s", repr(ex), str(ex))
        log.warning(traceback.format_exc())
    log.debug(
        "Returing SQL %s after %s (free %s/%s) for task: %s",
        "SELECT" if fetch else "INSERT",
        time.time() - qtime,
        psql_pool.freesize,
        psql_pool.size,
        asyncio.current_task().task_name,
    )
    return ret


async def make_snmp_request(host, snmp_command, oids, community="public"):
    """PySNMP glue"""
    try:
        if snmp_command not in ("get", "walk"):
            raise Exception(f"Unsupported snmp_command (must be get or walk)")

        cmd_args = [
            snmp_engine,
            snmp.CommunityData(community),
            snmp.UdpTransportTarget((host, 161), timeout=10),
            snmp.ContextData(),
        ]
        cmd_opts = {"lookupMib": False}

        if snmp_command == "get":
            if isinstance(oids, str):
                oids = [oids]
            cmd_oids = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]

            var_binds = []
            # Slicing OIDs to perform SNMP GET with a maximum of 50 objects and avoid fragmentation
            for cmd_oids_slice in (
                cmd_oids[i : min(i + 50, len(cmd_oids))]
                for i in (range(0, len(cmd_oids), 50))
            ):
                error_indication, error_status, error_index, _var_binds = await snmp.getCmd(
                    *cmd_args, *cmd_oids_slice, **cmd_opts
                )
                if error_indication:
                    raise Exception(f"error_indication: {error_indication}")
                if error_status:
                    raise (
                        Exception(
                            "{} at {}".format(
                                error_status.prettyPrint(),
                                error_index
                                and var_binds[int(error_index) - 1][0]
                                or "?",
                            )
                        )
                    )
                var_binds += _var_binds

        if snmp_command == "walk":
            if not isinstance(oids, str):
                raise Exception(
                    f"Unsupported OID list for snmp_command walk (must be unique string)"
                )

            cmd_oids = [snmp.ObjectType(snmp.ObjectIdentity(oids))]

            var_binds = []
            end_of_walk = False
            while not end_of_walk:
                # error_indication, error_status, error_index, var_binds_table = await snmp.bulkCmd(
                #     *cmd_args, 0, 50, *cmd_oids, **cmd_opts
                # )
                error_indication, error_status, error_index, var_binds_table = await snmp.nextCmd(
                    *cmd_args, *cmd_oids, **cmd_opts
                )
                if error_indication:
                    raise Exception(f"error_indication: {error_indication}")
                if error_status:
                    raise (
                        Exception(
                            "{} at {}".format(
                                error_status.prettyPrint(),
                                error_index
                                and var_binds[int(error_index) - 1][0]
                                or "?",
                            )
                        )
                    )

                for _var_binds in var_binds_table:
                    if snmp.isEndOfMib(_var_binds):
                        break
                    for oid, value in _var_binds:
                        # log.debug("%s %s", oid, value)
                        if oids not in str(oid):
                            end_of_walk = True
                            break
                        var_binds.append((oid, value))
                cmd_oids = _var_binds

        results = {}
        for oid, value in var_binds:
            if isinstance(value, (NoSuchInstance, NoSuchObject)):
                log.warning("Object %s does not exist on %s", oid, host)
                results[str(oid)] = None
            else:
                results[str(oid)] = value.prettyPrint()
        return results

    except Exception as ex:
        log.warning(
            "Error when performing SNMP request %s on %s with %s",
            snmp_command,
            host,
            oids,
        )
        log.warning("%s: %s", repr(ex), str(ex))
        log.warning(oids)
        raise ex
    return {}


if __name__ == "__main__":
    main()
