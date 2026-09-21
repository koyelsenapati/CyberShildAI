"""
CyberShield AI
DNS Lookup
"""

import dns.resolver

def dns_lookup(domain: str) -> dict:
    """
    Retrieve DNS records.
    """

    result = {
        "status": "Success",
        "records": {
            "A": [],
            "AAAA": [],
            "MX": [],
            "NS": [],
            "TXT": [],
            "CNAME": [],
        },
    }

    record_types = [
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "CNAME",
    ]

    try:

        for record in record_types:

            try:

                answers = dns.resolver.resolve(domain, record)

                result["records"][record] = [
                    str(answer)
                    for answer in answers
                ]

            except Exception:
                pass

        has_records = any(
            len(records) > 0
            for records in result["records"].values()
        )

        if not has_records:
            result["status"] = "No Records"

    except Exception as e:

        result["status"] = "Failed"
        result["error"] = str(e)

    return result

def lookup_dns(domain: str) -> dict:
    """
    Compatibility wrapper.
    """
    return dns_lookup(domain)
