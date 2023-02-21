"""Регистрация маршрутов"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


# Экземпляр класса конструктора для создания шаблонизаторов
templates = Jinja2Templates(directory="game_blog/templatest")
router = APIRouter()  # Создание регистрации маршрутов


# Применение маршрутизации
@router.get("/", response_class=HTMLResponse)
async def root(request: Request):  # Request Тип данных 'запрос'
    """Обработчик пути "/" """
    return templates.TemplateResponse('index.html', {'request': request})
