from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from src.shared.core.database import engine
from src.shared.core.models import Base
from src.user.infrastructure.models import UserModel
from src.board.infrastructure.sqlalchemy.models import PostModel
from src.auth.router import router as auth_router
from src.auth.security import secret_key
from src.board.presentation.router import router as posts_router


@asynccontextmanager
async def lifespan(app):
    secret_key()
    # 수업 공용 DB에는 실수로 테이블을 만들지 않습니다.
    if engine.url.database in ("postgres", "template0", "template1"):
        raise RuntimeError("게시판 전용 DB를 DATABASE_URL에 지정하세요. 공용 수업 DB는 변경하지 않습니다.")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        await engine.dispose()


app = FastAPI(title="개인 게시판 API", version="1.0.0", lifespan=lifespan)


@app.exception_handler(SQLAlchemyError)
async def database_error(request: Request, exc: SQLAlchemyError):
    return JSONResponse(status_code=500, content={"detail": "DB 처리에 실패했습니다."})


app.include_router(auth_router)
app.include_router(posts_router)
