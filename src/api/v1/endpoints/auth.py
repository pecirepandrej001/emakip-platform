from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from src.core.database import get_db
from src.core.security import create_access_token, hash_password, verify_password
from src.db.repositories.user_repository import UserRepository

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    if await repo.get_by_email(str(payload.email)):
        raise HTTPException(status_code=409, detail="Email already registered")
    user = await repo.create(
        email=str(payload.email), full_name=payload.full_name, hashed_password=hash_password(payload.password)
    )
    return TokenResponse(access_token=create_access_token(user.email))

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db)):
    user = await UserRepository(session).get_by_email(str(payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(user.email))
