"""
CyberShield AI
Dashboard CRUD
"""

from sqlalchemy.orm import Session

from app.models.dashboard import Dashboard

def get_dashboard(
    db: Session,
    user_id: int,
):
    dashboard = (
        db.query(Dashboard)
        .filter(Dashboard.user_id == user_id)
        .first()
    )

    if dashboard is None:
        dashboard = Dashboard(
            user_id=user_id,
            security_score=100,
            total_scans=0,
            total_alerts=0,
            total_vulnerabilities=0,
            status="Safe",
        )

        db.add(dashboard)
        db.commit()
        db.refresh(dashboard)

    return dashboard

def update_dashboard(
    db: Session,
    user_id: int,
    data: dict,
):
    dashboard = get_dashboard(
        db=db,
        user_id=user_id,
    )

    for key, value in data.items():
        if hasattr(dashboard, key):
            setattr(dashboard, key, value)

    db.commit()
    db.refresh(dashboard)

    return dashboard
