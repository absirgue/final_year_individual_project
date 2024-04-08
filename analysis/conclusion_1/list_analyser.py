from analysis.conclusion_1.list_transformations import ListTransformations

class ListAnalyser:
    """
    Helper class for the analysis of lists of values.
    """

    # Returns the index of the element in a list of dictionary with maximum value for a given key.
    def get_values_for_max_key_value(self,list_of_dicts, key_of_interest):
        list = ListTransformations().extract_list_from_list_of_dics(list_of_dicts,key_of_interest)
        best_idx = self.get_idx_of_max_value(list)
        if best_idx != None:
            return list_of_dicts[best_idx]
        else:
            return None
    
    def get_idx_of_max_value(self,list):
        max_value = -10**9
        best_idx = None
        for element_idx,element in enumerate(list):
                if (element != None) and element >= max_value:
                    max_value = element
                    best_idx= element_idx
        return best_idx