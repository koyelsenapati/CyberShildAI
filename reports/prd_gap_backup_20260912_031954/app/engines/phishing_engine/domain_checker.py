"""
CyberShield AI
Domain Checker
"""

import socket
from urllib.parse import urlparse

from app.shared.whois_lookup import whois_lookup

SUSPICIOUS_TLDS = {
    "zip",
    "xyz",
    "top",
    "click",
    "gq",
    "cf",
    "ml",
    "tk",
    "work",
    "country",
    "kim",
    "rest",
    "support",
    "info"
}

def analyze_domain(url: str) -> dict:
    """
    Analyze domain information.
    """

    parsed = urlparse(url)

    domain = parsed.netloc.lower()

    result = {

        "domain": domain,

        "ip_address": None,

        "tld": None,

        "subdomains": 0,

        "punycode": False,

        "suspicious_tld": False,

        "whois": None,

        "domain_age_days": None,

        "status": "Safe"
    }

    # Resolve IP
    try:

        result["ip_address"] = socket.gethostbyname(domain)

    except Exception:

        result["ip_address"] = None

    # Punycode Detection
    if domain.startswith("xn--"):

        result["punycode"] = True

    # TLD
    parts = domain.split(".")

    if len(parts) >= 2:

        result["tld"] = parts[-1]

        result["subdomains"] = max(
            len(parts) - 2,
            0
        )

    if result["tld"] in SUSPICIOUS_TLDS:

        result["suspicious_tld"] = True

    # WHOIS Lookup
    whois_data = whois_lookup(domain)

    result["whois"] = whois_data

    if whois_data:

        age = whois_data.get("age_days")

        if age is not None:

            result["domain_age_days"] = age

            if age < 30:

                result["status"] = "Suspicious"

    if result["punycode"]:

        result["status"] = "Suspicious"

    if result["suspicious_tld"]:

        result["status"] = "Suspicious"

    if result["subdomains"] >= 4:

        result["status"] = "Suspicious"

    return result
