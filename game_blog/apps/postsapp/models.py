"""Создание модели для сущности posts"""
import datetime

from sqlalchemy import Boolean, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from database.base_class import Base


class Post(Base):
    """Модель БД для Post"""

    uid = Column(UUIDType, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    content = Column(String)
    owner_id = Column(UUIDType, ForeignKey("user.uid"))

    owner = relationship("User", back_populates="post")
