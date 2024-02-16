import numpy as np
import random 
from clustering.p_norm import PNorm

class KMeans:

    def __init__(self,K,error_tolerance):
        self.K = K
        self.error_tolerance = error_tolerance
        self.centroids = []
    
    def set_centroids(self, centroids):
        self.centroids = centroids
    
    def cluster(self,data):
        if len(data) < self.K:
            raise ValueError("K can not be greater than the number of data points.")
        self.clusters = None
        self.centroids = []
        self.labels = []
        self.iteration_count = 0
        print(data)
        features_count = data.shape[1]
        if not self.centroids:
            self.initialize_random_cluster_centroids(data)
        prev_centroids = [np.zeros(features_count) for _ in range(self.K)]
        while not np.isclose(self.centroids, prev_centroids, atol=self.error_tolerance).all():
            self.clusters = [[] for _ in range(self.K)]
            for point in data:
                best_cluster_idx = None
                lowest_distance = 10**9
                for cluster_idx, cluster in enumerate(self.centroids):
                    distance = PNorm(features_count).calculate_norm(cluster,point)
                    if distance <lowest_distance:
                        lowest_distance = distance
                        best_cluster_idx = cluster_idx
                self.clusters[best_cluster_idx].append(point)
                self.labels.append(best_cluster_idx)
            prev_centroids = self.centroids
            self.centroids = [np.mean(cluster, axis=0) for cluster in self.clusters]
            for i, centroid in enumerate(self.centroids):
                if np.isnan(centroid).any():
                    self.centroids[i] = prev_centroids[i]
            self.iteration_count += 1
        return self.clusters

    def get_labels(self):
        return self.labels    
     
    def initialize_random_cluster_centroids(self,data):
        while len(self.centroids) < self.K:
            random_cluster_center = data.iloc[random.randint(0,data.shape[0]-1)]
            if not self.is_array_in_2d_array(random_cluster_center,self.centroids):
                self.centroids.append(random_cluster_center)
    
    def is_array_in_2d_array(self,array, twoD_array):
        for row in twoD_array:
            if np.array_equal(array, row):
                return True
        return False

    def get_centroids(self):
        return self.centroids

    def get_clusters(self):
        clean_clusters = []
        for cluster in self.clusters:
            clean_cluster = []
            for element in cluster:
                clean_cluster.append(element[0])
            clean_clusters.append(clean_cluster)
        return self.clusters

    def get_iteration_count(self):
        return self.iteration_count