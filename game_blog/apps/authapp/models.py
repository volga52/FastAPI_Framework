"""Модуль создания сущности зарегистрированного пользователя"""
import datetime
import json
import time

from authlib.jose import JsonWebSignature
from sqlalchemy import Boolean, Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType, UUIDType
from uuid import uuid4

from apps.postsapp.models import Post
from setting.config import SECRET_KEY
from database.base_class import Base


class User(Base):
    # __tablename__ = 'authapp'
    # Имя таблицы проставляется автоматически
    # Это свойство установили в классе game_blog.database.base_class.CustomBase

    uid = Column(UUIDType, default=uuid4, primary_key=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(EmailType)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    post = relationship("Post", back_populates="owner")
    token = Column(String(64), nullable=True)

    def get_reset_token(self, expires_sec=1800):
        jws = JsonWebSignature(['HS256'])
        protected = {'alg': 'HS256'}
        payload = json.dumps({'expires_sec': expires_sec,
                              'time_sending': time.time(),
                              'user_uid': str(self.uid)}).encode('utf-8')
        secret = SECRET_KEY
        return jws.serialize_compact(protected, payload, secret). \
            decode('utf-8')

    @staticmethod
    def get_pay_from_reset_token(token):
        jws = JsonWebSignature(['HS256'])
        data = jws.deserialize_compact(token, SECRET_KEY)
        payload_json = json.loads(data['payload'])

        time_left = payload_json['time_sending'] + payload_json['expires_sec'] \
                    - time.time()
        print(time_left)

        if time_left < 0:
            return False
        else:
            return payload_json


class Token(Base):
    uid = Column(UUIDType, default=uuid4, primary_key=True)
    token = Column(UUIDType, unique=True, nullable=True,
                   index=True, default=uuid4)
    expires = Column(DateTime)
    user_uid = Column(UUIDType, ForeignKey('user.uid'))
