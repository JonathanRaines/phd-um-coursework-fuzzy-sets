from dataclasses import dataclass
from typing import Any

from fuzzy_sets.classes import FuzzySet, FuzzySetMember


@dataclass
class AlphaRange:
    alpha_min: float
    alpha_max: float
    crisp_set: set[Any]

    def __repr__(self) -> str:
        return f"AlphaRange(({self.alpha_min}, {self.alpha_max}], {self.crisp_set})"

    def __str__(self) -> str:
        sorted_values = sorted(self.crisp_set)
        sorted_values = [str(value) for value in sorted_values]
        return (
            f"{{{', '.join(sorted_values)}}}: α ∈ ({self.alpha_min}, {self.alpha_max}]"
        )


def alpha_cut(fuzzy_set: FuzzySet, alpha: float) -> {Any}:
    return [member.value for member in fuzzy_set.members if member.membership >= alpha]


def alpha_ranges(fuzzy_set: FuzzySet) -> list[AlphaRange]:
    unique_memberships = sorted(
        list({member.membership for member in fuzzy_set.members})
    )

    alpha_ranges: list[AlphaRange] = []
    for index, membership in enumerate(unique_memberships):
        alpha_min = unique_memberships[index - 1] if index > 0 else 0.0
        alpha_max = membership
        crisp_set = {
            member.value
            for member in fuzzy_set.members
            if member.membership >= alpha_max and member.membership > alpha_min
        }
        alpha_ranges.append(AlphaRange(alpha_min, alpha_max, crisp_set))

    return alpha_ranges


def fuzzy_set_from_alpha_ranges(alpha_ranges: list[AlphaRange]) -> FuzzySet:
    # Get all the values by finding the largest crisp set
    sorted_alpha_ranges = sorted(alpha_ranges, key=lambda x: len(x.crisp_set))
    largest_alpha_range = sorted_alpha_ranges[-1]
    values = largest_alpha_range.crisp_set

    members = set()
    for value in values:
        ranges_containing_value = [
            alpha_range
            for alpha_range in alpha_ranges
            if value in alpha_range.crisp_set
        ]
        # Find the largest alpha range containing the value
        max_alpha = sorted(ranges_containing_value, key=lambda x: x.alpha_max)[-1]
        members.add(FuzzySetMember(value, max_alpha.alpha_max))

    return FuzzySet(members)
