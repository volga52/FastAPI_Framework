"""Создание модели для сущности posts"""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Boolean, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from database.base_class import Base


class Post(Base):
    """Модель БД для Post"""

    uid = Column(UUIDType, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    image = Column(String)
    content = Column(Text)
    owner_id = Column(UUIDType, ForeignKey("user.uid"))

    owner = relationship("User", back_populates="post")
