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

def count_distance(solution_file):
    hubs, connections = load_solution(solution_file)
    total_distance = 0
    for i in range(len(flows)):
        for j in range(len(flows)):
            if flows[i, j] > 0:
                total_distance += flows[i, j] * (distances[i, connections[i][1]] + distances[connections[i][1], connections[j][1]] + distances[j, connections[j][1]])
    return total_distance

total_distances = []
C = [0, 10, 20, 30, 50, 100]
for i in C:
    total_distance = count_distance(f"output/k_2_a_75_c_{i}.sol")
    print(f"{total_distance} for C = {i}")
    total_distances.append(total_distance)

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(C, total_distances, '-s', color='blue', label='Total Distance Traveled', markerfacecolor='white', markersize=8, markeredgewidth=2, markeredgecolor='blue', alpha=0.75)
ax.set_xlabel('Intermediate Cost (C)')
ax.set_ylabel('Total Distance Traveled')
ax.set_title('Total Distance Traveled vs. Intermediate Cost (C)')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(loc='lower right')

# Show the plot
plt.tight_layout()
plt.show()