import numpy as np
from sklearn.metrics.pairwise import pairwise_distances

class WCSS:

    def compute_wcss(self, labels, centroids):
        wcss = 0
        unique_labels = np.unique(labels)

        for label in unique_labels:
            cluster_points = data[np.array(labels) == label]
            centroid = centroids[label]

            # Calculate squared distances within the cluster
            cluster_distances = pairwise_distances(cluster_points, [centroid], metric='euclidean')**2
            wcss += np.sum(cluster_distances)