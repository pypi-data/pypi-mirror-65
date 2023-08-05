from histographer.analysis.ranking.format import relative_favorability_from_comparisons, centrality_matrix_from_comparisons
from histographer.analysis.ranking.mock import mock_compare, mock_compare_btl

from typing import List, Tuple, Callable
import numpy as np


def balanced_rank_estimation(comparisons: List[Tuple[int, int]], n_objects: int) -> np.ndarray:
    """
    Implements the BRE-algorithm to find an ordering based on pairwise comparisons
    :param comparisons: A list containing tuples representing comparisons of the form (winner, loser)
    :param n_objects: The number of different objects the comparisons are sampled from
    :return: A numpy array of integers between 0 and n_objects ranked by their favorability
    """
    relative_favorability = relative_favorability_from_comparisons(comparisons, n_objects)
    relative_favorability[relative_favorability.nonzero()] = 2 * relative_favorability[relative_favorability.nonzero()] - 1
    scores = np.sum(relative_favorability, axis=1)
    return np.argsort(scores)


def elo(comparisons: List[Tuple[int, int]], n_objects: int) -> np.ndarray:
    """
    Implements the ELO-algorithm to find an ordering based on pairwise comparisons
    :param comparisons: A list containing tuples representing comparisons of the form (winner, loser)
    :param n_objects: The number of different objects the comparisons are sampled from
    :return: A numpy array of integers between 0 and n_objects ranked by their favorability
    """
    scores = np.full(n_objects, 1000, dtype=float)
    for winner, loser in comparisons:
        prob_result = 1 / (1 + 1.0 * np.power(10, (scores[winner] - scores[loser]) / 400))
        scores[winner] += (1 - prob_result) * 800 / len(comparisons)
        scores[loser] -= prob_result * 800 / len(comparisons)

    return np.argsort(scores)


def rank_centrality(comparisons: List[Tuple[int, int]], n_objects: int) -> np.ndarray:
    """
    Finds an ordering based on pairwise comparison using a random-walk interpretation over
    a rank centrality graph.
    :param comparisons: A list containing tuples representing comparisons of the form (winner, loser)
    :param n_objects: The number of different objects the comparisons are sampled from
    :return: A numpy array of integers between 0 and n_objects ranked by their favorability
    """
    cm = centrality_matrix_from_comparisons(comparisons, n_objects)

    eigenvalues, eigenvectors = np.linalg.eig(cm.T)
    scores = eigenvectors[:, np.isclose(eigenvalues, 1)]
    scores = scores[:, 0]
    scores /= np.sum(scores)
    return np.argsort(scores)


def iterate_active_elo(scores: np.ndarray):
    """
    Performs one iteration of the active ELO algorithm. Selects the two objects which have the closest
    scores and compares them. Updates are made to the scores-array based on the results of this comparison
    :param scores: A numpy array containing the current estimated elo-scores of all objects
    :return: Nothing
    """
    differences = np.abs(np.subtract.outer(scores, scores))
    np.fill_diagonal(differences, np.inf)
    a, b = np.argwhere(differences == np.min(differences))[0, :]
    winner, loser = mock_compare(a, b)

    prob_result = 1 / (1 + 1.0 * np.power(10, (scores[winner] - scores[loser]) / 400))
    scores[winner] += (1 - prob_result) * 800 / 500
    scores[loser] -= prob_result * 800 / 500


def active_elo(n_comparisons: int, n_objects: int):
    """
    Calls iterate_active_elo iteratively to generate a ranking.
    :param n_comparisons: The number of times iterate_active_elo will be called
    :param n_objects: The number of different objects the comparisons are sampled from
    :return: A numpy array of integers between 0 and n_objects ranked by their favorability
    """
    scores = np.full(n_objects, 1000, dtype=float)
    for _ in range(n_comparisons):
        iterate_active_elo(scores)

    return np.argsort(scores)


def compute_elo_scores(image_ids: List[int], comparisons: List[Tuple[int, int]]) -> np.ndarray:
    """
    Implements the ELO-algorithm to return ELO-scores for each item based on the pairwise comparisons
    :param image_ids: A list containing the id of every item in the population the comparisons are drawn from
    :param comparisons: A list containing tuples representing comparisons of the form (winner, loser)
    :return: A numpy array of the scores of each of the items
    """
    id_to_index = {im_id: i for i, im_id in enumerate(image_ids)}
    scores = np.full(len(image_ids), 1000, dtype=float)
    for winner, loser in comparisons:
        winner, loser = id_to_index[winner], id_to_index[loser]
        prob_result = 1 / (1 + 1.0 * np.power(10, (scores[winner] - scores[loser]) / 400))
        scores[winner] += (1 - prob_result) * 800 / len(comparisons)
        scores[loser] -= prob_result * 800 / len(comparisons)

    return scores
