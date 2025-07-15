import json



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