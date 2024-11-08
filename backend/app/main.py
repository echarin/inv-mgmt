from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from .db.session import clear_db, create_db_and_tables
from .routes import items


@asynccontextmanager # see https://fastapi.tiangolo.com/advanced/events/#async-context-manager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    clear_db()


app = FastAPI(
    title="Inventory Management App",
    description="This is a simple inventory management app",
    version="0.0.1",

    dependencies=[],
    lifespan=lifespan
)

app.include_router(items.router)


@app.get("/")
async def root():
    return {"hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)