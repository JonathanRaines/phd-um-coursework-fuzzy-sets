from dataclasses import dataclass
from typing import Any


@dataclass
class FuzzySetMember:
    value: Any
    membership: float

    # Enable sorting by membership
    def __lt__(self, other: "FuzzySetMember"):
        if not isinstance(other, FuzzySetMember):
            return NotImplemented
        return self.membership < other.membership

    def __repr__(self) -> str:
        return f"FuzzySetMember({self.value}, {self.membership})"

    def __str__(self) -> str:
        return f"{self.value}/{self.membership}"

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class FuzzySet:
    members: set[FuzzySetMember]

    @property
    def member_values(self) -> list[float]:
        return {member.value for member in self.members}

    def __str__(self) -> str:
        return " + ".join([str(member) for member in sorted(self.members)])

    def __repr__(self) -> str:
        return f"FuzzySet({self.members})"
