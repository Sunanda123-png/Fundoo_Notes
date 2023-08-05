import logging
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(filename="fundoo.log", encoding="utf-8", level=logging.INFO,
                    format='%(asctime)s:%(filename)s:%(levelname)s:%(lineno)d:%(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger()


class Settings(BaseSettings):
    """
    This class is created for validation and assigning type of value it accept
    """
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL: str
    PASSWORD: str
    BASE_URL: str


settings = Settings()
