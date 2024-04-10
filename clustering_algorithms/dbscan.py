from clustering_algorithms.p_norm import PNorm

class DBSCAN:
    """
    Reference implementation of DBSCAN for experimentation purposes.

    It is not optimal in terms of run time and is therefore not used in our research.
    """
    def __init__(self, data, eps=0.5, Minpts=5):
        self.eps = eps
        self.Minpts = Minpts
        self.data = data
        self.cluster_labels = DBSCANClusterLabelsList(len(data))

    def cluster(self):
        current_cluster_count = 1
        for data_point_idx in range(len(self.data)):
            if self.cluster_labels.get_label(data_point_idx) == 0:
                idx_of_neighboring_points = self.get_indexes_of_points_in_region(self.data[data_point_idx])
                if len(idx_of_neighboring_points) < self.Minpts:
                    self.cluster_labels.set_label(data_point_idx, -1)
                else:
                    self.expand_cluster(data_point_idx, idx_of_neighboring_points, current_cluster_count)
                    current_cluster_count += 1
        return current_cluster_count - 1

    def expand_cluster(self, source_idx, neighbors_idxs, cluster_nb):
        self.cluster_labels.set_label(source_idx,cluster_nb)
        i = 0
        while i < len(neighbors_idxs):    
            current_idx = neighbors_idxs[i]
            if self.cluster_labels.get_label(current_idx) == -1:
                self.cluster_labels.set_label(current_idx,cluster_nb)
            elif self.cluster_labels.get_label(current_idx) == 0:
                self.cluster_labels.set_label(current_idx,cluster_nb)
                neighbors_of_neighbor = self.get_indexes_of_points_in_region(self.data[current_idx])
                if len(neighbors_of_neighbor) >= self.Minpts:
                    neighbors_idxs = neighbors_idxs + neighbors_of_neighbor
            i += 1        
    
    def get_indexes_of_points_in_region(self, data_point):
        neighbors = []
        for point_idx in range(len(self.data)):
            if PNorm(len(data_point)).calculate_norm(data_point,self.data[point_idx]) < self.eps:
                neighbors.append(point_idx)
        return neighbors


class DBSCANClusterLabelsList:

    def __init__(self, length):
        self.labels = [0]*length

    def get_label(self, index):
        return self.labels[index]

    def set_label(self,index, value):
        self.labels[index] = value