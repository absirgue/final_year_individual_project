class DataTypeIsolator:

    def __init__(self,data_frame, credit_rating_col_name):
        self.CREDIT_RATING_COLUMN_NAME = credit_rating_col_name
        self.data = data_frame
    
    def isolate_data_types(self,data_types):
        names_columns_to_delete = self.get_names_columns_to_delete(data_types)
        self.data.drop(names_columns_to_delete, axis=1,inplace=True)
        return self.data
    
    def get_names_columns_to_delete(self,data_type_names):
        column_names= self.data.columns
        names_columns_to_delete = []
        for column_name in column_names:
                if not (self.is_equivalent_to_at_least_one_col_name(data_type_names,column_name) or column_name == self.CREDIT_RATING_COLUMN_NAME):
                    names_columns_to_delete.append(column_name)
        return names_columns_to_delete
    
    def is_equivalent_to_at_least_one_col_name(self,data_type_names, column_name):
        equivalent_to_at_least_one_col_name = False
        for dt_name in data_type_names:
            if self.column_names_are_equivalent(dt_name,column_name):
                equivalent_to_at_least_one_col_name = True
        return equivalent_to_at_least_one_col_name

    def column_names_are_equivalent(self,dt_name,column_name):
        if "." in column_name:
            column_name = column_name.split(".")[0]
        return column_name == dt_name