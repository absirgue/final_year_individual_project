import math
import numpy as np
import scipy.stats as sp
# For each cluster then, we can locate if it’s the higher, lower, 
# or median range of each of the columns
class CreditRatingCluster:

    def __init__(self):
        self.companies_count = 0
        self.entropy = None
        self.credit_ratings_counts = {}
        self.data = {}
    
    def get_companies_count(self):
        return self.companies_count

    def get_is_significant_cluster(self,first_junk_credit_rating,signifcance_threshold_for_split):
        count_investment_grade = 0
        count_junk = 0
        for credit_rating in self.credit_ratings_counts:
            if credit_rating >  first_junk_credit_rating:
                count_investment_grade +=1
            if credit_rating <= signifcance_threshold_for_split:
                count_junk +=1 
        return (count_investment_grade/self.companies_count > signifcance_threshold_for_split and count_investment_grade/self.companies_count<1) or (count_junk/self.companies_count > signifcance_threshold_for_split and count_junk/self.companies_count<1)

    def get_credit_ratings_proportion(self):
        percent_proportions = {}
        for rating in self.credit_ratings_counts.keys():
            percent_proportions[rating] = round((self.credit_ratings_counts[rating]/self.companies_count) * 100,2)
        return percent_proportions
    
    def get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(self, col_idx, credit_rating):
        data = self.data[credit_rating]
        col_values = self.get_list_of_col_values(data, col_idx)
        return self.get_measures_of_location_and_dispersion(col_values)

    def get_list_of_col_values(self,data, col_idx):
        data = []
        for element in data:
            data.append(element[col_idx])
        return data
    
    def get_rating_range(self):
        return max(self.credit_ratings_counts.keys()) - min(self.credit_ratings_counts.keys())
    
    def get_measures_of_location_and_dispersion(self,data):
        data = np.array(data)
        mean = data.mean()
        median = np.median(data)
        mode = sp.mode(data)[0][0]
        q_25 = np.quantile(data, 0.25)
        q_75 = np.quantile(data, 0.75)
        std = np.std(data)
        return {"Mean":mean,"Median":median,"Mode":mode,"1st Quartile":q_25,"3rd Quartile":q_75,"Standard Deviation":std}

    # TO BE USED FOR PRED.
    def get_measures_of_location_and_dispersion_for_credit_ratings_values(self):
        data = []
        for rating in self.credit_ratings_counts.keys():
            for i in range(self.credit_ratings_counts[rating]):
                data.append(rating)
        return self.get_measures_of_location_and_dispersion(data)

    def get_entropy(self):
        entropy = 0
        for cr in self.credit_ratings_counts.keys():
            p = self.credit_ratings_counts[cr] / self.companies_count
            entropy += p*math.log2(p)
        return -1 * entropy

    def add_clustered_credit_rating(self, credit_rating, data):
        self.companies_count += 1
        self.insert_rating_in_proportion(credit_rating)
        self.insert_rating_and_data(credit_rating,data)
        
    def insert_rating_in_proportion(self, credit_rating):
        if credit_rating in self.credit_ratings_counts.keys():
            self.credit_ratings_counts[credit_rating] = 1
        else:
            self.credit_ratings_counts[credit_rating] += 1
    
    def insert_rating_and_data(self, credit_rating,data):
        if credit_rating in self.credit_ratings_counts.keys():
            self.credit_ratings_counts[credit_rating] = [data]
        else:
            self.credit_ratings_counts[credit_rating] = self.credit_ratings_counts[credit_rating].append(data)