"""
mds_coordinates.py

Provides utility functions to generate 2D coordinates from a distance matrix
using Multi-Dimensional Scaling (MDS). Supports incomplete distance matrices
via estimation heuristics.
"""
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

def check_distance_matrix(d_ij: np.ndarray, complete: bool) -> None:
    if not isinstance(d_ij, np.ndarray) or d_ij.ndim != 2:
        raise ValueError("Input must be a 2D NumPy array.")
    if complete and d_ij.shape[0] != d_ij.shape[1]:
        raise ValueError("Matrix must be square if marked as complete.")


def estimate_missing_distances(d_ij: np.ndarray, nb_est: int = 4) -> np.ndarray:
    """
    Estimate distances between facilities using shared customer distances.

    Parameters
    ----------
    d_ij : np.ndarray
        IxJ array of distances between facilities and customers.
    nb_est : int
        Number of customer reference points to use per pairwise estimate.

    Returns
    -------
    np.ndarray
        Extended (I+J)x(I+J) symmetric distance matrix for MDS.
    """
    d = d_ij.T  # Transpose: shape becomes J x I
    J, I = d.shape
    dist_ii = np.empty((I, I))

    for i in range(I):
        for i_prime in range(I):
            UB, LB = np.max(d), 0
            for j in np.argsort(d[:, i])[:nb_est]:
                UB = min(UB, d[j, i] + d[j, i_prime])
                LB = max(LB, abs(d[j, i] - d[j, i_prime]))
            dist_ii[i, i_prime] = (UB + LB) / 2
    np.fill_diagonal(dist_ii, 0)
    return np.block([
        [d, np.zeros((J, I))],
        [np.zeros((I, J)), dist_ii]
    ])


def generate_coordinates_from_mds(distance_matrix: np.ndarray) -> np.ndarray:
    mds = MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=1,
              dissimilarity="precomputed", n_jobs=1)
    return mds.fit_transform(distance_matrix)


def get_mds_coordinates(d_ij: np.ndarray, complete_distance_matrix: bool = False, nb_est: int = 4) -> np.ndarray:
    """
    Generate 2D coordinates for candidate-customer distance matrix using MDS.

    Parameters
    ----------
    d_ij : np.ndarray
        (I x J) or (I+J x I+J) distance matrix.
    complete_distance_matrix : bool
        Whether the matrix is already square and complete.
    nb_est : int
        Number of customer reference points to use for estimation.

    Returns
    -------
    np.ndarray
        (I+J x 2) array of 2D coordinates.
    """
    check_distance_matrix(d_ij, complete_distance_matrix)

    if complete_distance_matrix:
        d = d_ij
    else:
        d = estimate_missing_distances(d_ij, nb_est)

    return generate_coordinates_from_mds(d)


def store_coordinates(coord: np.ndarray, path: str) -> None:
    """
    Store 2D coordinates as a JSON file.

    Parameters
    ----------
    coord : np.ndarray
        Array of shape (n_points, 2), typically from `get_mds_coordinates()`.
    path : str
        Path to output JSON file.
    """
    with open(path, "w") as f:
        json.dump(coord.tolist(), f, indent=1)

