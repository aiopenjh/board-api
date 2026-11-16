from sqlalchemy import select
from src.board.infrastructure.sqlalchemy.models import PostModel


async def list_posts(db, offset, limit):
    result = await db.scalars(select(PostModel).order_by(PostModel.post_id.desc()).offset(offset).limit(limit))
    return result.all()


async def find_post(db, post_id):
    return await db.get(PostModel, post_id)


async def save_post(db, post):
    db.add(post)
    await db.flush()
    await db.refresh(post)
    return post
