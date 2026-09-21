from sqlalchemy.orm import Session

from app.models.login_log import LoginLog

def create_login_log(db: Session, user_id: int, ip: str, status: str):
    log = LoginLog(user_id=user_id, ip_address=ip, status=status)
    db.add(log)
    db.commit()
