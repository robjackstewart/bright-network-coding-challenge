from __future__ import annotations
import re
from typing import Tuple

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

        jobs = await self._jobs_repository.jobs()
        members = await self._members_repository.members()
        jobs_by_members = {}

        locations = set([job.location.lower() for job in jobs])

        for member in members:
            jobs_for_member = []
            lower_bio = GetOpportunitiesQuery.__strip_non_alphanumeric_chars(
                member.bio.lower())
            bio_tokens = GetOpportunitiesQuery.__get_tokens(lower_bio)
            meaningful_bio_words = set(
                GetOpportunitiesQuery.__extract_meaningful_words(bio_tokens))
            for job in jobs:
                lower_case_job_title = job.title.lower()
                for word in meaningful_bio_words:
                    if word not in locations and word in lower_case_job_title and job not in jobs_for_member:
                        jobs_for_member.append(job)
            
            

            jobs_by_members[member] = jobs_for_member

        return jobs_by_members

    def __get_tokens(subject: str) -> list[Tuple[str, str]]:
        tokens = nltk.word_tokenize(subject)
        return nltk.pos_tag(tokens)

    def __extract_meaningful_words(tokens: list[Tuple[str, str]]):
        return [word for word, pos in tokens if pos in ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'] and len(word) > 1]

    def __strip_non_alphanumeric_chars(subject: str):
        return re.sub(r'[^a-zA-Z0-9 ]', '', subject)

    # def __get_geographies(self, subject: str):
    #     result = self._spacy(subject)
    #     return [ent.text for ent in result.ents if ent.label_ == 'GPE']
