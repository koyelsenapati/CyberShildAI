"""
CyberShield AI
Network Scan Service
"""

import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.engines.security_engine.network_scanner import scan_network
from app.crud.network_scan import create_network_scan

def start_network_scan(
    db: Session,
    user_id: int,
    target: str,
):
    """
    Scan an authorized network target,
    save the result,
    and return the scan information.
    """

    try:

        # -------------------------
        # Run Network Scan
        # -------------------------

        result = scan_network(target)

        # -------------------------
        # Save Database
        # -------------------------

        scan = create_network_scan(
            db,
            {
                "user_id": user_id,
                "target": target,
                "status": result.get("status", "Failed"),
                "devices_found": result.get("devices_found", 0),
                "open_ports": result.get("open_ports", 0),
                "scan_duration": str(
                    result.get("scan_duration", 0)
                ),
                "risk_level": result.get(
                    "risk_level",
                    "Low",
                ),
                "result": json.dumps(
                    result,
                    default=str,
                ),
            },
        )

        return {
            "message": "Network Scan Completed",
            "scan": scan,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Network Scan Failed: {str(error)}",
        )
