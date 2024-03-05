from analysis.conclusion_1.iterators.birch_iterator import BIRCHIterator
from analysis.conclusion_1.helper import create_ints_list
from graph.graphing_helper import GraphingHelper
from interface_beautifier import InterfaceBeautifier

class BIRCHSuperIterator:

    def __init__(self,data,max_nb_of__clusters = None):
        self.data = data
        self.MIN_K_TO_TEST = 2
        self.MAX_K_TO_TEST = int(self.data.shape[0])
        if max_nb_of__clusters and self.data.shape[0] > max_nb_of__clusters:
            self.MAX_K_TO_TEST = max_nb_of__clusters
        self.alg_name = "BIRCH"
    
    def iterate(self):
        self.silhouette_score_data = []
        self.calinski_harabasz_data = []
        self.WCSS_data = []
        k_values = create_ints_list(self.MIN_K_TO_TEST,self.MAX_K_TO_TEST,1)
        for K in k_values:
            birch_iterator = BIRCHIterator(data=self.data,number_of_clusters=K)
            birch_iterator.iterate()
            optimum = birch_iterator.get_optimal()
            self.calinski_harabasz_data.append([K,optimum["Calinski Harabasz Index Optimum"]["Calinski Harabasz Index"],optimum["Calinski Harabasz Index Optimum"]["Threshold Value"],optimum["Calinski Harabasz Index Optimum"]["Branching Factor"],optimum["Calinski Harabasz Index Optimum"]["Time"]])
            self.silhouette_score_data.append([K,optimum["Silhouette Score Optimum"]["Silhouette Score"],optimum["Silhouette Score Optimum"]["Threshold Value"],optimum["Silhouette Score Optimum"]["Branching Factor"],optimum["Silhouette Score Optimum"]["Time"]])
            InterfaceBeautifier().print_percentage_progress("Progress on BIRCH Hyperparameters Optimization",(k_values.index(K)+1)*100/len(k_values))
        return self.get_optimal()
    
    def get_optimal(self):
        calinski_best = self.get_values_for_max_measure_value("Calinski Harabasz Index")
        silhouette_best = self.get_values_for_max_measure_value("Silhouette Score")
        return {"Calinski Harabasz Index Optimum":
                {"K": calinski_best[0],"Running Time":calinski_best[4],"Threshold Value": calinski_best[2],"Branching Factor": calinski_best[3],"Calinski Harabasz Index":calinski_best[1]},
                "Silhouette Score Optimum":
                {"K": silhouette_best[0],"Threshold Value": calinski_best[2],"Running Time":silhouette_best[4],"Branching Factor": silhouette_best[3],"Silhouette Score":silhouette_best[1]},
                }

    def get_performance_on_given_K(self, K):
        return_value = {"K":K,"Running Time":{}, "Threshold Value":{}, "Branching Factor":{}}
        something_found = False
        for calinski_perf in self.calinski_harabasz_data:
            if calinski_perf[0] == K:
                return_value["Calinski Harabasz Index"] = calinski_perf[1]
                return_value["Running Time"]["Calinski Harabasz Index Optimum"] = calinski_perf[4]
                return_value["Threshold Value"]["Calinski Harabasz Index Optimum"] = calinski_perf[2]
                return_value["Branching Factor"]["Calinski Harabasz Index Optimum"] = calinski_perf[3]
                something_found = True
        for silhouette_perf in self.silhouette_score_data:
            if silhouette_perf[0] == K:
                return_value["Silhouette Score"] = silhouette_perf[1]
                return_value["Running Time"]["Silhouette Score Optimum"] = silhouette_perf[4]
                return_value["Threshold Value"]["Silhouette Score Optimum"] = silhouette_perf[2]
                return_value["Branching Factor"]["Silhouette Score Optimum"] = silhouette_perf[3]
                something_found = True
        return return_value if something_found else None
    
    def get_values_for_max_measure_value(self,measure_of_interest):
        list = None
        match measure_of_interest:
            case "Silhouette Score":
                list = self.silhouette_score_data
            case "Calinski Harabasz Index":
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

    def extract_value_pairs_at_indexes(self,list,idx_1,idx_2):
        points = []
        for element in list:
            points.append([element[idx_1], element[idx_2]])
        return points

    def graph(self,folder_name=None):
        GraphingHelper().plot_2d_array_of_points(self.extract_value_pairs_at_indexes(self.calinski_harabasz_data,0,1),"K value","Calinski-Harabasz Index","BIRCH: Calinski-Harabasz Index values across K values",folder_name)
        GraphingHelper().plot_2d_array_of_points(self.extract_value_pairs_at_indexes(self.silhouette_score_data,0,1),"K value","Silhouette Score","BIRCH: Silhouette Score values across K values",folder_name)
        GraphingHelper().plot_2d_array_of_points(self.extract_value_pairs_at_indexes(self.silhouette_score_data,2,4),"Threshold Value","Time","BIRCH: Time across Thresholds",folder_name)
        GraphingHelper().plot_2d_array_of_points(self.extract_value_pairs_at_indexes(self.silhouette_score_data,3,4),"Branching Factor","Time","BIRCH: Time across Branching Factors",folder_name)


