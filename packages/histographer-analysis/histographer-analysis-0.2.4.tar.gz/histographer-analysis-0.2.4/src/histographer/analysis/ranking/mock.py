from typing import List, Tuple
from random import sample, random


def generate_mock_comparisons(n_comparisons: int, n_objects: int, error_rate: float) -> List[Tuple[int, int]]:
    """
    Used to generate a set of mock pairwise comparisons for testing purposes.
    :param n_comparisons: The number of comparisons to be generated
    :param n_objects: The number of objects the comparisons will be sampled from
    :param error_rate: The probability that a superior object is deemed inferior
    :return: A list of tuples of the form (a, b), which indicate that 'a' compared favorably to 'b'
    """
    comparisons = []
    population = range(n_objects)
    for _ in range(n_comparisons):
        a, b = sample(population, 2)

        if random() < error_rate * abs(a - b) * 2 / n_objects:
            comparisons.append((min(a, b), max(a, b)))
        else:
            comparisons.append((max(a, b), min(a, b)))

    return comparisons


def generate_mock_comparisons_btl(n_comparisons: int, n_objects: int) -> List[Tuple[int, int]]:
    """
    Generates n_comparisons number of pairwise comparisons based on the bradley Bradley-Terry-Luce model for
    comparative judgement. Each object, i, has a weighting, w_i, associated with it. The probability that an object
    i compares favorably with j is given by w_i / (w_i + w_j). In this test-function, these weightings are simply
    the integers in range(n_objects). This function yields a correct result for approximately 95% of comparisons.
    :param n_comparisons: The number of comparisons to be generated
    :param n_objects: The number of objects the comparisons will be sampled from
    :return: A list of tuples of the form (a, b), which indicate that 'a' compared favorably to 'b'
    """
    comparisons = []
    population = range(n_objects)
    for _ in range(n_comparisons):
        a, b = sample(population, 2)
        if a / (a + b) > random():
            comparisons.append((a, b))
        else:
            comparisons.append((b, a))

    return comparisons


def mock_compare_btl(a: int, b: int) -> Tuple[int, int]:
    """
    Generates a single comparison of a and b based on BTL model.
    :param a: Score of object being compared
    :param b: Score of object being compared
    :return: Tuple containing (winner, loser)
    """
    if a / (a + b) > random():
        return a, b
    else:
        return b, a


def mock_compare(a: int, b: int, error_rate: float = 0.05) -> Tuple[int, int]:
    """
    Generates a single comparison of a and b.
    :param a: Score of object being compared
    :param b: Score of object being compared
    :return: Tuple containing (winner, loser)
    """
    if random() > error_rate:
        return max(a, b), min(a, b)
    else:
        return min(a, b), max(a, b)
