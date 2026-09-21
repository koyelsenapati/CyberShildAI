"""
CyberShield AI
Authentication Schemas
"""

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)

class RegisterRequest(BaseModel):

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username"
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="User password"
    )

class LoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8
    )

class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"

class RegisterResponse(BaseModel):

    message: str

    user_id: int

class UserResponse(BaseModel):

    id: int

    username: str

    full_name: str

    email: EmailStr

    role: str

    is_active: bool

    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True
    )

class LoginResponse(BaseModel):

    message: str

    access_token: str

    token_type: str = "bearer"

    user: UserResponse
