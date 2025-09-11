import asyncio

import aiohttp

from enums import AvailableStatus
from schemas.university_schemas import UniversityDTO


class Monitor:
    @staticmethod
    async def update_universities(universities_list: list[UniversityDTO]) -> list[UniversityDTO]:
        updated_universities = await asyncio.gather(*[Monitor.update_university(_) for _ in universities_list])

        return updated_universities

    @staticmethod
    async def update_university(university: UniversityDTO) -> UniversityDTO:
        status = await Monitor._get_status_code(str(university.url))

        if status == 200:
            university.availability = AvailableStatus.available
        else:
            university.availability = AvailableStatus.not_available

        return university

    @staticmethod
    async def _get_status_code(url: str) -> int:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                status = resp.status
                return status


# if __name__ == '__main__':
#     data = [
#         {
#             "id": 1,
#             "name": "dshdh",
#             "url": "https://www.youtube.com/watch?v=t7ufjzWKVk4&list=PLeLN0qH0-mCXARD_K-USF2wHctxzEVp40&index=4&ab_channel=АртёмШумейко",
#             "availability": AvailableStatus.available,
#             "rating": 4
#         }, {
#             "id": 1,
#             "name": "dshdh",
#             "url": "https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.ScalarResult",
#             "availability": AvailableStatus.available,
#             "rating": 4
#         },
#         {
#             "id": 1,
#             "name": "dshdh",
#             "url": "https://docs.pydantic.dev/latest/api/networks/#pydantic.networks.HttpUrl",
#             "availability": AvailableStatus.available,
#             "rating": 4
#         },
#         {
#             "id": 1,
#             "name": "dshdh",
#             "url": "https://docs.python.org/3.12/library/typing.html#typing.List",
#             "availability": AvailableStatus.available,
#             "rating": 4
#         },
#         {
#             "id": 1,
#             "name": "dshdh",
#             "url": "https://habr.com/ru/companies/piter/articles/920194/",
#             "availability": AvailableStatus.available,
#             "rating": 4
#         },

#     ]
#
#     dtos = [UniversityDTO(**_) for _ in data]
#     start_time = time.time()
#     print(asyncio.run(Monitor.update_universities(dtos)))
#     print("--- %s seconds ---" % (time.time() - start_time))
