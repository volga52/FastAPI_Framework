"""Создание модели для сущности posts"""
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from game_blog.db_core import Base


class Post(Base):
    """Модель для БД Pjst"""
    __tablename__ = "posts"

    uid = Column(UUIDType, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(Integer, ForeignKey("users.uid"))

    owner = relationship("User", back_populates="posts")
