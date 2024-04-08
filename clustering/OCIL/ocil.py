from clustering.OCIL.cluster import Cluster
import random
import math 
import pandas as pd
class OCIL:
    """
    Reference implementation of OCIL for experimentation purposes.
    We will not study this algorithm further.
    """
    
    def __init__(self,K):
        self.K = K
        
    def cluster(self,data):
        self.initialization(data)
        noChange = False
        while not noChange:
            noChange = True
            for index, data_point in self.data.iterrows():
                best_cluster_idx = self.get_max_similarity_cluster_idx(self,data_point)
                if best_cluster_idx != self.Y[index]:
                    noChange = False
                    self.clusters[best_cluster_idx].add_point(self.get_categorical_values_for_point(data_point),self.get_numerical_values_for_point(data_point))
                    if self.Y[index]:
                        self.clusters[self.Y[index]].remove_point(self.get_categorical_values_for_point(data_point),self.get_numerical_values_for_point(data_point))
        return self.Y
    
    def initialization(self,data):
        self.data,self.categorical_data_count = self.organise_data_by_type(data)
        self.intialize_clusters(self.K)
        self.compute_categorical_attributes_importance()
        self.Y = [None]*self.data.shape[0]

    def get_max_similarity_cluster_idx(self, data_point):
        max_similarity = 0
        best_cluster_idx = None
        for cluster_idx, cluster in enumerate(self.clusters):
            similarity = self.get_cluster_point_similarity(cluster,data_point)
            # >= because it is possible that the best similarity is 0
            if similarity >= max_similarity:
                best_cluster_idx = cluster_idx
        return best_cluster_idx

    def compute_categorical_attributes_importance(self):
        H_ar_ordered_list = []
        H_ar_sum = 0
        for col_idx in range(self.categorical_data_count):
            categorical_attribute_values = self.data.iloc[:, col_idx]
            H_ar = self.compute_categorical_attribute_H_ar(categorical_attribute_values)
            H_ar_ordered_list.append(H_ar)
            H_ar_sum += H_ar
        self.categorical_attributes_importance = [] 
        for H_ar in H_ar_ordered_list:
            self.categorical_attributes_importance.append(H_ar/H_ar_sum)
    
    def compute_categorical_attribute_H_ar(self, attribute_values):
        m_r = attribute_values.nunique()
        sigma_not_null = self.get_count_non_null_values(attribute_values)
        sum = 0
        considered_values = []
        for value in attribute_values:
            if value and value != "" and not (value in considered_values):
                sigma_equal_value = attribute_values.value_counts().get(value, 0)
                p_a_rt = sigma_equal_value/sigma_not_null
                # ln is used, but this changes nothing for validity of our relative entropy study.
                sum += p_a_rt*math.log(p_a_rt)
                considered_values.append(value)
        return (-1/m_r)*sum


    def get_count_non_null_values(self, column):
        non_null_values = column[column.notnull() & (column != "")]
        return len(non_null_values)

    def get_cluster_point_similarity(self,cluster, data_point):
        similarity_on_categorical_attributes = self.get_cluster_point_similarity_on_categorical_attributes(cluster, data_point)
        similarity_on_numerical_attributes = self.get_cluster_point_similarity_on_numerical_attributes(cluster,data_point)
        similarity = 0 
        if similarity_on_categorical_attributes:
            similarity += (self.categorical_data_count/(self.categorical_data_count+1)) * similarity_on_categorical_attributes
        if similarity_on_numerical_attributes:
            similarity += (1/(self.categorical_data_count+1))*similarity_on_numerical_attributes
        return similarity
    
    def get_cluster_point_similarity_on_categorical_attributes(self,cluster, data_point):
        if self.categorical_data_count>0:
            similarity = 0
            for i in range(self.categorical_data_count):
                similarity += self.categorical_attributes_importance[i] * cluster.get_similarity_for_categorical_attribute(i,data_point[i])
            return similarity
        else:
            return 0

    def get_cluster_point_similarity_on_numerical_attributes(self, cluster, data_point):
        if self.categorical_data_count < len(data_point):
            sum_of_similarities_to_all_clusters = 0
            numerical_attributes_vector = self.get_numerical_values_for_point(data_point)
            for cluster_i in self.clusters:
                sum_of_similarities_to_all_clusters+= cluster_i.get_exp_difference_for_numerical_attributes(numerical_attributes_vector)
            return cluster.get_exp_difference_for_numerical_attributes(numerical_attributes_vector)/sum_of_similarities_to_all_clusters
        else:
            return 0

    def intialize_clusters(self,K):
        self.clusters = []
        idx_points_used = []
        for i in range(K):
            cluster = Cluster(self.categorical_data_count)
            pointFound = False
            while not pointFound:
                idx_first_point = random.randint(0, self.data.shape[0]-1)
                if not(idx_first_point in idx_points_used):
                    pointFound = True
            cluster.add_point(self.get_categorical_values_for_point(self.data.iloc[idx_first_point]),self.get_numerical_values_for_point(self.data.iloc[idx_first_point]))
            self.clusters.append(cluster)
    
    def get_categorical_values_for_point(self,row):
        if isinstance(row,pd.DataFrame):
            return row[:self.categorical_data_count].values
        return row[:self.categorical_data_count]
    
    def get_numerical_values_for_point(self,row):
        if isinstance(row,pd.DataFrame):
            return row[self.categorical_data_count:].values
        return row[self.categorical_data_count:]

    def organise_data_by_type(self,data):
        if isinstance(data, pd.DataFrame):
            categorical_columns = data.select_dtypes(include='object').columns
            numerical_columns = data.select_dtypes(exclude='object').columns
            organized_columns = list(categorical_columns) + list(numerical_columns)
            df_organized = data[organized_columns]
            return df_organized, len(categorical_columns)
        return 0,None

    def get_clusters(self):
        clusters = [[]*self.K]
        for data_point_idx, data_point_cluster_idx in enumerate(self.Y):
            clusters[data_point_cluster_idx].append(self.iloc[data_point_idx])
        return clusters
