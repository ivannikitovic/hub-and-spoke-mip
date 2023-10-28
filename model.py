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
K = 3  # Number of hubs

# Create a new model
m = gp.Model("hub_and_spoke")

# Decision Variables
x = m.addMVar((N, N), vtype=GRB.BINARY, name="x")
y = m.addMVar((N, N), vtype=GRB.BINARY, name="y")

# Objective Function
obj = sum(flows[i, j] * (distances[i, k] * x[i, k] + alpha * distances[k, l] * y[k, l] + distances[l, j] * x[l, j])
          for i in range(N) for j in range(N) for k in range(N) for l in range(N))
m.setObjective(obj, GRB.MINIMIZE)

# Constraints
for i in range(N):
    m.addConstr(sum(x[i, j] for j in range(N)) == 1)

for i in range(N):
    for j in range(N):
        m.addConstr(x[i, j] <= x[j, j])
        
m.addConstr(sum(x[i, i] for i in range(N)) == K)

for i in range(N):
    for j in range(N):
        if i != j:
            m.addConstr(y[i, j] <= x[i, i])
            m.addConstr(y[i, j] <= x[j, j])

# Optimize model
m.optimize()

if m.status == GRB.OPTIMAL:
    x_sol = x.X
    y_sol = y.X
    print("Optimal solution found!")
    print(f"Objective value:         {m.ObjVal}")

    point_to_point_distance = np.sum(flows * distances)

    print(f"Point-to-Point Distance: {point_to_point_distance}")

    
    print("\nChosen hubs (in city indices):")
    for i in range(N):
        if x_sol[i, i] > 0.5:
            print(i)
            
    print("\nRoutes:")
    for i in range(N):
        for j in range(N):
            if x_sol[i, j] > 0.5 and i != j:
                print(f"City {i} -> Hub {j}")
else:
    print("No solution found!")
