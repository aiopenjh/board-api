from sqlalchemy import BigInteger, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.shared.core.models import Base


class PostModel(Base):
    __tablename__ = "posts"
    post_id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
