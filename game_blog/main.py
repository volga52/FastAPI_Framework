from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from apps.mainapp.routes import api_router


def create_app(debug=True):
    """Создание приложения FastAPI"""
    app = FastAPI(debug=debug)
    # mount - монтировать
    app.mount('/static',
              StaticFiles(directory='static'), name='static')
    app.include_router(api_router)
    return app
