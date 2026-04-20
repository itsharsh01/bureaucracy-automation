from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from src.db.base_class import Base
from enum import Enum

class UserRole(str, Enum):
    company = "company"
    customer = "customer"
    admin = "admin"
    operator = "operator"

class User(Base):
    __tablename__ = "app_users"
    __table_args__ = {"schema": "public", "extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.customer)
    department = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
