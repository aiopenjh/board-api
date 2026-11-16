from fastapi import HTTPException
from src.board.infrastructure.sqlalchemy import repository


async def require_post(db, post_id):
    post = await repository.find_post(db, post_id)
    if post is None:
        raise HTTPException(404, "게시글을 찾을 수 없습니다.")
    return post


def require_author(post, user_id):
    if post.author_id != user_id:
        raise HTTPException(403, "작성자만 수정하거나 삭제할 수 있습니다.")
