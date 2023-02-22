"""Модуль обработчик данных"""
import json


class PostRequest:
    """Класс-обработчик данных запроса"""
    @staticmethod
    def parse_body_json(data: bytes):
        """Декодирование данных из json-данных"""
        data = data.decode('utf-8')
        data = json.loads(data)
        return data
