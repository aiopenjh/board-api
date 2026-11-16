from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, Field, ConfigDict
from src.auth.dependencies import DB, CurrentUser
from src.board.infrastructure.sqlalchemy.models import PostModel
from src.board.infrastructure.sqlalchemy import repository
from src.board.application.service import require_post, require_author

router = APIRouter(prefix="/posts", tags=["게시글"])


class PostInput(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=100000)


class PostResponse(PostInput):
    id: int
    author_id: int


def response(post):
    return PostResponse(id=post.post_id, title=post.title, content=post.content, author_id=post.author_id)


@router.get("", response_model=list[PostResponse])
async def list_posts(db: DB, offset: int = Query(0, ge=0), limit: int = Query(20, ge=1, le=100)):
    return [response(p) for p in await repository.list_posts(db, offset, limit)]


@router.get("/{post_id}", response_model=PostResponse)
async def detail(post_id: int, db: DB):
    return response(await require_post(db, post_id))


@router.post("", response_model=PostResponse, status_code=201)
async def create(data: PostInput, db: DB, user: CurrentUser):
    post = PostModel(title=data.title, content=data.content, author_id=user.user_id)
    return response(await repository.save_post(db, post))


@router.put("/{post_id}", response_model=PostResponse)
async def update(post_id: int, data: PostInput, db: DB, user: CurrentUser):
    post = await require_post(db, post_id)
    require_author(post, user.user_id)
    post.title, post.content = data.title, data.content
    return response(await repository.save_post(db, post))


@router.delete("/{post_id}", status_code=204)
async def delete(post_id: int, db: DB, user: CurrentUser):
    post = await require_post(db, post_id)
    require_author(post, user.user_id)
    await db.delete(post)
    await db.flush()
    return Response(status_code=204)
