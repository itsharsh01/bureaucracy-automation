from sqlalchemy import Column, Integer, String
from src.db.base_class import Base

class User(Base):
    __tablename__ = "auth_users"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
