"""
CyberShield AI
Dashboard Model
"""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base

class Dashboard(Base):
    __tablename__ = "dashboard"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    security_score = Column(
        Integer,
        default=100,
        nullable=False,
    )

    total_scans = Column(
        Integer,
        default=0,
        nullable=False,
    )

    total_alerts = Column(
        Integer,
        default=0,
        nullable=False,
    )

    total_vulnerabilities = Column(
        Integer,
        default=0,
        nullable=False,
    )

    status = Column(
        String(20),
        default="Safe",
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
