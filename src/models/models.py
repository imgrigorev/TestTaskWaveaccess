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
from sqlalchemy_utils import EmailType, PasswordType

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(EmailType(50), unique=True, nullable=False)
    role = Column(String(70), unique=False, nullable=True)
    # role_id = Column(Integer, ForeignKey('user_role.id'), nullable=True)
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

# class Role(Base):
#     __tablename__ = "user_role"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(50))
#
#     users = relationship("User", back_populates="role_id")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)
    priority = Column(String(50))
    status = Column(String(50), nullable=False)
    title = Column(String(50))
    description = Column(String())
    executor_id = Column(Integer)
    # executor = Column(String)
    creator = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)


# class Status(Base):
#     __tablename__ = "status"
#
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50), nullable=False)




