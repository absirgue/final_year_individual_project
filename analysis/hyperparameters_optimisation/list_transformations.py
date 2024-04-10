class ListTransformations:
    """"
    Helper method for manipulating list of values.
    """

    def extract_list_from_list_of_dics(self, input_list, key):
        list = []
        for dict in input_list:
            list.append(dict[key])
        return list

    def extract_2d_list_from_list_of_dics(self, input_list, x_value_key, y_value_key):
        list = []
        for dict in input_list:
            list.append([dict[x_value_key],dict[y_value_key]])
        return list
    
    def extract_3d_list_from_list_of_dics(self, input_list, x_value_key, y_value_key,z_value_key):
        list = []
        for dict in input_list:
            list.append([dict[x_value_key],dict[y_value_key],dict[z_value_key]])    
        return list