"""
mds_coordinates.py

Provides utility functions to generate 2D coordinates from a distance matrix
using Multi-Dimensional Scaling (MDS). As in facility location problems distance 
matrices are often incomplete as only distances between candidates and customers, 
and, i.e., not between candidates and candidates / customers and customers are 
provided, these distances are estimated.
"""
import numpy as np
import json
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

def check_distance_matrix(d_ij: np.ndarray, complete: bool) -> None:
    """
    Validates the structure of a distance matrix.

    Parameters
    ----------
    d_ij : np.ndarray
        The input distance matrix, expected to be a 2D NumPy array.
    complete : bool
        Whether the matrix is expected to be square (i.e., complete pairwise distances).

    Raises
    ------
    TypeError
        If the input is not a NumPy array.
    ValueError
        If the input is not 2-dimensional.
    ValueError
        If 'complete' is True and the matrix is not square.
    """
    if not isinstance(d_ij, np.ndarray):
        raise TypeError(f"Expected input of type np.ndarray, got {type(d_ij)}.")

    if d_ij.ndim != 2:
        raise ValueError(f"Input array must be 2-dimensional, got {d_ij.ndim} dimensions.")

    if complete and d_ij.shape[0] != d_ij.shape[1]:
        raise ValueError(
            f"Matrix marked as complete must be square, "
            f"but received shape {d_ij.shape}."
        )

def estimate_missing_distances(d_ij: np.ndarray, nb_est: int = 4) -> np.ndarray:
    """
    Estimate pairwise distances between facilities using the distances to 
    their respective nearest customers.

    Parameters
    ----------
    d_ij : np.ndarray
        A (I x J) array of distances from I facilities to J customers.
    nb_est : int, optional
        Number of customer reference points to use per pairwise estimate.
        Must be less than or equal to J. Default is 4.

    Returns
    -------
    np.ndarray
        An (I+J) x (I+J) symmetric distance matrix for use in MDS.

    Raises
    ------
    ValueError
        If nb_est > J or d_ij is not a 2D NumPy array.
    """
    if not isinstance(d_ij, np.ndarray) or d_ij.ndim != 2:
        raise ValueError("Input must be a 2D NumPy array of shape (I, J).")

    d = d_ij.T  # Transpose to shape (J x I)
    J, I = d.shape

    if nb_est > J:
        raise ValueError(f"nb_est ({nb_est}) cannot exceed number of customers (J={J}).")

    dist_ii = np.empty((I, I))

    # Estimate pairwise facility-facility distances
    for i in range(I):
        for i_prime in range(I):
            # Initialize bounds
            UB = np.max(d)
            LB = 0.0

            # Use nb_est closest customers to facility i as references
            reference_customers = np.argsort(d[:, i])[:nb_est]

            for j in reference_customers:
                dist_sum = d[j, i] + d[j, i_prime]
                dist_diff = abs(d[j, i] - d[j, i_prime])
                UB = min(UB, dist_sum)
                LB = max(LB, dist_diff)

            dist_ii[i, i_prime] = (UB + LB) / 2

    np.fill_diagonal(dist_ii, 0.0)

    # Assemble full (I+J)x(I+J) symmetric distance matrix
    top = np.hstack([d, np.zeros((J, I))])
    bottom = np.hstack([np.zeros((I, J)), dist_ii])
    return np.vstack([top, bottom])

def generate_coordinates_from_mds(
    distance_matrix: np.ndarray,
    n_components: int = 2,
    max_iter: int = 3000,
    eps: float = 1e-9,
    random_state: int = 1,
) -> np.ndarray:
    """
    Apply MDS to a precomputed distance matrix to obtain low-dimensional coordinates.

    Parameters
    ----------
    distance_matrix : np.ndarray
        A symmetric (n x n) distance matrix representing pairwise dissimilarities.
    n_components : int, optional
        The number of dimensions for the output coordinates. Default is 2.
    max_iter : int, optional
        Maximum number of iterations for MDS optimization. Default is 3000.
    eps : float, optional
        Convergence tolerance. Default is 1e-9.
    random_state : int, optional
        Random seed for reproducibility. Default is 1.

    Returns
    -------
    np.ndarray
        An (n x n_components) array of coordinates in reduced space.

    Raises
    ------
    ValueError
        If the input matrix is not square or contains NaNs.
    """
    if distance_matrix.ndim != 2 or distance_matrix.shape[0] != distance_matrix.shape[1]:
        raise ValueError("Input must be a square distance matrix.")
    if np.isnan(distance_matrix).any():
        raise ValueError("Distance matrix must not contain NaN values.")

    mds = MDS(
        n_components=n_components,
        max_iter=max_iter,
        eps=eps,
        dissimilarity="precomputed",
        random_state=random_state
    )

    return mds.fit_transform(distance_matrix)

def get_mds_coordinates(
    d_ij: np.ndarray,
    complete_distance_matrix: bool = False,
    nb_est: int = 4
) -> np.ndarray:
    """
    Generate 2D coordinates from a facility-customer distance matrix using MDS.

    If the input matrix is incomplete (i.e., only facility-to-customer distances),
    missing facility-to-facility distances are heuristically estimated before
    applying Multi-Dimensional Scaling (MDS).

    Parameters
    ----------
    d_ij : np.ndarray
        An (I x J) array (incomplete) or (I+J x I+J) array (complete) of pairwise distances.
    complete_distance_matrix : bool, optional
        Set to True if `d_ij` is already a square, symmetric distance matrix. Default is False.
    nb_est : int, optional
        Number of reference customers to use for estimating missing distances
        if the matrix is incomplete. Default is 4.

    Returns
    -------
    np.ndarray
        An (I+J x 2) array of 2D coordinates suitable for plotting or spatial analysis.

    Raises
    ------
    ValueError
        If input matrix is invalid or estimation parameters are inconsistent.
    """
    check_distance_matrix(d_ij, complete=complete_distance_matrix)

    if complete_distance_matrix:
        distance_matrix = d_ij
    else:
        distance_matrix = estimate_missing_distances(d_ij, nb_est)

    return generate_coordinates_from_mds(distance_matrix)

def store_coordinates(coord: np.ndarray, path: str) -> None:
    """
    Store 2D coordinates as a JSON file.

    Parameters
    ----------
    coord : np.ndarray
        A NumPy array of shape (n_points, 2) containing 2D spatial coordinates.
    path : str
        File path (including `.json`) to save the coordinate data.

    Raises
    ------
    ValueError
        If `coord` is not a 2D array with two columns.
    IOError
        If writing to the file fails due to OS-related issues.
    """
    if not isinstance(coord, np.ndarray) or coord.ndim != 2 or coord.shape[1] != 2:
        raise ValueError("coord must be a 2D NumPy array with shape (n_points, 2).")

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(coord.tolist(), f, indent=2)
    except OSError as e:
        raise IOError(f"Failed to write coordinates to '{path}': {e}")