# Spatial Patterns Underlying Facility Location Problems: Visualization and Classification

## Description
The code allows visualizing spatial point patterns underlying facility location instances by inferring representative coordinates for candidates and customers in a 2-dimensional space based on the transport cost matrix. Based on these coordinates the spatial point pattern can be classified as clustered, random, or evenly distributed.

## Files
- data:
- example.json: transport cost matrix from cap131 instance from ORLIB data set
- plots:
- example.png: spatial point pattern estimated with GetCoordinates.py
- example_convex_hull.png: Convex hull used as to approximate the area for the hypothesis test on the underlying spatial pattern used in InferSpatial.py
- GetCoordinates.py: Class to generate coordinates via multi-dimensional scaling. 
- InferSpatial.py: Class to classify spatial point patterns based on retrieved coordinates.
- LICENSE.md: 
- README.md
- 

## Authors
- Hannah Bakker
