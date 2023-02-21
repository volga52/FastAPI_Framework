"""Инициация пакета и приложения FastAPI"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from game_blog import apps
from game_blog.apps.mainapp.routes import router

from game_blog.db_core import engine

apps.users.models.Base.metadata.create_all(bind=engine)
apps.posts.models.Base.metadata.create_all(bind=engine)


def create_app(debug=True):
    """Создание приложения FastAPI"""
    app = FastAPI(debug=debug)
    # mount - монтировать
    app.mount('/static',
              StaticFiles(directory='game_blog/static'), name='static')
    app.include_router(router)
    return app
