# -*- coding: utf-8 -*-
"""
@author: hannah.bakker@kit.edu / 
@date: 16.07.2024
"""
import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import scipy.stats as stats

from GetCoordinates import GetCoordinates as GetCoordinates

class InferSpatial():
    """
        
    """ 
    
    def __init__(self, coord, confidence_level = 0.99):
        """
            Classify spatial pattern. 

        Parameters
        ----------
        coord : numpy array (I+J)x2
            Numpy array with coordinates.
        confidence_level : float, optional
            Confidence level to determine quantile in standard normal distribution. The default is 0.99.

        Returns
        -------
        None.

        """
        
        z_limit = self.retrieve_confidence_bounds(confidence_level)
        
        self.coord = coord
        self.hull = ConvexHull(coord)
        self.A  = self.hull.volume

        distance_matrix = cdist(self.coord, self.coord)
 
        nearest_neighbor_distances = np.zeros(self.coord.shape[0])
        for i in range(self.coord.shape[0]):
            # Set the diagonal to infinity to ignore the distance to itself
            distance_matrix[i, i] = np.inf
            # Find the minimum distance in the row (nearest neighbor distance)
            nearest_neighbor_distances[i] = np.min(distance_matrix[i])
                
        D_o = np.mean(nearest_neighbor_distances)  
        D_E = 0.5/np.sqrt((self.coord.shape[0])/(self.A))
        
        z = (D_o-D_E)/(0.26136/np.sqrt((self.coord.shape[0])*(self.coord.shape[0])/(self.A)))
    
        if z <z_limit:
            self.pattern = "clustered"
        elif z>-1*z_limit:
            self.pattern = "even"
        else:
            self.pattern = "random"
    
        print(f"Given the confidence level of {confidence_level} spatial pattern underlying these points can be considered {self.pattern} (z={round(z,2)}).")
  
    def retrieve_confidence_bounds(self, confidence_level):
        """
            Get respective quantile of the standard normal distribution.
        """
        alpha = 1 - confidence_level
        return stats.norm.ppf(alpha / 2)
        
    
    def plot(self, store, path = None):
        """
            Plot candidates and customers.

        Parameters
        ----------
        store : boolean
            Whether to store the plot or not.
        path : string
            Path. Default None.

        Returns
        -------
        None.

        """

        plt.figure(figsize=(8, 6))
        for simplex in self.hull.simplices:
            plt.plot(coord[simplex, 0], coord[simplex, 1], 'k-')
        plt.scatter(self.coord[:,0], self.coord[:,1]) 
        
        plt.title(f"Convex Hull with Area: {self.A:.2f}")
        plt.grid(True)
        if store: plt.savefig(path, format='png')                
        plt.show()

if __name__ == "__main__":
    # Example - cost matrix from cap41-74 from ORLIB CFLP insantance
    data = json.load(open("data/example.json"))
    d = np.asarray(data["c_ij"])
    #if coordinates are not available, estimate them via getcoordinates
    getcoord = GetCoordinates(d) 
    coord = getcoord.coord
       
    spatial = InferSpatial(coord)
    spatial.plot(store = True, path = "plots/example_convex_hull.png")
    

