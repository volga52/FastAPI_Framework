import os
from pathlib import Path

from fastapi.templating import Jinja2Templates

from .img_extension import IMG_EXTENSION_LIST
from setting.setting_core import Setting
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


config = Setting()

SECRET_KEY = config.secret_key.get_secret_value()
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

DB_USER = config.db_user
PG_PASSWORD = config.pg_password
DB_PASS = config.db_pass
DB_NAME = config.db_name
DB_HOST = config.db_host
MAIL_USERNAME = config.mail_username
MAIL_PASSWORD = config.mail_password.get_secret_value()
MAIL_ADDRESS = config.mail_address

ROOT_URL = Path(__file__).resolve().parent.parent
MEDIA_URL = os.path.join(ROOT_URL, 'media')

SQLALCHEMY_DATABASE_URL = ''.join(['sqlite:///./', DB_NAME])
ALEMBIC_SQLALCHEMY_DATABASE_URL = ''.join(['sqlite:///./', DB_NAME])

# Экземпляр класса конструктора для создания шаблонизаторов
templates = Jinja2Templates(directory="templatest")

TemplateResponse = templates.TemplateResponse

# Настройки для почтового сервера
mail_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_ADDRESS,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.bk.ru",
    MAIL_FROM_NAME="Test Messages",
    MAIL_TLS=False,
    MAIL_SSL=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
