import numpy as np

class CreditRatingAnalyzer:
    """
    Offers analysis of the properties of a credit rating based on the companies assigned this
    rating in our data set
    """

    def __init__(self):
        self.credit_rating = None
        self.data = []
    
    # Returns the number of companies assigned this rating.
    def get_companies_count(self):
        return len(self.data)

    # Add a company, characterized by its data, to the list of companies assigned this rating.
    def insert_company(self, company_rating, company_data):
        if not self.credit_rating:
            self.credit_rating = company_rating
        elif self.credit_rating != company_rating:
            return None
        self.data.append(company_data)
    
    """
    Returns measures of location and dispersion for the values of a given column across
    all companies assigned this rating.
    """
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
    
    # Returns the indexed of the X most important columns.
    def get_top_X_most_important_columns(self,X,full_data):
        X_best_cols = self.get_X_smaller_normalized_range(X,full_data)
        return X_best_cols

    """
    Returns the indexes of the X columns where the range of values in this column for all companies
    assigned this rating divided by the range of values in this column across the entire data set
    are the smallest. 
    """
    def get_X_smaller_normalized_range(self, X,full_data):
        cols_normalized_range = {}
        for col_idx in range(len(self.data[0])):
            normalized_range = self.get_col_normalized_range(col_idx,full_data)
            if len(cols_normalized_range.keys()) < X:
                cols_normalized_range[normalized_range] = col_idx
            else:
                current_min = min(cols_normalized_range.keys())
                if normalized_range < current_min:
                    del cols_normalized_range[current_min]
                    cols_normalized_range[normalized_range] = col_idx
        return cols_normalized_range.values()

    def get_col_normalized_range(self,col_idx,full_data):
        if col_idx > full_data.shape[1]:
            return 0
        overall_range = np.max(full_data[:, col_idx]) - np.min(full_data[:, col_idx])
        cr_col_values = self.get_list_of_col_values(col_idx)
        cr_range = max(cr_col_values)-  min(cr_col_values)
        return cr_range/overall_range

    def get_list_of_col_values(self,col_idx):
        data = []
        for element in self.data:
            data.append(element[col_idx])
        return data