import pytest
from fuzzy_sets.classes import FuzzySet, FuzzySetMember
from fuzzy_sets.alpha import AlphaRange, alpha_cut, alpha_ranges


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


def test_alpha_ranges(frood):
    assert alpha_ranges(frood) == [
        AlphaRange(0.0, 0.1, {"Arthur Dent", "Ford Prefect", "Marvin", "Vogon"}),
        AlphaRange(0.1, 0.5, {"Arthur Dent", "Ford Prefect"}),
        AlphaRange(0.5, 1.0, {"Ford Prefect"}),
    ]


cuts = [
    (0.0, {"Arthur Dent", "Ford Prefect", "Marvin", "Vogon"}),
    (0.1, {"Arthur Dent", "Ford Prefect", "Marvin", "Vogon"}),
    (0.2, {"Arthur Dent", "Ford Prefect", "Marvin", "Vogon"}),
    (0.5, {"Arthur Dent", "Ford Prefect"}),
    (1.0, {"Ford Prefect"}),
]


@pytest.mark.parametrize("alpha,expected", cuts)
def test_alpha_cut(alpha, expected, frood):
    alpha_cut(frood, alpha) == expected
