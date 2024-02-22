import os
import json
from analysis.conclusion_2.credit_rating_cluster import CreditRatingCluster

class ClustersAnalyzer:

    def __init__(self,folder_name, encoding_first_junk_rating, cluster_labels,data_ordered_credit_ratings,credit_ratings_analyzers,data,col_names):
        self.PROPORTION_OF_RATING_IN_CLUSTER_CONSIDERED_SIGNIFICANT = 0.15
        self.PROPORTION_OF_COLUMNS_WE_WANT_EXPLAINED = 0.2
        self.JUNK_INVEST_GRADE_SPLIT_CONSIDERED_SIGNIFICANT = 0.15
        self.FOLDER_NAME = folder_name
        self.ENCODING_FIRST_JUNK_RATING = encoding_first_junk_rating
        self.row_credit_ratings = data_ordered_credit_ratings
        self.cluster_labels = cluster_labels
        self.credit_ratings_analyzers = credit_ratings_analyzers
        self.data = data
        self.col_names = col_names
        
    
    def analyze(self):
        analysis = {}
        credit_rating_clusters = self.create_credit_rating_clusters()
        nb_clusters_with_various_cr_ranges = len(self.get_clusters_with_various_cr_ranges(credit_rating_clusters))
        analysis["Clusters with significant ranges (count)"] = nb_clusters_with_various_cr_ranges
        nb_clusters_with_significant_incoherencies = len(self.get_singificant_clusters(credit_rating_clusters))
        analysis["Significant Clusters (count)"] = nb_clusters_with_significant_incoherencies
        clusters_entropy =  self.get_clusters_entropies(credit_rating_clusters)
        analysis["Cluster entropies"] = clusters_entropy
        max_entropy = max(clusters_entropy)
        analysis["Maximum entropy"] = max_entropy
        weighted_avg_entropy = self.compute_weigthed_avg_entropy(credit_rating_clusters,clusters_entropy)
        analysis["Weighted average entropy"] = weighted_avg_entropy
        if nb_clusters_with_various_cr_ranges or nb_clusters_with_significant_incoherencies:
            incoherencies_explanations = self.explain_incoherencies(credit_rating_clusters)
            analysis["Incoherencies explanations"] = incoherencies_explanations
        self.save_analysis(analysis)
        return analysis
    
    def save_analysis(self,analysis):
        file_path = os.path.join(self.FOLDER_NAME, "analysis.json")
        with open(file_path, 'w') as json_file:
            json.dump(analysis, json_file)

    def explain_incoherencies(self, credit_rating_clusters):
        clusters_with_notable_ranges = set(self.get_clusters_with_various_cr_ranges(credit_rating_clusters))
        significant_clusters = set(self.get_singificant_clusters(credit_rating_clusters))
        clusters_requiring_explanations = clusters_with_notable_ranges+significant_clusters
        unique_clusters_requiring_explanations = list(set(clusters_requiring_explanations))
        explanations = {}
        for cluster_idx in range(len(unique_clusters_requiring_explanations)):
            credit_ratings_held_in_significant_proportion = unique_clusters_requiring_explanations[cluster_idx].get_credit_ratings_held_in_significant_proportions(self.PROPORTION_OF_RATING_IN_CLUSTER_CONSIDERED_SIGNIFICANT)
            cluster_explanations = {}
            for rating in credit_ratings_held_in_significant_proportion:
                cluster_explanations["RATING " +rating] = []
                analyzer = self.credit_ratings_analyzers[rating] if rating in self.credit_ratings_analyzers.keys() else None
                if analyzer:
                    important_columns = analyzer.get_top_X__most_important_columns(self.PROPORTION_OF_COLUMNS_WE_WANT_EXPLAINED)
                    for col_idx in important_columns:
                        cr_col_values = analyzer.get_measures_of_location_and_dispersion(col_idx)
                        cluster_members_col_values = unique_clusters_requiring_explanations[cluster_idx].get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(self, col_idx, rating)
                        cluster_explanations["RATING " +rating] = cluster_explanations["RATING " +rating].append({self.get_col_name(col_idx):{"Credit Rating Statistics":cr_col_values,"Cluster Statistics":cluster_members_col_values}})
            explanations["CLUSTER "+cluster_idx] =  cluster_explanations
        return explanations 
           
    def get_col_name(self,col_idx):
        return self.col_names[col_idx]
    
    def compute_weigthed_avg_entropy(self,credit_rating_clusters,clusters_entropy):
        weighted_sum = 0
        for cr_cluster_idx in range(len(credit_rating_clusters)):
            weighted_sum += clusters_entropy[cr_cluster_idx]*(credit_rating_clusters[cr_cluster_idx].get_companies_count()/len(self.data))
        return weighted_sum
    
    def get_clusters_entropies(self, credit_rating_clusters):
        entropies = []
        for cr_cluster in credit_rating_clusters:
            entropies.append(cr_cluster.get_entropy())
        return entropies

    def get_singificant_clusters(self, credit_rating_clusters):
        clusters = []
        for cr_cluster in credit_rating_clusters:
            if cr_cluster.get_is_significant_cluster(self.ENCODING_FIRST_JUNK_RATING,self.JUNK_INVEST_GRADE_SPLIT_CONSIDERED_SIGNIFICANT):
                clusters.append(cr_cluster) 
        return clusters 
    
    def get_clusters_with_various_cr_ranges(self, credit_rating_clusters):
        clusters = []
        for cr_cluster in credit_rating_clusters:
            if cr_cluster.get_rating_range() > 3:
                clusters.append(cr_cluster)
        return clusters
        
    def create_credit_rating_clusters(self):
        credit_rating_clusters = {}
        for rating_idx in range(len(self.row_credit_ratings)):
            rating = self.row_credit_ratings[rating_idx]
            if rating in credit_rating_clusters.keys():
                credit_rating_clusters[rating].add_clustered_credit_rating(rating, self.data[rating_idx])
            else:
                new_credit_rating_cluster = CreditRatingCluster()
                new_credit_rating_cluster.add_clustered_credit_rating(rating,self.data[rating_idx])
                credit_rating_clusters[rating] = new_credit_rating_cluster
        return credit_rating_clusters.values()