from unittest.mock import patch
import uuid
import pytest
from asyncclick.testing import CliRunner
import src.cli.main
from src.application.queries.get_opportunities import GetOpportunitiesQuery
from src.domain.value_objects import Job, Member


@pytest.mark.asyncio
async def test_show_prints_result_of_get_opportunities_query(runner: CliRunner):
    # Arrange
    job1 = Job(location=str(uuid.uuid4()), title=str(uuid.uuid4()))
    job2 = Job(location=str(uuid.uuid4()), title=str(uuid.uuid4()))
    member1 = Member(name=str(uuid.uuid4()), bio=str(uuid.uuid4()))
    member2 = Member(name=str(uuid.uuid4()), bio=str(uuid.uuid4()))
    jobs: list[Job] = [job1, job2]
    query_result: dict[Member, list[Job]] = {member1: jobs, member2: jobs}
    expected = f"""
Jobs for {member1.name} ({member1.bio}):
    {job1.title} ({job1.location})
    {job2.title} ({job2.location})
Jobs for {member2.name} ({member2.bio}):
    {job1.title} ({job1.location})
    {job2.title} ({job2.location})
""".strip()

    with patch(
        f"{src.cli.main.__name__}.{GetOpportunitiesQuery.__name__}", autospec=True
    ) as mock_query_class:
        mock_query_instance = mock_query_class.return_value
        mock_query_instance.execute.return_value = query_result

        # Act
        result = await runner.invoke(src.cli.main.show)

        # Assert
        assert result.exit_code == 0
        assert result.output.strip() == expected
