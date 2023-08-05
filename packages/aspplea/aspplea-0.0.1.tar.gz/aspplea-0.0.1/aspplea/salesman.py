#!/usr/bin/env python
# coding: utf-8

# In[5]:


import numpy as np
import pandas as pd
from asppleasalesman import exact
from asppleasalesman import heuristic

# In[6]:


def dataimport(filename):
    """
    Imports data matrix from filename
    
    Parameters
    ----------
    filename: CSV file
              File should contain the (symmetric) data matrix with nodes/("cities") as column and row indices (as first row/column)
              
    Returns
    ------
    data: Pandas DataFrame
    
    """
    
    data = pd.read_csv(filename,sep=';',index_col=0,engine='python')
    return data


# In[7]:


def salesman(filename):
    """
    Finds best possible solution to the input symmetric TSP, either by exact calculation or a nearest-neighbour method
    
    Uses dataimport to import the data matrix, checks the size of the data matrix. 
    For problems with 8 or fewer nodes it calls the shortestpath function from exact to calculate exact solution.
    For problems with more than 8 nodes it calls the findbestroute function from heuristic to calculate the best possible solution available to the nearest neighbour algorithm.
    In the latter case, it calculates the lower and upper limit and mean path and prints them for comparison.
    
    Parameters
    ---------
    filename: CSV file 
              See dataimport
              
    Returns
    ------
    shortest: Vector or list of strings (nodes/cities)
              Indices of data in order of shortest route
              Either absolute shortest route or shortest route it could find for problems greater 8
    distance: Float
              Distance travelled by shortest route
    """
    data = dataimport(filename)
    Maxlength = 0
    for i in range(len(data)):
        Maxlength +=data.iloc[:,i].max()
    
    if data.size <= 64:
        print("Exact method will be used")
        #Load exact method
        from exact import shortestpath
        distance, shortest = shortestpath(data,Maxlength)
        print("Shortest path: ", shortest)
        print("Length: ", distance)
        
    else:
        print("I will use a heuristic method to find a best guess as the dataset is larger than 8")
        from heuristic import findbestroute
        shortest, distance = findbestroute(data,Maxlength)
        print("This is the shortest route I could find with the nearest neighbour method: ", shortest)
        print("Length: ", distance)
    
        print("Here is how it compares:")
        Minlength = 0
        for i in range(len(data)):
            Minlength +=data.iloc[:,i].min()
        print("Sum of distances from each city to nearest neighbour: ",Minlength)
        print("Sum of distances from each city to farthest neighbour: ",Maxlength)
        Average = len(data)*data.mean().mean()
        print("Average distance of random tour: ",Average)
        
    return shortest,distance


# In[8]:





# In[ ]:





# In[ ]:





# In[ ]:




