from clustering.p_norm import PNorm
from clustering.vector_calculations import VectorCalculations
from clustering.k_means import KMeans
import sys 

class FastGlobalKMeans:

    def __init__(self,K,error_tolerance=0.001):
        self.K = K
        self.error_tolerance = error_tolerance
    
    def cluster(self,data):
        self.kmeans = KMeans(1,self.error_tolerance)
        self.kmeans.cluster(data)
        last_centroids = self.kmeans.get_centroids()
        for i in range(2, self.K+1):
            next_centroid = self.get_best_next_cluster_centroid(last_centroids, data)
            last_centroids.append(next_centroid)
            self.kmeans = KMeans(i, self.error_tolerance)
            self.kmeans.set_centroids(last_centroids)
            self.kmeans.cluster(data)
            last_centroids = self.kmeans.get_centroids()
        return self.kmeans.get_clusters()

    def get_labels(self):
        return self.kmeans.get_labels()

    def get_clusters(self):
        return self.kmeans.get_clusters()

    def get_centroids(self):
        return self.kmeans.get_centroids()
    
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
            squared_euclidian_dist = VectorCalculations().get_squared_euclidian_distance(xj, closest_centroid)
            squared_p_norm = PNorm(len(xj)).calculate_norm(data_point, xj)**2
            bn += max(squared_euclidian_dist-squared_p_norm, 0)
        return bn
    
    def get_closest_point(self, point, list):
        minimum_dist = sys.float_info.max
        closest_point = None
        for list_element in list:
            dist = PNorm(len(point)).calculate_norm(point, list_element)
            if dist < minimum_dist:
                minimum_dist = dist
                closest_point = list_element
        return closest_point