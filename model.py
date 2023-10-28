# flake8: noqa

import gurobipy as gp
from gurobipy import GRB

from math import sqrt
import numpy as np
import scipy.sparse as sp
import pandas as pd


# Load the data
cities_df = pd.read_csv("data/cities_small.csv")
packages_df = pd.read_csv("data/packages_small.csv")

N = len(cities_df)


def euclidean_distance(lat1, lon1, lat2, lon2):
    return sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)


distances = np.zeros((N, N))
for i in range(N):
    for j in range(N):
        lat1, lon1 = cities_df.iloc[i][['lat', 'lon']]
        lat2, lon2 = cities_df.iloc[j][['lat', 'lon']]
        distances[i, j] = euclidean_distance(lat1, lon1, lat2, lon2)

flows = np.zeros((N, N))
for index, row in packages_df.iterrows():
    origin = row['origin']
    destination = row['destination']
    flows[origin, destination] = row['packages']

alpha = 0.75  # Discount factor
K = 3 # Number of hubs

# Create a new model
m = gp.Model("hub_and_spoke")
m.setParam(GRB.Param.TimeLimit, 600)  # seconds

# Decision Variables
x = m.addMVar((N, N), vtype=GRB.BINARY, name="x")
h = m.addMVar(N, vtype=GRB.BINARY, name="h")

# Objective Function
obj = sum(flows[i, j] * x[i, k] * x[j, l] * 
                        (distances[i, k] + 
                        alpha * distances[k, l] + 
                        distances[l, j])
          for i in range(N) for j in range(N) for k in range(N) for l in range(N))

m.setObjective(obj, GRB.MINIMIZE)

# Constraints
for i in range(N):
    m.addConstr(sum(x[i, j] for j in range(N)) == 1)

for i in range(N):
    for k in range(N):
        m.addConstr(x[i, k] <= h[k])

m.addConstr(h.sum() == K)

# Optimize model
m.optimize()

m.write("k_3_a_75.sol")

# if solution available, print
if m.status == 2 or m.status >= 7:
    x_sol = x.X
    h_sol = h.X
    print(f"Objective value:         {m.ObjVal}")

    point_to_point_distance = np.sum(flows * distances)
    print(f"Point-to-Point Distance: {point_to_point_distance}")

    print("\nChosen hubs (in city indices):")
    for k in range(N):
        if h_sol[k] > 0.5:
            print(k)
            
    print("\nRoutes:")
    for i in range(N):
        for k in range(N):
            if x_sol[i, k] > 0.5 and h_sol[k] > 0.5:
                print(f"City {i} -> Hub {k}")
else:
    print("No solution found!")
