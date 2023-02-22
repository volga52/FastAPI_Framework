import pathlib
from pydantic import BaseSettings, SecretStr, SecretBytes


class Setting(BaseSettings):
    secret_key: SecretBytes

    db_user: str
    pg_password: str
    db_pass: str
    db_name: str
    db_host: str

    class Config:
        env_file = f"{pathlib.Path(__file__).resolve().parent}/.env"
        env_file_encoding = 'utf-8'
