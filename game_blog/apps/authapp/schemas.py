from typing import Optional, List

from pydantic import BaseModel, EmailStr, UUID4, Field, validator
from datetime import datetime


class UserBase(BaseModel):
    """Формирует тело ответа с деталями пользователя"""
    uid: str
    email: EmailStr
    username: str


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias='access_token')
    expires: datetime
    token_type: Optional[str] = 'bearer'

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        """Конвертирует UUID в hex строку"""
        return value.hex


class User(UserBase):
    """Формирует тело ответа с деталями пользователя и token-ом"""
    token: TokenBase = ()


class UserCreate(BaseModel):
    """Проверяет sing-up запрос"""
    username: str
    email: EmailStr
    password: str


class EmailSchema(BaseModel):
    email: List[EmailStr]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
