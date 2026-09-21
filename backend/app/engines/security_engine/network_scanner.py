"""
CyberShield AI
Advanced Network Scanner

Purpose:
- Network/host discovery
- TCP port scanning
- Service/version detection
- Basic network risk calculation

Use only against systems/networks you own
or have explicit permission to scan.
"""

import ipaddress
import time

import nmap

from app.shared.risk_calculator import calculate_network_risk

# Create Nmap scanner instance
scanner = nmap.PortScanner()

def _validate_target(target: str) -> str:
    """
    Validate and normalize the scan target.

    Supported examples:
    - 127.0.0.1
    - 192.168.1.10
    - hostname.example
    - authorized CIDR such as 192.168.1.0/24
    """

    if not target or not target.strip():
        raise ValueError("Scan target cannot be empty.")

    target = target.strip()

    # Validate IP or CIDR when possible.
    # Hostnames are allowed if they are not valid IP/CIDR values.
    try:
        ipaddress.ip_address(target)
        return target
    except ValueError:
        pass

    try:
        ipaddress.ip_network(target, strict=False)
        return target
    except ValueError:
        pass

    # Basic hostname validation
    if len(target) > 253:
        raise ValueError("Invalid target hostname.")

    if any(char in target for char in [" ", "\n", "\r", "\t"]):
        raise ValueError("Invalid characters in target.")

    return target

def _build_empty_result(target: str) -> dict:
    """
    Create a consistent network scan result.
    """

    return {
        "scanner": "network",
        "status": "Completed",
        "target": target,
        "hosts": [],
        "devices_found": 0,
        "open_ports": 0,
        "scan_duration": 0,
        "risk_level": "Low",
        "risk_score": 0,
        "error": None,
    }

def scan_network(target: str) -> dict:
    """
    Execute a network scan.

    Returns:
        dict: Structured network scan result.
    """

    start_time = time.time()

    try:
        target = _validate_target(target)

    except ValueError as exc:
        return {
            "scanner": "network",
            "status": "Failed",
            "target": target,
            "hosts": [],
            "devices_found": 0,
            "open_ports": 0,
            "scan_duration": 0,
            "risk_level": "Unknown",
            "risk_score": 0,
            "error": str(exc),
        }

    result = _build_empty_result(target)

    try:
        # -Pn : skip host discovery
        # -T4 : faster timing template
        # -F  : fast/common ports
        # -sV : service/version detection
        scanner.scan(
            hosts=target,
            arguments="-Pn -T4 -F -sV",
        )

        for host in scanner.all_hosts():

            host_info = scanner[host]

            host_data = {
                "ip": host,
                "hostname": host_info.hostname(),
                "state": host_info.state(),
                "ports": [],
            }

            if "tcp" in host_info:

                for port, service in host_info["tcp"].items():

                    port_info = {
                        "port": port,
                        "protocol": "tcp",
                        "state": service.get(
                            "state",
                            "unknown",
                        ),
                        "service": service.get(
                            "name",
                            "",
                        ),
                        "product": service.get(
                            "product",
                            "",
                        ),
                        "version": service.get(
                            "version",
                            "",
                        ),
                    }

                    host_data["ports"].append(
                        port_info
                    )

                    if port_info["state"] == "open":
                        result["open_ports"] += 1

            result["hosts"].append(host_data)

        result["devices_found"] = len(
            result["hosts"]
        )

        # Calculate scan duration
        result["scan_duration"] = round(
            time.time() - start_time,
            2,
        )

        # Calculate network risk
        try:
            risk_result = calculate_network_risk(
                result["open_ports"]
            )

            # Support both simple string and structured
            # risk calculator implementations.
            if isinstance(risk_result, dict):

                result["risk_level"] = risk_result.get(
                    "risk_level",
                    "Low",
                )

                result["risk_score"] = risk_result.get(
                    "risk_score",
                    0,
                )

            else:
                result["risk_level"] = str(
                    risk_result
                )

        except Exception:
            # Scanner result should remain available even
            # if risk calculation fails.
            result["risk_level"] = "Unknown"
            result["risk_score"] = 0

        return result

    except nmap.PortScannerError as exc:

        result["status"] = "Failed"
        result["error"] = (
            f"Nmap scanner error: {str(exc)}"
        )
        result["scan_duration"] = round(
            time.time() - start_time,
            2,
        )

        return result

    except Exception as exc:

        result["status"] = "Failed"
        result["error"] = str(exc)
        result["scan_duration"] = round(
            time.time() - start_time,
            2,
        )

        return result

def scan_target(target: str) -> dict:
    """
    Compatibility wrapper.

    Used by the Vulnerability Scanner
    and other CyberShield AI services.
    """

    return scan_network(target)
