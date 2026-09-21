from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.schemas.alert import AlertCreate

def create_alert(
    db: Session,
    data: AlertCreate,
    user_id: int,
) -> Alert:
    alert = Alert(
        user_id=user_id,
        title=data.title,
        description=data.description,
        severity=data.severity,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def get_alerts(db: Session, user_id: int) -> list[Alert]:
    return (
        db.query(Alert)
        .filter(Alert.user_id == user_id)
        .order_by(Alert.id.desc())
        .all()
    )
