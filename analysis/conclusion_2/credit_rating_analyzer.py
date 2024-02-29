import numpy as np
import scipy.stats as sp
from sklearn.neighbors import KernelDensity
from scipy.integrate import quad
from scipy.stats import norm

class CreditRatingAnalyzer:

    def __init__(self):
        self.credit_rating = None
        self.data = []
    
    def insert_company(self, company_rating, company_data):
        if not self.credit_rating:
            self.credit_rating = company_rating
        elif self.credit_rating != company_rating:
            return None
        self.data.append(company_data)
    
    def get_measures_of_location_and_dispersion(self,col_idx):
        data = []
        for comp in self.data:
            data.append(comp[col_idx])
        data = np.array(data)
        mean = data.mean()
        median = np.median(data)
        q_25 = np.quantile(data, 0.25)
        q_75 = np.quantile(data, 0.75)
        std = np.std(data)
        return {"Mean":mean,"Median":median,"1st Quartile":q_25,"3rd Quartile":q_75,"Standard Deviation":std}
    
    def get_top_X_most_important_columns(self,X,full_data):
        X_best_cols = self.get_X_smaller_normalized_range(X,full_data)
        return X_best_cols

    def get_X_smaller_normalized_range(self, X,full_data):
        cols_entropy = {}
        for col_idx in range(len(self.data[0])):
            entropy = self.get_col_normalized_range(col_idx,full_data)
            if len(cols_entropy.keys()) < X:
                cols_entropy[entropy] = col_idx
            else:
                current_min = min(cols_entropy.keys())
                if entropy > current_min:
                    del cols_entropy[current_min]
                    cols_entropy[entropy] = col_idx
        return cols_entropy.values()
    
    def get_col_normalized_range(self,col_idx,full_data):
        overall_range = np.max(full_data[:, col_idx]) - np.min(full_data[:, col_idx])
        cr_col_values = self.get_list_of_col_values(col_idx)
        cr_range = max(cr_col_values)-  min(cr_col_values)
        return cr_range/overall_range

    def get_column_differential_entropy(self, col_idx):
        data = self.get_list_of_col_values(col_idx)
        data = np.array(data)
        kde = norm.pdf
        pdf_values = kde(data, data)
        result, _ = quad(lambda x: -pdf_values[np.abs(data - x).argmin()] * np.log(pdf_values[np.abs(data - x).argmin()]), -np.inf, np.inf)
        return result
    
    def get_list_of_col_values(self,col_idx):
        data = []
        for element in self.data:
            data.append(element[col_idx])
        return data