"""
CyberShield AI
Web Scan Model
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class WebScan(Base):
    __tablename__ = "web_scans"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    url = Column(
        String(500),
        nullable=False,
    )

    status = Column(
        String(50),
        default="Completed",
    )

    response_time = Column(
        Float,
    )

    risk_level = Column(
        String(20),
    )

    ssl_status = Column(
        Text,
    )

    result = Column(
        Text,
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

    # Relationship with User model
    user = relationship(
        "User",
        back_populates="web_scans",
    )
