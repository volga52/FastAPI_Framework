"""Модуль обработчик данных"""
import json

from apps.authapp.utils import get_current_user


class PostRequest:
    """Класс-обработчик данных запроса"""
    @staticmethod
    def parse_body_json(data: bytes):
        """Декодирование данных из json-данных"""
        data = data.decode('utf-8')
        data = json.loads(data)
        return data


async def setup_user_dict(request, db):
    """Создание словаря данных для текущего пользователя"""
    token = request.cookies.get('token')
    response_dict = {'request': request}

    if token:
        user = await get_current_user(db, token)
        response_dict['user'] = user

    return response_dict
