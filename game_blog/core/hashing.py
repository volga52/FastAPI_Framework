"""
Модуль содержит компоненты хеширования
"""
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """Класс обеспечивающий хеширование"""
    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Хеширование паролей пользователей"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """Обеспечение конвертации содержимого запросов"""
        return pwd_context.hash(password)
