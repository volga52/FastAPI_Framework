"""Регистрация маршрутов"""
from fastapi import APIRouter, Depends
from fastapi.requests import Request
# from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from apps.authapp.router import user_router
from apps.authapp.utils import get_current_user

from setting.config import TemplateResponse
from core.requests_framework import setup_user_dict
# from setting.decorators import login_required
from database.session import get_db


# Экземпляр класса конструктора для создания шаблонизаторов
# templates = Jinja2Templates(directory="game_blog/templates")

api_router = APIRouter()  # Создание регистрации маршрутов
api_router.include_router(user_router)


# Применение маршрутизации
@api_router.get("/", response_class=HTMLResponse)
@api_router.post("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    """Обработчик пути "/" """
    request.name = 'home'
    response_dict = await setup_user_dict(request, db)
    # return templates.TemplateResponse('index.html', {'request': request})
    # return TemplateResponse('index.html', {'request': request})
    return TemplateResponse('index.jinja2', response_dict)
