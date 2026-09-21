from datetime import datetime

from app.services.network_telemetry import (
    get_network_telemetry,
)

def test_network_telemetry_schema():
    data = get_network_telemetry()

    assert isinstance(data, dict)
    assert "timestamp" in data
    assert "statistics" in data
    assert "packets" in data

    datetime.fromisoformat(
        data["timestamp"].replace("Z", "+00:00")
    )

def test_network_statistics_are_valid():
    data = get_network_telemetry()
    statistics = data["statistics"]

    assert statistics["packets_per_second"] >= 0
    assert statistics["active_connections"] >= 0
    assert statistics["bandwidth"] >= 0

    protocols = statistics["protocols"]

    assert set(protocols.keys()) == {
        "TCP",
        "UDP",
        "ICMP",
    }

    for value in protocols.values():
        assert 0 <= value <= 100

    assert (
        sum(protocols.values()) == 100
        or sum(protocols.values()) == 0
    )

def test_network_records_are_valid():
    data = get_network_telemetry()

    packets = data["packets"]

    assert isinstance(packets, list)

    ids = set()

    for packet in packets:
        assert packet["id"]
        assert packet["id"] not in ids
        ids.add(packet["id"])

        datetime.fromisoformat(
            packet["timestamp"].replace("Z", "+00:00")
        )

        assert packet["protocol"] in {
            "TCP",
            "UDP",
        }

        assert isinstance(packet["port"], int)
        assert packet["port"] >= 0

        assert packet["status"] in {
            "NORMAL",
            "SUSPICIOUS",
        }

        assert isinstance(
            packet["source_ip"],
            str,
        )

        assert isinstance(
            packet["destination_ip"],
            str,
        )

        assert packet["size"] >= 0

def test_network_connection_ids_are_stable():
    first = get_network_telemetry()
    second = get_network_telemetry()

    first_map = {
        (
            p["protocol"],
            p["source_ip"],
            p["destination_ip"],
            p["port"],
        ): p["id"]
        for p in first["packets"]
    }

    second_map = {
        (
            p["protocol"],
            p["source_ip"],
            p["destination_ip"],
            p["port"],
        ): p["id"]
        for p in second["packets"]
    }

    common_keys = set(first_map) & set(second_map)

    for key in common_keys:
        assert first_map[key] == second_map[key]
