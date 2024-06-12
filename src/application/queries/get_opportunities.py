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

    async def execute(self) -> dict[Member, list[Job]]:
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('punkt', quiet=True)
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('words', quiet=True)

        jobs = await self._jobs_repository.jobs()
        members = await self._members_repository.members()
        jobs_by_members = {}

        locations = set([job.location.lower() for job in jobs])

        # jobs_by_meaningful_words: dict[str, list[Job]] = {}
        jobs_by_location: dict[str, list[str]] = {}

        for job in jobs:
            if job.location.lower() in jobs_by_location.keys():
                jobs_by_location[job.location.lower()].append(job)
            else:
                jobs_by_location[job.location.lower()] = [job]

        #     words = set(job.title.lower().split())
        #     for word in words:
        #         if word in jobs_by_meaningful_words:
        #             jobs_by_meaningful_words[word] = jobs_by_meaningful_words[word].append(
        #                 job)
        #         else:
        #             jobs_by_meaningful_words[word] = [job]

        # members_by_meaningful_words: dict[str, list[Member]] = {}
        # members_by_location: dict[str, list[str]] = {}

        # for member in members:
        #     lower_bio = GetOpportunitiesQuery.__strip_non_alphanumeric_chars(
        #         member.bio.lower())
        #     bio_tokens = GetOpportunitiesQuery.__get_tokens(lower_bio)
        #     meaningful_bio_words = set(
        #         GetOpportunitiesQuery.__extract_meaningful_words(bio_tokens))
        #     locations = set([])
        #     for location in location:
        #         if location in members_by_location:
        #             members_by_location[location] = members_by_location[location].append(
        #                 member)
        #         else:
        #             members_by_location[location] = [member]
        #     for word in meaningful_bio_words:
        #         if word not in locations and word in members_by_meaningful_words:
        #             members_by_meaningful_words[word] = members_by_meaningful_words[word].append(
        #                 member)
        #         else:
        #             members_by_meaningful_words[word] = [member]

        # all_words: set[str] = set(members_by_meaningful_words.keys() +
        #                           jobs_by_meaningful_words.keys())

        # for word in all_words:

        for member in members:
            jobs_for_member = []
            lower_bio = GetOpportunitiesQuery.__strip_non_alphanumeric_chars(
                member.bio.lower())
            bio_tags = GetOpportunitiesQuery.__get_tags(lower_bio)
            meaningful_bio_words = set(
                GetOpportunitiesQuery.__extract_meaningful_words(bio_tags))
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

            jobs_by_members[member] = jobs_for_member

        return jobs_by_members

    def __get_tags(subject: str) -> list[Tuple[str, str]]:
        tokens = nltk.word_tokenize(subject)
        return nltk.pos_tag(tokens)

    def __calculate_preferred_geographies(bio: str, available_geographies: list[str] = []) -> Optional[list[str]]:
        locations_in_bio = [
            location for location in available_geographies if location in bio.lower()]
        return locations_in_bio
        # if len(locations_in_bio) < 1:
        #     return None
        # else:
        #     return available_geographies[0]

    # def __extract_geographies(tags: list[Tuple[str, str]]):
    #     entities = nltk.chunk.ne_chunk(tags)
    #     return [chunk for chunk in entities if isinstance(chunk, nltk.tree.Tree) and chunk.label() == 'GPE']

    def __extract_meaningful_words(tokens: list[Tuple[str, str]]) -> list[str]:
        return [word for word, pos in tokens if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and len(word) > 1]

    def __strip_non_alphanumeric_chars(subject: str):
        return re.sub(r'[^a-zA-Z0-9 ]', '', subject)

    # def __get_geographies(self, subject: str):
    #     result = self._spacy(subject)
    #     return [ent.text for ent in result.ents if ent.label_ == 'GPE']
