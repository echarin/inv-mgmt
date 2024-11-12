from sqlmodel import Session, SQLModel, create_engine

from ..config.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def clear_db():
    SQLModel.metadata.drop_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def init_db(session: Session):
    user = session.exec()