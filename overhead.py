# flake8: noqa

import numpy as np
from data_loader import load_data, load_solution
import matplotlib.pyplot as plt

# Hyperparameters
cities_file = "data/cities_small.csv"
packages_file = "data/packages_small.csv"

# Load the data
N, flows, distances = load_data(cities_file, packages_file)
total_packages = np.sum(flows)

def count_transfers(solution_file):
    hubs, connections = load_solution(solution_file)
    num_transfers = 0
    for i in range(len(flows)):
        for j in range(len(flows)):
            if flows[i, j] > 0:
                if connections[i][1] not in [i, j]:
                    num_transfers += flows[i, j]
                if connections[j][1] not in [i, j]:
                    num_transfers += flows[i, j]
    return num_transfers

costs = []
K = [1, 2, 4, 6]
for i in K:
    num_transfers = count_transfers(f"output/k_{i}_a_75.sol")
    print(f"{num_transfers / total_packages} * c per package for k = {i}")
    costs.append(num_transfers)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(K, costs, '-s', color='blue', label='Total Overhead Cost (* c)', markerfacecolor='white', markersize=8, markeredgewidth=2, markeredgecolor='blue', alpha=0.75)
ax.set_xlabel('Number of Hubs (K)')
ax.set_ylabel('Total Overhead Cost (* c)')
ax.set_title('Total Overhead Cost vs. Number of Hubs')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(loc='upper right')

# Show the plot
plt.tight_layout()
plt.show()