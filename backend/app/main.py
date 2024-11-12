from contextlib import asynccontextmanager
from tenacity import retry, wait_fixed, stop_after_delay

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.session import create_db_and_tables
from .router import items_router


@retry(wait=wait_fixed(2), stop=stop_after_delay(30))
def initialize_database():
    create_db_and_tables()

@asynccontextmanager  # see https://fastapi.tiangolo.com/advanced/events/#async-context-manager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Inventory Management App",
    description="This is a simple inventory management app",
    version="0.0.1",
    dependencies=[],
    lifespan=lifespan,
)

app.include_router(items_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
