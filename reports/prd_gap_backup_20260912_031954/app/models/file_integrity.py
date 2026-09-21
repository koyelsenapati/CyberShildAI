"""
CyberShield AI
File Integrity Model
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class FileIntegrity(Base):
    __tablename__ = "file_integrity"

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

    file_path = Column(
        String(500),
        nullable=False,
    )

    file_hash = Column(
        String(255),
        nullable=False,
    )

    algorithm = Column(
        String(50),
        default="SHA256",
    )

    status = Column(
        String(50),
        default="Safe",
    )

    result = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="file_integrity_records",
    )
