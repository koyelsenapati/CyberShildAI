"""
CyberShield AI
Recommendation Engine
"""

def generate_recommendations(scan_report: dict) -> list[dict]:
    """
    Generate security recommendations
    based on scan results.
    """

    recommendations = []

    web = scan_report.get("web_scan")

    if web:

        if web.get("ssl_status") != "Valid":

            recommendations.append({
                "priority": "Critical",
                "title": "Enable HTTPS",
                "description": (
                    "Install a valid SSL/TLS certificate "
                    "and redirect all HTTP traffic to HTTPS."
                )
            })

        headers = web.get("security_headers")

        if headers == "Poor":

            recommendations.append({
                "priority": "High",
                "title": "Improve Security Headers",
                "description": (
                    "Add Content-Security-Policy, "
                    "Strict-Transport-Security, "
                    "X-Frame-Options and other "
                    "recommended HTTP security headers."
                )
            })

        if web.get("cookies") == "Weak":

            recommendations.append({
                "priority": "Medium",
                "title": "Secure Cookies",
                "description": (
                    "Use Secure, HttpOnly and SameSite "
                    "cookie attributes."
                )
            })

        if web.get("sql_injection") == "Possible SQL Injection":

            recommendations.append({
                "priority": "Critical",
                "title": "Fix SQL Injection",
                "description": (
                    "Use parameterized queries or ORM "
                    "instead of dynamic SQL."
                )
            })

        if web.get("xss") == "Possible XSS":

            recommendations.append({
                "priority": "Critical",
                "title": "Mitigate XSS",
                "description": (
                    "Validate input, encode output "
                    "and enforce a Content Security Policy."
                )
            })

        if web.get("csrf") == "Possible Missing CSRF":

            recommendations.append({
                "priority": "High",
                "title": "Implement CSRF Protection",
                "description": (
                    "Add CSRF tokens to every "
                    "state-changing form."
                )
            })

    network = scan_report.get("network_scan")

    if network:

        ports = network.get("open_ports", 0)

        if ports > 10:

            recommendations.append({
                "priority": "High",
                "title": "Reduce Open Ports",
                "description": (
                    "Close unused services and "
                    "restrict access using firewall rules."
                )
            })

    phishing = scan_report.get("phishing")

    if phishing:

        confidence = phishing.get(
            "confidence",
            {}
        )

        verdict = confidence.get(
            "verdict",
            "Safe"
        )

        if verdict == "Phishing":

            recommendations.append({
                "priority": "Critical",
                "title": "Block Suspicious URL",
                "description": (
                    "Do not visit or distribute "
                    "this website. Add it to "
                    "your organization's blocklist."
                )
            })

    if not recommendations:

        recommendations.append({
            "priority": "Info",
            "title": "No Critical Issues",
            "description": (
                "No major vulnerabilities were "
                "identified during this scan."
            )
        })

    return recommendations
