import pytest
from fuzzy_sets.classes import FuzzySet, FuzzySetMember


@pytest.fixture
def test_fuzzy_set_members():
    return [
        FuzzySetMember("Ford Prefect", 1.0),
        FuzzySetMember("Ford Prefect", 0.8),
    ]


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
