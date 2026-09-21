from sqlalchemy.orm import Session

from app.crud.dashboard import get_dashboard as dashboard_crud
from app.models.scan import Scan
from app.models.alert import Alert
from app.models.vulnerability import Vulnerability
from app.models.network_scan import NetworkScan
from app.services.network_monitor_service import get_network_snapshot

def get_dashboard(
    db: Session,
    user_id: int,
):
    dashboard = dashboard_crud(
        db=db,
        user_id=user_id,
    )

    return {
        "security_score": dashboard.security_score,
        "total_scans": dashboard.total_scans,
        "total_alerts": dashboard.total_alerts,
        "total_vulnerabilities": dashboard.total_vulnerabilities,
        "status": dashboard.status,
    }

def get_dashboard_statistics(
    db: Session,
    user_id: int,
):
    total_scans = (
        db.query(Scan)
        .filter(Scan.user_id == user_id)
        .count()
    )

    total_network_scans = (
        db.query(NetworkScan)
        .filter(NetworkScan.user_id == user_id)
        .count()
    )

    total_alerts = (
        db.query(Alert)
        .filter(Alert.user_id == user_id)
        .count()
    )

    total_vulnerabilities = (
        db.query(Vulnerability)
        .filter(Vulnerability.user_id == user_id)
        .count()
    )

    critical_vulnerabilities = (
        db.query(Vulnerability)
        .filter(
            Vulnerability.user_id == user_id,
            Vulnerability.severity.ilike("Critical"),
        )
        .count()
    )

    threat_count = (
        db.query(Alert)
        .filter(
            Alert.user_id == user_id,
            Alert.status.ilike("Open"),
        )
        .count()
    )

    total_scan_activity = (
        total_scans + total_network_scans
    )

    if total_vulnerabilities == 0 and total_alerts == 0:
        security_score = 100
    else:
        penalty = (
            critical_vulnerabilities * 15
            + max(
                total_vulnerabilities
                - critical_vulnerabilities,
                0,
            ) * 3
            + total_alerts * 2
        )

        security_score = max(
            0,
            min(
                100,
                100 - penalty,
            ),
        )

    network_snapshot = get_network_snapshot()

    network_statistics = network_snapshot.get(
        "statistics",
        {},
    )

    return {
        "security_score": security_score,
        "threat_count": threat_count,
        "alert_count": total_alerts,
        "vulnerability_count": total_vulnerabilities,
        "critical_vulnerabilities": critical_vulnerabilities,
        "active_connections": network_statistics.get(
            "active_connections",
            0,
        ),
        "packets_per_second": network_statistics.get(
            "packets_per_second",
            0,
        ),
        "total_scans": total_scan_activity,
    }
