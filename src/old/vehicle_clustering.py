import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import numpy as np
import folium
from folium.plugins import MarkerCluster
import seaborn as sns

from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from collections import Counter

# Read the data
df = pd.read_csv("C:/Users/lyf86/Desktop/vehicle_project/Electric_Vehicle_Population_Data.csv")

# Extract longitude
def extract_longitude(location):
    if isinstance(location, str):
        return float(location.split(' ')[1][1:])
    return None

# Extract latitude
def extract_latitude(location):
    if isinstance(location, str):
        return float(location.split(' ')[2][:-1])
    return None

df['Longitude'] = df['Vehicle Location'].apply(extract_longitude)
df['Latitude'] = df['Vehicle Location'].apply(extract_latitude)

# Filter points within the range of Washington state (WA)
df = df.dropna(subset=['Longitude', 'Latitude'])
df = df[(df['Latitude'] >= 45.5) & (df['Latitude'] <= 49.0) &
        (df['Longitude'] >= -124.0) & (df['Longitude'] <= -116.9)]

# Haversine distance function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth (in kilometers)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Compute latitude and longitude distance matrix
coordinates = df[['Latitude', 'Longitude']].to_numpy()
n_clusters = 20

# Initialize random cluster centers
np.random.seed(42)
initial_centers = coordinates[np.random.choice(coordinates.shape[0], n_clusters, replace=False)]

# Custom implementation of KMeans
for _ in range(100):  # Maximum of 100 iterations
    # Compute distance matrix (Haversine distance)
    distances = np.array([
        [haversine(lat1, lon1, center[0], center[1]) for center in initial_centers]
        for lat1, lon1 in coordinates
    ])
    # Assign each point to the nearest cluster center
    labels = np.argmin(distances, axis=1)
    # Recalculate cluster centers
    new_centers = np.array([
        coordinates[labels == cluster].mean(axis=0) if np.any(labels == cluster) else center
        for cluster, center in enumerate(initial_centers)
    ])
    # Check for convergence
    if np.allclose(initial_centers, new_centers, atol=1e-4):
        break
    initial_centers = new_centers

cluster_centers = initial_centers
df['Cluster'] = labels


# Visualization using a map
mc = MarkerCluster()
map_usa = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()],
                     tiles='cartodbpositron', zoom_start=6)

# Add cluster centers to the map
for i, (lat, lon) in enumerate(cluster_centers):
    print(f"Adding Cluster {i} at location: ({lat}, {lon})")
    mc.add_child(folium.Marker(
        location=[lat, lon],
        popup=f"Cluster {i}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ))

# Add MarkerCluster to the map
map_usa.add_child(mc)

# Create a scatter plot of the clustered points
plt.figure(figsize=(10, 8))
sns.scatterplot(x=df['Longitude'], y=df['Latitude'], hue=df['Cluster'], palette='tab20', s=60, alpha=0.7)

# Plot the cluster centers
for i, (lat, lon) in enumerate(cluster_centers):
    plt.scatter(lon, lat, color='black', s=100, marker='x', label=f"Center {i}" if i == 0 else "")  # Mark the center with black 'x'

# Set the plot labels
plt.title("Clustered Electric Vehicle Locations", fontsize=16)
plt.xlabel("Longitude", fontsize=14)
plt.ylabel("Latitude", fontsize=14)

# Show the legend
plt.legend(title="Clusters")

# Display the plot
plt.show()


# Count the number of each vehicle type in Cluster 10
cluster_10_points = df[df['Cluster'] == 10]
vehicle_counts = Counter(cluster_10_points['Make'])

# Filter data for Tesla vehicles in Cluster 10
tesla_models = cluster_10_points[cluster_10_points['Make'] == 'TESLA']['Model']

# Count the number of different Tesla models
tesla_model_counts = Counter(tesla_models)

# Extract model names and corresponding counts
model_labels, model_values = zip(*tesla_model_counts.items())

# Plot a bar chart
def plot_bar_chart(model_labels, model_values):
    plt.figure(figsize=(10, 6))
    plt.bar(model_labels, model_values, color='skyblue', alpha=0.8)
    plt.xlabel("Tesla Models", fontsize=12)
    plt.ylabel("Number of Vehicles", fontsize=12)
    plt.title("Tesla Model Distribution in Cluster 10", fontsize=14)
    plt.xticks(rotation=45, ha='right')  # Rotate X-axis labels
    plt.tight_layout()
    plt.show()
