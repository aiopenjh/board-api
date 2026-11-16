from typing import Annotated
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.shared.core.database import get_db
from src.user.infrastructure.models import UserModel
from src.auth.security import decode_token

DB = Annotated[AsyncSession, Depends(get_db, scope="function")]
bearer = HTTPBearer(auto_error=False)


async def current_user(db: DB, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]):
    error = HTTPException(401, "로그인이 필요합니다.", headers={"WWW-Authenticate": "Bearer"})
    if credentials is None:
        raise error
    try:
        user_id = decode_token(credentials.credentials)
    except (jwt.PyJWTError, ValueError, KeyError, TypeError):
        raise error
    user = await db.get(UserModel, user_id)
    if user is None:
        raise error
    return user


CurrentUser = Annotated[UserModel, Depends(current_user)]
