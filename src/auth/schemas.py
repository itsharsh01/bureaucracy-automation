from pydantic import BaseModel
from typing import Optional
from src.auth.models import UserRole

class LoginRequest(BaseModel):
    email: str
    password: str
    role: UserRole

class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    name: Optional[str] = None

class LoginResponse(BaseModel):
    token: str
    user: UserResponse
