"""This module considers a conditional probability distribution given a fuzzy proposition.

In other words, a fuzzy set of possible worlds. P is a probability distribution on W (the set of all possible worlds), 
and ~A is a fuzzy set on W. P(w|A) = integral of P(w|~A) dα from α 0 to 1.
"""

from dataclasses import dataclass
from typing import Any

from fuzzy_sets import alpha
from fuzzy_sets.classes import FuzzySet


@dataclass
class Probability:
    value: Any
    probability: float

    def post_init(self):
        if not 0 < self.probability <= 1:
            raise ValueError(
                "Probability must be greater than 0, and less than or equal to 1 (0 < probability <= 1)"
            )

    def __eq__(self, other: "Probability") -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def __str__(self) -> str:
        return f"P({self.value}) = {self.probability:.3f}"

    def __repr__(self) -> str:
        return f"Probability({self.value}, {self.probability})"


@dataclass
class ProbabilityDistribution(set[Probability]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def values(self) -> list[float]:
        return [probability.value for probability in self]

    @property
    def probabilities(self) -> list[float]:
        return [probability.probability for probability in self]

    def __str__(self) -> str:
        return ", ".join([str(probability) for probability in self])

    def __repr__(self) -> str:
        return f"ProbabilityDistribution({self})"


def conditional(
    probability: Probability,
    distribution: ProbabilityDistribution,
    condition: FuzzySet,
) -> Probability:
    alpha_representation = alpha.alpha_ranges(condition)
    total: float = 0
    for range in alpha_representation:
        total_p_of_crisp_set = sum(
            [p.probability for p in distribution if p.value in range.crisp_set]
        )
        p_given_crisp_set = (
            probability.probability / total_p_of_crisp_set
            if probability.value in range.crisp_set
            else 0
        )
        integral_range = range.alpha_max - range.alpha_min
        integral_between_alpha_range = p_given_crisp_set * integral_range
        total += integral_between_alpha_range
    return Probability(probability.value, total)


def conditional_distribution(
    distribution: ProbabilityDistribution, condition: FuzzySet
) -> ProbabilityDistribution:
    # Return a new discrete distribution with the conditional probabilities
    return ProbabilityDistribution(
        {
            conditional(probability, distribution, condition)
            for probability in distribution
        }
    )
