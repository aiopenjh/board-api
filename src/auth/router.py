from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from starlette.concurrency import run_in_threadpool
from src.auth.dependencies import DB
from src.auth.security import hash_password, verify_password, issue_token
from src.user.infrastructure.models import UserModel

router = APIRouter(prefix="/auth", tags=["인증"])


class Credentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value):
        return str(value).lower()

    @field_validator("password")
    @classmethod
    def limit_bytes(cls, value):
        if len(value.encode()) > 72:
            raise ValueError("비밀번호는 UTF-8 기준 72바이트 이하여야 합니다.")
        return value


class UserResponse(BaseModel):
    id: int
    email: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(data: Credentials, db: DB):
    user = UserModel(email=str(data.email), password_hash=await run_in_threadpool(hash_password, data.password))
    db.add(user)
    try:
        await db.flush()
    except IntegrityError:
        raise HTTPException(409, "이미 등록된 이메일입니다.")
    return UserResponse(id=user.user_id, email=user.email)


@router.post("/login", response_model=TokenResponse)
async def login(data: Credentials, db: DB):
    user = await db.scalar(select(UserModel).where(UserModel.email == str(data.email)))
    if user is None or not await run_in_threadpool(verify_password, data.password, user.password_hash):
        raise HTTPException(401, "이메일 또는 비밀번호가 올바르지 않습니다.", headers={"WWW-Authenticate": "Bearer"})
    return TokenResponse(access_token=issue_token(user.user_id))
