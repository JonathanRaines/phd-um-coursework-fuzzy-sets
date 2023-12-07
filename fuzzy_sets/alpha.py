from dataclasses import dataclass
from typing import Any

from fuzzy_sets.classes import FuzzySet


@dataclass
class AlphaRange:
    alpha_min: float
    alpha_max: float
    crisp_set: set[Any]

    def __repr__(self) -> str:
        return f"AlphaRange(({self.alpha_min}, {self.alpha_max}], {self.crisp_set})"

    def __str__(self) -> str:
        sorted_values = sorted(self.crisp_set)
        return (
            f"{{{', '.join(sorted_values)}}}: α ∈ ({self.alpha_min}, {self.alpha_max}]"
        )


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


def alpha_cut(fuzzy_set: FuzzySet, alpha: float) -> {Any}:
    return [member.value for member in fuzzy_set.members if member.membership >= alpha]
