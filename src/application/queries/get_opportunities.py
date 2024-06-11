from __future__ import annotations
from src.application.common.interfaces.interfaces import JobsRepositoryInterface, MembersRepositoryInterface
from src.domain.value_objects import Job, Member

class GetOpportunitiesQuery:
    def __init__(self, jobs_repository: JobsRepositoryInterface, members_repository: MembersRepositoryInterface):
        self.jobs_repository = jobs_repository
        self.members_repository = members_repository

    def execute(self) -> dict[Member, list[Job]]:
        jobs = self.jobs_repository.jobs()
        members = self.members_repository.members()
