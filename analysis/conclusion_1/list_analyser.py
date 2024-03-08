from analysis.conclusion_1.list_transformations import ListTransformations

class ListAnalyser:

    def get_values_for_max_measure_value(self,list_of_dicts, key_of_interest):
        list = ListTransformations().extract_list_from_list_of_dics(list_of_dicts,key_of_interest)
        if key_of_interest == "Calinski Harabasz Index":
            print(list)
        best_idx = self.get_idx_of_max_value(list,print_pls=key_of_interest == "Calinski Harabasz Index")
        if key_of_interest == "Calinski Harabasz Index":
            print("BEST INDEX")
            print(best_idx)
            print("WAS")
        if best_idx:
            return list_of_dicts[best_idx]
        else:
            return None
       
    def get_idx_of_max_value(self,list,print_pls=False):
        max_value = -10**9
        best_idx = None
        for element_idx,element in enumerate(list):
                if print_pls:
                    print(element_idx)
                    print(element)
                    print(element== True)
                    print(element >= max_value)
                    print(element != None)
                if element != None and element >= max_value:
                    print("THERE IS ONE")
                    max_value = element
                    best_idx= element_idx
        return best_idx