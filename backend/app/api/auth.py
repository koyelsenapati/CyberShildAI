from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)

from app.services.auth_service import (
    register,
    login,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=RegisterResponse
)
def register_user(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register(
        db=db,
        request=request,
    )

@router.post(
    "/login",
    response_model=LoginResponse
)
def login_user(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return login(
        db=db,
        request=request,
    )
