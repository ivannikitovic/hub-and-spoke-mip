# flake8: noqa

import matplotlib.pyplot as plt
import pandas as pd

# Hyperparameters
solution_file = "output/k_2_a_75.sol"
cities_file = "data/cities_small.csv"

# 1. Extract data from example.sol
hubs = {}
connections = []
with open(solution_file, 'r') as file:
    for line in file:
        if line.startswith("h["):
            node, val = line.split()
            node_idx = int(node.split('[')[1].split(']')[0])
            hubs[node_idx] = int(val)
        elif line.startswith("x["):
            nodes, val = line.split()
            start_node, end_node = [int(idx) for idx in nodes.split('[')[1].split(']')[0].split(',')]
            if int(val) == 1:
                connections.append((start_node, end_node))

# 2. Extract data from .csv file
df = pd.read_csv(cities_file)

# 3. Plotting
plt.figure(figsize=(10, 10))
for i, row in df.iterrows():
    # Plot hubs as green stars and spokes as blue circles
    color = 'g' if hubs[row['id']] == 1 else 'b'
    marker = '*' if hubs[row['id']] == 1 else 'o'
    size = 1500 if hubs[row['id']] == 1 else 500
    plt.scatter(row['lon'], row['lat'], c=color, marker=marker, s=size)
    plt.text(row['lon'] + 2, row['lat'], str(int(row['id'])), va='center', fontsize=16, color='black')

for connection in connections:
    start = df.loc[connection[0]]
    end = df.loc[connection[1]]
    plt.plot([start['lon'], end['lon']], [start['lat'], end['lat']], 'r-')

# Add dummy points for legend
plt.scatter([], [], c='g', marker='*', s=150, label='Hub Node')
plt.scatter([], [], c='b', marker='o', s=50, label='Spoke Node')

plt.title('Hub and Spoke Model')
plt.xlabel('Longitude (x)')
plt.ylabel('Latitude (y)')
plt.grid(True)
plt.legend()
plt.show()
