import json
from unittest.mock import AsyncMock, Mock, PropertyMock, patch
import uuid

from httpx import AsyncClient, Response
import pytest

from src.domain.value_objects import Job, Member
from src.infrastructure.repositories import JobsRepository, MembersRepository


@pytest.mark.asyncio
async def test_jobs_repository_jobs_returns_jobs_from_api():
    # Arrange
    base_url = str(uuid.uuid4())
    jobs_repository = JobsRepository(base_url)
    job = Job(location=str(uuid.uuid4()), title=str(uuid.uuid4()))
    jobs = [job]
    jobs_json_response = [job.to_dict()]

    with patch(f"{JobsRepository.__module__}.{AsyncClient.__name__}.{AsyncClient.get.__name__}", return_value=Response(200, json=jobs_json_response)) as get_mock:

        # Act
        result = await jobs_repository.jobs()

        # Assert
        assert result == jobs


@pytest.mark.asyncio
async def test_members_repository_members_returns_members_from_api():
    # Arrange
    base_url = str(uuid.uuid4())
    members_repository = MembersRepository(base_url)
    member = Member(name=str(uuid.uuid4()), bio=str(uuid.uuid4()))
    members = [member]
    members_json_response = [member.to_dict()]

    with patch(f"{MembersRepository.__module__}.{AsyncClient.__name__}.{AsyncClient.get.__name__}", return_value=Response(200, json=members_json_response)) as get_mock:

        # Act
        result = await members_repository.members()

        # Assert
        assert result == members
