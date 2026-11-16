from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from src.shared.core.models import Base


class UserModel(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)
