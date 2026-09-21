import requests

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "<body onload=alert(1)>",
]

def detect_xss(url: str) -> dict:
    """
    Detect possible Reflected XSS vulnerabilities.
    """

    result = {"status": "Safe", "payload": None, "confidence": 0}

    for payload in XSS_PAYLOADS:
        try:
            response = requests.get(url + payload, timeout=5)

            if payload in response.text:
                result["status"] = "Possible XSS"

                result["payload"] = payload

                result["confidence"] = 90

                return result

        except Exception:
            continue

    return result
