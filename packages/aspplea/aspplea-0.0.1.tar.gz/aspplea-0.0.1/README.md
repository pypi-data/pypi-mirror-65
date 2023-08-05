# ISPP Traveling Salesman

This package uses either the analytical method (datasets < 8) or the nearest-neighbour method to try to find a route for a symmetric TSP from a data matrix

This package works on csv input files containing the symmetric matrix of distances for the TSP including indices, for examples see:
[Github Repository](https://github.com/LeaHohmann/TravelingSalesperson)

To use, import the salesman module and call salesman.salesman(filename)

# Requirements

This package uses the numpy and pandas packages
