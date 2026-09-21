from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class WhoisRecord(Base):
    __tablename__ = "whois_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    domain = Column(
        String(255),
        nullable=False
    )

    registrar = Column(
        String(255),
        nullable=True
    )

    owner_info = Column(
        String(500),
        nullable=True
    )

    registration_date = Column(
        DateTime,
        nullable=True
    )

    expiry_date = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String(50),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="whois_records"
    )
