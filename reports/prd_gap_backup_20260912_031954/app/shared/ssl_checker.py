"""
CyberShield AI
SSL Checker
"""

import socket
import ssl
from urllib.parse import urlparse

def _flatten_certificate_name(name) -> dict:
    """
    Convert Python SSL certificate name tuples into a flat dictionary.
    """
    result = {}

    if not name:
        return result

    try:
        for attribute_group in name:
            if not attribute_group:
                continue

            for key, value in attribute_group:
                result[str(key)] = value

    except (TypeError, ValueError):
        return {}

    return result

def check_ssl(url: str) -> dict:
    """
    Check SSL certificate and TLS protocol.
    """

    result = {
        "status": "Unknown",
        "issuer": None,
        "subject": None,
        "expires": None,
        "protocol": None,
    }

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname

        if not hostname:
            result["status"] = "Invalid"
            result["error"] = "Unable to determine hostname."
            return result

        if parsed.scheme != "https":
            result["status"] = "No SSL"
            return result

        context = ssl.create_default_context()

        with socket.create_connection(
            (hostname, 443),
            timeout=5,
        ) as sock:

            with context.wrap_socket(
                sock,
                server_hostname=hostname,
            ) as secure_socket:

                cert = secure_socket.getpeercert()

                result["issuer"] = _flatten_certificate_name(
                    cert.get("issuer")
                )

                result["subject"] = _flatten_certificate_name(
                    cert.get("subject")
                )

                result["expires"] = cert.get("notAfter")
                result["protocol"] = secure_socket.version()

                result["status"] = "Valid"

    except ssl.SSLCertVerificationError as e:
        result["status"] = "Invalid"
        result["error"] = str(e)

    except (socket.timeout, socket.gaierror, ConnectionError) as e:
        result["status"] = "Error"
        result["error"] = str(e)

    except Exception as e:
        result["status"] = "Invalid"
        result["error"] = str(e)

    return result

def analyze_ssl(url: str) -> dict:
    """
    Compatibility wrapper.
    """
    return check_ssl(url)
