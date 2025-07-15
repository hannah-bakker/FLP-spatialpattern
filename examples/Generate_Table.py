# -*- coding: utf-8 -*-
"""
@author: hannah.bakker@kit.edu / 
@date: 16.07.2024
"""
import os
import numpy as np
import pandas as pd
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
        
        self.z = (D_o-D_E)/(0.26136/np.sqrt((self.coord.shape[0])*(self.coord.shape[0])/(self.A)))
    
        if self.z <z_limit:
            self.pattern = "clustered"
        elif self.z >-1*z_limit:
            self.pattern = "even"
        else:
            self.pattern = "random"
    
        print(f"Given the confidence level of {confidence_level} spatial pattern underlying these points can be considered {self.pattern} (z={round(self.z,2)}).")
  
    def retrieve_confidence_bounds(self, confidence_level):
        """
            Get respective quantile of the standard normal distribution.
        """
        alpha = 1 - confidence_level
        return stats.norm.ppf(alpha / 2)
        
    
    def plot(self, store, path = None, cand_cust = None ):
        """
            Plot candidates and customers.

        Parameters
        ----------
        store : boolean
            Whether to store the plot or not.
        cand_cust : Tuple
            Whether to visually distinguish between candidates and customers. If a tuple, then (num_candidates, num_customers). Default None.
        path : string
            Path. Default None.

        Returns
        -------
        None.

        """

        plt.figure(figsize=(8, 6))
        for simplex in self.hull.simplices:
            plt.plot(coord[simplex, 0], coord[simplex, 1], 'k-')
        if cand_cust is not None: 
            #candidates
            plt.scatter(self.coord[:cand_cust[1],0], self.coord[:cand_cust[1],1], marker = "^", s = 80, label =  "customers")#, "^", 
            plt.scatter(self.coord[cand_cust[1]:,0], self.coord[cand_cust[1]:,1], marker = ".", s = 80, label = "candidates")#, "."
            plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol = 2, fontsize=16)
        else:
            plt.scatter(self.coord[:,0], self.coord[:,1]) 
        
        plt.title(f"Convex Hull with Area: {self.A:.2f}", fontsize=16)
        plt.grid(True)
        if store: plt.savefig(path, format='png', bbox_inches='tight')                
        plt.show()

if __name__ == "__main__":
    df = pd.DataFrame()
    for set_name in [
                    # "DEL-1991",
                    # "HOL-1999",
                    # "Yang",
                    # "ORLIB",
                    # "ORLIB-small",
                    "TBED1"
                    ]:
        for name in os.listdir("D:/data/"+set_name+"/"):
            data = json.load(open("D:/data/"+set_name+"/"+name))
            d = np.asarray(data["params"]["c_ij"])
            #if coordinates are not available, estimate them via getcoordinates
            getcoord = GetCoordinates(d) 
            coord = getcoord.coord
           # getcoord.store("data/coordinates/"+set_name+"/"+name[:-5]+".json")
            
            spatial = InferSpatial(coord)
            
            dict_data = {"set":set_name,
                         "inst":name[:-5],
                         "I":data["params"]["I"],
                         "J":data["params"]["J"],                         
                         "z-value": spatial.z,
                         "spatial_pattern":spatial.pattern
                        }
         #   spatial.plot(store = True, path = "plots/"+set_name+"/"+name[:-5]+".png",cand_cust = (data["params"]["I"], data["params"]["J"]) )
            if df.empty:
                df = pd.DataFrame(pd.Series(dict_data), columns=[len(df)+1]).transpose()
            else:
                df.loc[len(df)+1] = pd.Series(dict_data)                       
            df.to_excel("pattern1.xlsx")
