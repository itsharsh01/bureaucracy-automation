from sqlalchemy import Column, Integer, Text, ForeignKey
from src.db.base_class import Base

class ChatSession(Base):
    __tablename__ = "chatbot_sessions"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("public.auth_users.id"))
    transcript = Column(Text)
