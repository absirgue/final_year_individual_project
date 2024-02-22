import numpy as np
import scipy.stats as sp
from sklearn.neighbors import KernelDensity
from scipy.integrate import quad
# Add a class that calculates the ranges, mean, median, quartiles, 
# entropy on each of the columns for each of the ratings
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
        mode = sp.mode(data)[0][0]
        q_25 = np.quantile(data, 0.25)
        q_75 = np.quantile(data, 0.75)
        std = np.std(data)
        return {"Mean":mean,"Median":median,"Mode":mode,"1st Quartile":q_25,"3rd Quartile":q_75,"Standard Deviation":std}
    
    def get_top_X__most_important_columns(self,X):
        count_top_20_percent = int(len(self.data[0])*X)
        X_best_entropies,cols_entropy = self.get_X_best_entropies(count_top_20_percent)
        best_cols = []
        for entropy in X_best_entropies:
            for key, val in cols_entropy:
                if val == entropy:
                    best_cols.append(key)
        return best_cols

    def get_X_best_entropies(self, X):
        cols_entropy = {}
        best_entropies = []
        for col_idx in range(len(self.data[0])):
            entropy = self.get_column_differential_entropy(col_idx)
            cols_entropy[col_idx] = entropy
            if len(best_entropies) < X:
                best_entropies.append(entropy)
            else:
                if entropy > min(best_entropies):
                    best_entropies.pop(min(best_entropies))
                    best_entropies.append(entropy)
        return best_entropies,cols_entropy

    def get_column_differential_entropy(self, col_idx):
        data = self.get_list_of_col_values(col_idx)
        # 'auto' so that Kernel's bandwith is automatically 
        # calculated (avoids assumption of Gaussian distribution)
        kernel_density_obj = KernelDensity(kernel='auto')
        kernel_density_obj.fit(data)
        prob_density_function = kernel_density_obj.score_samples(data)
        def differential_entropy_formula(value, prob_density_function):
            return -prob_density_function(value) * np.log2(prob_density_function(value))
        entropy, _ = quad(differential_entropy_formula, np.min(data), np.max(data), args=(prob_density_function,))
        return entropy
    
    def get_list_of_col_values(self,col_idx):
        data = []
        for element in self.data:
            data.append(element[col_idx])
        return data