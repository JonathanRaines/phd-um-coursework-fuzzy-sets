from dataclasses import dataclass
from typing import Any

from fuzzy_sets.classes import FuzzySet, FuzzySetMember


@dataclass
class AlphaRange:
    """A crisp set that is true between a min and a max alpha value.

    Attributes:
        alpha_min: The minimum alpha value for which the crisp set is true.
        alpha_max: The maximum alpha value for which the crisp set is true.
        crisp_set: The set of values.
    """

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
    """Return the crisp set for a given alpha value.

    Args:
        fuzzy_set: The fuzzy set.
        alpha[float]: The alpha value (between 0 and 1)

    Returns:
        set[Any]: The crisp set.

    Raises:
        ValueError: If alpha is not between 0 and 1.

    Examples:
        >>> fuzzy_set = FuzzySet(
                            {FuzzySetMember(1, 0.2),
                            FuzzySetMember(2, 0.4),
                            FuzzySetMember(3, 0.6),
                            FuzzySetMember(4, 0.8)}
                        )
        >>> alpha_cut(fuzzy_set, 0.5)
        {3, 4}
    """
    if alpha < 0 or alpha > 1:
        raise ValueError(f"Alpha value must be between 0 and 1, got {alpha}")
    return {member.value for member in fuzzy_set if member.membership >= alpha}


def alpha_ranges(fuzzy_set: FuzzySet) -> list[AlphaRange]:
    """Produce an alpha cut representation of a fuzzy set.

    Args:
        fuzzy_set (FuzzySet): The fuzzy set to represent/convert.

    Returns:
        list[AlphaRange]: A list of alpha ranges that represent the fuzzy set.

    Examples:
        >>> froodiness = FuzzySet(
                            {
                                FuzzySetMember("Ford Prefect", 1.0),
                                FuzzySetMember("Zaphod Beeblebrox", 1.0),
                                FuzzySetMember("Trillian", 0.7),
                                FuzzySetMember("Fenchurch", 0.7),
                                FuzzySetMember("Slartibartfast", 0.6),
                                FuzzySetMember("Arthur Dent", 0.5),
                                FuzzySetMember("Deep Thought", 0.4),
                                FuzzySetMember("Agrajag", 0.3),
                                FuzzySetMember("The poor whale", 0.2),
                                FuzzySetMember("Marvin", 0.1),
                                FuzzySetMember("Vogon", 0.1),
                            }
                        )
        >>> print("Froodiness:", froodiness)
        Froodiness: Vogon/0.1 + Marvin/0.1 + The poor whale/0.2 + Agrajag/0.3 + Deep Thought/0.4 + Arthur Dent/0.5 + Slartibartfast/0.6 + Trillian/0.7 + Fenchurch/0.7 + Ford Prefect/1.0 + Zaphod Beeblebrox/1.0
        >>> ranges = alpha_ranges(froodiness)
        >>> print(\"\\n\".join([str(range) for range in ranges]))
        {Agrajag, Arthur Dent, Deep Thought, Fenchurch, Ford Prefect, Marvin, Slartibartfast, The poor whale, Trillian, Vogon, Zaphod Beeblebrox}: α ∈ (0.0, 0.1]
        {Agrajag, Arthur Dent, Deep Thought, Fenchurch, Ford Prefect, Slartibartfast, The poor whale, Trillian, Zaphod Beeblebrox}: α ∈ (0.1, 0.2]
        {Agrajag, Arthur Dent, Deep Thought, Fenchurch, Ford Prefect, Slartibartfast, Trillian, Zaphod Beeblebrox}: α ∈ (0.2, 0.3]
        {Arthur Dent, Deep Thought, Fenchurch, Ford Prefect, Slartibartfast, Trillian, Zaphod Beeblebrox}: α ∈ (0.3, 0.4]
        {Arthur Dent, Fenchurch, Ford Prefect, Slartibartfast, Trillian, Zaphod Beeblebrox}: α ∈ (0.4, 0.5]
        {Fenchurch, Ford Prefect, Slartibartfast, Trillian, Zaphod Beeblebrox}: α ∈ (0.5, 0.6]
        {Fenchurch, Ford Prefect, Trillian, Zaphod Beeblebrox}: α ∈ (0.6, 0.7]
        {Ford Prefect, Zaphod Beeblebrox}: α ∈ (0.7, 1.0]
    """
    unique_memberships = sorted(list({member.membership for member in fuzzy_set}))

    alpha_ranges: list[AlphaRange] = []
    for index, membership in enumerate(unique_memberships):
        alpha_min = unique_memberships[index - 1] if index > 0 else 0.0
        alpha_max = membership
        crisp_set = {
            member.value
            for member in fuzzy_set
            if member.membership >= alpha_max and member.membership > alpha_min
        }
        alpha_ranges.append(AlphaRange(alpha_min, alpha_max, crisp_set))

    return alpha_ranges


def fuzzy_set_from_alpha_ranges(alpha_ranges: list[AlphaRange]) -> FuzzySet:
    """Convert an alpha cut representation into a fuzzy set.

    Args:
        alpha_ranges (list[AlphaRange]): A list of alpha ranges representing the alpha cuts.

    Returns:
        FuzzySet: The fuzzy set representation

    Examples:
        >>> fun_alpha_ranges = [
                AlphaRange(0, 0.5, {"video games", "uncertainty modelling coursework"}),
                AlphaRange(0.5, 1, {"uncertainty modelling coursework"}),
            ]
        >>> print(\"\\n\".join([str(range) for range in fun_alpha_ranges]))
        {uncertainty modelling coursework, video games}: α ∈ (0, 0.5]
        {uncertainty modelling coursework}: α ∈ (0.5, 1]
        >>> print(fuzzy_sets.alpha.fuzzy_set_from_alpha_ranges(fun_alpha_ranges))
        video games/0.5 + uncertainty modelling coursework/1
    """
    # Get all the values by finding the largest crisp set
    sorted_alpha_ranges = sorted(alpha_ranges, key=lambda x: len(x.crisp_set))
    largest_alpha_range = sorted_alpha_ranges[-1]
    values = largest_alpha_range.crisp_set

    members = FuzzySet()
    for value in values:
        ranges_containing_value = [
            alpha_range
            for alpha_range in alpha_ranges
            if value in alpha_range.crisp_set
        ]
        # Find the largest alpha range containing the value
        max_alpha = sorted(ranges_containing_value, key=lambda x: x.alpha_max)[-1]
        members.add(FuzzySetMember(value, max_alpha.alpha_max))

    return members
