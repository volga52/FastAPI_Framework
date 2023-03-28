from typing import Optional
from pydantic import BaseModel
import datetime
from apps.authapp.schemas import User


class PostBase(BaseModel):
    """Базовое тело модели (состав)"""
    title: str
    body: str


class PostList(PostBase):
    """Лист, экземпляр модели"""
    created_date: Optional[datetime.datetime]
    owner_id: int
    owner: User

    class Config:
        orm_model = True
