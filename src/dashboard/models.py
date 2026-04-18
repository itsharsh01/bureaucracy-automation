from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from datetime import datetime
from src.db.base_class import Base

class Complaint(Base):
    __tablename__ = "complaints"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    complaint = Column(Text, nullable=False)
    product = Column(String, nullable=False)
    dispute_probability = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    route_to_human = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)