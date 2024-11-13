import os
from typing import ClassVar
from pydantic import MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


# come back to https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file
# reference: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/config.py
class Settings(BaseSettings):
    # ".env" compared to "./backend/app/config/config.py"
    BASE_DIR: ClassVar[str] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_file_path: ClassVar[str] = os.path.join(BASE_DIR, '.env')

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_ignore_empty=True,
        extra="ignore",
        env_file_encoding="utf-8",
    )

    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MySQLDsn.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_USER,
            password=self.MYSQL_PASSWORD,
            host=self.MYSQL_HOST,
            port=self.MYSQL_PORT,
            path=f"{self.MYSQL_DATABASE}",
        )

settings = Settings()

# also see https://github.com/JakubPluta/gymhero/blob/main/gymhero/config.py for inspiration on using different settings
