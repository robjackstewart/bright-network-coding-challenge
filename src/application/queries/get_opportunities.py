from __future__ import annotations
import re
from typing import Optional, Tuple

import nltk
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

    async def execute(self) -> dict[Member, set[Job]]:
        jobs = await self._jobs_repository.jobs()
        members = await self._members_repository.members()
        jobs_by_members = {}

        locations = set([job.location.lower() for job in jobs])

        jobs_by_location: dict[str, list[str]] = {}

        for job in jobs:
            if job.location.lower() in jobs_by_location.keys():
                jobs_by_location[job.location.lower()].append(job)
            else:
                jobs_by_location[job.location.lower()] = [job]

        for member in members:
            jobs_for_member = []
            lower_bio = GetOpportunitiesQuery.__strip_non_alphanumeric_chars(
                member.bio.lower())
            meaningful_bio_words = [word for word in GetOpportunitiesQuery.__strip_non_alphanumeric_chars(
                lower_bio).split() if len(word) > 3]
            preferred_geographies: list[str] = GetOpportunitiesQuery.__calculate_preferred_geographies(
                lower_bio, locations)
            jobs_to_consider_for_member_based_on_geography: list[Job] = []
            if len(preferred_geographies) > 0:
                for preferred_geopraphy in preferred_geographies:
                    jobs_to_consider_for_member_based_on_geography.extend(
                        jobs_by_location[preferred_geopraphy])
            else:
                jobs_to_consider_for_member_based_on_geography = jobs
            for job in jobs_to_consider_for_member_based_on_geography:
                lower_case_job_title = job.title.lower()
                for word in meaningful_bio_words:
                    if word not in locations and word in lower_case_job_title and job not in jobs_for_member:
                        jobs_for_member.append(job)

            jobs_by_members[member] = set(jobs_for_member)

        return jobs_by_members

    def __calculate_preferred_geographies(bio: str, available_geographies: list[str] = []) -> Optional[list[str]]:
        locations_in_bio = [
            location for location in available_geographies if location in bio.lower()]
        return locations_in_bio

    def __strip_non_alphanumeric_chars(subject: str):
        return re.sub(r'[^a-zA-Z0-9 ]', '', subject)
