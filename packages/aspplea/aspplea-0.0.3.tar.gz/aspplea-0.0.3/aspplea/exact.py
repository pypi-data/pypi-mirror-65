#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from itertools import permutations
import numpy as np
import pandas as pd
    


# In[ ]:


def shortestpath(inputdataframe,distance):
    """
    Calculates shortest path from data matrix with symmetric TSP analytically
    
    Finds shortest path by iterating through all possible paths and keeping the shortest one.
    Uses the vector of indices of the data matrix as a path vector and permutates it, calculates the distance and compares to the previous value, then keeps the shorter one.
    
    Parameters
    ---------
    inpudataframe: Pandas DataFrame
                   Passed from salesman.salesman function (or use the salesman.dataimport function to retrieve it from file)
    distance: Float
              Maximum possible route length, passed from salesman.salesman
                   
    Returns
    ------
    shortest: Vector of strings
              Indices of inputdataframe in order of shortest route
    distance: Float
              Distance travelled by shortest route
    
    """
    pathvector = np.array(inputdataframe.index)
    permutating_vector = pathvector[:-1]
    
    for permutating_path in permutations(permutating_vector,len(permutating_vector)):
        path = np.append(permutating_path,pathvector[-1])
        rearrangeddata = inputdataframe.reindex(path,axis='columns')
        rolledpath = np.roll(path,len(path)-1)
        rearrangeddata = rearrangeddata.reindex(rolledpath,axis='index')
        pathlength = np.sum(np.diagonal(rearrangeddata))
        if pathlength < distance:
                distance = pathlength
                shortest = path 
                
    return distance, shortest
            

        

