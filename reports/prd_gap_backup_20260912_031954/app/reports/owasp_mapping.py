"""
CyberShield AI
OWASP Top 10 Mapping
"""

OWASP_MAP = {

    "SQL Injection": {

        "category": "A03:2021 - Injection",

        "reference":
        "https://owasp.org/Top10/A03_2021-Injection/"
    },

    "Cross Site Scripting": {

        "category":
        "A03:2021 - Injection",

        "reference":
        "https://owasp.org/Top10/"
    },

    "CSRF": {

        "category":
        "A01:2021 - Broken Access Control",

        "reference":
        "https://owasp.org/Top10/"
    },

    "SSL Misconfiguration": {

        "category":
        "A05:2021 - Security Misconfiguration",

        "reference":
        "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"
    },

    "Missing Security Headers": {

        "category":
        "A05:2021 - Security Misconfiguration",

        "reference":
        "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"
    },

    "Weak Cookies": {

        "category":
        "A07:2021 - Identification and Authentication Failures",

        "reference":
        "https://owasp.org/Top10/"
    }
}

def map_owasp(cvss_results: list):
    """
    Map vulnerabilities to OWASP Top 10.
    """

    mappings = []

    for item in cvss_results:

        info = OWASP_MAP.get(
            item["name"]
        )

        if info:

            mappings.append({

                "name": item["name"],

                "category": info["category"],

                "reference": info["reference"],

                "cvss": item["cvss"],

                "severity": item["severity"]

            })

    return mappings
