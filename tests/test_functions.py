import pytest

from fuzzy_sets.base import FuzzySet, FuzzySetMember
from fuzzy_sets.functions import real_to_real, apply
from fuzzy_set_for_testing import die_high_score, die_low_score

die_high_score
die_low_score


def test_real_to_real(die_high_score):
    doubled = real_to_real(lambda x: x * 2, die_high_score)
    assert doubled == FuzzySet(
        {
            FuzzySetMember(12, 1.0),
            FuzzySetMember(10, 0.5),
        }
    )


# Test a ValueError is raised if we provide a non-monotonic function
def test_real_to_real_non_monotonic(die_high_score):
    with pytest.raises(ValueError):
        real_to_real(lambda x: x * 0, die_high_score)


def test_apply(die_high_score, die_low_score):
    added = apply(lambda x, y: x + y, die_high_score, die_low_score)
    assert added == FuzzySet(
        {
            FuzzySetMember(7, 1.0),
            FuzzySetMember(6, 0.5),
            FuzzySetMember(8, 0.5),
            FuzzySetMember(5, 0.25),
        }
    )
