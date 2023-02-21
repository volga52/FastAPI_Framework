"""Создание модели для сущности пользователь"""
import datetime

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType

from game_blog.db_core import Base


class User(Base):
    """Модель для БД пользователь"""
    __tablename__ = "users"

    uid = Column(UUIDType, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")     # owner-владелец
