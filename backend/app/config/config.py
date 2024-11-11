from pydantic_settings import BaseSettings

# come back to https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file 
class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"
    connect_args: dict = {"check_same_thread": False}

    # class Config:
    #     env_file = ".env"

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]

settings = Settings()

# also see https://github.com/JakubPluta/gymhero/blob/main/gymhero/config.py for inspiration on using different settings