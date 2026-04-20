from pydantic import BaseModel
from typing import Optional
from src.auth.models import UserRole

class LoginRequest(BaseModel):
    email: str
    password: str
    role: UserRole


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: UserRole
    name: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None
    company: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    name: Optional[str] = None
    department: Optional[str] = None
    company_name: Optional[str] = None


class RegisterResponse(BaseModel):
    message: str
    user: UserResponse


class LoginResponse(BaseModel):
    token: str
    user: UserResponse
