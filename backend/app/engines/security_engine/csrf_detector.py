from bs4 import BeautifulSoup

CSRF_KEYWORDS = [
    "csrf",
    "csrf_token",
    "_csrf",
    "_token",
    "authenticity_token",
    "xsrf",
    "xsrf_token",
]

def detect_csrf(html: str) -> dict:
    """
    Detect possible CSRF protection in HTML forms.
    """

    result = {
        "status": "Protected",
        "forms": 0,
        "protected_forms": 0,
        "unprotected_forms": 0,
        "confidence": 100,
    }

    soup = BeautifulSoup(html, "html.parser")

    forms = soup.find_all("form")

    result["forms"] = len(forms)

    if len(forms) == 0:
        result["status"] = "No Forms"

        result["confidence"] = 100

        return result

    protected = 0

    for form in forms:
        inputs = form.find_all("input")

        token_found = False

        for field in inputs:
            name = field.get("name", "").strip().lower()

            field_id = field.get("id", "").strip().lower()

            if name in CSRF_KEYWORDS or field_id in CSRF_KEYWORDS:
                token_found = True
                break

        if token_found:
            protected += 1

    result["protected_forms"] = protected

    result["unprotected_forms"] = len(forms) - protected

    if protected == len(forms):
        result["status"] = "Protected"

        result["confidence"] = 100

    elif protected > 0:
        result["status"] = "Partially Protected"

        result["confidence"] = 70

    else:
        result["status"] = "Possible Missing CSRF"

        result["confidence"] = 90

    return result
