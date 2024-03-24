import os
from analysis.conclusion_2.credit_rating_cluster import CreditRatingCluster
from analysis.conclusion_3.predictive_power_analyser import PredictivePowerAnalyser
from graph.graphing_helper import GraphingHelper
from data_preparation.credit_rating_encoding import CreditRatingEncoding
class ClustersAnalyzer:

    def __init__(self,entity_ids,data_source, encoding_first_junk_rating=None, cluster_labels=None,data_ordered_credit_ratings=None,credit_ratings_analyzers=None,data=None,col_names=None):
        self.entity_ids = entity_ids
        self.data_source = data_source
        self.PROPORTION_OF_RATING_IN_CLUSTER_CONSIDERED_SIGNIFICANT = 0.2
        self.NUMBER_OF_COLUMNS_WE_WANT_EXPLAINED = 5
        self.JUNK_INVEST_GRADE_SPLIT_CONSIDERED_SIGNIFICANT = 0.2
        self.ENCODING_FIRST_JUNK_RATING = encoding_first_junk_rating
        self.row_credit_ratings = data_ordered_credit_ratings
        self.cluster_labels = cluster_labels
        self.credit_ratings_analyzers = credit_ratings_analyzers
        self.data = data
        self.col_names = col_names
    
    def analyze(self,folder_name_for_graph,alg_name):
        analysis = {}
        credit_rating_clusters = self.create_credit_rating_clusters()
        predictions_analysis = PredictivePowerAnalyser(self.data_source,self.entity_ids).analyse(credit_rating_clusters)
        analysis["Predictive Power"] = predictions_analysis
        nb_shares_of_companies_by_cluster = self.get_share_of_companies_in_each_clusters(credit_rating_clusters)
        analysis["Share of total companies in each clusters"] = nb_shares_of_companies_by_cluster
        nb_clusters_with_various_cr_ranges = len(self.get_clusters_with_various_cr_ranges(credit_rating_clusters))
        analysis["Clusters with significant ranges (count)"] = nb_clusters_with_various_cr_ranges
        nb_clusters_with_significant_incoherencies = len(self.get_singificant_clusters(credit_rating_clusters))
        analysis["Significant Clusters (count)"] = nb_clusters_with_significant_incoherencies
        cluster_credit_ratings_shares = self.get_cluster_cr_shares(credit_rating_clusters)
        analysis["Cluster Credit Ratings Shares"] = cluster_credit_ratings_shares
        clusters_range = self.get_cluster_ranges(credit_rating_clusters)
        clusters_share_of_overal_credit_ratings = self.get_clusters_share_of_overal_credit_ratings(credit_rating_clusters)
        analysis["Share of total companies with given credit rating in each cluter"] = clusters_share_of_overal_credit_ratings
        analysis["Cluster ranges"] = clusters_range
        clusters_metric_of_location_and_dispersion = self.get_measures_of_location_and_dispersion(credit_rating_clusters)
        analysis["Cluster metrics of location and dispersion"] = clusters_metric_of_location_and_dispersion
        clusters_entropy =  self.get_clusters_entropies(credit_rating_clusters)
        analysis["Cluster entropies"] = clusters_entropy
        max_entropy = max(clusters_entropy)
        analysis["Maximum entropy"] = max_entropy
        weighted_avg_entropy = self.compute_weigthed_avg_entropy(credit_rating_clusters)
        analysis["Weighted average entropy"] = weighted_avg_entropy
        if nb_clusters_with_various_cr_ranges or nb_clusters_with_significant_incoherencies:
            incoherencies_explanations = self.explain_incoherencies(credit_rating_clusters)
            analysis["Incoherencies explanations"] = incoherencies_explanations
        self.create_and_save_graph(credit_rating_clusters,folder_name_for_graph,alg_name)

        return analysis

    def get_clusters_share_of_overal_credit_ratings(self,credit_rating_clusters):
        shares = []
        for cluster in credit_rating_clusters:
            cluster_shares = {}
            cr_counts = cluster.get_credit_ratings_counts()
            for cr, count in cr_counts.items():
                cluster_shares[CreditRatingEncoding().compute_letter_grade_from_numeric_encoding(cr)] = count/self.credit_ratings_analyzers[cr].get_companies_count()
            shares.append(cluster_shares)
        return shares

    def get_share_of_companies_in_each_clusters(self,credit_rating_clusters):
        shares = []
        for cr_cluster in credit_rating_clusters:
            count = cr_cluster.get_companies_count() if cr_cluster.get_companies_count() else 0
            shares.append(count/len(self.cluster_labels))
        sum = 0 
        for share in shares:
            sum += share
        shares.append({"SUM":sum})
        return shares

    def create_and_save_graph(self, cr_clusters,folder_name,alg_name):
        data = {}
        for cluster_idx in range(len(cr_clusters)):
            data[("CLUSTER "+str(cluster_idx))] = cr_clusters[cluster_idx].get_list_of_credit_ratings_appearances()
        GraphingHelper().create_box_plot("Cluster","Credit Rating", alg_name+" Clusters and held credit ratings",data,folder_name)

    def get_cluster_cr_shares(self,credit_rating_clusters):
        counts = []
        for cr_cluster in credit_rating_clusters:
            counts.append(cr_cluster.get_credit_ratings_shares())
        return counts
    
    def get_measures_of_location_and_dispersion(self,credit_rating_clusters):
        measures = []
        for cr_cluster in credit_rating_clusters:
            measures.append(cr_cluster.get_measures_of_location_and_dispersion_for_credit_ratings_values())
        return measures

    def get_cluster_ranges(self,credit_rating_clusters):
        ranges = []
        for cr_cluster in credit_rating_clusters:
            ranges.append(cr_cluster.get_rating_range())
        return ranges

    def explain_incoherencies(self, credit_rating_clusters):
        clusters_with_notable_ranges = set(self.get_clusters_with_various_cr_ranges(credit_rating_clusters))
        significant_clusters = set(self.get_singificant_clusters(credit_rating_clusters))
        clusters_requiring_explanations = clusters_with_notable_ranges.union(significant_clusters)
        unique_clusters_requiring_explanations = list(set(clusters_requiring_explanations))
        explanations = {}
        for cluster_idx in range(len(unique_clusters_requiring_explanations)):
            credit_ratings_held_in_significant_proportion = unique_clusters_requiring_explanations[cluster_idx].get_credit_ratings_held_in_significant_proportions(self.PROPORTION_OF_RATING_IN_CLUSTER_CONSIDERED_SIGNIFICANT)
            cluster_explanations = {}
            for rating in credit_ratings_held_in_significant_proportion:
                analyzer = self.credit_ratings_analyzers[rating] if rating in self.credit_ratings_analyzers.keys() else None
                if analyzer:
                    important_columns = analyzer.get_top_X_most_important_columns(self.NUMBER_OF_COLUMNS_WE_WANT_EXPLAINED,self.data)
                    for col_idx in important_columns:
                        cr_col_values = analyzer.get_measures_of_location_and_dispersion(col_idx)
                        cluster_members_col_values = unique_clusters_requiring_explanations[cluster_idx].get_measures_of_location_and_dispersion_for_col_of_credit_rating_instances(col_idx, rating)
                        comparison = self.compare_cluster_and_credit_rating_values(cr_col_values,cluster_members_col_values)
                        key = "RATING " +CreditRatingEncoding().compute_letter_grade_from_numeric_encoding(rating)
                        if not (key in cluster_explanations.keys()):
                            cluster_explanations[key] = [{self.get_col_name(col_idx) if self.col_names else str(col_idx):{"Comparison":comparison,"Credit Rating Statistics":cr_col_values,"Cluster Statistics":cluster_members_col_values}}]
                        else:
                            initial_value = cluster_explanations[key]
                            initial_value.append({self.get_col_name(col_idx) if self.col_names else str(col_idx):{"Comparison":comparison,"Credit Rating Statistics":cr_col_values,"Cluster Statistics":cluster_members_col_values}})
                            cluster_explanations[key] = initial_value
            explanations["CLUSTER "+str(cluster_idx)] =  cluster_explanations
        return explanations 
           

    def compare_cluster_and_credit_rating_values(self, credit_rating_values, cluster_values):
        if cluster_values["Mean"] >= credit_rating_values["3rd Quartile"]:
            return "Cluster elements in highest 75%"
        elif cluster_values["Mean"] > credit_rating_values["Median"]:
            return "Cluster elements in upper half"
        elif cluster_values["Mean"] <= credit_rating_values["1st Quartile"]:
            return "Cluster elements in lowest 25%"
        elif cluster_values["Mean"] < credit_rating_values["Median"]:
            return "Cluster elements in lower half"
        else:
            return "Cluster elements are located around median"

    def get_col_name(self,col_idx):
        if not self.col_names:
            return ""
        elif col_idx >= len(self.col_names):
            raise IndexError
        else:
            return self.col_names[col_idx]
    
    def compute_weigthed_avg_entropy(self,credit_rating_clusters):
        weighted_sum = 0
        for cr_cluster_idx in range(len(credit_rating_clusters)):
            credit_rating_cluster = credit_rating_clusters[cr_cluster_idx]
            weighted_sum += credit_rating_cluster.get_entropy()*(credit_rating_cluster.get_companies_count()/len(self.data))
        return weighted_sum
    
    def get_clusters_entropies(self, credit_rating_clusters):
        entropies = []
        for cr_cluster in credit_rating_clusters:
            entropies.append(cr_cluster.get_entropy())
        return entropies

    def get_singificant_clusters(self, credit_rating_clusters):
        clusters = []
        for cr_cluster in credit_rating_clusters:
            if cr_cluster.get_is_significant_cluster():
                clusters.append(cr_cluster) 
        return clusters 
    
    def get_clusters_with_various_cr_ranges(self, credit_rating_clusters):
        clusters = []
        for cr_cluster in credit_rating_clusters:
            if cr_cluster.get_rating_range() > 4:
                clusters.append(cr_cluster)
        return clusters
        
    def create_credit_rating_clusters(self):
        credit_rating_clusters = {}
        for element_idx in range(len(self.cluster_labels)):
            label = self.cluster_labels[element_idx]
            if label in credit_rating_clusters.keys():
                credit_rating_clusters[label].add_clustered_credit_rating(self.row_credit_ratings[element_idx], self.data[element_idx],element_idx)
            else:
                new_credit_rating_cluster = CreditRatingCluster(self.ENCODING_FIRST_JUNK_RATING,self.JUNK_INVEST_GRADE_SPLIT_CONSIDERED_SIGNIFICANT)
                new_credit_rating_cluster.add_clustered_credit_rating(self.row_credit_ratings[element_idx], self.data[element_idx],element_idx)
                credit_rating_clusters[label] = new_credit_rating_cluster
        return list(credit_rating_clusters.values())