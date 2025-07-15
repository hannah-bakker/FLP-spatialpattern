# spatial_analysis

A Python module for analyzing and visualizing spatial point patterns, with a focus on facility location problems. The tools provided here allow for the estimation and embedding of spatial coordinates from distance matrices — even in cases where only partial distance information is available (e.g., distances between facilities and customers, but not between facilities themselves).

This module was developed to support research in location analysis, particularly for studying the structural properties of instances in capacitated facility location problems (CFLP) and related models.
---

## 🔍 Module Overview

### `mds_coordinates.py`

This submodule provides utility functions for estimating pairwise distances and computing 2D embeddings using classical Multi-Dimensional Scaling (MDS).

#### Key Features

- **Estimate Missing Distances**  
  Heuristically reconstructs symmetric distance matrices when only facility-to-customer distances are known.

- **Multi-Dimensional Scaling (MDS)**  
  Projects the reconstructed distance matrix into a 2D Euclidean space for visualization or further pattern analysis.

- **Robust Input Validation**  
  Checks input dimensions, matrix completeness, and numeric consistency.

- **File Output**  
  Stores computed coordinates as JSON for use in experiments or visualizations.

---

### `pattern_classifier.py`

This submodule provides statistical tools to analyze and classify spatial patterns based on nearest-neighbor distances.

#### Key Features

- **Pattern Classification**  
  Identifies spatial distributions as `clustered`, `random`, or `even` by comparing observed nearest-neighbor distances with theoretical expectations under complete spatial randomness (CSR).

- **Z-Score Test**  
  Implements a two-sided statistical test for deviation from CSR using convex hull-based area estimation.

- **Confidence Level Control**  
  Supports custom significance thresholds (e.g., 95%, 99%).

---

## 🧪 Example Usage

```python
from spatial_analysis.mds_coordinates import get_mds_coordinates, store_coordinates
from spatial_analysis.pattern_classifier import infer_spatial_pattern
import numpy as np

# Example: distance matrix from 3 facilities to 4 customers
d_ij = np.array([
    [10, 20, 30, 40],
    [20, 10, 25, 35],
    [30, 25, 10, 20]
])

# Generate 2D coordinates
coords = get_mds_coordinates(d_ij, complete_distance_matrix=False)

# Store to file
store_coordinates(coords, "coords.json")

# Classify spatial pattern
result = infer_spatial_pattern(coords)
print(result["pattern"])  # "random", "clustered", or "even"
