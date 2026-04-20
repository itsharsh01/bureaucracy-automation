import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum, DateTime
from src.db.base_class import Base


class QueryStatus(str, enum.Enum):
    PENDING = "PENDING"
    SOLVED = "SOLVED"
    CLOSED = "CLOSED"


class Query(Base):
    """Stores every citizen query raised through the chatbot."""

    __tablename__ = "chatbot_queries"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True, index=True)
    state = Column(String(100), nullable=False)
    company = Column(String(200), nullable=False)
    query_text = Column(Text, nullable=False)
    company_response = Column(Text, nullable=True)
    department = Column(String(200), nullable=False)         # ML model prediction
    status = Column(
        SQLEnum(QueryStatus, name="querystatus"),
        default=QueryStatus.PENDING,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
