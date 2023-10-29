import pandas as pd
from math import sqrt
import numpy as np


def euclidean_distance(lat1, lon1, lat2, lon2):
    return sqrt((lon2 - lon1)**2 + (lat2 - lat1)**2)


def load_data(city_file, package_file):
    cities_df = pd.read_csv(city_file)
    packages_df = pd.read_csv(package_file)

    N = len(cities_df)

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

    return N, flows, distances


def load_solution(solution_file):
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

    return hubs, connections
