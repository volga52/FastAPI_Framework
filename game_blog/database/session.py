from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from game_blog.setting.config import SQLALCHEMY_DATABASE_URL


# Объект подключения
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args={"check_same_thread": False})
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """Функция создает объект сессии"""
    try:
        # Создание объекта сессии
        db = SessionLocal()
        yield db
    finally:
        db.close()
