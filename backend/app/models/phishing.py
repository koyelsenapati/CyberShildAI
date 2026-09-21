"""Phishing scan persistence model matching the current Alembic schema."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base

class PhishingScan(Base):
    __tablename__ = "phishing_scans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String(500), nullable=False)
    prediction = Column(String(50), nullable=False)
    probability = Column(Float, nullable=False)
    confidence_score = Column(Integer, nullable=False)
    verdict = Column(String(50), nullable=False)
    domain = Column(String(255), nullable=True)
    reputation = Column(String(100), nullable=True)
    risk_level = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="phishing_scans")
