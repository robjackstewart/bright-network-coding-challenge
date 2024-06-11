from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    title: str
    location: str


@dataclass(frozen=True)
class Member:
    name: str
    bio: str
