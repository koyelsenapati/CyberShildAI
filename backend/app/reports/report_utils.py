"""
CyberShield AI
Report Utilities
"""

from datetime import datetime, timezone

def report_metadata():

    return {

        "generated_at": datetime.now(timezone.utc),

        "generator": "CyberShield AI",

        "version": "1.0.0"
    }
