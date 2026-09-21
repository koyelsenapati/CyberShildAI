"""
CyberShield AI
Prompt Builder
"""

def build_prompt(scan_report: dict) -> str:
    """
    Convert scan report into a structured AI prompt.
    """

    prompt = []

    prompt.append(
        "You are a senior cybersecurity analyst."
    )

    prompt.append(
        "Analyze the following security scan report."
    )

    prompt.append(
        "Explain the vulnerabilities."
    )

    prompt.append(
        "Provide remediation steps."
    )

    prompt.append(
        "Prioritize the findings."
    )

    prompt.append("")

    # ---------------------------------
    # Web Scan
    # ---------------------------------

    web = scan_report.get("web_scan")

    if web:

        prompt.append("=== WEB SCAN ===")

        for key, value in web.items():

            prompt.append(
                f"{key}: {value}"
            )

        prompt.append("")

    # ---------------------------------
    # Network Scan
    # ---------------------------------

    network = scan_report.get("network_scan")

    if network:

        prompt.append("=== NETWORK SCAN ===")

        for key, value in network.items():

            prompt.append(
                f"{key}: {value}"
            )

        prompt.append("")

    # ---------------------------------
    # Phishing
    # ---------------------------------

    phishing = scan_report.get("phishing")

    if phishing:

        prompt.append("=== PHISHING ===")

        for key, value in phishing.items():

            prompt.append(
                f"{key}: {value}"
            )

        prompt.append("")

    # ---------------------------------
    # Final Instructions
    # ---------------------------------

    prompt.append(
        "Return:"
    )

    prompt.append(
        "1. Executive Summary"
    )

    prompt.append(
        "2. Risk Analysis"
    )

    prompt.append(
        "3. Recommended Fixes"
    )

    prompt.append(
        "4. Priority Order"
    )

    prompt.append(
        "5. Final Security Rating"
    )

    return "\n".join(prompt)
