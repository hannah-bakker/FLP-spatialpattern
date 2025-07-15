"""
Spatial pattern classification module for 2D point sets.

Provides statistical classification based on nearest-neighbor distances
compared to complete spatial randomness (CSR).
"""

import numpy as np
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import scipy.stats as stats

def infer_spatial(coord: np.ndarray, confidence_level: float = 0.99) -> dict:
    """
    Classifies the spatial pattern of a given set of 2D coordinates as
    'clustered', 'random', or 'even', based on nearest neighbor distances
    and comparison to a theoretical expectation.

    Parameters
    ----------
    coord : np.ndarray
        A (n x 2) array of 2D coordinates (e.g., facility or demand points).
    confidence_level : float, optional
        Confidence level (between 0 and 1) to determine the threshold
        for classification. Default is 0.99.

    Returns
    -------
    dict
        A dictionary with keys:
        - "pattern": str, one of {'clustered', 'random', 'even'}
        - "z_score": float, test statistic
        - "z_limit": float, critical value threshold
    """
    
    if not isinstance(coord, np.ndarray) or coord.ndim != 2 or coord.shape[1] != 2:
        raise ValueError("coord must be a 2D NumPy array with shape (n_points, 2).")
    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be in the interval (0, 1).")

    z_limit = retrieve_confidence_bounds(confidence_level)
    
    hull = ConvexHull(coord)
    area = hull.volume  # For 2D, .volume returns area

    # Compute pairwise distance matrix
    distance_matrix = cdist(coord, coord)
    np.fill_diagonal(distance_matrix, np.inf)  # Ignore self-distance

    # Compute nearest neighbor distances
    nearest_neighbor_distances = np.min(distance_matrix, axis=1)
            
    D_o = np.mean(nearest_neighbor_distances)
    D_E = 0.5 / np.sqrt(coord.shape[0] / area)

    z_numerator = D_o - D_E
    z_denominator = 0.26136 / np.sqrt((coord.shape[0] ** 2) / area)
    z_score = z_numerator / z_denominator

    # Classify pattern based on z-score
    if z_score < z_limit:
        pattern = "clustered"
    elif z_score > -z_limit:
        pattern = "even"
    else:
        pattern = "random"

    return {
        "pattern": pattern,
        "z_score": z_score,
        "z_limit": z_limit
    }

def retrieve_confidence_bounds(confidence_level: float) -> float:
    """
    Returns the lower (negative) quantile z-value for a given confidence level 
    based on the standard normal distribution.

    Parameters:
        confidence_level (float): Confidence level between 0 and 1 (e.g., 0.95 for 95%).

    Returns:
        float: The z-score corresponding to the lower tail (i.e., -z_{1 - α/2}) 
               of the confidence interval.
    
    Raises:
        ValueError: If confidence_level is not in the open interval (0, 1).
    """
    if not (0 < confidence_level < 1):
        raise ValueError("confidence_level must be between 0 and 1 (exclusive).")
    
    alpha = 1 - confidence_level
    return stats.norm.ppf(alpha / 2)
    
