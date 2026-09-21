"""
CyberShield AI
Cookie Security Analyzer
"""

def analyze_cookies(headers: dict) -> dict:
    """
    Analyze HTTP cookies.
    """

    result = {
        "status": "No Cookies",
        "secure": False,
        "http_only": False,
        "same_site": False,
    }

    try:
        cookies = headers.get("Set-Cookie", "")

        if not cookies:
            return result

        result["secure"] = "Secure" in cookies
        result["http_only"] = "HttpOnly" in cookies
        result["same_site"] = "SameSite" in cookies

        if (
            result["secure"]
            and result["http_only"]
            and result["same_site"]
        ):
            result["status"] = "Secure"

        elif (
            result["secure"]
            or result["http_only"]
            or result["same_site"]
        ):
            result["status"] = "Partially Secure"

        else:
            result["status"] = "Weak"

    except Exception as e:
        result["status"] = "Unknown"
        result["error"] = str(e)

    return result
