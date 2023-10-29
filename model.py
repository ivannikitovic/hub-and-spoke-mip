# flake8: noqa

import gurobipy as gp
from gurobipy import GRB

import numpy as np
from data_loader import load_data

# Hyperparameters
cities_file = "data/cities_small.csv"
packages_file = "data/packages_small.csv"
output_dir = "output"
TIMEOUT = 600  # seconds
ALPHA = 0.75  # Discount factor
K = 2 # Number of hubs

# Load the data
N, flows, distances = load_data(cities_file, packages_file)

# Create a new model
m = gp.Model("hub_and_spoke")
m.setParam(GRB.Param.TimeLimit, TIMEOUT)  # seconds

# Decision Variables
x = m.addMVar((N, N), vtype=GRB.BINARY, name="x")
h = m.addMVar(N, vtype=GRB.BINARY, name="h")

# Objective Function
obj = sum(flows[i, j] * x[i, k] * x[j, l] * 
                        (distances[i, k] + 
                        ALPHA * distances[k, l] + 
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

output_name = f"k_{K}_a_{int(ALPHA*100)}.sol"
m.write(f"{output_dir}/{output_name}")

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
