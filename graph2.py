# flake8: noqa

import matplotlib.pyplot as plt

# Data
number_of_hubs = [1, 2, 4, 6]
total_distance = [1.8327569109521568e+07, 1.3531340148177857e+07, 1.0904054497059487e+07, 8964540.32239324]

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(number_of_hubs, total_distance, '-s', color='blue', label='Total Distance', markerfacecolor='white', markersize=8, markeredgewidth=2, markeredgecolor='blue', alpha=0.75)
ax.set_xlabel('Number of Hubs (K)')
ax.set_ylabel('Total Distance Traveled')
ax.set_title('Total Distance Traveled vs. Number of Hubs')
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend(loc='upper right')

# Show the plot
plt.tight_layout()
plt.show()
