import os
import json
from analysis.data_configuration import DataConfiguration
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.dimensionality_evaluation import DimensionalityEvaluation
from data_preparation.data_preparator import DataPreparator
from data_treatment.principal_component_analysis import PrincipalComponentAnalysis
from analysis.conclusion_1.iterators.birch_super_iterator import BIRCHSuperIterator
from analysis.conclusion_1.iterators.dbscan_iterator import DBSCANIterator
from analysis.conclusion_1.iterators.fast_global_kmeans_iterator import FastGlobalKMeansIterator
from analysis.conclusion_1.iterators.fuzzy_cmean_iterator import FuzzyCMeansIterator
from analysis.conclusion_1.iterators.kmeans_iterator import KMeansIterator
from analysis.data_configuration import DataConfiguration

class AlgorithmsBestPerformanceEvaluation:

    def __init__(self,run_pca=False):
        self.RESULTS_FILE_NAME = "performance_metrics.json"
        self.run_pca = run_pca
        self.set_configurations_to_test()
    
    def set_configurations_to_test(self):
        credit_health_avg = DataConfiguration()
        credit_health_avg.set_to_default_configuration("CREDIT HEALTH",average_by_category=True)
        credit_model_avg = DataConfiguration()
        credit_model_avg.set_to_default_configuration("CREDIT MODEL",average_by_category=True)
        both_config_credit_health_and_credit_model_avg = DataConfiguration()
        both_config_credit_health_and_credit_model_avg.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",average_by_category=True)
        credit_health__config = DataConfiguration()
        credit_health__config.set_to_default_configuration("CREDIT HEALTH")
        credit_model_config = DataConfiguration()
        credit_model_config.set_to_default_configuration("CREDIT MODEL")
        both_config_credit_health_and_credit_model = DataConfiguration()
        both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL")
        self.configurations_to_test = {"CREDIT HEALTH - CR PILAR AVERAGES":credit_health_avg,"CREDIT MODEL - CR PILAR AVERAGES":credit_model_avg,"BOTH CREDIT HEALTH AND CREDIT MODEL":both_config_credit_health_and_credit_model_avg,"CREDIT HEALTH":credit_health__config,"CREDIT MODEL":credit_model_config,"BOTH CREDIT HEALTH AND CREDIT MODEL":both_config_credit_health_and_credit_model}
    
    def get_optimal_parameters(self):
        optimal_col_emptiness_tresholds = EmptyRowsDeletionEvaluation(self.configurations_to_test).run_evaluation()
        optimal_dimensions = DimensionalityEvaluation(self.configurations_to_test).run_evaluation(optimal_col_emptiness_tresholds)
        return optimal_col_emptiness_tresholds,optimal_dimensions
    
    def run_evaluation(self):
        algorithms_best_perf = {}
        algorithms_perf_on_others_optimal_K = {}
        algorithms_perf_on_nb_unique_credit_ratings = {}
        algorithms_best_perf_K_superior_credit_ratings_count = {}
        optimal_col_emptiness_tresholds,optimal_dimensions = self.get_optimal_parameters()
        for config in self.configurations_to_test.keys():
            optimal_ks = set()
            folder_name = self.get_folder_name(config)
            config_optimal_results = {}
            data,nb_credit_ratings = self.prepare_data(config,optimal_col_emptiness_tresholds,optimal_dimensions)
            max_k_value_to_test = nb_credit_ratings+10
            birch_iterator = self.measure_birch_optimality(data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test)
            print("********* BIRCH DONE *********")
            dbscan_iterator = self.measure_dbscan_optimality(data,config_optimal_results,optimal_ks,folder_name)
            print("********* DBSCAN DONE *********")
            kmeans_iterator = self.measure_kmeans_optimality(data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test)
            print("********* KMEANS DONE *********")
            fgkm_iterator = self.measure_fast_global_kmeans_optimality(data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test)
            print("********* FGKM DONE *********")
            fuzzy_cmeans_iterator = self.measure_fuzzy_cmeans_optimality(data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test)
            print("********* FUZZY C DONE *********")
            algorithms_best_perf[config] = config_optimal_results
            perf_on_respective_optimals = self.compute_algs_performance_on_each_others_optimals(optimal_ks,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator)
            algorithms_perf_on_others_optimal_K[config] = perf_on_respective_optimals
            best_perf_when_K_greater_than_nb_credit_ratings = self.compute_algs_performance_when_K_greater_credit_ratings_count(nb_credit_ratings,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator,max_k_value_to_test)
            algorithms_best_perf_K_superior_credit_ratings_count[config] = best_perf_when_K_greater_than_nb_credit_ratings
            perf_on_clusters_count = self.compute_algs_performance_on_nb_cluster(nb_credit_ratings,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator)
            algorithms_perf_on_nb_unique_credit_ratings[config] = perf_on_clusters_count
        self.save_results(algorithms_best_perf,algorithms_perf_on_others_optimal_K,algorithms_perf_on_nb_unique_credit_ratings,algorithms_best_perf_K_superior_credit_ratings_count)
        self.print_results(algorithms_best_perf,algorithms_perf_on_others_optimal_K,algorithms_perf_on_nb_unique_credit_ratings,algorithms_best_perf_K_superior_credit_ratings_count)
        return algorithms_best_perf,algorithms_perf_on_others_optimal_K
    
    def save_results(self,algorithms_best_perf,algorithms_perf_on_others_optimal_K,algorithms_perf_on_nb_unique_credit_ratings,algorithms_best_perf_K_superior_credit_ratings_count):
        data = {}
        data["algorithms best performance"] = algorithms_best_perf
        data["algorithms performance on others optimal K number"] = algorithms_perf_on_others_optimal_K
        data["algorithms performance on number of unique credit ratings"] = algorithms_perf_on_nb_unique_credit_ratings
        data["algorithms best performance when K>number of credit ratings"] = algorithms_best_perf_K_superior_credit_ratings_count
        file_path = os.path.join(self.get_folder_name(), self.RESULTS_FILE_NAME)
        # Write the dictionary to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

    def get_folder_name(self, config_name=None):
        folder_name = "conclusion_1_graphs/algorithms_comparisons/"
        if self.run_pca:
            folder_name +="/with_pca"
        else:
            folder_name +="/without_pca"
        if config_name:
            folder_name += "/"+config_name
        return folder_name

    def compute_algs_performance_on_nb_cluster(self,nb_clusters,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator):
        perf_on_clusters_count = {}
        kmeans_perf = kmeans_iterator.get_performance_on_given_K(nb_clusters)
        perf_on_clusters_count[kmeans_iterator.alg_name] = kmeans_perf
        birch_perf = birch_iterator.get_performance_on_given_K(nb_clusters)
        perf_on_clusters_count[birch_iterator.alg_name] = birch_perf
        fuzzy_cmeans_perf = fuzzy_cmeans_iterator.get_performance_on_given_K(nb_clusters)
        perf_on_clusters_count[fuzzy_cmeans_iterator.alg_name] = fuzzy_cmeans_perf
        fgkm_perf = fgkm_iterator.get_performance_on_given_K(nb_clusters)
        perf_on_clusters_count[fgkm_iterator.alg_name] = fgkm_perf
        dbscan_perf = dbscan_iterator.get_performance_on_given_K(nb_clusters)
        perf_on_clusters_count[dbscan_iterator.alg_name] = dbscan_perf
        return perf_on_clusters_count

    def compute_algs_performance_when_K_greater_credit_ratings_count(self,nb_credit_ratings,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator,max_k_value_to_test):
        result = {}
        result["BIRCH"] = self.get_best_alg_performance_on_given_range_from_iterator(birch_iterator,nb_credit_ratings,max_k_value_to_test)
        result["DBSCAN"] = self.get_best_alg_performance_on_given_range_from_iterator(dbscan_iterator,nb_credit_ratings,max_k_value_to_test)
        result["K-MEANS"] = self.get_best_alg_performance_on_given_range_from_iterator(kmeans_iterator,nb_credit_ratings,max_k_value_to_test)
        result["Fast Global K-Means"] = self.get_best_alg_performance_on_given_range_from_iterator(fgkm_iterator,nb_credit_ratings,max_k_value_to_test)
        result["Fuzz C-Means"] = self.get_best_alg_performance_on_given_range_from_iterator(fuzzy_cmeans_iterator,nb_credit_ratings,max_k_value_to_test)
        return result
    
    def get_best_alg_performance_on_given_range_from_iterator(self,iterator,min_val,max_val):
        best_calinski_harabasz = 0
        best_silhouette_score = 0
        best_perf = None
        for i in range(min_val,max_val+1):
            result = iterator.get_performance_on_given_K(i)
            if result and "Silhouette Score" in result.keys() and "Calinski Harabasz Index" in result.keys() and result["Silhouette Score"] > best_silhouette_score and result["Calinski Harabasz Index"] > best_calinski_harabasz:
                best_perf = result
                best_calinski_harabasz = result["Calinski Harabasz Index"]
                best_silhouette_score = result["Silhouette Score"]
        return best_perf
    
    def compute_algs_performance_on_each_others_optimals(self,optimal_ks,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator):
        perf_on_respective_optimals = {}
        for K in optimal_ks:
            perf_on_respective_optimals[K] = {}
            kmeans_perf = kmeans_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][kmeans_iterator.alg_name] = kmeans_perf
            birch_perf = birch_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][birch_iterator.alg_name] = birch_perf
            fuzzy_cmeans_perf = fuzzy_cmeans_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][fuzzy_cmeans_iterator.alg_name] = fuzzy_cmeans_perf
            fgkm_perf = fgkm_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][fgkm_iterator.alg_name] = fgkm_perf
            dbscan_perf = dbscan_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][dbscan_iterator.alg_name] = dbscan_perf
        return perf_on_respective_optimals

    def print_results(self,algorithms_best_perf,algorithms_perf_on_others_optimal_K,algorithms_perf_on_nb_unique_credit_ratings,algorithms_best_perf_K_superior_credit_ratings_count):
        print("***************************************************************\n")
        if self.run_pca:
            print("!!!!!!!!!!!!!! CONCLUSION 1 (WITH PCA) RESULTS !!!!!!!!!!!!!!\n")
        else:
            print("!!!!!!!!!!!!!! CONCLUSION 1 (WITHOUT PCA) RESULTS !!!!!!!!!!!!!!\n")
        print("############## OPTIMAL PERFORMANCE OF THE ALGORITHMS ##############\n")
        print(algorithms_best_perf)
        print("\n############## PERFORMANCE ON OTHERS OPTIMAL K ##############\n")
        print(algorithms_perf_on_others_optimal_K)
        print("\n############## PERFORMANCE ON NUMBER OF UNIQUE CREDIT RATINGS ##############\n")
        print(algorithms_perf_on_nb_unique_credit_ratings)
        print("\n############## PERFORMANCE WHEN K>NUMBER OF CREDIT RATINGS ##############\n")
        print(algorithms_best_perf_K_superior_credit_ratings_count)
        print("\n***************************************************************")

    def measure_fuzzy_cmeans_optimality(self,data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test):
        fuzzy_cmeans_iterator = FuzzyCMeansIterator(data,max_k_value_to_test)
        fuzzy_cm_optimal_config = fuzzy_cmeans_iterator.iterate()
        config_optimal_results[fuzzy_cmeans_iterator.alg_name] = fuzzy_cm_optimal_config
        optimal_ks.add(fuzzy_cm_optimal_config["C"])
        fuzzy_cmeans_iterator.graph(folder_name)
        return fuzzy_cmeans_iterator

    def measure_fast_global_kmeans_optimality(self,data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test):
        #  nb_credit_ratings bcs Fast Global KMeans is very slow 
        fast_global_kmeans_iterator = FastGlobalKMeansIterator(data,max_k_value_to_test)
        fgkm_optimal_config = fast_global_kmeans_iterator.iterate()
        config_optimal_results[fast_global_kmeans_iterator.alg_name] = fgkm_optimal_config
        optimal_ks.add(fgkm_optimal_config["K"])
        fast_global_kmeans_iterator.graph(folder_name)
        return fast_global_kmeans_iterator

    def measure_kmeans_optimality(self,data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test):
        kmeans_iterator = KMeansIterator(data,max_k_value_to_test)
        kmeans_optimal_config = kmeans_iterator.iterate()
        config_optimal_results[kmeans_iterator.alg_name] = kmeans_optimal_config
        optimal_ks.add(kmeans_optimal_config["K"])
        kmeans_iterator.graph(folder_name)
        return kmeans_iterator
    
    def measure_dbscan_optimality(self,data,config_optimal_results,optimal_ks,folder_name):
        dbscan_iterator = DBSCANIterator(data)
        dbscan_optimal_config = dbscan_iterator.iterate()
        config_optimal_results[dbscan_iterator.alg_name] = dbscan_optimal_config
        optimal_ks.add(dbscan_optimal_config["Calinski Harabasz Index Optimum"]["Number of Clusters"])
        optimal_ks.add(dbscan_optimal_config["Silhouette Score Optimum"]["Number of Clusters"])
        dbscan_iterator.graph(folder_name)
        return dbscan_iterator

    def measure_birch_optimality(self,data,config_optimal_results,optimal_ks,folder_name,max_k_value_to_test):
        birch_iterator = BIRCHSuperIterator(data,max_k_value_to_test)
        birch_optimal_config = birch_iterator.iterate()
        config_optimal_results[birch_iterator.alg_name] = birch_optimal_config
        optimal_ks.add(birch_optimal_config["Calinski Harabasz Index Optimum"]["K"])
        optimal_ks.add(birch_optimal_config["Silhouette Score Optimum"]["K"])
        birch_iterator.graph(folder_name)
        return birch_iterator

    def prepare_data(self,config,optimal_col_emptiness_tresholds,optimal_dimensions):
        col_emptiness_thresh = optimal_col_emptiness_tresholds[config]
        dimensionality = optimal_dimensions[config]
        configuration = DataConfiguration()
        configuration.set_to_default_configuration("RAW NUMBERS")
        data_preparator = DataPreparator(data_source=configuration.get_data_source(),configuration=configuration)
        data = data_preparator.apply_configuration(col_emptiness_thresh)
        credit_ratings = data_preparator.get_credit_ratings()
        unique_credit_ratings = set(credit_ratings)
        if self.run_pca:
            dimensioned_data = PrincipalComponentAnalysis(data,dimensionality).reduce_dimensionality()
            return dimensioned_data,len(unique_credit_ratings)
        else:
            return data,len(unique_credit_ratings)