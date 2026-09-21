import whois

def whois_lookup(domain: str) -> dict:
    """
    Retrieve WHOIS information for a domain.
    """

    result = {
        "domain": domain,
        "registrar": "Unknown",
        "creation_date": None,
        "expiration_date": None,
        "updated_date": None,
        "country": "Unknown",
        "organization": "Unknown",
        "emails": [],
        "status": "Unavailable",
    }

    try:
        info = whois.whois(domain)

        result["registrar"] = info.registrar or "Unknown"

        if isinstance(info.creation_date, list):
            result["creation_date"] = str(info.creation_date[0])
        else:
            result["creation_date"] = str(info.creation_date)

        if isinstance(info.expiration_date, list):
            result["expiration_date"] = str(info.expiration_date[0])
        else:
            result["expiration_date"] = str(info.expiration_date)

        if isinstance(info.updated_date, list):
            result["updated_date"] = str(info.updated_date[0])
        else:
            result["updated_date"] = str(info.updated_date)

        result["country"] = getattr(info, "country", "Unknown")
        result["organization"] = getattr(info, "org", "Unknown")

        emails = getattr(info, "emails", [])

        if isinstance(emails, str):
            emails = [emails]

        result["emails"] = emails

        result["status"] = "Available"

    except Exception as e:
        result["error"] = str(e)

    return result
