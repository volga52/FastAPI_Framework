from typing import List, Optional   # Типы данных для аннотации

from fastapi import Request
from sqlalchemy.orm import Session

# from game_blog.core.hashing import Hasher
# from game_blog.core.requests_framework import PostRequest
from game_blog.apps.authapp.models import User


class UserForm:
    """Базовый класс для всех userform"""
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None

    async def load_data(self):
        """Вытягивание данных переопределяемый метод"""
        pass

    async def is_valid(self, db: Session):
        """Валидация данных переопределяемый метод"""
        return True

    async def validate_username(self, db: Session):
        """Проверка пользователя"""
        user = db.query(User).filter(User.username == self.username).first()
        if user:
            self.errors.append(
                f"User with username {self.username} has already")


class UserCreationForm(UserForm):
    """Класс создания поьзователя"""
    def __init__(self, request: Request):
        super().__init__(request)
        self.password: Optional[str] = None
        self.email: Optional[str] = None
        self.confirm_password: Optional[str] = None

    async def load_data(self):
        """Из формы вытягиваем параметры"""
        form = await self.request.form()
        self.username = form.get('username')
        self.email = form.get('email')
        self.password = form.get('password')
        self.confirm_password = form.get('confirm_password')

    async def is_valid(self, db: Session):
        """Валидация данных"""
        await self.validate_username(db)
        await self.validate_email(db)
        if not self.username or not len(self.username) >= 3:
            self.errors.append("Username should be > 3 chars")

        if not self.password or not len(self.password) >= 4:
            self.errors.append("Password must be > 4 chars")
        if not self.errors:
            return True
        return False

    async def validate_email(self, db: Session):
        """Проверка email на повтор"""
        user = db.query(User).filter(User.email == self.email).first()
        if user:
            self.errors.append(f"User with email {self.email} has already")
