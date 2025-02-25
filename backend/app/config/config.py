import os

from pydantic import AnyUrl, MySQLDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    DEBUG: bool = ENVIRONMENT == "dev"

    # these default values are used for testing/dev environments
    MYSQL_DATABASE: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_PORT: int = 0

    SQLITE_DATABASE_URL: str = "sqlite:///./database.db"

    @property
    def DATABASE_URL(self) -> AnyUrl:
        # used for unit tests and running backend for local development
        if self.ENVIRONMENT == "dev":
            return AnyUrl.build(
                scheme="sqlite",
                host="",
                path=self.SQLITE_DATABASE_URL.replace("sqlite:///", ""),
            )
        # used for running app locally on production build, or when deployed
        else:
            return MySQLDsn.build(
                scheme="mysql+pymysql",
                username=self.MYSQL_USER,
                password=self.MYSQL_PASSWORD,
                host=self.MYSQL_HOST,
                port=self.MYSQL_PORT,
                path=f"{self.MYSQL_DATABASE}",
            )


settings = Settings()
