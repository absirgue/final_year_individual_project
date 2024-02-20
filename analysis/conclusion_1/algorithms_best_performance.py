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

    def __init__(self,data_source):
        self.data_source = data_source
        self.set_configurations_to_test()
        # self.MAX_NUMBER_OF_CLUSTERS_TO_TRY = 80
        self.MAX_NUMBER_OF_CLUSTERS_TO_TRY=3
    
    def set_configurations_to_test(self):
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS")
        both_config = DataConfiguration()
        both_config.set_to_default_configuration("BOTH")
        self.configurations_to_test = {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH":both_config}
    
    def get_optimal_parameters(self):
        optimal_col_emptiness_tresholds = EmptyRowsDeletionEvaluation().run_evaluation(self.data_source)
        optimal_dimensions = DimensionalityEvaluation().run_evaluation(self.data_source,optimal_col_emptiness_tresholds)
        return optimal_col_emptiness_tresholds,optimal_dimensions
    
    def run_evaluation(self):
        algorithms_best_perf = {}
        algorithms_perf_on_others_optimal_K = {}
        optimal_col_emptiness_tresholds,optimal_dimensions = self.get_optimal_parameters()
        print(optimal_col_emptiness_tresholds)
        print(optimal_dimensions)
        for config in self.configurations_to_test.keys():
            optimal_ks = set()
            folder_name = "conclusion_1_graphs/algorithms_comparisons/"+config
            config_optimal_results = {}
            data = self.prepare_data(config,optimal_col_emptiness_tresholds,optimal_dimensions)
            birch_iterator = self.measure_birch_optimality(data,config_optimal_results,optimal_ks,folder_name)
            dbscan_iterator = self.measure_dbscan_optimality(data,config_optimal_results,optimal_ks,folder_name)
            kmeans_iterator = self.measure_kmeans_optimality(data,config_optimal_results,optimal_ks,folder_name)
            fgkm_iterator = self.measure_fast_global_kmeans_optimality(data,config_optimal_results,optimal_ks,folder_name)
            fuzzy_cmeans_iterator = self.measure_fuzzy_cmeans_optimality(data,config_optimal_results,optimal_ks,folder_name)
            algorithms_best_perf[config] = config_optimal_results
            perf_on_respective_optimals = self.compute_algs_performance_on_each_others_optimals(optimal_ks,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator)
            algorithms_perf_on_others_optimal_K[config] = perf_on_respective_optimals
        self.print_results(algorithms_best_perf,algorithms_perf_on_others_optimal_K)
        return algorithms_best_perf,algorithms_perf_on_others_optimal_K
    
    def compute_algs_performance_on_each_others_optimals(self,optimal_ks,kmeans_iterator,birch_iterator,dbscan_iterator,fuzzy_cmeans_iterator,fgkm_iterator):
        perf_on_respective_optimals = {}
        for K in optimal_ks:
            perf_on_respective_optimals[K] = {}
            kmeans_perf = kmeans_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][kmeans_iterator.alg_name] = kmeans_perf
            birch_perf = birch_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][birch_iterator.alg_name] = birch_perf
            fuzzy_cmeans_perf = fuzzy_cmeans_iterator.get_performance_on_given_C(K)
            perf_on_respective_optimals[K][fuzzy_cmeans_iterator.alg_name] = fuzzy_cmeans_perf
            fgkm_perf = fgkm_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][fgkm_iterator.alg_name] = fgkm_perf
            dbscan_perf = dbscan_iterator.get_performance_on_given_K(K)
            perf_on_respective_optimals[K][dbscan_iterator.alg_name] = dbscan_perf
        return perf_on_respective_optimals

    def print_results(self,algorithms_best_perf,algorithms_perf_on_others_optimal_K):
        print("***************************************************************\n")
        print("!!!!!!!!!!!!!! CONCLUSION 1 RESULTS !!!!!!!!!!!!!!\n")
        print("############## OPTIMAL PERFORMANCE OF THE ALGORITHMS ##############\n")
        print(algorithms_best_perf)
        print("\n############## PERFORMANCE ON OTHERS OPTIMAL K ##############\n")
        print(algorithms_perf_on_others_optimal_K)
        print("\n***************************************************************")

    def measure_fuzzy_cmeans_optimality(self,data,config_optimal_results,optimal_ks,folder_name):
        fuzzy_cmeans_iterator = FuzzyCMeansIterator(data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
        fuzzy_cm_optimal_config = fuzzy_cmeans_iterator.iterate()
        config_optimal_results[fuzzy_cmeans_iterator.alg_name] = fuzzy_cm_optimal_config
        optimal_ks.add(fuzzy_cm_optimal_config["C"])
        fuzzy_cmeans_iterator.graph(folder_name)
        return fuzzy_cmeans_iterator

    def measure_fast_global_kmeans_optimality(self,data,config_optimal_results,optimal_ks,folder_name):
        fast_global_kmeans_iterator = FastGlobalKMeansIterator(data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
        fgkm_optimal_config = fast_global_kmeans_iterator.iterate()
        config_optimal_results[fast_global_kmeans_iterator.alg_name] = fgkm_optimal_config
        optimal_ks.add(fgkm_optimal_config["K"])
        fast_global_kmeans_iterator.graph(folder_name)
        return fast_global_kmeans_iterator

    def measure_kmeans_optimality(self,data,config_optimal_results,optimal_ks,folder_name):
        kmeans_iterator = KMeansIterator(data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
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

    def measure_birch_optimality(self,data,config_optimal_results,optimal_ks,folder_name):
        birch_iterator = BIRCHSuperIterator(data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
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
        data = DataPreparator(data_source=self.data_source,configuration=configuration).apply_configuration(col_emptiness_thresh)
        dimensioned_data = PrincipalComponentAnalysis(data,dimensionality).reduce_dimensionality()
        return dimensioned_data