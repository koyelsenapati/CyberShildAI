import hashlib
import time
from datetime import datetime, timezone
from typing import Any

import psutil

_previous_io = None
_previous_time = None

def _calculate_rate(current_value: int) -> float:
    global _previous_io
    global _previous_time

    now = time.monotonic()

    if _previous_io is None or _previous_time is None:
        _previous_io = current_value
        _previous_time = now
        return 0.0

    elapsed = now - _previous_time

    if elapsed <= 0:
        return 0.0

    delta = current_value - _previous_io

    _previous_io = current_value
    _previous_time = now

    return round(max(delta, 0) / elapsed, 2)

def _get_protocol(connection: Any) -> str:
    if connection.type == 1:
        return "TCP"

    if connection.type == 2:
        return "UDP"

    return "UNKNOWN"

def _get_status(connection: Any) -> str:
    if connection.status == psutil.CONN_ESTABLISHED:
        return "NORMAL"

    if connection.status in {
        psutil.CONN_SYN_SENT,
        psutil.CONN_SYN_RECV,
    }:
        return "SUSPICIOUS"

    return "NORMAL"

def _get_address(value: Any) -> tuple[str, int]:
    if not value:
        return "", 0

    try:
        return value.ip or "", int(value.port or 0)
    except (AttributeError, TypeError, ValueError):
        return "", 0

def _stable_connection_id(
    protocol: str,
    source_ip: str,
    source_port: int,
    destination_ip: str,
    destination_port: int,
) -> str:
    raw = (
        f"{protocol}|"
        f"{source_ip}|{source_port}|"
        f"{destination_ip}|{destination_port}"
    )

    digest = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()[:16]

    return f"{protocol}-{digest}"

def _build_packet_records(
    connections: list[Any],
) -> list[dict]:
    records = []
    seen_connections = set()

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    for connection in connections[:50]:
        protocol = _get_protocol(connection)

        if protocol == "UNKNOWN":
            continue

        source_ip, source_port = _get_address(
            connection.laddr
        )

        destination_ip, destination_port = _get_address(
            connection.raddr
        )

        port = (
            destination_port
            or source_port
            or 0
        )

        connection_key = (
            protocol,
            source_ip,
            source_port,
            destination_ip,
            destination_port,
        )

        if connection_key in seen_connections:
            continue

        seen_connections.add(connection_key)

        status = _get_status(connection)

        connection_id = _stable_connection_id(
            protocol=protocol,
            source_ip=source_ip,
            source_port=source_port,
            destination_ip=destination_ip,
            destination_port=destination_port,
        )

        records.append(
            {
                "id": connection_id,
                "timestamp": timestamp,
                "source_ip": source_ip or "0.0.0.0",
                "destination_ip": destination_ip or "0.0.0.0",
                "protocol": protocol,
                "port": port,
                # psutil.net_connections() does not expose
                # per-connection packet size. Do not fabricate it.
                "size": 0,
                "status": status,
            }
        )

    return records

def get_network_telemetry() -> dict:
    counters = psutil.net_io_counters()

    connections = []

    try:
        connections = psutil.net_connections(
            kind="inet"
        )
    except (
        psutil.AccessDenied,
        OSError,
    ):
        connections = []

    active_connections = sum(
        1
        for connection in connections
        if connection.status
        == psutil.CONN_ESTABLISHED
    )

    total_packets = (
        counters.packets_sent
        + counters.packets_recv
    )

    packets_per_second = _calculate_rate(
        total_packets
    )

    total_bytes = (
        counters.bytes_sent
        + counters.bytes_recv
    )

    bytes_per_second = _calculate_rate(
        total_bytes
    )

    bandwidth_mbps = round(
        bytes_per_second * 8 / 1_000_000,
        2,
    )

    tcp_count = 0
    udp_count = 0

    for connection in connections:
        protocol = _get_protocol(connection)

        if protocol == "TCP":
            tcp_count += 1

        elif protocol == "UDP":
            udp_count += 1

    total_protocol_connections = (
        tcp_count + udp_count
    )

    protocols = {
        "TCP": 0,
        "UDP": 0,
        "ICMP": 0,
    }

    if total_protocol_connections > 0:
        protocols["TCP"] = round(
            tcp_count
            / total_protocol_connections
            * 100
        )

        protocols["UDP"] = 100 - protocols["TCP"]

    packets = _build_packet_records(
        connections
    )

    return {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "statistics": {
            "packets_per_second":
                packets_per_second,

            "active_connections":
                active_connections,

            "bandwidth":
                bandwidth_mbps,

            "protocols":
                protocols,
        },

        "packets": packets,
    }
