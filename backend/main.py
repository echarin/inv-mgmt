import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"hello world"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)