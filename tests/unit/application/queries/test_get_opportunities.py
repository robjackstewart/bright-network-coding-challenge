from unittest.mock import create_autospec
import uuid

import pytest
from src.application.common.interfaces import (
    GeographyCalculatorInterface,
    JobsRepositoryInterface,
    MembersRepositoryInterface,
)
from src.application.queries.get_opportunities import GetOpportunitiesQuery
from src.domain.value_objects import Job, Member


@pytest.mark.asyncio
async def test_execute_returns_correct_jobs_based_on_words_and_location():
    # Arrange
    joe = Member(name="Joe", bio="I'm a designer from London, UK")
    marta = Member(name="Marta", bio="I'm looking for an internship in London")
    hassan = Member(name="Hassan", bio="I'm looking for a design job")
    grace = Member(
        name="Grace", bio="I'm looking for a job in marketing outside of London"
    )
    daisy = Member(
        name="Daisy",
        bio="I'm a software developer currently in Edinburgh but looking to relocate to London",
    )

    london_software_developer = Job(title="Software Developer", location="London")
    york_marketing_internship = Job(title="Marketing Internship", location="York")
    london_data_scientist = Job(title="Data Scientist", location="London")
    london_legal_internship = Job(title="Legal Internship", location="London")
    manchester_project_manager = Job(title="Project Manager", location="Manchester")
    london_sales_internship = Job(title="Sales Internship", location="London")
    london_ux_designer = Job(title="UX Designer", location="London")
    edinburgh_software_developer = Job(title="Software Developer", location="Edinburgh")

    jobs: list[Job] = [
        london_software_developer,
        york_marketing_internship,
        london_data_scientist,
        london_legal_internship,
        manchester_project_manager,
        london_sales_internship,
        london_ux_designer,
        edinburgh_software_developer,
    ]

    members: list[Member] = [joe, marta, hassan, grace, daisy]

    expected = {
        joe: [london_ux_designer],
        marta: [london_legal_internship, london_sales_internship],
        hassan: [london_ux_designer],
        grace: [],
        daisy: [london_software_developer],
    }
    jobs_repository = create_autospec(JobsRepositoryInterface, instance=True)
    jobs_repository.jobs.return_value = jobs
    members_repository = create_autospec(MembersRepositoryInterface, instance=True)
    members_repository.members.return_value = members
    geography_calculator = create_autospec(GeographyCalculatorInterface, instance=True)

    geography_calculator.extract_preferred_geographies.return_value = ["london"]

    query = GetOpportunitiesQuery(
        jobs_repository, members_repository, geography_calculator
    )

    # Act
    result = await query.execute()

    # Assert
    assert result == expected
