# -*- coding: utf-8 -*-
"""Prodigy_Machine Learning_2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qt7GnvIUcHPmFN7DBJVbawcUeAfRlsfH
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Load data
data = pd.read_csv('/content/Mall_Customers.csv')
data

# Check for null values
print("Null Values:")
print(data.isnull().sum())

# Descriptive statistics
print("Descriptive Statistics:")
print(data.describe())

# Explore unique values in 'Spending Score (1-100)' and 'Annual Income (k$)'
print("Unique Values in Spending Score:")
print(data['Spending Score (1-100)'].value_counts().unique())

print("Value Counts for Annual Income:")
print(data['Annual Income (k$)'].value_counts())

# Select relevant features for clustering
features = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
X = data[features]

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize K-means clustering algorithm
num_clusters = 5
kmeans = KMeans(n_clusters=num_clusters, random_state=42)

# Fit model to scaled data
kmeans.fit(X_scaled)
# Add cluster labels to the original DataFrame
data['Cluster'] = kmeans.labels_

# Visualize clusters
plt.scatter(data['Annual Income (k$)'], data['Spending Score (1-100)'], c=data['Cluster'], cmap='rainbow')
plt.xlabel('Annual Income')
plt.ylabel('Spending Score (1-100)')
plt.title('K-means Clustering of Customers')
plt.show()

# Print cluster centers
cluster_centers_scaled = kmeans.cluster_centers_
print("Cluster Centers (Scaled):")
print(cluster_centers_scaled)
cluster_centers_original = scaler.inverse_transform(cluster_centers_scaled)
print("Cluster Centers (Original):")
print(cluster_centers_original)

# Visualize cluster profiles
for cluster_id in range(num_clusters):
    cluster_data = data[data['Cluster'] == cluster_id]
    plt.scatter(cluster_data['Annual Income (k$)'], cluster_data['Spending Score (1-100)'], label=f'Cluster {cluster_id}')

plt.xlabel('Annual Income')
plt.ylabel('Spending Score (1-100)')
plt.title('Cluster Profiles')
plt.legend()
plt.show()

# Box plots for each feature within each cluster
for feature in features:
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='Cluster', y=feature, data=data)
    plt.title(f'Box Plot of {feature} by Cluster')
    plt.show()

# Pair plot colored by cluster
sns.pairplot(data=data, hue='Cluster', diag_kind='kde')
plt.title('Pair Plot Colored by Cluster')
plt.show()

# Distribution plots for each feature within each cluster
for feature in features:
    plt.figure(figsize=(8, 6))
    for cluster_id in range(num_clusters):
        cluster_data = data[data['Cluster'] == cluster_id]
        sns.histplot(cluster_data[feature], label=f'Cluster {cluster_id}', kde=True)
    plt.title(f'Distribution of {feature} by Cluster')
    plt.legend()
    plt.show()