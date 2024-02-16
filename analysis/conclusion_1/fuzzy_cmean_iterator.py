from analysis.conclusion_1.helper import create_ints_list
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
from skfuzzy.cluster import cmeans
import numpy as np 

class FuzzyCMeansIterator:

    def __init__(self,data,max_nb_of__clusters = None):
        self.data = data.astype(float).values
        print(self.data)
        self.NB_ITERATINS_PER_CONFIG = 5
        self.MIN_C_TO_TEST = 2
        self.MAX_C_TO_TEST = int(self.data.shape[0])
        self.M = 2
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_C_TO_TEST = max_nb_of__clusters
        self.alg_name = "Fuzzy C-Means"
    
    def iterate(self):
        self.silhouette_score_data = []
        self.calinski_harabasz_data = []
        self.wcss_data = []
        c_values = create_ints_list(self.MIN_C_TO_TEST,self.MAX_C_TO_TEST,1)
        for C in c_values:
            calinski_harabasz_sum = 0
            silhouette_score_sum = 0
            wcss_sum = 0
            for i in range(self.NB_ITERATINS_PER_CONFIG):
                cntr, u, _, _, _, _, _ = cmeans(self.data.T, c=C, m=self.M,error=0.001,maxiter=400)
                try:
                    fuzzy_cluster_labels = np.argmax(u, axis=0)
                    calinski_harabasz_sum+= calinski_harabasz_score(self.data, fuzzy_cluster_labels)
                    silhouette_score_sum += silhouette_score(self.data, fuzzy_cluster_labels)
                    wcss_sum += np.sum(np.power(np.linalg.norm(self.data.T - cntr.T[:, fuzzy_cluster_labels], axis=1), 2))
                except Exception as e:
                    calinski_harabasz_sum = 0
                    silhouette_score_sum = 0
            self.calinski_harabasz_data.append([C,calinski_harabasz_sum/self.NB_ITERATINS_PER_CONFIG])
            self.silhouette_score_data.append([C,silhouette_score_sum/self.NB_ITERATINS_PER_CONFIG])
            self.wcss_data.append([C,wcss_sum/self.NB_ITERATINS_PER_CONFIG])
        
    def get_optimal(self):
        wcss_inflection_points = FunctionAnalysis().get_inflection_points_from_x_y_2d_array(self.wcss_data)
        optimal_point = wcss_inflection_points[0]
        return {"K":optimal_point[0],"WCSS":optimal_point[1],"Silhouette Score": self.get_y_value_for_given_x(self.silhouette_score_data,optimal_point[0]),"Calinski Harbasz Index":self.get_y_value_for_given_x(self.calinski_harabasz_data,optimal_point[0])}
        
    def get_y_value_for_given_x(self,arr,x_val):
        for point in arr:
            if point[0] == x_val:
                return point[1]
        return None

    def graph(self):
        GraphingHelper().plot_2d_array_of_points(self.calinski_harabasz_data,"C value","Calinski-Harabasz Index","Fuzzy C-Means: Calinski-Harabasz Index values across K values")
        GraphingHelper().plot_2d_array_of_points(self.silhouette_score_data,"C value","Silhouette Score","Fuzzy C-Means: Silhouette Score values across K values")
        GraphingHelper().plot_2d_array_of_points(self.wcss_data,"C value","WCSS","Fuzzy C-Means: WCSS values across K values")


