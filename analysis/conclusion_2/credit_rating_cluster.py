import math
import numpy as np
import scipy.stats as sp

class CreditRatingCluster:

    def __init__(self,first_junk_credit_rating,significance_threshold_for_split):
        self.entropy = None
        self.credit_ratings_counts = {}
        self.data = {}
        self.first_junk_credit_rating = first_junk_credit_rating
        self.significance_threshold_for_split = significance_threshold_for_split
        self.dataframe_rows_with_their_ratings = {}
    
    def get_credit_ratings_counts(self):
        return self.credit_ratings_counts

    def get_credit_ratings_shares(self):
        shares = {}
        for cr,count in self.credit_ratings_counts.items():
            shares[cr] = count/self.get_companies_count()
        return shares

    def get_companies_count(self):
        companies_count = 0
        for count in self.credit_ratings_counts.values():
            companies_count += count
        return companies_count

    def get_is_significant_cluster(self):
        count_investment_grade = 0
        count_junk = 0
        for credit_rating in self.credit_ratings_counts:
            if float(credit_rating) >  self.first_junk_credit_rating:
                count_investment_grade +=self.credit_ratings_counts[credit_rating]
            if float(credit_rating) <= self.first_junk_credit_rating:
                count_junk +=self.credit_ratings_counts[credit_rating]
        return (count_investment_grade/self.get_companies_count() > self.significance_threshold_for_split) and (count_junk/self.get_companies_count() > self.significance_threshold_for_split)

    def get_credit_ratings_held_in_significant_proportions(self,significant_proportion):
        ratings = []
        for cr,count in self.credit_ratings_counts.items():
            if count/self.get_companies_count() > significant_proportion:
                ratings.append(cr)
        return ratings

    def get_credit_ratings_proportion(self):
        percent_proportions = {}
        for rating in self.credit_ratings_counts.keys():
            percent_proportions[rating] = (self.credit_ratings_counts[rating]/self.get_companies_count())
        return percent_proportions
    
    def get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(self, col_idx, credit_rating):
        if not (self.data and (credit_rating in self.data.keys()) and (col_idx<len(list(self.data.values())[0][0]))):
            return None
        data = self.data[credit_rating]
        col_values = self.get_list_of_col_values(data, col_idx)
        return self.get_measures_of_location_and_dispersion(col_values)

    def get_list_of_col_values(self,data, col_idx):
        col_values = []
        for element in data:
            col_values.append(element[col_idx])
        return col_values
    
    def get_rating_range(self):
        if not self.credit_ratings_counts:
            return None
        return max([float(x) for x in self.credit_ratings_counts.keys()]) - min([float(x) for x in self.credit_ratings_counts.keys()])
    
    def get_measures_of_location_and_dispersion(self,data):
        if len(data) == 0:
            return None
        data = np.array(data)
        mean = data.mean()
        median = np.median(data)
        q_25 = np.quantile(data, 0.25)
        q_75 = np.quantile(data, 0.75)
        std = np.std(data)
        return {"Mean":mean,"Median":median,"1st Quartile":q_25,"3rd Quartile":q_75,"Standard Deviation":std}

    def get_measures_of_location_and_dispersion_for_credit_ratings_values(self):
        if not self.credit_ratings_counts:
            return None
        data = self.get_list_of_credit_ratings_appearances()
        measures = self.get_measures_of_location_and_dispersion(data)
        measures["Is Signficant"] = self.get_is_significant_cluster()
        return measures
    
    def get_list_of_credit_ratings_appearances(self):
        cr_list = []
        for key in self.credit_ratings_counts.keys():
            for i in range(self.credit_ratings_counts[key]):
                cr_list.append(float(key))
        return cr_list

    def get_entropy(self):
        if not self.credit_ratings_counts:
            return None
        entropy = 0
        for cr_count in self.credit_ratings_counts.values():
            p = cr_count / self.get_companies_count()
            if p > 0:
                entropy += p*math.log2(p)
        return -1 * entropy if entropy else 0

    def add_clustered_credit_rating(self, credit_rating, data,dataframe_row_idx):
        self.insert_rating_in_proportion(credit_rating)
        self.insert_rating_and_data(credit_rating,data)
        self.dataframe_rows_with_their_ratings[dataframe_row_idx] = credit_rating
    
    def get_rows_difference_with_mean_rating(self):
        differences_with_mean = []
        cluster_mean_rating = self.get_measures_of_location_and_dispersion_for_credit_ratings_values()["Mean"]
        for row_idx in self.dataframe_rows_with_their_ratings.keys():
            diff = cluster_mean_rating - self.dataframe_rows_with_their_ratings[row_idx]
            differences_with_mean.append({row_idx:diff})
        return differences_with_mean
        
    def insert_rating_in_proportion(self, credit_rating):
        if credit_rating in self.credit_ratings_counts.keys():
            self.credit_ratings_counts[credit_rating] = self.credit_ratings_counts[credit_rating] + 1
        else:
            self.credit_ratings_counts[credit_rating] = 1
            
    def insert_rating_and_data(self, credit_rating,data):
        if not (credit_rating in self.data.keys()):
            self.data[credit_rating] = [data]
        else:
            cr_data = self.data[credit_rating]
            cr_data.append(data)
            self.data[credit_rating] = cr_data