"""
CyberShield AI
Web Security Scanner
"""

from app.engines.security_engine.csrf_detector import detect_csrf
from app.engines.security_engine.sql_injection import detect_sql_injection
from app.engines.security_engine.xss_detector import detect_xss

from app.shared.cookie_checker import analyze_cookies
from app.shared.header_analyzer import analyze_headers
from app.shared.helpers import (
    extract_domain,
    measure_response_time,
    normalize_url,
    safe_request,
    is_valid_url,
)

from app.shared.html_analyzer import analyze_html
from app.shared.risk_calculator import calculate_risk
from app.shared.robots_checker import check_robots
from app.shared.ssl_checker import check_ssl

def scan_website(url: str) -> dict:
    """
    Complete Website Security Scan
    """

    try:

        # -------------------------
        # Normalize URL
        # -------------------------

        url = normalize_url(url)

        if not is_valid_url(url):
            return {
                "status": "Failed",
                "message": "Invalid URL",
            }

        domain = extract_domain(url)

        # -------------------------
        # HTTP Request
        # -------------------------

        response = safe_request(url)

        if response is None:
            return {
                "status": "Failed",
                "message": "Unable to connect.",
            }

        # -------------------------
        # Basic Information
        # -------------------------

        response_time = measure_response_time(url)

        # -------------------------
        # Security Analysis
        # -------------------------

        ssl_result = check_ssl(url)

        header_result = analyze_headers(response.headers)

        cookie_result = analyze_cookies(response.headers)

        html_result = analyze_html(response.text)

        robots_result = check_robots(url)

        sql_result = detect_sql_injection(url)

        xss_result = detect_xss(url)

        csrf_result = detect_csrf(response.text)

        # -------------------------
        # Final Data
        # -------------------------

        result = {
            "status": "Completed",
            "domain": domain,
            "response_time": response_time,
            "ssl_status": ssl_result,
            "security_headers": header_result,
            "cookies": cookie_result,
            "html": html_result,
            "robots": robots_result,
            "sql_injection": sql_result,
            "xss": xss_result,
            "csrf": csrf_result,
        }

        # -------------------------
        # Risk Calculation
        # -------------------------

        result["risk_level"] = calculate_risk(result)

        return result

    except Exception as e:

        return {
            "status": "Failed",
            "message": str(e),
        }
