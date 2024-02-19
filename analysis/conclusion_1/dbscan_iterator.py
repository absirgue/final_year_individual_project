from analysis.conclusion_1.helper import create_floats_list,create_ints_list
from sklearn.cluster import DBSCAN
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
import sys 
import time
from analysis.conclusion_1.list_analyser import ListAnalyser
from analysis.conclusion_1.list_transformations import ListTransformations
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
        self.performance_data = []
        eps_values = create_floats_list(self.MIN_EPS,self.MAX_EPS,0.1)
        min_pts_values = create_ints_list(self.MIN_MIN_PTS,self.MAX_MIN_PTS,1)
        eps_values = [2,3]
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
                        calinski_harabasz_sum+= calinski_harabasz_score(self.data, labels)
                        silhouette_score_sum += silhouette_score(self.data, labels)
                    except:
                        calinski_harabasz_sum = None
                        silhouette_score_sum = None
                self.performance_data.append({"eps":eps,"min pts":min_pts,"calinski harabasz index":calinski_harabasz_sum/self.NB_ITERATIONS_PER_CONFIG if calinski_harabasz_sum else None,"silhouette score":silhouette_score_sum/self.NB_ITERATIONS_PER_CONFIG if silhouette_score_sum else None,"cluster counts":clusters_count/self.NB_ITERATIONS_PER_CONFIG,"time":time_sum/self.NB_ITERATIONS_PER_CONFIG})
        return self.get_optimal()
    
    def get_optimal(self):
        calinski_best = ListAnalyser().get_values_for_max_measure_value(self.performance_data,"calinski harabasz index")
        silhouette_best = ListAnalyser().get_values_for_max_measure_value(self.performance_data,"silhouette score")
        return {"Calinski Harbasz Index Optimum":
                {"Eps": calinski_best["eps"],"MinPts": calinski_best["min pts"],"Calinski Harbasz Index":calinski_best["calinski harabasz index"],"Number of Clusters":calinski_best["cluster counts"],"Time":calinski_best["time"]},
                "Silhouette Score Optimum":
                {"Eps": silhouette_best["eps"],"MinPts": silhouette_best["min pts"],"Silhouette Score":silhouette_best["silhouette score"],"Number of Clusters":calinski_best["cluster counts"],"Running Time":calinski_best["time"]},
                }

    def get_y_value_for_given_x(self,arr,x_val):
        for point in arr:
            if point[0] == x_val:
                return point[1]
        return None

    def graph(self,folder_name):
        GraphingHelper().plot_3d_array_of_ponts(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","cluster counts"),"Eps","MinPts","Number of Clusters","DBSCAN: Number of clusters across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_ponts(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","calinski harabasz index"),"Eps","MinPts","Calinski Harbasz Index","DBSCAN: Calinski-Harabasz Index values across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_ponts(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","silhouette score"),"Eps","MinPts","Silhouette Score","DBSCAN: Silhouette Score values across parameters",folder_name)
        GraphingHelper().plot_3d_array_of_ponts(ListTransformations().extract_3d_list_from_list_of_dics(self.performance_data,"eps","min pts","time"),"Eps","MinPts","Running Time","DBSCAN: Running time across paramters",folder_name)