from analysis.conclusion_1.helper import create_ints_list
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
from analysis.conclusion_1.list_transformations import ListTransformations
import time
from interface_beautifier import InterfaceBeautifier

class KMeansIterator:

    def __init__(self,data,max_nb_of__clusters = None,nb_iterations=5):
        self.performance_data=[]
        self.data = data
        self.NB_ITERATIONS_PER_CONFIG = nb_iterations
        self.MIN_K_TO_TEST = 2
        self.MAX_K_TO_TEST = int(self.data.shape[0])
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_K_TO_TEST = max_nb_of__clusters
        self.alg_name = "K-Means"
    
    def iterate(self):
        self.performance_data = []
        k_values = create_ints_list(self.MIN_K_TO_TEST,self.MAX_K_TO_TEST,1)
        for K in k_values:
            calinski_harabasz_sum = 0
            time_sum = 0
            silhouette_score_sum = 0
            WCSS_sum = 0
            for i in range(self.NB_ITERATIONS_PER_CONFIG):
                start_time = time.time()
                k_means = KMeans(n_clusters=K,n_init=1).fit(self.data)
                end_time = time.time()
                labels = k_means.labels_
                time_sum += (end_time-start_time)
                try:
                    calinski_harabasz_sum+= calinski_harabasz_score(self.data, labels)
                    silhouette_score_sum += silhouette_score(self.data, labels)
                except:
                    calinski_harabasz_sum += 0
                    silhouette_score_sum += 0
                WCSS_sum += k_means.inertia_
            self.performance_data.append({"K":K,"time":time_sum/self.NB_ITERATIONS_PER_CONFIG,"Calinski Harabasz Index":calinski_harabasz_sum/self.NB_ITERATIONS_PER_CONFIG,"Silhouette Score":silhouette_score_sum/self.NB_ITERATIONS_PER_CONFIG,"WCSS":WCSS_sum/self.NB_ITERATIONS_PER_CONFIG})
            InterfaceBeautifier().print_percentage_progress("Progress on K-Means Hyperparameters Optimization",(k_values.index(K)+1)*100/len(k_values))
        return self.get_optimal()
        
    def get_performance_on_given_K(self, K):
        for perf_data in self.performance_data:
            if perf_data["K"] == K:
                return perf_data
            
    def get_optimal(self):
        if not self.performance_data:
            return None
        elif len(self.performance_data) <2:
            return self.performance_data[0]
        else:
            WCSS_elbow_point = FunctionAnalysis().get_elbow_point_from_x_y_2d_array(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"K","WCSS"))
            optimal_point = self.find_perf_entry_for_given_K(WCSS_elbow_point[0])
            return {"K":optimal_point["K"],"WCSS":optimal_point["WCSS"],"Running":optimal_point["time"],"Silhouette Score": optimal_point["Silhouette Score"],"Calinski Harabasz Index":optimal_point["Calinski Harabasz Index"]}

    def find_perf_entry_for_given_K(self, K_val):
        for element in self.performance_data:
            if element["K"] == K_val:
                return element
        return None
    
    def graph(self,folder_name=None):
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"K","Calinski Harabasz Index"),"K value","Calinski-Harabasz Index","K-Means: Calinski-Harabasz Index values across K values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"K","Silhouette Score"),"K value","Silhouette Score","K-Means: Silhouette Score values across K values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"K","WCSS"),"K value","WCSS","K-Means: WCSS values across K values",folder_name)
        GraphingHelper().plot_2d_array_of_points(ListTransformations().extract_2d_list_from_list_of_dics(self.performance_data,"K","time"),"K value","Running Time","K-Means: Running time across K values",folder_name)

