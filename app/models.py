from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
jst = timezone(timedelta(hours=9))


def now_jst():
    return datetime.now(jst)


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    notes: Mapped[List["Note"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content_md: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=now_jst, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=now_jst, onupdate=now_jst, index=True
    )

    user: Mapped["User"] = relationship(back_populates="notes")

    def __repr__(self):
        return f"<Note {self.id} user={self.user_id}>"
