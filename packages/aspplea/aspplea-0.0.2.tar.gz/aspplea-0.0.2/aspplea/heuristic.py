#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import pandas as pd


# In[4]:


def nearestneighbour(inputdata,i,cityvector):
    """
    Finds a route by nearest neighbour algorithm for given starting point
    
    Finds the nearest still available (non-NaN) index in the matrix by searching for its column minimum, adds the index to the tour and the distance to tour length.
    Then replaces its own row by NaN and hands over to next stop it chose.
    
    Parameters
    ---------
    inputdata: Pandas DataFrame
               Matrix of symmetric TSP. Passed from findbestroute function
    i: integer
       Index position of starting point, passed from findbestroute function (iterator in findbestroute)
    cityvector: Vector of strings
                Vector containing the indices (nodes/"cities") of the data matrix, passed from findbestroute
    
    Returns
    ------
    route: Vector of strings
           Vector of indices in order of nearest neighbour route
    pathlengths: Float
                 Distance travelled by the nearest neighbour route
    """
    
    TSP = inputdata.copy()
    pathlength = 0
    node = cityvector[i]
    route = list([node])
    
    for j in range(len(cityvector)-1):
        pathlength += TSP[node].min()
        route.append(TSP[node].idxmin())
        TSP.loc[node,:] = np.nan
        node = route[j+1]
        j += 1
        
    return route, pathlength


# In[1]:


def findbestroute(inputdata,distance):
    """
    Iterates through different starting points for nearest neighbour and finds the shortest.
    
    Iterates through all indices of the data matrix and calls nearestneighbour on this starting point to find the nearest neighbour route, keeps the shortest.
    
    Parameters
    ---------
    inputdata: Pandas DataFrame
               Data matrix of the symmetric TSP, passed from salesman.salesman (or import from file with salesman.dataimport)
    distance: Float
              Longest possible distance (upper limit), passed from salesman.salesman
               
    Returns
    ------
    bestroute: Vector of strings
               Vector of data matrix indices in the order of shortest route it could find with this method
    distance:  Float
               Distance travelled by the output route
    """
    
    cityvector = np.array(inputdata.index)
    
    for i in range(len(cityvector)):
        route, pathlength = nearestneighbour(inputdata,i,cityvector)
        if pathlength < distance:
            distance = pathlength
            bestroute = route
        i += 1   
        
    return bestroute, distance
        


# In[ ]:





# In[ ]:




