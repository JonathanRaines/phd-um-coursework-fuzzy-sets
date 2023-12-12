import pytest

from fuzzy_sets.base import FuzzySet, FuzzySetMember
from fuzzy_set_for_testing import frood


# Fixtures


# A list of FuzzySetMembers with the same value but different memberships
# Note, this is a list, not a set, so it contains both values.
@pytest.fixture
def test_fuzzy_set_members():
    return [
        FuzzySetMember("Ford Prefect", 1.0),
        FuzzySetMember("Ford Prefect", 0.8),
    ]


frood


# Tests

# Check for memberships outside of the range (0, 1]
membership_values = [
    (-0.1),
    (0.0),
    (1.1),
]


# Confirm we get a value error if membership is outside of the range (0, 1]
@pytest.mark.parametrize("membership", membership_values)
def test_fuzzy_set_membership_range(membership):
    with pytest.raises(ValueError):
        FuzzySet({FuzzySetMember("Ford Prefect", membership)})


# Check two FuzzySetMembers with the same value but different memberships are equal
def test_fuzzy_set_member_eq(test_fuzzy_set_members):
    assert test_fuzzy_set_members[0] == test_fuzzy_set_members[1]


# Check the hashes of two FuzzySetMembers with the same value but different memberships are the same
def test_fuzzy_set_member_hash(test_fuzzy_set_members):
    a = test_fuzzy_set_members[0]
    b = test_fuzzy_set_members[1]
    assert hash(a) == hash(b)


# Check if we do try to add two memebers with the same value but different memberships, we only get one member
def test_fuzzy_set_double_membership(test_fuzzy_set_members):
    fuzzy_set = FuzzySet(test_fuzzy_set_members)
    assert len(fuzzy_set) == 1


def test_fuzzy_set_sorted_list(frood: FuzzySet):
    assert frood.sort_by_membership() == [
        FuzzySetMember("Marvin", 0.1),
        FuzzySetMember("Vogon", 0.1),
        FuzzySetMember("Arthur Dent", 0.5),
        FuzzySetMember("Ford Prefect", 1.0),
    ]
