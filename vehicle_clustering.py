import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter
import matplotlib.pyplot as plt

df = pd.read_csv("./Electric_Vehicle_Population_Data.csv")

def extract_longitude(location):
    if isinstance(location, str):
        return float(location.split(' ')[1][1:])
    return None

def extract_latitude(location):
    if isinstance(location, str):
        return float(location.split(' ')[2][:-1])
    return None

df['Longitude'] = df['Vehicle Location'].apply(extract_longitude)
df['Latitude'] = df['Vehicle Location'].apply(extract_latitude)

df = df.dropna(subset=['Longitude', 'Latitude'])

n_clusters = 20
kmeans = KMeans(n_clusters=n_clusters)
df['Cluster'] = kmeans.fit_predict(df[['Longitude', 'Latitude']])

cluster_brand_counts = df.groupby('Cluster')['Make'].apply(list).apply(Counter)

cluster_centers = kmeans.cluster_centers_

plt.figure(figsize=(12, 8))

for i, center in enumerate(cluster_centers):
    plt.scatter(center[0], center[1], label=f'Cluster {i}')

legend_texts = []
for cluster in range(n_clusters):
    max_percentage_brand = max(cluster_brand_counts[cluster], key=cluster_brand_counts[cluster].get)
    max_percentage_value = cluster_brand_counts[cluster][max_percentage_brand] / sum(cluster_brand_counts[cluster].values())

    legend_texts.append(f'Cluster {cluster}: {max_percentage_brand} ({max_percentage_value:.2%})')

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Cluster Distribution with Dominant Brand')
plt.legend(legend_texts)
plt.savefig("cluster_distribution.png")
plt.show()