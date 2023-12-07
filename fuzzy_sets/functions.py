from inspect import signature
import itertools
from typing import Callable

from fuzzy_sets.classes import FuzzySet, FuzzySetMember
from fuzzy_sets.alpha import AlphaRange
import fuzzy_sets.alpha


# TODO: Remove, it's superseded by apply()
def real_to_real(func: Callable[[float], float], fuzzy_set: FuzzySet) -> FuzzySet:
    """Takes in a function and a fuzzy set and returns a new fuzzy set with the function applied to each member's value

    The function must take in a single real number and return a single real number.

    Args:
        func (Callable[[float], float]): The function to apply to each member's value
        fuzzy_set (FuzzySet): The fuzzy set to apply the function to

    Raises:
        TypeError: If the fuzzy set does not contain real values

    Returns:
        FuzzySet: The new fuzzy set with the function applied to each member's value

    Examples:
        >>> fuzzy_set = FuzzySet({FuzzySetMember(1, 1), FuzzySetMember(2, 0.5), FuzzySetMember(3, 0.25)})
        >>> print(fuzzy_set)
        1/1 + 2/0.5 + 3/0.25
        >>> squared = real_to_real(lambda x: x ** 2, fuzzy_set)
        >>> print(squared)
        1/1 + 4/0.5 + 9/0.25
    """
    if not all(isinstance(member.value, int | float) for member in fuzzy_set.members):
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


def get_alpha_overlap(alpha_ranges: list[tuple[float, float]]) -> tuple[float, float]:
    """Takes in a list of alpha ranges and returns the overlapping alpha range

    Args:
        *alpha_ranges (tuple[float, float]): A list of alpha ranges

    Returns:
        tuple[float, float]: The overlapping alpha range

    Examples:
        >>> get_alpha_overlap((0, 0.5), (0.25, 0.75))
        (0.25, 0.5)
    """
    return (
        max(alpha_ranges, key=lambda x: x[0])[0],  # max lowest alpha
        min(alpha_ranges, key=lambda x: x[1])[1],  # min highest alpha
    )


def apply(func: Callable[[float], float], *input_sets: FuzzySet) -> FuzzySet:
    """Applies a function to multiple fuzzy sets using the alpha cut method

    Args:
        func (Callable[[float], float]): The function to the provided fuzzy sets
        *input_sets (FuzzySet): The fuzzy sets to apply the function to

    Raises:
        TypeError: If any fuzzy set does not contain real values
        ValueError: If the number of fuzzy sets does not match the number of inputs the function expects

    Returns:
        FuzzySet: The resulting fuzzy set

    Examples:
        >>> die_high_scores = FuzzySet(
                                {
                                    FuzzySetMember(1, 0.1),
                                    FuzzySetMember(2, 0.2),
                                    FuzzySetMember(3, 0.4),
                                    FuzzySetMember(4, 0.6),
                                    FuzzySetMember(5, 0.8),
                                    FuzzySetMember(6, 1.0),
                                }
                            )
        >>> print("Die high scores:", die_high_scores)
        Die high scores: 1/0.1 + 2/0.2 + 3/0.4 + 4/0.6 + 5/0.8 + 6/1.0
        >>> squared = fuzzy_sets.functions.apply(lambda x: x**2, die_high_scores)
        >>> print("Squared:", squared)
        Squared: 1/0.1 + 4/0.2 + 9/0.4 + 16/0.6 + 25/0.8 + 36/1.0

        >>> die_low_scores = FuzzySet(
                                {
                                    FuzzySetMember(1, 1.0),
                                    FuzzySetMember(2, 0.8),
                                    FuzzySetMember(3, 0.6),
                                    FuzzySetMember(4, 0.4),
                                    FuzzySetMember(5, 0.2),
                                    FuzzySetMember(6, 0.1),
                                }
                            )
        >>> print("Die low scores:", die_low_scores)
        Die low scores: 1/1.0 + 2/0.8 + 3/0.6 + 4/0.4 + 5/0.2 + 6/0.1
        >>> added = fuzzy_sets.functions.apply(lambda x, y: x + y, die_high_scores, die_low_scores)
        >>> print("Added:", added)
        2/0.1 + 12/0.1 + 3/0.2 + 11/0.2 + 4/0.4 + 10/0.4 + 5/0.6 + 9/0.6 + 6/0.8 + 8/0.8 + 7/1.0
    """
    # Check all fuzzy sets contain real values
    for fuzzy_set in input_sets:
        if not all(
            isinstance(member.value, int | float) for member in fuzzy_set.members
        ):
            raise TypeError("Fuzzy set must contain integer/real values")

    # Check correct number of inputs have been provided
    expected_input_length = len(signature(func).parameters)
    received_input_length = len(input_sets)
    if expected_input_length != received_input_length:
        raise ValueError(
            f"Function {func.__name__} expected {expected_input_length} parameter(s), but received {received_input_length}"
        )

    # Get the alpha ranges for each fuzzy set
    set_alpha_ranges = [fuzzy_sets.alpha.alpha_ranges(fs) for fs in input_sets]

    # Get all the possible combinations of alpha ranges
    set_alpha_range_combinations = list(itertools.product(*set_alpha_ranges))

    # For each combination, find the overlapping alpha ranges
    ranges_out = []
    for alpha_range_combination in set_alpha_range_combinations:
        ranges = [
            (range.alpha_min, range.alpha_max) for range in alpha_range_combination
        ]
        overlap = get_alpha_overlap(ranges)

        crisp_sets = [range.crisp_set for range in alpha_range_combination]
        value_pairs = itertools.product(*crisp_sets)

        # Apply the function to each value pair and keep the set of unique values
        values_out = {func(*value_pair) for value_pair in value_pairs}

        ranges_out.append(AlphaRange(overlap[0], overlap[1], values_out))

    return fuzzy_sets.alpha.fuzzy_set_from_alpha_ranges(ranges_out)
