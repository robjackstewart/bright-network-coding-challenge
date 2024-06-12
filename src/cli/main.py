from __future__ import annotations
import asyncclick as click
from src.application.queries.get_opportunities import GetOpportunitiesQuery

from src.infrastructure.repositories import JobsRepository, MembersRepository

BASE_URL = "https://bn-hiring-challenge.fly.dev"


# Main group (acts as the main entry point)
@click.group()
def cli():
    """Main CLI entry point"""
    pass


@cli.command()
# @click.option('--name', '-n', multiple=True, default=[], help='The name of the person for which to show opportunities')
async def show():
    """Greet someone"""

    jobs_repository = JobsRepository(BASE_URL)
    members_repository = MembersRepository(BASE_URL)

    query = GetOpportunitiesQuery(jobs_repository, members_repository)

    result = await query.execute()

    for member, jobs in result.items():
        click.echo(f"Jobs for {member.name} ({member.bio}):")
        for job in jobs:
            click.echo(f"    {job.title} ({job.location})")


if __name__ == "__main__":
    cli()
