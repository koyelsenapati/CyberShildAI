"""
CyberShield AI
Remediation Generator
"""

def generate_remediation(scan_report: dict) -> list[dict]:
    """
    Generate detailed remediation steps
    for detected vulnerabilities.
    """

    remediation = []

    web = scan_report.get("web_scan")

    if web:

        if web.get("ssl_status") != "Valid":

            remediation.append({

                "issue": "Missing SSL",

                "severity": "Critical",

                "steps": [

                    "Purchase or generate an SSL certificate.",

                    "Install the certificate on your web server.",

                    "Redirect HTTP traffic to HTTPS.",

                    "Enable HSTS (Strict-Transport-Security)."
                ],

                "references": [

                    "https://owasp.org/",
                    "https://developer.mozilla.org/"
                ]
            })

        if web.get("security_headers") == "Poor":

            remediation.append({

                "issue": "Missing Security Headers",

                "severity": "High",

                "steps": [

                    "Enable Content-Security-Policy.",

                    "Enable X-Frame-Options.",

                    "Enable X-Content-Type-Options.",

                    "Enable Referrer-Policy.",

                    "Enable Strict-Transport-Security."
                ],

                "references": [

                    "https://owasp.org/www-project-secure-headers/"
                ]
            })

        if web.get("sql_injection") == "Possible SQL Injection":

            remediation.append({

                "issue": "SQL Injection",

                "severity": "Critical",

                "steps": [

                    "Use parameterized queries.",

                    "Avoid string concatenation in SQL.",

                    "Validate all user input.",

                    "Use an ORM such as SQLAlchemy."
                ],

                "references": [

                    "https://owasp.org/www-community/attacks/SQL_Injection"
                ]
            })

        if web.get("xss") == "Possible XSS":

            remediation.append({

                "issue": "Cross-Site Scripting (XSS)",

                "severity": "Critical",

                "steps": [

                    "Sanitize user input.",

                    "Encode output.",

                    "Use Content Security Policy.",

                    "Avoid rendering raw HTML."
                ],

                "references": [

                    "https://owasp.org/www-community/attacks/xss/"
                ]
            })

        if web.get("csrf") == "Possible Missing CSRF":

            remediation.append({

                "issue": "CSRF",

                "severity": "High",

                "steps": [

                    "Generate CSRF tokens.",

                    "Validate tokens on every POST request.",

                    "Use SameSite cookies."
                ],

                "references": [

                    "https://owasp.org/www-community/attacks/csrf"
                ]
            })

    network = scan_report.get("network_scan")

    if network:

        if network.get("open_ports", 0) > 10:

            remediation.append({

                "issue": "Too Many Open Ports",

                "severity": "High",

                "steps": [

                    "Close unused ports.",

                    "Disable unnecessary services.",

                    "Configure firewall rules.",

                    "Allow only required traffic."
                ],

                "references": [

                    "https://nmap.org/book/"
                ]
            })

    phishing = scan_report.get("phishing")

    if phishing:

        verdict = phishing.get(
            "confidence",
            {}
        ).get(
            "verdict",
            "Safe"
        )

        if verdict == "Phishing":

            remediation.append({

                "issue": "Phishing Website",

                "severity": "Critical",

                "steps": [

                    "Do not enter credentials.",

                    "Block the URL.",

                    "Report the domain.",

                    "Warn affected users."
                ],

                "references": [

                    "https://www.cisa.gov/"
                ]
            })

    return remediation
