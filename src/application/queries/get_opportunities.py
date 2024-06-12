from __future__ import annotations
from src.application.common.interfaces import (
    GeographyCalculatorInterface,
    JobsRepositoryInterface,
    MembersRepositoryInterface,
)
from src.common.utils import replace_whitespace_with, strip_non_alphanumeric_chars
from src.domain.value_objects import Job, Member


class GetOpportunitiesQuery:
    MINIMUM_LENGTH_OF_BIO_WORDS_TO_CONSIDER: int = 3

    def __init__(
        self,
        jobs_repository: JobsRepositoryInterface,
        members_repository: MembersRepositoryInterface,
        geography_calculator: GeographyCalculatorInterface,
    ):
        self._jobs_repository = jobs_repository
        self._members_repository = members_repository
        self._geography_calculator = geography_calculator

    async def execute(self) -> dict[Member, list[Job]]:

        jobs = await self._jobs_repository.jobs()  # get all jobs
        members = await self._members_repository.members()  # get all members
        jobs_by_member = {}

        jobs_by_location: dict[str, list[Job]] = {}

        # populate the above dict with the job for the respective location
        for job in jobs:
            if job.location.lower() in jobs_by_location.keys():
                jobs_by_location[job.location.lower()].append(job)
            else:
                jobs_by_location[job.location.lower()] = [job]

        # get the distinct set of locations from the keys in the dict we just build
        locations = list(jobs_by_location.keys())

        for member in members:  # iterate over the members
            jobs_for_member = list()  # define an array that we will return
            #  convert to lower case, strip out non-alphanumeric characters and replace all whietspace with a single space in the bio for safe comparisons
            bio = replace_whitespace_with(
                strip_non_alphanumeric_chars(member.bio.lower()), " "
            )
            # define an array into which we will store the words we deem relevant for comparison with jobs
            meaningful_bio_words = []

            # add the word to the list of words for consideration if the word is long enough to be considered meaningful
            for word in bio.split():
                if (
                    len(word)
                    > GetOpportunitiesQuery.MINIMUM_LENGTH_OF_BIO_WORDS_TO_CONSIDER
                ):
                    meaningful_bio_words.append(word)

            # get the list of geographies desired based on the bio
            preferred_geographies: list[str] = (
                self._geography_calculator.extract_preferred_geographies(bio, locations)
            )

            jobs_to_consider_for_member: list[Job] = []

            # populate a list of jobs based on the geography preference
            # consider all jobs if no preference was calculated
            if any(preferred_geographies):
                for preferred_geopraphy in preferred_geographies:
                    jobs_to_consider_for_member.extend(
                        jobs_by_location[preferred_geopraphy]
                    )
            else:
                jobs_to_consider_for_member = jobs

            # process the relevant jobs for content linked to bio
            for job in jobs_to_consider_for_member:
                lower_case_job_title = job.title.lower()
                for word in meaningful_bio_words:
                    if (
                        word not in locations  # if the word is not a location
                        and word
                        in lower_case_job_title  # if the word exists in the job title
                    ):
                        # add job to list of opportunities
                        jobs_for_member.append(job)
                        break  # stop processing words for this job

            # set the value for this current member to be the list of relevant jobs
            jobs_by_member[member] = jobs_for_member

        return jobs_by_member
