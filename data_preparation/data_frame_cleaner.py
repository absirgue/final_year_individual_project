from data_preparation.cell_cleaning import CleanCellOfParenthesis
import pandas as pd
import numpy as np
class DataFrameCleaner:
    def __init__(self,data):
        self.data = data

    def remove_parenthetical_statements(self):
        self.data = self.data.apply(lambda x: x.map(CleanCellOfParenthesis().clean))
    
    def remove_non_numerical_columns(self):
        # Filter columns based on the criteria
        valid_columns = [col for col in self.data.columns if self.is_numeric_column(self.data[col])]
        df_valid = self.data[valid_columns]
        self.data = df_valid

    def is_numeric_column(self,column):
        return any(pd.to_numeric(column, errors='coerce').notna() | column.apply(lambda x: x in [None, "None"] or pd.isna(x) or not x or x=="").all())

    def get_data(self):
        return self.data
        
    def filter_columns(self,threshold):
        # Identify columns with too many empty cells
        columns_to_remove = self.data.columns[self.data.isna().sum() > threshold]

        # Identify and preserve columns with names starting with "CUSTOM"
        custom_columns = [col for col in self.data.columns if col.startswith("CUSTOM")]

        # Filter columns to keep
        columns_to_keep = custom_columns + [col for col in self.data.columns if col not in columns_to_remove]

        filtered_df = self.data[columns_to_keep]
        self.data = filtered_df

    def remove_rows_with_some_null_values(self,threshold_of_column_emptiness):
        self.data.replace('', pd.NA, inplace=True)
        self.data.replace('None', pd.NA, inplace=True)
        self.data.replace('nan', pd.NA, inplace=True)
        self.data.replace(np.NaN, pd.NA, inplace=True)
        self.data.replace(np.NAN, pd.NA, inplace=True)
        threshold = len(self.data) * threshold_of_column_emptiness
        # self.data.dropna(axis=1, thresh=threshold, subset=self.data.columns[
        # ~(self.data.columns.str.contains("CUSTOM") | self.data.columns.str.contains(" "))
        # ], inplace=True)
        self.filter_columns(threshold)
        self.write_to_csv()
        self.data.dropna(how='any',inplace=True)
        self.write_to_csv_2()

    def clean(self,threshold_of_column_emptiness):
        self.remove_parenthetical_statements()
        self.remove_non_numerical_columns()
        self.remove_rows_with_some_null_values(threshold_of_column_emptiness)
        return self.data

    def write_to_csv(self):
        df = pd.DataFrame(self.data)
        excel_filename = 'data_preparator_output_2.csv'
        df.to_csv(excel_filename, index=False)

    def write_to_csv_2(self):
        df = pd.DataFrame(self.data)
        excel_filename = 'data_preparator_output_3.csv'
        df.to_csv(excel_filename, index=False)