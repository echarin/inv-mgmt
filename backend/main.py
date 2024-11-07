import uvicorn
from fastapi import FastAPI

from backend.routers import items


app = FastAPI(
    title="Inventory Management App",
    description="This is a simple inventory management app",
    version="0.0.1",

    dependencies=[]
)


app.include_router(items.router)


@app.get("/")
def root():
    return {"hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)