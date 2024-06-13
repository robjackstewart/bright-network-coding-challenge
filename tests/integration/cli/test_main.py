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
        joe: set([london_ux_designer]),
        marta: set([london_legal_internship, london_sales_internship]),
        hassan: set([london_ux_designer]),
        grace: set([]),
        daisy: set([london_software_developer, edinburgh_software_developer]),
    }

    expected = f"""
Jobs for {joe.name} ({joe.bio}):
    {london_ux_designer.title} ({london_ux_designer.location})
Jobs for {marta.name} ({marta.bio}):
    {london_legal_internship.title} ({london_legal_internship.location})
    {london_sales_internship.title} ({london_sales_internship.location})
Jobs for {hassan.name} ({hassan.bio}):
    {london_ux_designer.title} ({london_ux_designer.location})
Jobs for {grace.name} ({grace.bio}):
    {york_marketing_internship.title} ({york_marketing_internship.location})
Jobs for {daisy.name} ({daisy.bio}):
    {london_software_developer.title} ({london_software_developer.location})
""".strip()

    # Act
    result = await runner.invoke(src.cli.main.show)

    # Assert
    assert result.exit_code == 0
    assert result.output.strip() == expected
