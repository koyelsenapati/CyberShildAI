from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class Report(Base):
    __tablename__ = "reports"

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

    report_type = Column(
        String(50),
        nullable=False
    )

    file_path = Column(
        String(500),
        nullable=True
    )

    json_file_path = Column(
        String(500),
        nullable=True,
    )

    status = Column(
        String(50),
        default="Generated"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    user = relationship(
        "User",
        back_populates="reports"
    )
