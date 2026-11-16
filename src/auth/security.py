import os
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt

ALGORITHM = "HS512"
TOKEN_MINUTES = 60


def secret_key():
    value = os.getenv("JWT_SECRET_KEY", "")
    if len(value.encode()) < 64:
        raise RuntimeError("JWT_SECRET_KEY를 임의의 64바이트 이상 값으로 설정하세요.")
    return value


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def issue_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": str(user_id), "iat": now, "exp": now + timedelta(minutes=TOKEN_MINUTES)},
                      secret_key(), algorithm=ALGORITHM)


def decode_token(token: str) -> int:
    payload = jwt.decode(token, secret_key(), algorithms=[ALGORITHM],
                         options={"require": ["sub", "iat", "exp"]})
    user_id = int(payload["sub"])
    if user_id <= 0:
        raise ValueError("잘못된 사용자")
    return user_id
