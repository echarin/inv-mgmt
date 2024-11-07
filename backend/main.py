from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

# global dependency
app = FastAPI(dependencies=[Depends(get_query_token)])

# to include all the routes from these routers, as part of the main app
app.include_router(users.router)
app.include_router(items.router)

# additional configuration outside the admin.py file
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}