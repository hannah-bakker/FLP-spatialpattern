# -*- coding: utf-8 -*-
"""
@author: hannah.bakker@kit.edu / stefan.nickel@kit.edu
@date: 16.07.2024
"""

import numpy as np
import json 
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

class GetCoordinates:
    """
        Get coordinates in a 2-dimensional plane approximating the spatial distribution of
        candidates and customers in a facility location
        problem that are representative of the distance relationships implied
        by the transportation matrix.
        
        Primarily to be used on benchmark instances for which real-coordinates
        are not available. Can, however, also be useful if real-world distances 
        do not adhere to Euclidean distances as the visualization allows apprehending
        the relative distance between points.
    """
    
    def __init__(self, d_ij, complete_distance_matrix = False,):
        """
            Generate 2D coordinates.
        
        Parameters:
            c_ij                        
            complete_distance_matrix    boolean: Indicates whether the distance matrix is complete in the sense that Default = False.
            
        """
        
        if self.check_type(d_ij, complete_distance_matrix): #check type
            self.d = d_ij.T # as there are usually more customers than candidates, 
                            # consider those as "samples" (thus, transpose)
            # retrieve dimensions
            self.I = np.shape(self.d)[1]
            self.J = np.shape(self.d)[0]
            
            
            #infer potentially missing values
            if not complete_distance_matrix:
                self.estimate_distances_between_j()
        
            #apply MDS
            self.scale()
                  
    def check_type(self, d_ij, complete_distance_matrix):
        """
            Checks whether input matrix fulfills requirements. 
            If not, errormessage is printed.

        Parameters
        ----------
        d_ij : object
            input object.
        complete_distance_matrix : boolean
            input boolean.

        Returns
        -------
        bool
            True: input matrix fulfills requirement: 2D numpy array.

        """
        if not isinstance(d_ij, np.ndarray) and d_ij.ndim == 2:
            print("Input data does not meet requirements. Please, provide 2D numpy array.")
        elif complete_distance_matrix and np.shape(d_ij)[0]!= np.shape(d_ij)[1]:
            print("Matrix is not symmetric, hance, cannot be complete distance matrix. Please, check again!")
        else:
            return True
        
        
    def estimate_distances_between_j(self, nbEst = 4):
        """
            If input matrix is of dimension IxJ, i.e., contains distances 
            between candidates (I) and customers (J) then it contains only 
            partial information on the distances between points. In order to 
            use MDS in the next step, relative distances between candidates 
            have to be estimated. Thus, approximated IXI matrix is appended.

        Parameters
        ----------
        nbEst : int, optional
            Number of customers used as reference points to 
            estimate distances between each candidate pair. The default is 4.

        Returns
        -------
        None.

        """
        
        dist_ii = np.empty([self.I,self.I])
        for i in range(self.I):
            for i_prime in range(self.I):
                UB = np.max(self.d)
                LB = 0
                for j in np.argsort(self.d[:, i])[:nbEst]:
                    UB = min(UB, self.d[j, i]+self.d[j, i_prime])
                    LB = max(LB, abs(self.d[j, i]-self.d[j, i_prime]))
                dist_ii[i,i_prime] = (UB+LB)/2
        np.fill_diagonal(dist_ii, 0) # estimation might not arrive at 0 for each 
                                     # point to itself
        print(dist_ii)
        self.d = np.concatenate([self.d, dist_ii])

        
    def scale(self):
        """
            Take input matrix and apply multi-dimensional scaling to reduce 
            information from extended distance matrix to 2 dimensions. 
            Input matrix self.d has dimensions (J+I)xI, output coord has 
            dimensions (J+I)x2.

        Returns
        -------
        None.

        """
      
        mds = MDS(n_components=2, 
                  max_iter=3000, 
                  eps=1e-9, 
                  random_state=1,
                  dissimilarity="euclidean", 
                  n_jobs=1)
        self.coord = mds.fit_transform(self.d)
            
        
    def to_string(self):
        """
            Print out coordinates.

        Returns
        -------
        None.

        """
        print(self.coord.round(2))

    def store(self, path):
        """
            Store coordintes as json.

        Parameters
        ----------
        path : string
            Path.

        Returns
        -------
        None.

        """
        with open(path, "w") as f:
            json.dump(self.coord.tolist(), f, indent=1)
            f.close()
        
        
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
        plt.scatter(self.coord[:self.J,0], self.coord[:self.J,1], marker = "^", label =  "customers")#, "^", 
        plt.scatter(self.coord[self.J:,0], self.coord[self.J:,1], marker = ".", label = "candidates")#, "."
        plt.legend()
        plt.title('Scatter Plot of Customers and Candidates')
        plt.grid(True)
        if store: plt.savefig(path, format='png')                
        plt.show()
   
  
if __name__ == "__main__":
    # Example - cost matrix from cap134 from ORLIB CFLP insantance
    data = json.load(open("data/example.json"))
    d = np.asarray(data["c_ij"])
    
    getcoord = GetCoordinates(d)
    getcoord.to_string()
    getcoord.store("data/coordinates/example.json")
    getcoord.plot(store = True, path = "plots/example.png")
    

