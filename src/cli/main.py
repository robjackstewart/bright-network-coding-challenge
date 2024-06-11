from __future__ import annotations
import click
import httpx

from src.application.queries.get_opportunities import GetOpportunitiesQuery
from src.domain.value_objects import Job, Member
from src.infrastructure.repositories import JobsRepository, MembersRepository


# Main group (acts as the main entry point)
@click.group()
def cli():
    """Main CLI entry point"""
    pass

@cli.command()
# @click.option('--name', '-n', multiple=True, default=[], help='The name of the person for which to show opportunities')
def show():
    """Greet someone"""

    rest_client = httpx.AsyncClient(base_url="https://bn-hiring-challenge.fly.dev")
    jobs_repository = JobsRepository(rest_client)
    members_repository = MembersRepository(rest_client)

    query = GetOpportunitiesQuery(jobs_repository, members_repository)

    result = query.execute()

    for member, jobs in result.items():
        click.echo(f"Jobs for {member.name}:")
        for job in jobs:
            click.echo(f"   {job.title} ({job.location})")

if __name__ == '__main__':
    cli()