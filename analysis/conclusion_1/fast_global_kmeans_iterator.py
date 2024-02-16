from analysis.conclusion_1.helper import create_ints_list
from clustering.fast_global_k_means import FastGlobalKMeans
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis

class FastGlobalKMeansIterator:

    def __init__(self,data,max_nb_of__clusters = None):
        self.data = data
        self.NB_ITERATINS_PER_CONFIG = 5
        self.MIN_K_TO_TEST = 2
        self.MAX_K_TO_TEST = int(self.data.shape[0])
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_K_TO_TEST = max_nb_of__clusters
        self.alg_name = "Fast Global K-Means"
    
    def iterate(self):
        self.silhouette_score_data = []
        self.calinski_harabasz_data = []
        self.wcss_data = []
        k_values = create_ints_list(self.MIN_K_TO_TEST,self.MAX_K_TO_TEST,1)
        for K in k_values:
            calinski_harabasz_sum = 0
            silhouette_score_sum = 0
            wcss_sum = 0
            for i in range(self.NB_ITERATINS_PER_CONFIG):
                fast = FastGlobalKMeans(K)
                labels = fast.cluster(self.data)
                try:
                    calinski_harabasz_sum+= calinski_harabasz_score(self.data, labels)
                    silhouette_score_sum += silhouette_score(self.data, labels)
                except:
                    calinski_harabasz_sum = 0
                    silhouette_score_sum = 0
                # wcss_sum += k_means.inertia_
            self.calinski_harabasz_data.append([K,calinski_harabasz_sum/self.NB_ITERATINS_PER_CONFIG])
            self.silhouette_score_data.append([K,silhouette_score_sum/self.NB_ITERATINS_PER_CONFIG])
            self.wcss_data.append([K,wcss_sum/self.NB_ITERATINS_PER_CONFIG])
        
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
        GraphingHelper().plot_2d_array_of_points(self.calinski_harabasz_data,"K value","Calinski-Harabasz Index","Fast Global K-Means: Calinski-Harabasz Index values across K values")
        GraphingHelper().plot_2d_array_of_points(self.silhouette_score_data,"K value","Silhouette Score","Fast Global K-Means: Silhouette Score values across K values")
        GraphingHelper().plot_2d_array_of_points(self.wcss_data,"K value","Fast Global WCSS","K-Means: WCSS values across K values")


