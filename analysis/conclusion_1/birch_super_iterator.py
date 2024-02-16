from analysis.conclusion_1.birch_iterator import BIRCHIterator
from analysis.conclusion_1.helper import create_ints_list
from graph.graphing_helper import GraphingHelper

class BIRCHSuperIterator:

    def __init__(self,data,max_nb_of__clusters = None):
        self.data = data
        self.NB_ITERATINS_PER_CONFIG = 1
        self.MIN_K_TO_TEST = 2
        self.MAX_K_TO_TEST = int(self.data.shape[0])
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_K_TO_TEST = max_nb_of__clusters
        self.alg_name = "BIRCH"
    
    def iterate(self):
        self.silhouette_score_data = []
        self.calinski_harabasz_data = []
        self.wcss_data = []
        k_values = create_ints_list(self.MIN_K_TO_TEST,self.MAX_K_TO_TEST,1)
        for K in k_values:
            birch_iterator = BIRCHIterator(data=self.data,number_of_clusters=K)
            birch_iterator.iterate()
            optimum = birch_iterator.get_optimal()
            optimum["Silhouette Score Optimum"]["Silhouette Score"]
            self.calinski_harabasz_data.append([K,optimum["Calinski Harbasz Index Optimum"]["Calinski Harbasz Index"],optimum["Calinski Harbasz Index Optimum"]["Treshold Value"],optimum["Calinski Harbasz Index Optimum"]["Branching Factor"]])
            self.silhouette_score_data.append([K,optimum["Silhouette Score Optimum"]["Silhouette Score"],optimum["Silhouette Score Optimum"]["Treshold Value"],optimum["Silhouette Score Optimum"]["Branching Factor"]])

    def get_optimal(self):
        calinski_best = self.get_values_for_max_measure_value("Calinski Harbasz Index")
        silhouette_best = self.get_values_for_max_measure_value("Silhouette Score")
        return {"Calinski Harbasz Index Optimum":
                {"K": calinski_best[0],"Treshold Value": calinski_best[2],"Branching Factor": calinski_best[3],"Calinski Harbasz Index":calinski_best[1]},
                "Silhouette Score Optimum":
                {"K": silhouette_best[0],"Branching Factor": silhouette_best[3],"Silhouette Score":silhouette_best[1]},
                }

    def get_values_for_max_measure_value(self,measure_of_interest):
        list = None
        match measure_of_interest:
            case "Silhouette Score":
                list = self.silhouette_score_data
            case "Calinski Harbasz Index":
                list = self.calinski_harabasz_data
        element = self.get_element_with_max_value_at_idx(list,1)
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

    def extract_K_and_metric_val(self,list):
        points = []
        for element in list:
            points.append([element[0], element[1]])
        print("POINTS")
        print(points)
        return points

    def graph(self):
        GraphingHelper().plot_2d_array_of_points(self.extract_K_and_metric_val(self.calinski_harabasz_data),"K value","Calinski-Harabasz Index","BIRCH: Calinski-Harabasz Index values across K values")
        GraphingHelper().plot_2d_array_of_points(self.extract_K_and_metric_val(self.silhouette_score_data),"K value","Silhouette Score","BIRCH: Silhouette Score values across K values")


