"""
CyberShield AI
User Service
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User

def get_all_users(db: Session):

    return db.query(User).all()

def get_user(db: Session, user_id: int):

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user

def delete_user(db: Session, user_id: int):

    user = get_user(db, user_id)

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully"
    }
