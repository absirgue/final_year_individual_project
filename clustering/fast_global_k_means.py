from clustering.p_norm import PNorm
from clustering.vector_calculations import VectorCalculations
# from clustering.k_means import KMeans
from sklearn.cluster import KMeans
import sys
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

class FastGlobalKMeans:

    def __init__(self,K,error_tolerance=0.001):
        self.K = K
        self.error_tolerance = error_tolerance
    
    def cluster(self,data):
        if self.K > data.shape[1]:
            raise ValueError()
        self.k_means = KMeans(n_clusters=1,n_init=1)
        self.k_means.fit(data)
        self.centroids = self.k_means.cluster_centers_
        self.labels = self.k_means.labels_
        for i in range(2, self.K+1):
            next_centroid = self.get_best_next_cluster_centroid(self.centroids, data)
            self.centroids = np.append(self.centroids,[np.array(next_centroid)],axis=0)
            self.k_means = KMeans(n_clusters=i, init=self.centroids, n_init=1)
            self.k_means.fit(data)
            self.centroids = self.k_means.cluster_centers_
            self.labels = self.k_means.labels_
        return self.get_labels()
    
    def get_labels(self):
        return self.labels

    def get_centroids(self):
        return self.centroids
    
    def get_best_next_cluster_centroid(self,last_cluster_centroids,data):
        max_bn = sys.float_info.min
        best_point = None
        for data_point in data:
            bn = self.calculate_bn(data_point, data,last_cluster_centroids)
            if bn > max_bn:
                max_bn = bn
                best_point = data_point
        return best_point
    
    def calculate_bn(self, data_point,data,last_cluster_centroids):
        closest_centroid = self.get_closest_point(data_point,last_cluster_centroids)
        bn = 0
        for xj in data:
            squared_euclidian_dist = np.linalg.norm(xj - closest_centroid)**2
            squared_p_norm = np.linalg.norm(data_point - xj, ord=len(xj))**2
            bn += max(squared_euclidian_dist-squared_p_norm, 0)
        return bn
    
    def get_closest_point(self, point, list):
        minimum_dist = sys.float_info.max
        closest_point = None
        for list_element in list:
            dist = np.linalg.norm(point - list_element)
            if dist < minimum_dist:
                minimum_dist = dist
                closest_point = list_element
        return closest_point