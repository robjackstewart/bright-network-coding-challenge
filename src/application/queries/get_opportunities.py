from __future__ import annotations

import spacy
from src.application.common.interfaces.interfaces import (
    JobsRepositoryInterface,
    MembersRepositoryInterface,
)
from src.domain.value_objects import Job, Member


class GetOpportunitiesQuery:
    def __init__(
        self,
        jobs_repository: JobsRepositoryInterface,
        members_repository: MembersRepositoryInterface,
    ):
        self._jobs_repository = jobs_repository
        self._members_repository = members_repository

    async def execute(self) -> dict[Member, list[Job]]:
        jobs = await self._jobs_repository.jobs()
        members = await self._members_repository.members()
        jobs_by_members = {}

        for member in members:
            jobs_for_member = []
            lower_case_bio = member.bio.lower()
            bio_words = set(lower_case_bio.split())
            for job in jobs:
                job_title_words = set(job.title.lower().split())
                common_words_between_bio_and_job_title = bio_words.intersection(job_title_words)
                if len(common_words_between_bio_and_job_title) > 0:
                    jobs_for_member.append(job)
            jobs_by_members[member] = jobs_for_member

        return jobs_by_members

    # def __get_geographies(self, subject: str):
    #     result = self._spacy(subject)
    #     return [ent.text for ent in result.ents if ent.label_ == 'GPE']
