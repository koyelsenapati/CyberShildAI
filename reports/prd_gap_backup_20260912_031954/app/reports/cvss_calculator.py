"""
CyberShield AI
CVSS Calculator
"""

def calculate_cvss(scan_report: dict):
    """
    Generate estimated CVSS findings.
    """

    findings = []

    # SQL Injection
    sql = scan_report.get("sql_injection", {})

    if sql.get("status") == "Possible SQL Injection":
        findings.append(
            {
                "name": "SQL Injection",
                "cvss": 9.8,
                "severity": "Critical",
            }
        )

    # XSS
    xss = scan_report.get("xss", {})

    if xss.get("status") == "Possible XSS":
        findings.append(
            {
                "name": "Cross Site Scripting",
                "cvss": 8.2,
                "severity": "High",
            }
        )

    # CSRF
    csrf = scan_report.get("csrf", {})

    if csrf.get("status") == "Possible Missing CSRF":
        findings.append(
            {
                "name": "CSRF",
                "cvss": 6.5,
                "severity": "Medium",
            }
        )

    # SSL
    if scan_report.get("ssl_status") != "Valid":
        findings.append(
            {
                "name": "SSL Misconfiguration",
                "cvss": 5.9,
                "severity": "Medium",
            }
        )

    # Security Headers
    headers = scan_report.get("security_headers", {})

    if headers.get("grade") == "Poor":
        findings.append(
            {
                "name": "Missing Security Headers",
                "cvss": 4.3,
                "severity": "Medium",
            }
        )

    # Cookies
    cookies = scan_report.get("cookies", {})

    if cookies.get("status") == "Weak":
        findings.append(
            {
                "name": "Weak Cookies",
                "cvss": 3.8,
                "severity": "Low",
            }
        )

    return findings
