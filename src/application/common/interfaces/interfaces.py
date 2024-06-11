from abc import ABC, abstractmethod
from typing import Optional
from src.domain.value_objects import Member
from src.domain.value_objects import Job


class JobsRepositoryInterface(ABC):

    @abstractmethod
    async def jobs(self) -> Optional[list[Job]]:
        """ Get all jobs

        :return: list[Job]
        """

class MembersRepositoryInterface(ABC):

    @abstractmethod
    async def members(self) -> Optional[list[Member]]:
        """ Get all jobs

        :return: list[Member]
        """