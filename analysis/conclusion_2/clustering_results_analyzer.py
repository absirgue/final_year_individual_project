import os
from data_treatment.principal_component_analysis import PrincipalComponentAnalysis
from analysis.data_configuration import DataConfiguration
from data_preparation.data_preparator import DataPreparator
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.dimensionality_evaluation import DimensionalityEvaluation
from analysis.conclusion_2.credit_rating_analyzer import CreditRatingAnalyzer
from analysis.conclusion_2.analysers.birch_analyser import BIRCHAnalyser
from analysis.conclusion_2.analysers.dbscan_analyser import DBSCANAnalyser
from analysis.conclusion_2.analysers.fast_global_kmeans_analyser import FastGlobalKMeansAnalyser
from analysis.conclusion_2.analysers.kmeans_analyser import KMeansAnalyser
from analysis.conclusion_2.analysers.fuzzy_c_means_analyser import FuzzyCMeansAnalyser
from analysis.json_helper import JSONHelper
from graph.graphing_helper import GraphingHelper
from interface_beautifier import InterfaceBeautifier
from data_preparation.credit_rating_encoding import CreditRatingEncoding

class ClusteringResultsAnalyzer:
    """
    Coordinates all actions for the analysis of all clustering results for all algorithms
    and across all data configurations and constraint for hyperparameter optimisation.
    """
    def __init__(self, source_file_path, output_dir,with_pca,configuration):
        self.clustering_results = JSONHelper().read(source_file_path)
        self.output_dir = output_dir
        self.configurations_to_study = configuration
        self.with_pca = with_pca

    def analyse(self):
        folder_name = self.output_dir
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

    """
    Performs the analysis of a specific data configurationa across all algorithms
    and constraints for hyperparameter optimisation.
    """
    def analyse_config(self, config_name, performances,folder_name):
        InterfaceBeautifier().print_major_annoucement("Analysing configuration "+config_name)
        folder_name += config_name + "/"
        if config_name in self.configurations_to_study:
            data_configuration = self.configurations_to_study[config_name]
        else:
            data_configuration = DataConfiguration()
            data_configuration.set_to_default_configuration(config_name)
        optimal_col_emptiness_treshold = EmptyRowsDeletionEvaluation({config_name:data_configuration}).run_evaluation()
        data_preparator = DataPreparator(data_source=data_configuration.get_data_source(),configuration=data_configuration)
        data = data_preparator.apply_configuration(optimal_col_emptiness_treshold[config_name])
        credit_ratings = data_preparator.get_credit_ratings()
        encoding_first_junk = CreditRatingEncoding().get_encoding_first_junk_rating()
        col_names = None
        if self.with_pca:
            optimal_dimensions = DimensionalityEvaluation({config_name:data_configuration}).run_evaluation({config_name:optimal_col_emptiness_treshold[config_name]})
            data = PrincipalComponentAnalysis(data,optimal_dimensions[config_name]).reduce_dimensionality()
        else:
            col_names = data_preparator.get_column_names()
            InterfaceBeautifier().print_information_statement("Analyser is not running PCA")
        entity_ids = data_preparator.get_entity_ids()
        credit_rating_analyzers = self.generate_credit_ratings_analysers(credit_ratings,data)
        InterfaceBeautifier().print_information_statement("Credit rating analysers have been generated")
        singificant_cluster_counts = {}
        if "BIRCH" in performances.keys() and performances["BIRCH"]:
            birch_analyser = BIRCHAnalyser(data_configuration.get_data_source(),entity_ids,col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            birch_analyser.analyse(performances["BIRCH"])
            name, significant_clusters_count = birch_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        InterfaceBeautifier().print_percentage_progress("Progress on Result Analysis",20)
        if "Fuzzy C-Means" in performances.keys() and performances["Fuzzy C-Means"]:
            fuzzy_c_analyser = FuzzyCMeansAnalyser(data_configuration.get_data_source(),entity_ids,col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            fuzzy_c_analyser.analyse(performances["Fuzzy C-Means"])
            name, significant_clusters_count = fuzzy_c_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        InterfaceBeautifier().print_percentage_progress("Progress on Result Analysis",40)
        if "K-Means" in performances.keys() and performances["K-Means"]:
            kmeans_analyser = KMeansAnalyser(data_configuration.get_data_source(),entity_ids,col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            kmeans_analyser.analyse(performances["K-Means"])
            name, significant_clusters_count = kmeans_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        InterfaceBeautifier().print_percentage_progress("Progress on Result Analysis",60)
        if "Fast Global K-Means" in performances.keys() and performances["Fast Global K-Means"]:
            fgkm_analyser = FastGlobalKMeansAnalyser(data_configuration.get_data_source(),entity_ids,col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            fgkm_analyser.analyse(performances["Fast Global K-Means"])
            name, significant_clusters_count = fgkm_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        InterfaceBeautifier().print_percentage_progress("Progress on Result Analysis",80)
        if "DBSCAN" in performances.keys() and performances["DBSCAN"]:
            dbscan_analyser = DBSCANAnalyser(data_configuration.get_data_source(),entity_ids,col_names,encoding_first_junk,folder_name,data,credit_ratings,credit_rating_analyzers)
            dbscan_analyser.analyse(performances["DBSCAN"])
            name, significant_clusters_count = dbscan_analyser.get_name_and_significant_cluster_count()
            singificant_cluster_counts[name] = significant_clusters_count
        InterfaceBeautifier().print_percentage_progress("Progress on Result Analysis",100)
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