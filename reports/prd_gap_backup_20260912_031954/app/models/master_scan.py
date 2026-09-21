from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class MasterScan(Base):
    __tablename__ = "master_scans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    target = Column(String(255), nullable=False)

    scan_type = Column(
        String(50),
        nullable=False,
        default="Full Scan",
    )

    risk_level = Column(
        String(50),
        nullable=False,
        default="Low",
    )

    result = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user = relationship(
        "User",
        back_populates="master_scans",
    )
