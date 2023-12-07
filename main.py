import fuzzy_sets.alpha
from fuzzy_sets.classes import FuzzySet, FuzzySetMember

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
    print("\n".join([str(cut) for cut in fuzzy_sets.alpha.alpha_ranges(frood)]))
