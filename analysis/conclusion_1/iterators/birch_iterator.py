import time
from analysis.conclusion_1.helper import create_floats_list,create_ints_list
from sklearn.cluster import Birch
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.conclusion_1.list_transformations import ListTransformations
from analysis.conclusion_1.list_analyser import ListAnalyser

class BIRCHIterator:

    def __init__(self,data,number_of_clusters):
        self.performance_data = []
        self.data = data
        self.NB_ITERATIONS_PER_CONFIG = 1
        self.CLUSTERS_COUNT = number_of_clusters
        self.MIN_BRANCHING_FACTOR = 2
        self.MAX_BRANCHING_FACTOR = 65
        self.MIN_THRESHOLD = 0.1
        self.MAX_THRESHOLD = 10
        self.alg_name = "BIRCH for "+str(number_of_clusters)+" clusters"
    
    def iterate(self):
        self.performance_data = []
        branching_factor_values = create_ints_list(self.MIN_BRANCHING_FACTOR,self.MAX_BRANCHING_FACTOR,5)
        threshold_values = create_floats_list(self.MIN_THRESHOLD,self.MAX_THRESHOLD,0.25)
        for threshold in threshold_values:
            for branching_factor in branching_factor_values:
                calinski_harabasz_sum = 0
                silhouette_score_sum = 0
                time_sum = 0
                for i in range(self.NB_ITERATIONS_PER_CONFIG):
                    start_time = time.time()
                    birch = Birch(threshold=threshold, branching_factor=branching_factor, n_clusters=self.CLUSTERS_COUNT).fit(self.data)
                    end_time = time.time()
                    time_sum += (end_time - start_time)
                    labels = birch.labels_
                    try:
                        calinski_harabasz_sum+= calinski_harabasz_score(self.data, labels)
                        silhouette_score_sum += silhouette_score(self.data, labels)
                    except:
                        calinski_harabasz_sum = 0
                        silhouette_score_sum = 0
                self.performance_data.append({"threshold":threshold,"branching factor":branching_factor,"Calinski Harabasz Index":calinski_harabasz_sum/self.NB_ITERATIONS_PER_CONFIG,"Silhouette Score":silhouette_score_sum/self.NB_ITERATIONS_PER_CONFIG,"time":time_sum/self.NB_ITERATIONS_PER_CONFIG})
        return self.get_optimal()

    def get_optimal(self):
        if not self.performance_data:
            return None
        calinski_best = ListAnalyser().get_values_for_max_measure_value(self.performance_data,"Calinski Harabasz Index")
        silhouette_best = ListAnalyser().get_values_for_max_measure_value(self.performance_data,"Silhouette Score")
        optimums = {}
        if calinski_best:
            optimums["Calinski Harabasz Index Optimum"] =  {"Threshold Value": calinski_best["threshold"],"Branching Factor": calinski_best["branching factor"],"Calinski Harabasz Index":calinski_best["Calinski Harabasz Index"],"Time":calinski_best["time"]}
        if silhouette_best:
            optimums["Silhouette Score Optimum"] = {"Threshold Value": silhouette_best["threshold"],"Branching Factor": silhouette_best["branching factor"],"Silhouette Score":silhouette_best["Silhouette Score"],"Time":silhouette_best["time"]}
        return optimums

    def graph(self,folder_name=None):
        GraphingHelper().plot_3d_array_of_points(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"threshold","branching factor","Calinski Harabasz Index"),"Threshold","Branching Factor","Calinski Harabasz Index","BIRCH: Calinski-Harabasz Index values across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_points(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"threshold","branching factor","Silhouette Score"),"Threshold","Branching Factor","Silhouette Score","BIRCH: Silhouette Score values across parameters",folder_name)