from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Job:
    title: str
    location: str

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True)
class Member:
    name: str
    bio: str

    def to_dict(self):
        return asdict(self)
