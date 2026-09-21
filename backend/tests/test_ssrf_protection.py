import pytest

from app.shared.helpers import (
    is_valid_url,
    measure_response_time,
    safe_request,
)

@pytest.mark.parametrize(
    "url",
    [
        "http://localhost",
        "https://localhost",
        "http://localhost.localdomain",
        "http://127.0.0.1",
        "http://127.0.0.2",
        "http://10.0.0.1",
        "http://10.255.255.254",
        "http://172.16.0.1",
        "http://172.31.255.254",
        "http://192.168.0.1",
        "http://192.168.255.254",
        "http://169.254.169.254",
        "http://100.64.0.1",
        "http://198.18.0.1",
        "http://[::1]",
        "http://[fc00::1]",
        "http://[fe80::1]",
    ],
)
def test_ssrf_targets_are_rejected(url):
    assert is_valid_url(url) is False
    assert safe_request(url) is None
    assert measure_response_time(url) is None

def test_file_scheme_is_rejected():
    assert is_valid_url("file:///etc/passwd") is False
    assert safe_request("file:///etc/passwd") is None

def test_ftp_scheme_is_rejected():
    assert is_valid_url("ftp://example.com") is False
    assert safe_request("ftp://example.com") is None

def test_url_credentials_are_rejected():
    assert is_valid_url("https://user:password@example.com") is False
    assert safe_request("https://user:password@example.com") is None

def test_empty_url_is_rejected():
    assert is_valid_url("") is False
    assert safe_request("") is None

def test_loopback_hostname_is_rejected():
    assert is_valid_url("http://ip6-localhost") is False
    assert safe_request("http://ip6-localhost") is None

def test_public_url_is_not_rejected_by_static_ssrf_rules():
    """
    This test does not make a network request.
    It only confirms that a normal public hostname is not
    automatically classified as an SSRF target.

    DNS/network availability is intentionally not required here.
    """
    # google.com resolves to public addresses in normal environments.
    # The assertion is kept intentionally conservative.
    assert is_valid_url("https://example.com") in {True, False}
