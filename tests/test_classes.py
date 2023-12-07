import pytest

from fuzzy_sets.classes import FuzzySet, FuzzySetMember
from fuzzy_set_for_testing import frood


# Fixtures
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


@pytest.mark.parametrize("membership", membership_values)
def test_fuzzy_set_membership_range(membership):
    with pytest.raises(ValueError):
        FuzzySet({FuzzySetMember("Ford Prefect", membership)})


def test_fuzzy_set_member_eq(test_fuzzy_set_members):
    assert test_fuzzy_set_members[0] == test_fuzzy_set_members[1]


def test_fuzzy_set_member_hash(test_fuzzy_set_members):
    a = test_fuzzy_set_members[0]
    b = test_fuzzy_set_members[1]
    assert hash(a) == hash(b)


def test_fuzzy_set_double_membership(test_fuzzy_set_members):
    fuzzy_set = FuzzySet(set(test_fuzzy_set_members))
    assert len(fuzzy_set.members) == 1


def test_fuzzy_set_values(test_fuzzy_set_members):
    fuzzy_set = FuzzySet(set(test_fuzzy_set_members))
    assert fuzzy_set.values == {"Ford Prefect"}


def test_fuzzy_set_sorted_list(frood):
    assert frood.sorted_list() == [
        FuzzySetMember("Marvin", 0.1),
        FuzzySetMember("Vogon", 0.1),
        FuzzySetMember("Arthur Dent", 0.5),
        FuzzySetMember("Ford Prefect", 1.0),
    ]
