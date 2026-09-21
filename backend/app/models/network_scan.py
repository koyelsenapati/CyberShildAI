"""
CyberShield AI
Network Scan Model
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class NetworkScan(Base):
    __tablename__ = "network_scans"

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

    target = Column(
        String(255),
        nullable=False,
    )

    status = Column(
        String(50),
        default="Pending",
        nullable=False,
    )

    devices_found = Column(
        Integer,
        default=0,
        nullable=False,
    )

    open_ports = Column(
        Integer,
        default=0,
        nullable=False,
    )

    scan_duration = Column(
        String(50),
        nullable=True,
    )

    risk_level = Column(
        String(20),
        default="Low",
        nullable=False,
    )

    result = Column(
        Text,
        nullable=True,
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
        back_populates="network_scans",
    )
