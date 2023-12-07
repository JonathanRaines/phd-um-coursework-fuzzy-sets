from typing import Callable

from fuzzy_sets.classes import FuzzySet, FuzzySetMember


def real_to_real(func: Callable[[int], int], fuzzy_set: FuzzySet) -> FuzzySet:
    if not all(isinstance(member.value, int) for member in fuzzy_set.members):
        raise TypeError("Fuzzy set must contain integer/real values")

    return FuzzySet(
        {
            FuzzySetMember(
                value=func(member.value),
                membership=member.membership,
            )
            for member in fuzzy_set.members
        }
    )
