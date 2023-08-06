from typing import List, Tuple
from histographer.analysis.ranking.algorithms import compute_elo_scores

import numpy as np


def suggest_pair(image_ids: List[int], comparisons: List[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Computes the ELO-scores for each item in image_ids and constructs a matrix consisting of the difference
    in ELO-score for each pair of items. The function returns the id's of the two items whose difference is the
    smallest.
    :param image_ids: A list of integer id's, one per item in the population that the comparisons are drawn from
    :param comparisons: A list containing tuples representing comparisons of the form (winner, loser)
    :return: A tuple with the id's of the two elements whose difference is the smallest out of any pair
    """
    scores = compute_elo_scores(image_ids, comparisons)
    differences = np.abs(np.subtract.outer(scores, scores))
    np.fill_diagonal(differences, np.inf)
    a, b = np.argwhere(differences == np.min(differences))[0, :]
    return image_ids[a], image_ids[b]
