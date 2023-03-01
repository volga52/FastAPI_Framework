import os

from fastapi.templating import Jinja2Templates

from setting.setting_core import Setting


config = Setting()

SECRET_KEY = config.secret_key.get_secret_value()
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

DB_USER = config.db_user
PG_PASSWORD = config.pg_password
DB_PASS = config.db_pass
DB_NAME = config.db_name
DB_HOST = config.db_host

SQLALCHEMY_DATABASE_URL = ''.join(['sqlite:///./', DB_NAME])
ALEMBIC_SQLALCHEMY_DATABASE_URL = ''.join(['sqlite:///./', DB_NAME])

# Экземпляр класса конструктора для создания шаблонизаторов
templates = Jinja2Templates(directory="templatest")

TemplateResponse = templates.TemplateResponse


if __name__ == '__main__':
    for key, value in config:
        print(f'{key}: {value} <{type(value)}>')
    print()
    print(SECRET_KEY)
    print(SQLALCHEMY_DATABASE_URL)
    print(ALEMBIC_SQLALCHEMY_DATABASE_URL)
