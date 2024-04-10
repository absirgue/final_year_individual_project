import time
import numpy as np 
from analysis.hyperparameters_optimisation.helper import create_ints_list
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
from skfuzzy.cluster import cmeans
from analysis.hyperparameters_optimisation.list_transformations import ListTransformations
from interface_beautifier import InterfaceBeautifier
class FuzzyCMeansIterator:
    """
    Coordinates all actions required to identify the optimal C value for Fuzzy C-Means to 
    perform optimally on a given data set.
    """

    def __init__(self,data,max_nb_of__clusters = None,nb_iterations=5):
        self.performance_data = []
        self.data = data
        self.NB_ITERATIONS_PER_CONFIG = nb_iterations
        self.MIN_C_TO_TEST = 2
        self.MAX_C_TO_TEST = int(self.data.shape[0])
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_C_TO_TEST = max_nb_of__clusters
        self.alg_name = "Fuzzy C-Means"
    
    def iterate(self):
        self.performance_data = []
        c_values = create_ints_list(self.MIN_C_TO_TEST,self.MAX_C_TO_TEST,1)
        for C in c_values:
            WCSS_sum = 0
            calinski_harabasz_sum = 0
            silhouette_score_sum = 0
            time_sum = 0
            for i in range(self.NB_ITERATIONS_PER_CONFIG):
                start_time = time.time()
                cntr, u, _, _, _, _, _ = cmeans(self.data.T, c=C, m=2,error=0.001,maxiter=400)
                end_time = time.time()
                time_sum += (end_time-start_time)
                try:
                    fuzzy_cluster_labels = np.argmax(u, axis=0)
                    calinski_harabasz_sum+= calinski_harabasz_score(self.data, fuzzy_cluster_labels)
                    silhouette_score_sum += silhouette_score(self.data, fuzzy_cluster_labels)
                    WCSS_sum += np.sum(np.power(np.linalg.norm(self.data.T - cntr.T[:, fuzzy_cluster_labels], axis=1), 2))
                except Exception as e:
                    calinski_harabasz_sum += 0
                    silhouette_score_sum += 0
            self.performance_data.append({"C":C,"Calinski Harabasz Index":calinski_harabasz_sum/self.NB_ITERATIONS_PER_CONFIG,"time":time_sum/self.NB_ITERATIONS_PER_CONFIG,"Silhouette Score":silhouette_score_sum/self.NB_ITERATIONS_PER_CONFIG,"WCSS":WCSS_sum/self.NB_ITERATIONS_PER_CONFIG})
            InterfaceBeautifier().print_percentage_progress("Progress on Fuzzy C-Means Hyperparameters Optimization",(c_values.index(C)+1)*100/len(c_values))
        return self.get_optimal()
    
    def get_performance_on_given_K(self, C):
        for perf_data in self.performance_data:
            if perf_data["C"] == C:
                return perf_data
    
    def get_optimal(self):
        if not self.performance_data:
            return None
        elif len(self.performance_data) <2:
            return self.performance_data[0]
        else:
            WCSS_elbow_point = FunctionAnalysis().get_elbow_point_from_x_y_2d_array(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","WCSS"))
            optimal_point = self.find_perf_entry_for_given_C(WCSS_elbow_point[0])
            return {"C":optimal_point["C"],"WCSS":optimal_point["WCSS"],"Silhouette Score": optimal_point["Silhouette Score"],"Running Time":optimal_point["time"],"Calinski Harabasz Index":optimal_point["Calinski Harabasz Index"]}

    def find_perf_entry_for_given_C(self, C_val):
        for element in self.performance_data:
            if element["C"] == C_val:
                return element
        return None
    
    def graph(self,folder_name=None):
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","Calinski Harabasz Index"),"C value","Calinski-Harabasz Index","Fuzzy C-Means: Calinski-Harabasz Index values across C values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","Silhouette Score"),"C value","Silhouette Score","Fuzzy C-Means: Silhouette Score values across C values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","WCSS"),"C value","WCSS","Fuzzy C-Means: WCSS values across C values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"C","time"),"C value","Running Time","Fuzzy C-Means: Running time across C values",folder_name)


