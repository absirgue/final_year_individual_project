from analysis.conclusion_1.helper import create_floats_list,create_ints_list
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
import sys 

class DBSCANIterator:

    def __init__(self,data):
        self.data = data
        self.NB_ITERATIONS_PER_CONFIG = 1
        self.MIN_EPS = 0.1
        self.MAX_EPS = 10
        self.MIN_MIN_PTS = 1
        self.MAX_MIN_PTS = 30
        self.alg_name = "DBSCAN"
    
    def iterate(self):
        self.silhouette_score_data = []
        self.calinski_harabasz_data = []
        self.clusters_count = []
        eps_values = create_floats_list(self.MIN_EPS,self.MAX_EPS,0.1)
        min_pts_values = create_ints_list(self.MIN_MIN_PTS,self.MAX_MIN_PTS,1)
        eps_values = [2,3]
        for eps in eps_values:
            for min_pts in min_pts_values:
                calinski_harabasz_sum = 0
                silhouette_score_sum = 0
                for i in range(self.NB_ITERATIONS_PER_CONFIG):
                    dbscan = DBSCAN(eps=eps,min_samples=min_pts).fit(self.data)
                    labels = dbscan.labels_
                    clusters_count = len(set(labels)) - (1 if -1 in labels else 0)
                    try:
                        calinski_harabasz_sum+= calinski_harabasz_score(self.data, labels)
                        silhouette_score_sum += silhouette_score(self.data, labels)
                    except:
                        calinski_harabasz_sum = None
                        silhouette_score_sum = None
                self.calinski_harabasz_data.append([eps,min_pts,calinski_harabasz_sum/self.NB_ITERATIONS_PER_CONFIG if calinski_harabasz_sum else None,clusters_count/self.NB_ITERATIONS_PER_CONFIG])
                self.clusters_count.append([eps,min_pts,clusters_count/self.NB_ITERATIONS_PER_CONFIG])
                self.silhouette_score_data.append([eps,min_pts,silhouette_score_sum/self.NB_ITERATIONS_PER_CONFIG if silhouette_score_sum else None,clusters_count/self.NB_ITERATIONS_PER_CONFIG])
        
    def get_optimal(self):
        calinski_best = self.get_values_for_max_measure_value("Calinski Harbasz Index")
        silhouette_best = self.get_values_for_max_measure_value("Silhouette Score")
        return {"Calinski Harbasz Index Optimum":
                {"Eps": calinski_best[0],"MinPts": calinski_best[1],"Calinski Harbasz Index":calinski_best[2],"Number of Clusters":calinski_best[3]},
                "Silhouette Score Optimum":
                {"Eps": silhouette_best[0],"MinPts": silhouette_best[1],"Calinski Harbasz Index":silhouette_best[2],"Number of Clusters":calinski_best[3]},
                }

    def get_values_for_max_measure_value(self,measure_of_interest):
        list = None
        match measure_of_interest:
            case "Silhouette Score":
                list = self.silhouette_score_data
            case "Calinski Harbasz Index":
                list = self.calinski_harabasz_data
        element = self.get_element_with_max_value_at_idx(list,2)
        return element

    def get_element_with_max_value_at_idx(self,list, idx):
        max_value = -10**9
        best_element = None
        for element in list:
            if element[idx]:
                if element[idx] >= max_value:
                    max_value = element[idx]
                    best_element = element
        return best_element

    def get_y_value_for_given_x(self,arr,x_val):
        for point in arr:
            if point[0] == x_val:
                return point[1]
        return None

    def graph(self):
        print(self.silhouette_score_data)
        GraphingHelper().plot_3d_array_of_ponts(self.clusters_count,"Eps","MinPts","Number of Clusters","DBSCAN: Number of clusters across parameters")
        GraphingHelper().plot_3d_array_of_ponts(self.calinski_harabasz_data,"Eps","MinPts","Calinski Harbasz Index","DBSCAN: Calinski-Harabasz Index values across parameters")
        GraphingHelper().plot_3d_array_of_ponts(self.silhouette_score_data,"Eps","MinPts","Silhouette Score","DBSCAN: Silhouette Score values across paramters")