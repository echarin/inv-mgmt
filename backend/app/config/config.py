from pydantic import MySQLDsn
from pydantic_settings import BaseSettings


# come back to https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file
# reference: https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/core/config.py
class Settings(BaseSettings):
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
