import pytest
from fuzzy_sets.classes import FuzzySet, FuzzySetMember


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
