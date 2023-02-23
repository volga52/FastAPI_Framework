from typing import List, Optional   # Типы данных для аннотации

from fastapi import Request
from sqlalchemy.orm import Session

from game_blog.apps.authapp.models import User
from game_blog.core.hashing import Hasher
from game_blog.core.requests_framework import PostRequest


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
    """Класс обработки формы создания поьзователя"""
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


class UserLoginForm(UserForm):
    """Класс обработки формы ввод логина и пароля"""
    def __init__(self, request: Request):
        super().__init__(request)
        self.password: Optional[str] = None
        self.user: Optional[str] = None

    async def load_data(self):
        data: bytes = await self.request.body()    # Получаемые данные в байтах
        data = PostRequest.parse_body_json(data)
        self.username = data.get('username')
        self.password = data.get('password')

    async def is_valid(self, db: Session):

        if not all(self.username, self.password):
            self.errors.append('Please input data')
        else:
            user = db.query(User).filter(
                User.username == self.username).first()
            self.user = user
            if not user:
                self.errors.append(f'No this user with '
                                   f'username: "{self.username}"')
            else:
                verified = Hasher.verify_password(self.password,
                                                  user.hashed_password)
                if not verified:
                    self.errors.append('Not correct password')
        if not self.errors:
            return True

        return False


class UserUpdateForm(UserForm):
    """Класс обработки формы изменение данных пользователя"""
    def __init__(self, request: Request):
        super().__init__(request)
        self.old_name: Optional[str] = None
        self.email: Optional[str] = None
        self.user: Optional[str] = None

    async def load_data(self):
        data: bytes = await self.request.body()
        data: dict = PostRequest.parse_body_json(data)
        self.username = data.get('username')
        self.email = data.get('email')
        self.old_name = data.get('old')

    async def is_valid(self, db: Session):
        await self.validate_username(db)
        await self.validate_email(db)

        if not self.errors:
            return True
        return False

    async def validate_email(self, db: Session):
        """Проверка email на повтор"""
        user = db.query(User).filter(User.email == self.email).first()
        if user:
            self.errors.append(f"User with email {self.email} has already")
