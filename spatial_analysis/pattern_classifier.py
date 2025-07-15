"""
pattern_classifier.py

Spatial pattern classification module for 2D point sets.

Classifies observed spatial patterns (e.g., facility or demand point layouts)
as 'clustered', 'random', or 'even' based on nearest-neighbor distances
compared to the expectation under complete spatial randomness (CSR).
"""

import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
from scipy.stats import norm


def infer_spatial_pattern(coord: np.ndarray, confidence_level: float = 0.99) -> dict:
    """
    Classify the spatial pattern of a 2D point set based on nearest-neighbor analysis.

    Compares the observed average nearest-neighbor distance to the theoretical expectation
    under complete spatial randomness (CSR) using a z-score test.

    Parameters
    ----------
    coord : np.ndarray
        A (n_points x 2) array of 2D coordinates (e.g., facilities or demand points).
    confidence_level : float, optional
        Confidence level for the hypothesis test, must be in (0, 1). Default is 0.99.

    Returns
    -------
    dict
        A dictionary containing:
        - "pattern": str, one of {"clustered", "random", "even"}
        - "z_score": float, the standardized test statistic
        - "z_limit": float, critical value for rejection region

    Raises
    ------
    ValueError
        If inputs are malformed or confidence level is invalid.
    """
    if not isinstance(coord, np.ndarray) or coord.ndim != 2 or coord.shape[1] != 2:
        raise ValueError("coord must be a 2D NumPy array with shape (n_points, 2).")

    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1 (exclusive).")

    n = coord.shape[0]
    z_limit = get_z_limit(confidence_level)

    # Estimate area via convex hull
    hull = ConvexHull(coord)
    area = hull.volume  # For 2D, volume == area

    # Pairwise distances excluding self-distances
    distance_matrix = cdist(coord, coord)
    np.fill_diagonal(distance_matrix, np.inf)
    nearest_distances = np.min(distance_matrix, axis=1)

    # Observed and expected distances
    D_obs = np.mean(nearest_distances)
    D_exp = 0.5 / np.sqrt(n / area)
    SE = 0.26136 / np.sqrt(n**2 / area)
    z_score = (D_obs - D_exp) / SE

    # Classification based on z-score
    if z_score < -z_limit:
        pattern = "clustered"
    elif z_score > z_limit:
        pattern = "even"
    else:
        pattern = "random"

    return {
        "pattern": pattern,
        "z_score": z_score,
        "z_limit": z_limit
    }


def get_z_limit(confidence_level: float) -> float:
    """
    Compute the two-sided critical z-value for a given confidence level.

    Parameters
    ----------
    confidence_level : float
        The desired confidence level in (0, 1), e.g. 0.95 or 0.99.

    Returns
    -------
    float
        The positive critical z-score such that P(|Z| > z) = alpha.
        (The lower threshold is -z, and upper is +z.)

    Raises
    ------
    ValueError
        If confidence_level is outside (0, 1).
    """
    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1 (exclusive).")

    alpha = 1 - confidence_level
    return norm.ppf(1 - alpha / 2)
