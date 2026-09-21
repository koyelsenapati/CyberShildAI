"""
CyberShield AI
Network Monitor Service
"""

from app.services.network_telemetry import get_network_telemetry

def get_network_snapshot() -> dict:
    """
    Return real-time network monitoring data.

    Uses psutil-based network telemetry from the host.
    """

    telemetry = get_network_telemetry()

    statistics = telemetry.get("statistics", {})

    return {
        "timestamp": telemetry.get("timestamp"),
        "statistics": {
            "packets_per_second": statistics.get(
                "packets_per_second",
                0,
            ),
            "active_connections": statistics.get(
                "active_connections",
                0,
            ),
            "bandwidth": statistics.get(
                "bandwidth",
                0,
            ),
            "protocols": statistics.get(
                "protocols",
                {
                    "TCP": 0,
                    "UDP": 0,
                    "ICMP": 0,
                },
            ),
        },
        "packets": telemetry.get(
            "packets",
            [],
        ),
    }
