from dataclasses import dataclass
from typing import Any


@dataclass
class FuzzySetMember:
    value: Any
    membership: float

    # Make sure membership is between 0 and 1
    def __post_init__(self):
        if not 0 < self.membership <= 1:
            raise ValueError("Membership must be between 0 and 1")

    def __repr__(self) -> str:
        return f"FuzzySetMember({self.value}, {self.membership})"

    def __str__(self) -> str:
        return f"{self.value}/{self.membership}"

    # Define eq and hash to allow for set operations
    def __eq__(self, other: "FuzzySetMember"):
        if not isinstance(other, FuzzySetMember):
            return NotImplemented
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


@dataclass
class FuzzySet:
    members: set[FuzzySetMember]

    @property
    def values(self) -> list[float]:
        return {member.value for member in self.members}

    def sorted_list(self) -> list[FuzzySetMember]:
        return sorted(self.members, key=lambda x: x.membership)

    def __str__(self) -> str:
        return " + ".join([str(member) for member in self.sorted_list()])

    def __repr__(self) -> str:
        return f"FuzzySet({self.members})"
