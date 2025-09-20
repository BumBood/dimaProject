import asyncio
from fastapi import FastAPI
from database import create_tables
from routers.universities_router import router_universities
from routers.auth_router import auth_router
from routers.review_routers import router_reviews
from routers.user_routers import router_user
from routers.tables_router import router_tables

import uvicorn

app = FastAPI()

app.include_router(router_universities)
app.include_router(router_tables)
app.include_router(router_reviews)
app.include_router(router_user)
app.include_router(auth_router)

if __name__ == "__main__":
    asyncio.run(create_tables())

    uvicorn.run("main:app", reload=True)