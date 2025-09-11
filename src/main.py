import asyncio
from fastapi import FastAPI
from database import create_tables
from routers.universities_router import router_universities

import uvicorn

app = FastAPI()

app.include_router(router_universities)

if __name__ == "__main__":
    asyncio.run(create_tables())

    uvicorn.run("main:app", reload=True)