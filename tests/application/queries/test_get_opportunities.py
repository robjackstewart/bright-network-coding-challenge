from unittest.mock import create_autospec
import uuid

import pytest
from src.application.common.interfaces.interfaces import (
    JobsRepositoryInterface,
    MembersRepositoryInterface,
)
from src.application.queries.get_opportunities import GetOpportunitiesQuery
from src.domain.value_objects import Job, Member


@pytest.mark.asyncio
async def test_execute_returns_all_jobs_for_all_members():
    # Arrange
    job1 = (Job(location=uuid.uuid4(), title=uuid.uuid4()),)
    job2 = (Job(location=uuid.uuid4(), title=uuid.uuid4()),)
    member1 = Member(name=uuid.uuid4(), bio=uuid.uuid4())
    member2 = Member(name=uuid.uuid4(), bio=uuid.uuid4())
    jobs: list[Job] = [job1, job2]
    members: list[Member] = [member1, member2]
    expected = {member1: jobs, member2: jobs}
    jobs_repository = create_autospec(JobsRepositoryInterface, instance=True)
    jobs_repository.jobs.return_value = jobs
    members_repository = create_autospec(MembersRepositoryInterface, instance=True)
    members_repository.members.return_value = members
    query = GetOpportunitiesQuery(jobs_repository, members_repository)

    # Act
    result = await query.execute()

    # Assert
    assert result == expected
