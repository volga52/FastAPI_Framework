"""Модуль создания сущности зарегистрированного пользователя"""
import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType

from apps.postsapp.models import Post
from database.base_class import Base


class User(Base):
    # __tablename__ = 'authapp'
    # Имя таблицы проставляется автоматически
    # Это свойство установили в классе game_blog.database.base_class.CustomBase

    uid = Column(UUIDType, default=uuid4, primary_key=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    email =Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")
    token = Column(String(64), nullable=True)


class Token(Base):
    uid = Column(UUIDType, default=uuid4, primary_key=True)
    token = Column(UUIDType, unique=True, nullable=True,
                   index=True, default=uuid4)
    expires = Column(DateTime)
    user_id = Column(UUIDType, ForeignKey('user.uid'))
