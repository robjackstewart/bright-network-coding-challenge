from typing import Type
from httpx import AsyncClient
from src.application.common.interfaces import (
    JobsRepositoryInterface,
    MembersRepositoryInterface,
)
from src.domain.value_objects import Job, Member


class RESTRepositoryBase:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def _fetch_many(self, url: str, entity_type: Type) -> list:
        async with AsyncClient(base_url=self.base_url) as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                entities = [entity_type(**item) for item in data]
                return entities
            else:
                return []


class JobsRepository(RESTRepositoryBase, JobsRepositoryInterface):

    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def jobs(self) -> list[Job]:
        return await self._fetch_many("/jobs.json", Job)


class MembersRepository(RESTRepositoryBase, MembersRepositoryInterface):

    def __init__(self, base_url: str):
        super().__init__(base_url)

    async def members(self) -> list[Member]:
        return await self._fetch_many("/members.json", Member)
