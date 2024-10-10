# Spatial Patterns Underlying Facility Location Problems: Visualization and Classification

## Description
The code allows visualizing spatial point patterns underlying facility location instances by inferring representative coordinates for candidates and customers in a 2-dimensional space based on the transport cost matrix. Based on these coordinates the spatial point pattern can be classified as clustered, random, or evenly distributed.

## Files
- data:
  - example.json: transport cost matrix from cap131 instance from ORLIB data set
  - capa1.json: transport cost matrix from capa1 instance from ORLIB data set
  - coordinates: folders with coordinates for different benchmark instances
- plots:
  - example.png: spatial point pattern estimated with GetCoordinates.py for example.json
  - example_convex_hull.png: Convex hull used to approximate the area for the hypothesis test on the underlying spatial pattern used in InferSpatial.py
  - capa1.png: spatial point pattern estimated with GetCoordinates.py for capa1.json
  - YAN-2012: plots for 20 benchmark instances presented in *Yang, Z. and Chu, F. and Chen, H.: A cut-and-solve based algorithm for the single-source capacitated facility location problem.
European Journal of Operational Research 221(3):521—532 (2012).*
  - DEL-1991: plots for 57 benchmark instances presented in *Delmaire, H. and Diaz, J. A. and Fernandez, E. and Ortega, M.: Reactive Grasp And Tabu Search Based Heuristics For The Single Source Capacitated Plan Location Problem. INFOR: Information Systems and Operational Research 37(3):194—225 (1999).*
  - HOL-1999: plots for 71 benchmark instances presented in *Holmberg, K. and R¨onnqvist, M. and Yuan, D.: An exact algorithm European Journal of Operational Research 113(3):544-–559 (1999). *
  - BEA-1989-s: plots for 36 small benchmark instances and 
  - BEA-1989-l: plots for 12 large benchmark instances presented in *Beasley, J. E.: OR-Library: Distributing Test Problems by Electronic Mail. Journal of the Operational Research Society 41(11):1069—1072 (1990).*
- GitHub_SpatialPointPatterns.pdf: Explanation of theoretical ideas underlying the code.
- GetCoordinates.py: Class to generate coordinates via multi-dimensional scaling. 
- InferSpatial.py: Class to classify spatial point patterns based on retrieved coordinates.
- LICENSE.md 
- README.md

## Example 

The file [data/example.json](data/example.json) contains the transport cost matrix from instance *cap131* from the ORLIB cap dataset available under [https://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html](https://people.brunel.ac.uk/~mastjjb/jeb/orlib/capinfo.html)

Running [GetCoordinates.py](GetCoordinates.py) will provide you with coordinates producing the spatial point pattern below: 

![Spatial point pattern - cap131 ORLIB instances](plots/example.png)

*Notice, that the data set was originally based on a US dataset and that the spatial distribution of the points resembles the distribution of cities on a US map. However, be aware that the MDS output is not deterministic, and different random states will produce different results.*

Running [InferSpatial.py](InferSpatial.py) on the above spatial point pattern will classify the underlying spatial point pattern in the area of the convex hull as **clustered**, indicating that the average nearest neighbor distance is less than what would be expected if the points were distributed randomly. 

![Convex Hull spatial point pattern - cap131 ORLIB instances](plots/example_convex_hull.png)

## Reference 
Bakker, H., & Nickel, S. (2024). Spatial Patterns Underlying Facility Location Problems: Visualization and Classification (v1.1). Zenodo. [https://doi.org/10.5281/zenodo.12771297](https://doi.org/10.5281/zenodo.12771297)

## Authors
- Hannah Bakker
- Stefan Nickel
