"""
CyberShield AI
Central Risk Calculator
"""

def calculate_risk(web_result: dict) -> str:
    """
    Calculate web security risk from the canonical web scan result.

    Risk factors:
    - SQL injection
    - XSS
    - CSRF
    - Invalid / missing SSL
    - Missing security headers
    - Weak cookies
    - Missing robots.txt

    Returns:
        Critical, High, Medium, or Low
    """

    if not web_result:
        return "Low"

    score = 0

    # ---------------------------------------------------------
    # SSL
    # ---------------------------------------------------------

    ssl_status = str(
        web_result.get("ssl_status", {}).get("status", "")
    ).lower()

    if ssl_status in {"invalid", "error"}:
        score += 25

    elif ssl_status in {"no ssl", "missing"}:
        score += 20

    # ---------------------------------------------------------
    # Security Headers
    # ---------------------------------------------------------

    headers = web_result.get("security_headers", {})

    if isinstance(headers, dict):
        missing_headers = headers.get("missing_headers", [])

        if isinstance(missing_headers, list):
            missing_count = len(missing_headers)
        else:
            missing_count = 0

        score += min(missing_count * 5, 25)

    # ---------------------------------------------------------
    # SQL Injection
    # ---------------------------------------------------------

    sql_result = web_result.get("sql_injection", {})

    if isinstance(sql_result, dict):
        sql_status = str(
            sql_result.get("status", "")
        ).lower()

        if "possible" in sql_status:
            score += 30

    # ---------------------------------------------------------
    # XSS
    # ---------------------------------------------------------

    xss_result = web_result.get("xss", {})

    if isinstance(xss_result, dict):
        xss_status = str(
            xss_result.get("status", "")
        ).lower()

        if "possible" in xss_status:
            score += 25

    # ---------------------------------------------------------
    # CSRF
    # ---------------------------------------------------------

    csrf_result = web_result.get("csrf", {})

    if isinstance(csrf_result, dict):
        csrf_status = str(
            csrf_result.get("status", "")
        ).lower()

        if csrf_status == "possible missing csrf":
            score += 15

        elif csrf_status == "partially protected":
            score += 8

    # ---------------------------------------------------------
    # Cookie Security
    # ---------------------------------------------------------

    cookie_result = web_result.get("cookies", {})

    if isinstance(cookie_result, dict):
        cookie_status = str(
            cookie_result.get("status", "")
        ).lower()

        if cookie_status == "weak":
            score += 10

        elif cookie_status == "partially secure":
            score += 5

    # ---------------------------------------------------------
    # Robots.txt
    # ---------------------------------------------------------

    robots_result = web_result.get("robots", {})

    if isinstance(robots_result, dict):
        robots_status = str(
            robots_result.get("status", "")
        ).lower()

        if robots_status == "missing":
            score += 2

    # ---------------------------------------------------------
    # Final Risk Level
    # ---------------------------------------------------------

    score = min(score, 100)

    if score >= 80:
        return "Critical"

    if score >= 50:
        return "High"

    if score >= 25:
        return "Medium"

    return "Low"

def calculate_network_risk(open_ports: int) -> str:
    """
    Calculate network risk from number of open ports.
    """

    if open_ports >= 10:
        return "Critical"

    if open_ports >= 6:
        return "High"

    if open_ports >= 3:
        return "Medium"

    return "Low"
