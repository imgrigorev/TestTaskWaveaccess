import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, force_auto_coercion, PasswordType

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(EmailType(50), unique=True, nullable=False)
    role = Column(String(50))
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)

    tokens = relationship(
        "UserToken",
        back_populates="user",
        lazy='dynamic',
        cascade="all, delete-orphan",
    )
    # posts = relationship(
    #     "Post",
    #     back_populates="author",
    #     lazy='joined',
    #     cascade="all, delete-orphan",
    # )

class UserToken(Base):
    __tablename__ = "user_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False
    )
    token = Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4
    )
    expires = Column(DateTime)

    user = relationship("User", back_populates="tokens", lazy='joined')

# class Task(Base):
#     __tablename__ = "tasks"
#     number = Column()
#     priority = Column(String(50))
#     status = Column(String(50))
#     title = Column(String(50))
#     description = Column(String())
#     executor = Column(String(50))
#     creator = Column(String(50))
#     created_at = Column(DateTime)
#     updated_at = Column(DateTime)
#     type = Column(String(50))
#     blocking_tasks = Column(String(50))
# task = Table(
#     'task',
#     metadata,
# Column("number", primary_key=True, index=True),
#     Column("username", String, nullable=False),
#     Column("priority", String, nullable=False),
#     Column("status", String, nullable=False),
#     Column("title", String, nullable=False),
#     Column("description", String, nullable=False),
#     Column("executor", String, nullable=False),
#     Column("creator", String, nullable=False),
#     Column("created_at",  TIMESTAMP, default=datetime.utcnow),
#     Column("updated_at",  TIMESTAMP, default=datetime.utcnow),
#     Column("type", String, nullable=False),
#     Column("blocking_tasks", String, nullable=False),
# )


