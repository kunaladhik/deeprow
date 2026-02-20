"""
Authentication request/response schemas

These define the contract between frontend and backend for signup/login.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignupRequest(BaseModel):
    """User signup request"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Minimum 8 characters")
    full_name: Optional[str] = None
    persona: Optional[str] = None  # teacher, nurse, researcher, etc.
    
    class Config:
        example = {
            "email": "alice@example.com",
            "password": "securepassword123",
            "full_name": "Alice Johnson",
            "persona": "teacher"
        }


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str
    
    class Config:
        example = {
            "email": "alice@example.com",
            "password": "securepassword123"
        }


class TokenResponse(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    """User profile response"""
    id: int
    email: str
    full_name: Optional[str] = None
    persona: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True
        example = {
            "id": 1,
            "email": "alice@example.com",
            "full_name": "Alice Johnson",
            "persona": "teacher",
            "created_at": "2024-01-15T10:30:00"
        }
