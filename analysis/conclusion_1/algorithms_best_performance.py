from analysis.data_configuration import DataConfiguration
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
from analysis.dimensionality_evaluation import DimensionalityEvaluation
from data_preparation.data_preparator import DataPreparator
from data_treatment.principal_component_analysis import PrincipalComponentAnalysis
from analysis.conclusion_1.birch_super_iterator import BIRCHSuperIterator
from analysis.conclusion_1.dbscan_iterator import DBSCANIterator
from analysis.conclusion_1.fast_global_kmeans_iterator import FastGlobalKMeansIterator
from analysis.conclusion_1.fuzzy_cmean_iterator import FuzzyCMeansIterator
from analysis.conclusion_1.kmeans_iterator import KMeansIterator
from analysis.data_configuration import DataConfiguration

class AlgorithmsBestPerformanceEvaluation:

    def __init__(self,data_source):
        self.data_source = data_source
        self.set_configurations_to_test()
        self.MAX_NUMBER_OF_CLUSTERS_TO_TRY = 80
    
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
        optimal_col_emptiness_tresholds,optimal_dimensions = self.get_optimal_parameters()
        print(optimal_col_emptiness_tresholds)
        print(optimal_dimensions)
        for config in self.configurations_to_test.keys():
            folder_name = "conclusion_1_graphs/algorithms_comparisons/"+config
            config_results = {}
            col_emptiness_thresh = optimal_col_emptiness_tresholds[config]
            dimensionality = optimal_dimensions[config]
            configuration = DataConfiguration()
            configuration.set_to_default_configuration("RAW NUMBERS")
            data = DataPreparator(data_source=self.data_source,configuration=configuration).apply_configuration(col_emptiness_thresh)
            print("DATA SHAPES")
            print(data.shape[1])
            print(data.shape[0])
            dimensioned_data = PrincipalComponentAnalysis(data,dimensionality).reduce_dimensionality()
            print("DIM SHAPES")
            print(dimensioned_data.shape[1])
            print(dimensioned_data.shape[0])
            # BIRCH
            birch_iterator = BIRCHSuperIterator(dimensioned_data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
            config_results[birch_iterator.alg_name] = birch_iterator.iterate()
            birch_iterator.graph(folder_name)
            print("BIRCH DONE")
            print(config_results)
            print("\n\n")
            # DBSCAN
            dbscan_iterator = DBSCANIterator(dimensioned_data)
            config_results[dbscan_iterator.alg_name] = dbscan_iterator.iterate()
            dbscan_iterator.graph(folder_name)
            print("DBSCAN DONE")
            print(config_results)
            print("\n\n")
            # KMeans
            kmeans_iterator = KMeansIterator(dimensioned_data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
            config_results[kmeans_iterator.alg_name] = kmeans_iterator.iterate()
            kmeans_iterator.graph(folder_name)
            print("KM DONE")
            print(config_results)
            print("\n\n")
            # Fast Global KMeans
            print("FGKM DONE")
            print(config_results)
            print("\n\n")
            fast_global_kmeans_iterator = FastGlobalKMeansIterator(dimensioned_data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
            config_results[fast_global_kmeans_iterator.alg_name] = fast_global_kmeans_iterator.iterate()
            fast_global_kmeans_iterator.graph(folder_name)
            # Fuzzy CMeans
            fuzzy_cmeans_iterator = FuzzyCMeansIterator(dimensioned_data,self.MAX_NUMBER_OF_CLUSTERS_TO_TRY)
            config_results[fuzzy_cmeans_iterator.alg_name] = fuzzy_cmeans_iterator.iterate()
            fuzzy_cmeans_iterator.graph(folder_name)
            algorithms_best_perf[config] = config_results
            print("FUZZY DONE")
            print(config_results)
            print("\n\n")
            print("algorithms_best_perf")
            print(algorithms_best_perf)
            print("config_results")
            print(config_results)
        print("done")
        print(algorithms_best_perf)