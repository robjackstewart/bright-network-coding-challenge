from dataclasses import dataclass

@dataclass
class Job:
    title: str
    location: str

@dataclass
class Member:
    name: str
    bio: str