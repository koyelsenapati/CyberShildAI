"""
CyberShield AI
Report Analyzer
"""

def analyze_report(scan_report: dict) -> dict:
    """
    Analyze scan report and summarize findings.
    """

    summary = {
        "total_findings": 0,
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }

    if not scan_report:
        return summary

    web = scan_report.get("web_scan")

    if web:

        risk = web.get("risk_level", "Low")

        summary["total_findings"] += 1

        if risk == "Critical":
            summary["critical"].append("Website Security")

        elif risk == "High":
            summary["high"].append("Website Security")

        elif risk == "Medium":
            summary["medium"].append("Website Security")

        else:
            summary["low"].append("Website Security")

    network = scan_report.get("network_scan")

    if network:

        risk = network.get("risk_level", "Low")

        summary["total_findings"] += 1

        if risk == "Critical":
            summary["critical"].append("Network")

        elif risk == "High":
            summary["high"].append("Network")

        elif risk == "Medium":
            summary["medium"].append("Network")

        else:
            summary["low"].append("Network")

    phishing = scan_report.get("phishing")

    if phishing:

        verdict = phishing.get(
            "confidence",
            {}
        ).get(
            "verdict",
            "Safe"
        )

        summary["total_findings"] += 1

        if verdict == "Phishing":

            summary["critical"].append(
                "Phishing Risk"
            )

        elif verdict == "High Risk":

            summary["high"].append(
                "Phishing Risk"
            )

        elif verdict == "Suspicious":

            summary["medium"].append(
                "Phishing Risk"
            )

        else:

            summary["low"].append(
                "Phishing Risk"
            )

    return summary
