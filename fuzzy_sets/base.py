"""
Base classes to implement fuzzy sets. The Fuzzy Set and Fuzzy Set Members. 
"""
from dataclasses import dataclass
from typing import Any


@dataclass
class FuzzySetMember:
    """An element in a fuzzy set.

    Args:
        value[Any]: The thing that is part of a set
        membership[float]: A value between 0 and 1 that represents how much the value is part of the set.
    """

    value: Any
    membership: float

    # Make sure membership is between 0 and 1
    def __post_init__(self):
        if not 0 < self.membership <= 1:
            raise ValueError(
                "Membership must be greater than 0, and less than or equal to 1 (0 < membership <= 1)"
            )

    def __repr__(self) -> str:
        return f"FuzzySetMember({self.value}, {self.membership})"

    # Enable printing in the standard mathematical notation
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
class FuzzySet(set[FuzzySetMember]):
    """An extension of the default Python set class that adds a few convenience methods."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Get just the elements in the set without their membership values
    @property
    def values(self) -> list[float]:
        """Return a set of just values."""
        return {member.value for member in self.members}

    # Get just the membership values without the elements
    def sort_by_membership(self) -> list[FuzzySetMember]:
        """Return the set sorted by membership, uses value as a tiebreaker."""
        return sorted(self, key=lambda x: (x.membership, x.value))

    def __str__(self) -> str:
        return " + ".join([str(member) for member in self.sort_by_membership()])

    def __repr__(self) -> str:
        return f"FuzzySet({self})"
