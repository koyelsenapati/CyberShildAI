import re
from email import policy
from email.parser import BytesParser
from urllib.parse import urlparse
import ipaddress

SUSPICIOUS_TERMS = {
    "verify",
    "urgent",
    "account suspended",
    "reset password",
    "confirm account",
    "security alert",
}

def analyze_email(raw_email: bytes) -> dict:
    message = BytesParser(policy=policy.default).parsebytes(raw_email)

    sender = message.get("From", "")
    subject = message.get("Subject", "")

    body_parts = []

    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                body_parts.append(part.get_content())
    else:
        body_parts.append(message.get_content())

    body = "\n".join(body_parts)

    links = re.findall(r"https?://[^\s<>\"]+", body)

    suspicious_terms = [
        term for term in SUSPICIOUS_TERMS
        if term in f"{subject} {body}".lower()
    ]

    suspicious_links = []

    for link in links:
        try:
            parsed = urlparse(link)
            hostname = (parsed.hostname or "").lower()
            suspicious = parsed.scheme not in {"http", "https"} or not hostname
            suspicious = suspicious or "@" in (parsed.netloc or "")
            suspicious = suspicious or hostname.startswith("xn--") or ".xn--" in hostname
            try:
                ipaddress.ip_address(hostname)
                suspicious = True
            except ValueError:
                pass
            if suspicious:
                suspicious_links.append(link)
        except ValueError:
            suspicious_links.append(link)

    score = min(
        100,
        len(suspicious_terms) * 15
        + len(suspicious_links) * 20
        + (15 if not sender else 0),
    )

    if score >= 70:
        classification = "Malicious"
    elif score >= 35:
        classification = "Suspicious"
    else:
        classification = "Safe"

    return {
        "sender": sender,
        "subject": subject,
        "links": links,
        "suspicious_terms": suspicious_terms,
        "suspicious_links": suspicious_links,
        "phishing_probability": score,
        "classification": classification,
    }
