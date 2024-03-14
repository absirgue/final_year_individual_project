import sys 
import time
from analysis.conclusion_1.helper import create_floats_list,create_ints_list
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.conclusion_1.list_analyser import ListAnalyser
from analysis.conclusion_1.list_transformations import ListTransformations
from interface_beautifier import InterfaceBeautifier
class DBSCANIterator:

    def __init__(self,data):
        self.performance_data = []
        self.data = data
        self.NB_ITERATIONS_PER_CONFIG = 1
        self.MIN_EPS = 0.1
        self.MAX_EPS = 90
        self.MIN_MIN_PTS = 1
        self.MAX_MIN_PTS = 30
        self.alg_name = "DBSCAN"
    
    def iterate(self):
        self.performance_data = []
        eps_values = create_floats_list(self.MIN_EPS,self.MAX_EPS,0.5)
        min_pts_values = create_ints_list(self.MIN_MIN_PTS,self.MAX_MIN_PTS,1)
        for eps in eps_values:
            for min_pts in min_pts_values:
                calinski_harabasz_sum = 0
                silhouette_score_sum = 0
                time_sum = 0
                for i in range(self.NB_ITERATIONS_PER_CONFIG):
                    start_time = time.time()
                    dbscan = DBSCAN(eps=eps,min_samples=min_pts).fit(self.data)
                    end_time = time.time()
                    time_sum += (end_time-start_time)
                    labels = dbscan.labels_
                    clusters_count = len(set(labels)) - (1 if -1 in labels else 0)
                    try:
                        calinski_harabasz_sum += calinski_harabasz_score(self.data, labels)
                        silhouette_score_sum += silhouette_score(self.data, labels)
                    except Exception as e:
                        calinski_harabasz_sum = None
                        silhouette_score_sum = None
                self.performance_data.append({"eps":eps,"min pts":min_pts,"Calinski Harabasz Index":round(calinski_harabasz_sum/self.NB_ITERATIONS_PER_CONFIG,3) if calinski_harabasz_sum else None,"Silhouette Score":round(silhouette_score_sum/self.NB_ITERATIONS_PER_CONFIG,3) if silhouette_score_sum else None,"cluster counts":clusters_count/self.NB_ITERATIONS_PER_CONFIG,"time":round(time_sum/self.NB_ITERATIONS_PER_CONFIG,6)})
            InterfaceBeautifier().print_percentage_progress("Progress on DSCAN Hyperparameters Optimization",(eps_values.index(eps)+1)*100/len(eps_values))
        return self.get_optimal()
    
    def get_performance_on_given_K(self, K):
        for perf_data in self.performance_data:
            if perf_data["cluster counts"] == K:
                return perf_data
        return None

    def get_optimal(self):
        if not self.performance_data:
            return None
        calinski_best = ListAnalyser().get_values_for_max_measure_value(self.performance_data,"Calinski Harabasz Index")
        silhouette_best = ListAnalyser().get_values_for_max_measure_value(self.performance_data,"Silhouette Score")
        optimums = {}
        if calinski_best:
            optimums["Calinski Harabasz Index Optimum"] =  {"Eps": calinski_best["eps"],"MinPts": calinski_best["min pts"],"Calinski Harabasz Index":calinski_best["Calinski Harabasz Index"],"Number of Clusters":calinski_best["cluster counts"],"Time":calinski_best["time"]}
        if silhouette_best:
            optimums["Silhouette Score Optimum"] = {"Eps": silhouette_best["eps"],"MinPts": silhouette_best["min pts"],"Silhouette Score":silhouette_best["Silhouette Score"],"Number of Clusters":silhouette_best["cluster counts"],"Running Time":silhouette_best["time"]}
        return optimums

    def get_y_value_for_given_x(self,arr,x_val):
        for point in arr:
            if point[0] == x_val:
                return point[1]
        return None

    def graph(self,folder_name=None):
        GraphingHelper().plot_3d_array_of_points(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","cluster counts"),"Eps","MinPts","Number of Clusters","DBSCAN: Number of clusters across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_points(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","Calinski Harabasz Index"),"Eps","MinPts","Calinski Harabasz Index","DBSCAN: Calinski-Harabasz Index values across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_points(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","Silhouette Score"),"Eps","MinPts","Silhouette Score","DBSCAN: Silhouette Score values across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_points(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","time"),"Eps","MinPts","Running Time","DBSCAN: Running time across paramters",folder_name)