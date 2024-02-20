from analysis.conclusion_1.helper import create_ints_list
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
import time
from skfuzzy.cluster import cmeans
import numpy as np 
from analysis.conclusion_1.list_transformations import ListTransformations
class FuzzyCMeansIterator:

    def __init__(self,data,max_nb_of__clusters = None):
        self.data = data
        self.NB_ITERATINS_PER_CONFIG = 5
        self.MIN_C_TO_TEST = 2
        self.MAX_C_TO_TEST = int(self.data.shape[0])
        self.M = 2
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_C_TO_TEST = max_nb_of__clusters
        self.alg_name = "Fuzzy C-Means"
    
    def iterate(self):
        self.performance_data = []
        c_values = create_ints_list(self.MIN_C_TO_TEST,self.MAX_C_TO_TEST,1)
        for C in c_values:
            wcss_sum = 0
            calinski_harabasz_sum = 0
            silhouette_score_sum = 0
            time_sum = 0
            for i in range(self.NB_ITERATINS_PER_CONFIG):
                cntr, u, _, _, _, _, _ = cmeans(self.data.T, c=C, m=self.M,error=0.001,maxiter=400)
                try:
                    start_time = time.time()
                    fuzzy_cluster_labels = np.argmax(u, axis=0)
                    end_time = time.time()
                    time_sum += (end_time-start_time)
                    calinski_harabasz_sum+= calinski_harabasz_score(self.data, fuzzy_cluster_labels)
                    silhouette_score_sum += silhouette_score(self.data, fuzzy_cluster_labels)
                    wcss_sum += np.sum(np.power(np.linalg.norm(self.data.T - cntr.T[:, fuzzy_cluster_labels], axis=1), 2))
                except Exception as e:
                    calinski_harabasz_sum += 0
                    silhouette_score_sum += 0
            self.performance_data.append({"C":C,"calinski harabasz index":calinski_harabasz_sum/self.NB_ITERATINS_PER_CONFIG,"time":time_sum/self.NB_ITERATINS_PER_CONFIG,"silhouette score":silhouette_score_sum/self.NB_ITERATINS_PER_CONFIG,"wcss":wcss_sum/self.NB_ITERATINS_PER_CONFIG})
        return self.get_optimal()
    
    def get_performance_on_given_C(self, C):
        for perf_data in self.performance_data:
            if perf_data["C"] == C:
                return perf_data
    
    def get_optimal(self):
        wcss_inflection_points = FunctionAnalysis().get_inflection_points_from_x_y_2d_array(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","wcss"))
        optimal_point = wcss_inflection_points[0]
        optimal_point = self.find_perf_entry_for_given_C(optimal_point[0])
        return {"C":optimal_point["C"],"WCSS":optimal_point["wcss"],"Silhouette Score": optimal_point["calinski harabasz index"],"Running Time":optimal_point["time"],"Calinski Harbasz Index":optimal_point["calinski harabasz index"]}

    def find_perf_entry_for_given_C(self, C_val):
        for element in self.performance_data:
            if element["C"] == C_val:
                return element
        return None
    
    def graph(self,folder_name):
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","calinski harabasz index"),"C value","Calinski-Harabasz Index","Fuzzy C-Means: Calinski-Harabasz Index values across C values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","silhouette score"),"C value","Silhouette Score","Fuzzy C-Means: Silhouette Score values across C values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","wcss"),"C value","WCSS","Fuzzy C-Means: WCSS values across C values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","time"),"C value","Running Time","Fuzzy C-Means: Running time across C values",folder_name)


