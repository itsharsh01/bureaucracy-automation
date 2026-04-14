from sqlalchemy import Column, Integer, String
from src.db.base_class import Base

class DashboardMetric(Base):
    __tablename__ = "dashboard_metrics"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String, index=True)
    metric_value = Column(Integer)
