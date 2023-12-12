from fuzzy_sets import probability
import fuzzy_sets.alpha
from fuzzy_sets.alpha import AlphaRange
from fuzzy_sets.classes import FuzzySet, FuzzySetMember
from fuzzy_sets.probability import ProbabilityDistribution, Probability
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

    print()

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

    die_low_scores = FuzzySet(
        {
            FuzzySetMember(1, 1.0),
            FuzzySetMember(2, 0.8),
            FuzzySetMember(3, 0.6),
            FuzzySetMember(4, 0.4),
            FuzzySetMember(5, 0.2),
            FuzzySetMember(6, 0.1),
        }
    )

    print("Die high scores:", die_high_scores)
    squared = fuzzy_sets.functions.real_to_real(lambda x: x**2, die_high_scores)
    print("Squared:", squared)
    halved = fuzzy_sets.functions.real_to_real(lambda x: x / 2, die_high_scores)
    print("Halved:", halved)

    print()

    print("Die low scores:", die_low_scores)
    added = fuzzy_sets.functions.apply(
        lambda x, y: x + y, die_high_scores, die_low_scores
    )
    print("Added:", added)

    three_way_add = fuzzy_sets.functions.apply(
        lambda x, y, z: x + y + z, die_high_scores, die_low_scores, squared
    )
    print("Three way add:", three_way_add)

    print(f"\n{' Fuzzy Propositions ':=^100}")

    # Only for printing
    W = {("H", "H"), ("H", "T"), ("T", "H"), ("T", "T")}
    print("W, set of possible worlds for tossing two coins:", W)

    fair_distribution = ProbabilityDistribution(
        {
            Probability(("H", "H"), 0.25),
            Probability(("H", "T"), 0.25),
            Probability(("T", "H"), 0.25),
            Probability(("T", "T"), 0.25),
        }
    )

    print("Fair distribution:\n", str(fair_distribution))

    print()

    all_heads = FuzzySet(
        {
            FuzzySetMember(("H", "H"), 1.0),
        }
    )

    conditional_distribution = probability.conditional_distribution(
        fair_distribution, all_heads
    )
    print(
        "Conditional distribution given all heads obtained:\n",
        str(conditional_distribution),
    )
    print(
        f"Sum of conditional probabilities: {sum(conditional_distribution.probabilities):.3f}"
    )

    print()

    at_least_one_head = FuzzySet(
        {
            FuzzySetMember(("H", "H"), 1.0),
            FuzzySetMember(("T", "H"), 1.0),
            FuzzySetMember(("H", "T"), 1.0),
        }
    )

    conditional_distribution = probability.conditional_distribution(
        fair_distribution, at_least_one_head
    )
    print(
        "Conditional distribution given at_least_one_head obtained:\n",
        str(conditional_distribution),
    )
    print(
        f"Sum of conditional probabilities: {sum(conditional_distribution.probabilities):.3f}"
    )

    print()

    good_result = FuzzySet(
        {
            FuzzySetMember(("H", "H"), 1.0),
            FuzzySetMember(("H", "T"), 0.5),
            FuzzySetMember(("T", "H"), 0.5),
        }
    )

    conditional_distribution = probability.conditional_distribution(
        fair_distribution, good_result
    )

    print(
        "Conditional distribution given a good result was obtained:\n",
        str(conditional_distribution),
    )

    print(
        f"Sum of conditional probabilities: {sum(conditional_distribution.probabilities):.3f}"
    )

    print()

    unfair_distribution = ProbabilityDistribution(
        {
            Probability(("H", "H"), 0.25**2),
            Probability(("H", "T"), 0.25 * 0.75),
            Probability(("T", "H"), 0.75 * 0.25),
            Probability(("T", "T"), 0.75**2),
        }
    )

    print("Unfair distribution (P(H) = 0.25, P(T) = 0.75):\n", str(unfair_distribution))

    unfair_conditional_distribution = probability.conditional_distribution(
        unfair_distribution, good_result
    )

    print("Unfair conditional distribution:\n", str(unfair_conditional_distribution))

    print(
        f"Sum of conditional probabilities: {sum(unfair_conditional_distribution.probabilities):.3f}"
    )
