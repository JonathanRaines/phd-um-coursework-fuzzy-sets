"""This module considers a conditional probability distribution given a fuzzy proposition.

In other words, a fuzzy set of possible worlds. P is a probability distribution on W (the set of all possible worlds), 
and ~A is a fuzzy set on W. P(w|A) = integral of P(w|~A) dα from α 0 to 1.
"""

from dataclasses import dataclass
from typing import Any

from fuzzy_sets import alpha
from fuzzy_sets.base import FuzzySet


@dataclass
class Probability:
    """A value for a random variable and its probability.

    Args:
        value[Any]: A possible value for a random variable.
        probability[float]: The probability the random variable is equal to that value. Between 0 and 1.
    """

    value: Any
    probability: float

    def post_init(self):
        """Raises a ValueError if the probability is not between 0 and 1."""
        if not 0 <= self.probability <= 1:
            raise ValueError("Probability must be between 0 and 1 (0 <= p <= 1)")

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
    """An extension of the set class. Represents a discrete probability distribution."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def values(self) -> list[float]:
        """Return a list of just possible values."""
        return [probability.value for probability in self]

    @property
    def probabilities(self) -> list[float]:
        """Return a list of probabilities."""
        return [probability.probability for probability in self]

    def sort_by_probability(self) -> list[Probability]:
        """Return the set sorted by probability, uses value as a tiebreaker."""
        return sorted(self, key=lambda x: (x.probability, x.value))

    def __str__(self) -> str:
        return ", ".join(
            [str(probability) for probability in self.sort_by_probability()]
        )

    def __repr__(self) -> str:
        return f"ProbabilityDistribution({self})"


def conditional(
    probability: Probability,
    distribution: ProbabilityDistribution,
    condition: FuzzySet,
) -> Probability:
    """Calculates the conditional probability given a prior distribution and a fuzzy condition.

    Args:
        probability (Probability): A value and likelihood pair
        distribution (ProbabilityDistribution): The prior distribution
        condition (FuzzySet): The fuzzy condition

    Returns:
        Probability: The conditional probability given the fuzzy condition
    """
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
    """Calculates the conditional probability distribution given a prior distribution and a fuzzy condition.

    Calls conditional() on each probability in the distribution.

    Args:
        distribution (ProbabilityDistribution): The prior distribution
        condition (FuzzySet): The fuzzy condition

    Returns:
        ProbabilityDistribution: The conditional probability distribution given the fuzzy condition

    Examples:
        >>> fair_distribution = ProbabilityDistribution(
                {
                    Probability(("H", "H"), 0.25),
                    Probability(("H", "T"), 0.25),
                    Probability(("T", "H"), 0.25),
                    Probability(("T", "T"), 0.25),
                }
            )
        >>> good_result_condition = FuzzySet(
                {
                    FuzzySetMember(("H", "H"), 1.0),
                    FuzzySetMember(("H", "T"), 0.5),
                    FuzzySetMember(("T", "H"), 0.5),
                }
            )
        >>> print(str(conditional_distribution(fair_distribution, good_result_condition)))
        P(('T', 'T')) = 0.000, P(('H', 'T')) = 0.167, P(('T', 'H')) = 0.167, P(('H', 'H')) = 0.667
    """
    # Return a new discrete distribution with the conditional probabilities
    return ProbabilityDistribution(
        {
            conditional(probability, distribution, condition)
            for probability in distribution
        }
    )
