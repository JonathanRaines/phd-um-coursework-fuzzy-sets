import pytest
from fuzzy_sets.base import FuzzySet, FuzzySetMember


@pytest.fixture
def frood():
    return FuzzySet(
        {
            FuzzySetMember("Ford Prefect", 1.0),
            FuzzySetMember("Arthur Dent", 0.5),
            FuzzySetMember("Marvin", 0.1),
            FuzzySetMember("Vogon", 0.1),
        }
    )


@pytest.fixture
def die_high_score():
    return FuzzySet(
        {
            FuzzySetMember(6, 1.0),
            FuzzySetMember(5, 0.5),
        }
    )


@pytest.fixture
def die_low_score():
    return FuzzySet(
        {
            FuzzySetMember(1, 1.0),
            FuzzySetMember(2, 0.5),
        }
    )
