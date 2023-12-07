from pprint import pprint
import fuzzy_sets.alpha
from fuzzy_sets.alpha import AlphaRange
from fuzzy_sets.classes import FuzzySet, FuzzySetMember
import fuzzy_sets.functions

if __name__ == "__main__":
    frood = FuzzySet(
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
    print(f"\n{' Fuzzy Set ':=^100}")
    print("Froodiness:")
    print(frood)

    print(f"\n{' Alpha Cut ':=^100}")
    print("~Frood_0.5:", fuzzy_sets.alpha.alpha_cut(frood, 0.5))

    print(f"\n{' Alpha Ranges ':=^100}")
    frood_alpha_ranges = fuzzy_sets.alpha.alpha_ranges(frood)
    print("\n".join([str(range) for range in frood_alpha_ranges]))

    print(f"\n{' Fuzzy Set from Alpha Ranges ':=^100}")
    fun_alpha_ranges = [
        AlphaRange(0, 0.5, {"video games", "uncertainty modelling coursework"}),
        AlphaRange(0.5, 1, {"uncertainty modelling coursework"}),
    ]
    print("\n".join([str(range) for range in fun_alpha_ranges]))
    print(fuzzy_sets.alpha.fuzzy_set_from_alpha_ranges(fun_alpha_ranges))
    print("\n")
    frood_from_alpha_ranges = fuzzy_sets.alpha.fuzzy_set_from_alpha_ranges(
        frood_alpha_ranges
    )
    print(fuzzy_sets.alpha.fuzzy_set_from_alpha_ranges(frood_alpha_ranges))

    print(f"\n{' Real to Real Functions ':=^100}")
    die_high_scores = FuzzySet(
        {
            FuzzySetMember(1, 0.1),
            FuzzySetMember(2, 0.2),
            FuzzySetMember(3, 0.4),
            FuzzySetMember(4, 0.6),
            FuzzySetMember(5, 0.8),
            FuzzySetMember(6, 1.0),
        }
    )
    squared = fuzzy_sets.functions.real_to_real(lambda x: x**2, die_high_scores)
    print("Squared:", squared)
    squared = fuzzy_sets.functions.real_to_real(lambda x: x**2, die_high_scores)
    print("Squared:", squared)
