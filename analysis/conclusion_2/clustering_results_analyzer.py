import json
import os
import numpy as np
from sklearn.cluster import Birch
from sklearn.cluster import DBSCAN
from clustering.fast_global_k_means import FastGlobalKMeans
from skfuzzy.cluster import cmeans
from data_treatment.principal_component_analysis import PrincipalComponentAnalysis
from sklearn.cluster import KMeans
from analysis.data_configuration import DataConfiguration
from data_preparation.data_preparator import DataPreparator
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.dimensionality_evaluation import DimensionalityEvaluation
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer
from analysis.conclusion_2.credit_rating_analyzer import CreditRatingAnalyzer
from analysis.conclusion_2.analysers.birch_analyser import BIRCHAnalyser
from analysis.conclusion_2.analysers.dbscan_analyser import DBSCANAnalyser
from analysis.conclusion_2.analysers.fast_global_kmeans_analyser import FastGlobalKMeansAnalyser
from analysis.conclusion_2.analysers.kmeans_analyser import KMeansAnalyser
from analysis.conclusion_2.analysers.fuzzy_c_means_analyser import FuzzyCMeansAnalyser
from analysis.json_helper import JSONHelper
from graph.graphing_helper import GraphingHelper

class ClusteringResultsAnalyzer:
    def __init__(self, source_file_path, output_dir,with_pca):
        self.clustering_results = JSONHelper().read(source_file_path)
        self.output_dir = output_dir
        self.optimal_col_emptiness_tresholds = EmptyRowsDeletionEvaluation().run_evaluation()
        self.with_pca = with_pca
        if self.with_pca:
            self.optimal_dimensions = DimensionalityEvaluation().run_evaluation(self.optimal_col_emptiness_tresholds)

    def analyse(self):
        folder_name = "conclusion_2_results/"
        if self.with_pca:
            folder_name += "with_pca/"
        else:
            folder_name += "without_pca/"
        self.analyse_algorithms_best_performance_with_K_superior_to_credit_ratings_count(folder_name)
        self.analyse_algorithms_best_performance_with_credit_ratings_count(folder_name)
        self.analyse_algorithms_best_performance(folder_name)
        
    def analyse_algorithms_best_performance_with_K_superior_to_credit_ratings_count(self,folder_name):
        folder_name += "greater_than_number_of_credit_ratings/"
        for config_name in self.clustering_results["algorithms best performance when K>number of credit ratings"].keys():
            self.analyse_config(config_name,self.clustering_results["algorithms best performance when K>number of credit ratings"][config_name],folder_name)

    def analyse_algorithms_best_performance_with_credit_ratings_count(self,folder_name):
        folder_name += "number_of_credit_ratings/"
        for config_name in self.clustering_results["algorithms performance on number of unique credit ratings"].keys():
            self.analyse_config(config_name,self.clustering_results["algorithms performance on number of unique credit ratings"][config_name],folder_name)

    def analyse_algorithms_best_performance(self,folder_name):
        folder_name += "best_performance/"
        for config_name in self.clustering_results["algorithms best performance"].keys():
            self.analyse_config(config_name,self.clustering_results["algorithms best performance"][config_name],folder_name)

    def analyse_config(self, config_name, performances,folder_name):
        print("ANALYSING CONFIG " + config_name)
        folder_name += config_name + "/"
        data_configuration = DataConfiguration()
        data_configuration.set_to_default_configuration(config_name)
        data_preparator = DataPreparator(data_source=data_configuration.get_data_source(),configuration=data_configuration)
        data = data_preparator.apply_configuration(self.optimal_col_emptiness_tresholds[config_name])
        credit_ratings = data_preparator.get_credit_ratings()
        encoding_first_junk = data_preparator.get_encoding_of_first_junk_rating()
        col_names = None
        if self.with_pca:
            data = PrincipalComponentAnalysis(data,self.optimal_dimensions[config_name]).reduce_dimensionality()
        else:
            col_names = data_preparator.get_column_names()
            print("NOT RUNNING PCA")
        credit_rating_analyzers = self.generate_credit_ratings_analysers(credit_ratings,data)
        print("GENERATED CREDIT RATING ANALYSERS")
        singificant_cluster_counts = {}
        if "BIRCH" in performances.keys() and performances["BIRCH"]:
            birch_analyser = BIRCHAnalyser(col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            birch_analyser.analyse(performances["BIRCH"])
            name, significant_clusters_count = birch_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        if "Fuzzy C-Means" in performances.keys() and performances["Fuzzy C-Means"]:
            fuzzy_c_analyser = FuzzyCMeansAnalyser(col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            fuzzy_c_analyser.analyse(performances["Fuzzy C-Means"])
            name, significant_clusters_count = fuzzy_c_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        if "K-Means" in performances.keys() and performances["K-Means"]:
            kmeans_analyser = KMeansAnalyser(col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            kmeans_analyser.analyse(performances["K-Means"])
            name, significant_clusters_count = kmeans_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        if "Fast Global K-Means" in performances.keys() and performances["Fast Global K-Means"]:
            fgkm_analyser = FastGlobalKMeansAnalyser(col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            fgkm_analyser.analyse(performances["Fast Global K-Means"])
            name, significant_clusters_count = fgkm_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        if "DBSCAN" in performances.keys() and performances["DBSCAN"]:
            dbscan_analyser = DBSCANAnalyser(col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            dbscan_analyser.analyse(performances["DBSCAN"])
            name, significant_clusters_count = dbscan_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        GraphingHelper().create_bar_chart_from_dictionary(singificant_cluster_counts,"Algorithm Name", "Number of Significant Clusters","Number of Significant Clusters for each Algorithm", folder_name)

    def generate_credit_ratings_analysers(self,credit_ratings,data):
        credit_ratings_analysers = {}
        for cr_idx in range(len(credit_ratings)):
            if credit_ratings[cr_idx] in credit_ratings_analysers.keys():
                analyser = credit_ratings_analysers[credit_ratings[cr_idx]]
                analyser.insert_company(credit_ratings[cr_idx], data[cr_idx])
            else:
                analyser = CreditRatingAnalyzer()
                analyser.insert_company(credit_ratings[cr_idx], data[cr_idx])
                credit_ratings_analysers[credit_ratings[cr_idx]] = analyser
        return credit_ratings_analysers
    
    def analyse_birch(self, col_names,encoding_first_junk,folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers):
        optimum_names = ["Calinski Harabasz Index Optimum","Silhouette Score Optimum"]
        for optimum in optimum_names:
            birch = Birch(threshold=float(performance_metrics[optimum]["Threshold Value"]), branching_factor=int(performance_metrics[optimum]["Branching Factor"]), n_clusters=int(performance_metrics[optimum]["K"])).fit(data)
            labels = birch.labels_
            self.analyse_alg_optimum(col_names,encoding_first_junk,labels,"BIRCH",folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers,optimum)
    
    def analyse_alg_optimum(self,col_names,encoding_first_junk,labels,alg_name,folder_name, data, credit_ratings, performance_metrics,credit_rating_analyzers,optimum):
        analysis = {}
        analysis["Algorithm Parameters"] = {"Threshold Value":performance_metrics[optimum]["Threshold Value"],"Braching Factor":performance_metrics[optimum]["Branching Factor"],"K":performance_metrics[optimum]["K"]}
        if "calinski" in optimum.lower():
            analysis["Algorithm Performance"] = {"Calinski Harabasz Index":performance_metrics[optimum]["Calinski Harabasz Index"]}
        elif "silhouette" in optimum.lower():
            analysis["Algorithm Performance"] = {"Silhouette Score":performance_metrics[optimum]["Silhouette Score"]}
        cluster_analyzer = ClustersAnalyzer(encoding_first_junk,labels,credit_ratings,credit_rating_analyzers,data,col_names)
        analysis["Clusters Content Analysis"] = cluster_analyzer.analyze()
        self.save_analysis(folder_name,alg_name+"_"+optimum,analysis)
    