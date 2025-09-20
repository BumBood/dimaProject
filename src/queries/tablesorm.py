from database import engine
from models import Base
class TablesORM:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        return {'ok': True, 'message': 'Tables created.'}