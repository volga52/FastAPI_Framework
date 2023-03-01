"""Регистрация маршрутов"""
from fastapi import APIRouter, Request
# from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from game_blog.apps.authapp.router import user_router
from game_blog.setting.config import TemplateResponse


# Экземпляр класса конструктора для создания шаблонизаторов
# templates = Jinja2Templates(directory="game_blog/templatest")

api_router = APIRouter()  # Создание регистрации маршрутов
api_router.include_router(user_router)


# Применение маршрутизации
@api_router.get("/", response_class=HTMLResponse)
async def root(request: Request):  # Request Тип данных 'запрос'
    """Обработчик пути "/" """
    # return templates.TemplateResponse('index.html', {'request': request})
    return TemplateResponse('index.html', {'request': request})
