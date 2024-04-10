import pandas as pd
import numpy as np
from data_preprocessing.cell_cleaning import CleanCellOfParenthesis

class DataFrameCleaner:
    """
    Centralizes all actions needed for the cleaning of our data frame.
    """

    def __init__(self,data):
        self.data = data

    # Coordinates all cleaning operations.
    def clean(self,threshold_of_column_emptiness):
        self.remove_parenthetical_statements()
        self.remove_non_numerical_columns()
        self.remove_rows_with_some_null_values(threshold_of_column_emptiness)
        return self.data

    # Removes all parenthetical statements from all values in our data frame.
    def remove_parenthetical_statements(self):
        self.data = self.data.apply(lambda x: x.map(CleanCellOfParenthesis().clean))
    
    # Removes all columns which are not strictly comprised of numbers.
    def remove_non_numerical_columns(self):
        valid_columns = [col for col in self.data.columns if self.is_numeric_column(self.data[col])]
        df_valid = self.data[valid_columns]
        self.data = df_valid

    # Returns True if a column is strictly comprised of numbers.
    def is_numeric_column(self,column):
        return any(pd.to_numeric(column, errors='coerce').notna() | column.apply(lambda x: x in [None, "None"] or pd.isna(x) or not x or x=="").all())

    def get_data(self):
        return self.data

    # Remove all columns that have a number of empty cells higher than a given threshold.  
    def remove_too_empty_cols(self,threshold):
        columns_to_remove = self.data.columns[self.data.isna().sum() > threshold]
        columns_to_keep =[col for col in self.data.columns if col not in columns_to_remove]
        filtered_df = self.data[columns_to_keep]
        self.data = filtered_df

    # Remove all rows that include undefined values after all columns which are too empty 
    # have been removed.
    def remove_rows_with_some_null_values(self,threshold_of_column_emptiness):
        # All the set of characters below are different possible values we consider as undefined.
        self.data.replace('', pd.NA, inplace=True)
        self.data.replace('None', pd.NA, inplace=True)
        self.data.replace('nan', pd.NA, inplace=True)
        self.data.replace('- ', pd.NA, inplace=True)
        self.data.replace('-', pd.NA, inplace=True)
        self.data.replace('--', pd.NA, inplace=True)
        self.data.replace('---', pd.NA, inplace=True)
        self.data.replace('NM', pd.NA, inplace=True)
        self.data.replace(np.NaN, pd.NA, inplace=True)
        self.data.replace(np.NAN, pd.NA, inplace=True)
        threshold = len(self.data) * threshold_of_column_emptiness
        self.remove_too_empty_cols(threshold)
        self.data.dropna(how='any',inplace=True)