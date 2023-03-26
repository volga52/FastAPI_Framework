import hashlib
import random
import string

# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_mail import MessageSchema, FastMail
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta

from apps.authapp.models import User, Token
from apps.authapp.schemas import UserCreate
from setting.config import mail_conf


def get_random_string(length=12):
    """Генерирует случайную строку, 'соль'"""
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    """Генерирует хеш из пароля и соли"""
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac('sha256', password.encode(),
                              salt.encode(), 100_000)
    # Получаем hash в виде 16-тиричной строки
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    """Проверяет хеш пароля с хешем из БД"""
    salt, hashed = hashed_password.split('$')
    return hash_password(password, salt) == hashed


async def get_user_by_email(email: str, db: Session):
    """Возвращает информацию о пользователе по email"""
    user = db.query(User).filter(User.email == email).first()
    return user


async def get_user_by_token(token: str, db: Session):
    """Получение юзера по token-у, актуальному"""
    user = db.query(User).join(Token).filter(
        and_(Token.token == token, Token.expires > datetime.now())).first()
    return user


async def get_token_by_user(user_uid: str, db: Session):
    """Получаем объект token, актуальный, по id пользователя"""
    token = db.query(Token).filter(
        and_(Token.user_uid == user_uid, Token.expires > datetime.now())
        ).first()
    return token


async def create_user_token(user_uid: str, db: Session):
    """Создание token-а для пользователя по его id"""
    token = Token(
        expires=datetime.now() + timedelta(weeks=2),
        user_uid=user_uid
    )
    db.add(token)
    db.commit()
    return token


async def do_hash_password(password):
    """Непосредственное создание хеша"""
    salt = get_random_string()
    hashed_password = hash_password(password, salt)
    return f"{salt}${hashed_password}"


async def create_user(user: UserCreate, db: Session):
    """Создание пользователя в БД"""
    hashed_password = await do_hash_password(user.password)
    user_db = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    user_uid = user_db.uid

    return {**user.dict(), 'uid': user_uid, 'is_active': True}


async def get_current_user(db: Session, token: str):
    """Получение текущего пользователя по token-у"""
    user = await get_user_by_token(token, db)
    return user


async def send_message(url, user: User):
    """Отправка сообщения пользователю о смене пароля"""
    html = f"""For reset password use this url '{url}'"""
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[user.email],  # List of recipients, as many as you can pass
        body=html,
        subtype="html"
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)
