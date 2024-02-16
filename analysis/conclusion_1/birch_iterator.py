from analysis.conclusion_1.helper import create_floats_list,create_ints_list
from sklearn.cluster import Birch
from sklearn.metrics import calinski_harabasz_score,silhouette_score
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis

class BIRCHIterator:

    def __init__(self,data,number_of_clusters):
        self.data = data
        self.NB_ITERATINS_PER_CONFIG = 1
        # TO DO - change values
        self.CLUSTERS_COUNT = number_of_clusters
        self.MIN_BRANCHING_FACTOR = 5
        self.MAX_BRANCHING_FACTOR = 65
        self.MIN_THRESHOLD = 0.1
        self.MAX_THRESHOLD = 10
        self.alg_name = "BIRCH for "+str(number_of_clusters)+" clusters"
    
    def iterate(self):
        self.silhouette_score_data = []
        self.calinski_harabasz_data = []
        branching_factor_value = create_ints_list(self.MIN_BRANCHING_FACTOR,self.MAX_BRANCHING_FACTOR,5)
        threshold_factor_value = create_floats_list(self.MIN_THRESHOLD,self.MAX_THRESHOLD,0.25)
        for threshold in threshold_factor_value:
            for branching_factor in branching_factor_value:
                calinski_harabasz_sum = 0
                silhouette_score_sum = 0
                for i in range(self.NB_ITERATINS_PER_CONFIG):
                    birch = Birch(threshold=threshold, branching_factor=branching_factor, n_clusters=self.CLUSTERS_COUNT).fit(self.data)
                    labels = birch.labels_
                    try:
                        calinski_harabasz_sum+= calinski_harabasz_score(self.data, labels)
                        silhouette_score_sum += silhouette_score(self.data, labels)
                    except:
                        calinski_harabasz_sum = 0
                        silhouette_score_sum = 0
                self.calinski_harabasz_data.append([threshold,branching_factor,calinski_harabasz_sum/self.NB_ITERATINS_PER_CONFIG])
                self.silhouette_score_data.append([threshold,branching_factor,silhouette_score_sum/self.NB_ITERATINS_PER_CONFIG])
        
    def get_optimal(self):
        calinski_best = self.get_values_for_max_measure_value("Calinski Harbasz Index")
        silhouette_best = self.get_values_for_max_measure_value("Silhouette Score")
        return {"Calinski Harbasz Index Optimum":
                {"Treshold Value": calinski_best[0],"Branching Factor": calinski_best[1],"Calinski Harbasz Index":calinski_best[2]},
                "Silhouette Score Optimum":
                {"Treshold Value": silhouette_best[0],"Branching Factor": silhouette_best[1],"Calinski Harbasz Index":silhouette_best[2]},
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
        GraphingHelper().plot_3d_array_of_ponts(self.calinski_harabasz_data,"Threshold","Branching Factor","Calinski Harbasz Index","BIRCH: Calinski-Harabasz Index values across parameters")
        GraphingHelper().plot_3d_array_of_ponts(self.silhouette_score_data,"Threshold","Branching Factor","Silhouette Score","BIRCH: Silhouette Score values across paramters")