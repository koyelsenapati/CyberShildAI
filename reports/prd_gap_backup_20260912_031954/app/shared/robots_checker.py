"""
CyberShield AI
Robots.txt Checker
"""

import requests

def check_robots(url: str) -> dict:
    """
    Check robots.txt availability.
    """

    robots_url = url.rstrip("/") + "/robots.txt"

    result = {
        "status": "Missing",
        "url": robots_url,
        "accessible": False,
    }

    try:

        response = requests.get(
            robots_url,
            timeout=5,
            allow_redirects=True,
        )

        if response.status_code == 200:

            result["status"] = "Found"
            result["accessible"] = True

        elif response.status_code == 403:

            result["status"] = "Forbidden"

        elif response.status_code == 404:

            result["status"] = "Missing"

        else:

            result["status"] = f"HTTP {response.status_code}"

    except Exception as e:

        result["status"] = "Error"
        result["error"] = str(e)

    return result
