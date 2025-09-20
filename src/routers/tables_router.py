import asyncio
from fastapi import APIRouter
from parser.monitoring import Monitor
from queries.tablesorm import TablesORM
from queries.universityorm import UniversityORM


router_tables = APIRouter()


@router_tables.on_event("startup")
async def startup():
    # if sorted(inspect(sync_engine).get_table_names()) != sorted(list(Base.metadata.tables.keys())):
    await TablesORM.create_tables()

# async def run_update_universities():
#     while True:
#         await UniversityORM.universities_update()
#         await asyncio.sleep(30)

# @router_tables.on_event("startup")
# async def startup_update_universities():
#     update_task = asyncio.create_task(run_update_universities())
#     await update_task