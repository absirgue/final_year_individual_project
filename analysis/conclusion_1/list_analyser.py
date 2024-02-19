from analysis.conclusion_1.list_transformations import ListTransformations

class ListAnalyser:

    def get_values_for_max_measure_value(self,perf_data, key_measure_of_interest):
        list = ListTransformations().extract_list_from_list_of_dics(perf_data,key_measure_of_interest)
        best_idx = self.get_idx_of_max_value(list)
        return perf_data[best_idx]

    def get_idx_of_max_value(self,list):
        max_value = -10**9
        best_idx = None
        for element_idx,element in enumerate(list):
                if element and element >= max_value:
                    max_value = element
                    best_idx= element_idx
        return best_idx