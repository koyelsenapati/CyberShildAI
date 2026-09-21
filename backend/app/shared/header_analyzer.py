"""
CyberShield AI
Header Analyzer
"""

def analyze_headers(headers: dict) -> dict:
    """
    Analyze HTTP Security Headers.
    """

    required_headers = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]

    try:

        missing_headers = [
            header
            for header in required_headers
            if header not in headers
        ]

        if len(missing_headers) == 0:
            grade = "Good"

        elif len(missing_headers) <= 2:
            grade = "Average"

        else:
            grade = "Poor"

        return {
            "grade": grade,
            "missing_headers": missing_headers,
            "present_headers": len(required_headers) - len(missing_headers),
            "total_required": len(required_headers),
        }

    except Exception as e:

        return {
            "grade": "Unknown",
            "missing_headers": [],
            "present_headers": 0,
            "total_required": len(required_headers),
            "error": str(e),
        }
