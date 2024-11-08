from pydantic_settings import BaseSettings

# come back to https://fastapi.tiangolo.com/advanced/settings/#reading-a-env-file 
class Settings(BaseSettings):
    database_url: str = "sqlite:///./database.db"
    connect_args: dict = {"check_same_thread": False}

    # class Config:
    #     env_file = ".env"

settings = Settings()