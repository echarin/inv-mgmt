from sqlmodel import Session, SQLModel, create_engine

from ..config.config import settings


engine = create_engine(settings.database_url, connect_args=settings.connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session