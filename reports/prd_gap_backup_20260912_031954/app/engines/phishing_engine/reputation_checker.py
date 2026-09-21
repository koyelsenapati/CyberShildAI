"""
CyberShield AI
Reputation Checker

Future Integrations:
- VirusTotal
- Google Safe Browsing
- AbuseIPDB
- PhishTank
"""

import socket

from app.shared.dns_lookup import dns_lookup

PRIVATE_IP_PREFIXES = (
    "10.",
    "127.",
    "172.",
    "192.168."
)

def check_reputation(domain: str) -> dict:
    """
    Basic domain/IP reputation analysis.
    """

    result = {

        "domain": domain,

        "ip": None,

        "dns_status": "Unknown",

        "blacklisted": False,

        "reputation": "Good",

        "confidence": 100,

        "details": []
    }

    try:

        ip = socket.gethostbyname(domain)

        result["ip"] = ip

    except Exception:

        result["reputation"] = "Unknown"

        result["confidence"] = 20

        result["details"].append(
            "Unable to resolve domain."
        )

        return result

    dns = dns_lookup(domain)

    result["dns_status"] = dns.get(
        "status",
        "Unknown"
    )

    if dns.get("status") != "Success":

        result["confidence"] -= 20

        result["details"].append(
            "DNS lookup failed."
        )

    if ip.startswith(PRIVATE_IP_PREFIXES):

        result["reputation"] = "Suspicious"

        result["confidence"] -= 40

        result["details"].append(
            "Private IP detected."
        )

    result["details"].append(
        "Blacklist lookup not enabled."
    )

    result["details"].append(
        "Google Safe Browsing integration pending."
    )

    result["details"].append(
        "VirusTotal integration pending."
    )

    return result
