"""
CyberShield AI
HTML Analyzer
"""

from bs4 import BeautifulSoup

def analyze_html(html: str) -> dict:
    """
    Analyze HTML page.
    """

    result = {
        "title": "Unknown",
        "forms": 0,
        "inputs": 0,
        "password_fields": 0,
        "scripts": 0,
        "external_scripts": 0,
        "inline_scripts": 0,
        "images": 0,
        "links": 0,
        "login_form": False,
        "html5": False,
    }

    try:

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        if soup.title and soup.title.string:
            result["title"] = soup.title.string.strip()

        forms = soup.find_all("form")
        result["forms"] = len(forms)

        inputs = soup.find_all("input")
        result["inputs"] = len(inputs)

        password_fields = soup.find_all(
            "input",
            {"type": "password"},
        )

        result["password_fields"] = len(password_fields)

        result["login_form"] = len(password_fields) > 0

        scripts = soup.find_all("script")

        result["scripts"] = len(scripts)

        external = 0
        inline = 0

        for script in scripts:

            if script.get("src"):
                external += 1
            else:
                inline += 1

        result["external_scripts"] = external
        result["inline_scripts"] = inline

        result["images"] = len(
            soup.find_all("img")
        )

        result["links"] = len(
            soup.find_all("a")
        )

        result["html5"] = (
            "<!doctype html>" in html.lower()
        )

    except Exception as e:

        result["error"] = str(e)

    return result
