"""Модуль создания сущности зарегистрированного пользователя"""
import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType

# from apps.postapp import Post
from game_blog.db_core import Base


class User(Base):
    __tablename__ = 'authapp'

    uid = Column(UUIDType, default=uuid4, primary_key=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    email =Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")
    token = Column(String(64), nullable=True)
