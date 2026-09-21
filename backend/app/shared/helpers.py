"""
CyberShield AI
Helper Functions
"""

import ipaddress
import socket
import time
from urllib.parse import urlparse

import requests

# ============================================================
# SSRF PROTECTION
# ============================================================

_BLOCKED_NETWORKS = (
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("198.18.0.0/15"),
    ipaddress.ip_network("224.0.0.0/4"),
    ipaddress.ip_network("240.0.0.0/4"),

    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
    ipaddress.ip_network("fe80::/10"),
    ipaddress.ip_network("ff00::/8"),
)

def _is_blocked_ip(ip: str) -> bool:
    """
    Return True when an IP belongs to a private,
    loopback, link-local, multicast, reserved, or
    otherwise unsafe network range.
    """

    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return True

    return any(
        address in network
        for network in _BLOCKED_NETWORKS
    )

def _resolve_all_ips(hostname: str) -> list[str]:
    """
    Resolve all IPv4/IPv6 addresses for a hostname.
    """

    try:
        results = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM,
        )
    except (socket.gaierror, OSError):
        return []

    addresses = []

    for result in results:
        sockaddr = result[4]

        if not sockaddr:
            continue

        ip = sockaddr[0]

        if ip not in addresses:
            addresses.append(ip)

    return addresses

def _is_safe_hostname(hostname: str) -> bool:
    """
    Validate hostname and ensure every resolved IP is safe.
    """

    if not hostname:
        return False

    hostname = hostname.rstrip(".").lower()

    # Direct IP address
    try:
        address = ipaddress.ip_address(hostname)
        return not _is_blocked_ip(str(address))
    except ValueError:
        pass

    # Explicit localhost names
    blocked_names = {
        "localhost",
        "localhost.localdomain",
        "ip6-localhost",
        "ip6-loopback",
    }

    if hostname in blocked_names:
        return False

    # Resolve every address. If any address is unsafe,
    # reject the hostname rather than trusting one result.
    addresses = _resolve_all_ips(hostname)

    if not addresses:
        return False

    return all(
        not _is_blocked_ip(address)
        for address in addresses
    )

def _validate_request_url(url: str) -> str | None:
    """
    Normalize and validate a URL before making a network request.
    """

    url = normalize_url(url)

    try:
        parsed = urlparse(url)
    except Exception:
        return None

    if parsed.scheme.lower() not in {"http", "https"}:
        return None

    if not parsed.hostname:
        return None

    # Reject credentials in URLs.
    # Example:
    # https://user:password@example.com
    if parsed.username is not None or parsed.password is not None:
        return None

    if not _is_safe_hostname(parsed.hostname):
        return None

    return url

# ============================================================
# URL HELPERS
# ============================================================

def normalize_url(url: str) -> str:
    """
    Ensure URL has HTTP/HTTPS scheme.
    """

    url = str(url).strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url

def extract_domain(url: str) -> str:
    """
    Extract domain from URL.
    """

    parsed = urlparse(normalize_url(url))

    return parsed.netloc.lower()

def is_valid_url(url: str) -> bool:
    """
    Validate URL and reject SSRF targets.
    """

    try:
        return _validate_request_url(url) is not None
    except Exception:
        return False

def is_valid_ip(ip: str) -> bool:
    """
    Validate IP Address.
    """

    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def resolve_ip(domain: str):
    """
    Resolve Domain to IP.
    """

    try:
        address = socket.gethostbyname(domain)

        if _is_blocked_ip(address):
            return None

        return address

    except Exception:
        return None

# ============================================================
# SAFE HTTP REQUEST
# ============================================================

def safe_request(url: str, timeout: int = 10):
    """
    SSRF-safe HTTP GET request.

    Important security properties:
    - HTTP/HTTPS only
    - private/internal IPs blocked
    - loopback blocked
    - link-local blocked
    - multicast/reserved ranges blocked
    - localhost blocked
    - URL credentials blocked
    - redirects disabled so an external server cannot redirect
      the scanner into an internal address
    """

    validated_url = _validate_request_url(url)

    if validated_url is None:
        return None

    try:
        response = requests.get(
            validated_url,
            timeout=timeout,
            allow_redirects=False,
            headers={
                "User-Agent": "CyberShield-AI/1.0"
            },
        )

        return response

    except requests.RequestException:
        return None

def measure_response_time(url: str) -> float | None:
    """
    Measure response time using the SSRF-safe request helper.
    """

    validated_url = _validate_request_url(url)

    if validated_url is None:
        return None

    try:
        start = time.perf_counter()

        response = safe_request(
            validated_url,
            timeout=10,
        )

        end = time.perf_counter()

        if response is None:
            return None

        return round(end - start, 3)

    except Exception:
        return None
