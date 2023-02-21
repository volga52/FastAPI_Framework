"""Инициация пакета и приложения FastAPI"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from game_blog import users, posts
from game_blog.main.routes import router

from game_blog.db_core import engine
from game_blog.users import models
from game_blog.posts import models

users.models.Base.metadata.create_all(bind=engine)
posts.models.Base.metadata.create_all(bind=engine)


def create_app(debug=True):
    """Создание приложения FastAPI"""
    app = FastAPI(debug=debug)
    # mount - монтировать
    app.mount('/static',
              StaticFiles(directory='game_blog/static'), name='static')
    app.include_router(router)
    return app
