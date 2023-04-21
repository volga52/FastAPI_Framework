"""Модуль содержит механизм извлечения конфиденциальных данных из файла .env"""
import pathlib

from pydantic import BaseSettings, SecretBytes, SecretStr


class Setting(BaseSettings):
    """Класс организации данных"""
    secret_key: SecretBytes

    db_user: str
    pg_password: str
    db_pass: str
    db_name: str
    db_host: str

    mail_username: str
    mail_password: SecretStr
    mail_address: str

    class Config:
        # env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"
        # env_file = f"{pathlib.Path(__file__).resolve().parent.parent}/.env"
        env_file = ["/etc/secrets/.env",
                    f"{pathlib.Path(__file__).resolve().parent}/.env",
                    f"{pathlib.Path(__file__).resolve().parent.parent}/.env"]

        env_file_encoding = 'utf-8'
