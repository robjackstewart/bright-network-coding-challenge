
from typing import List, Type
from httpx import AsyncClient
from src.application.common.interfaces.interfaces import JobsRepositoryInterface
from src.domain.value_objects import Job, Member

class RepositoryBase:
    def __init__(self, rest_client):
        self.rest_client = rest_client

    async def fetch_many(self, url: str, entity_type: Type) -> list:
        async with self.rest_client as client:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                entities = [entity_type(**item) for item in data]
                return entities
            else:
                return []

class JobsRepository(RepositoryBase, JobsRepositoryInterface):

    def __init__(self, rest_client: AsyncClient):
        super().__init__(rest_client)

    async def jobs(self) -> list[Job]:
        return await self.fetch_many("/members.json", Job)


class MembersRepository(RepositoryBase, JobsRepositoryInterface):

    def __init__(self, rest_client):
        super().__init__(rest_client)

    async def members(self) -> list[Member]:
        return await self.fetch_many("/jobs.json", Member)