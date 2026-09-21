from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class SSLCertificate(Base):
    __tablename__ = "ssl_certificates"

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

    issuer = Column(
        String(255),
        nullable=True
    )

    valid_from = Column(
        DateTime,
        nullable=True
    )

    valid_to = Column(
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
        back_populates="ssl_certificates"
    )
