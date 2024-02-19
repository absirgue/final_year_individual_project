from analysis.data_configuration import DataConfiguration
from data_treatment.principal_component_analysis import PrincipalComponentAnalysisPerformanceMeasurement
from data_preparation.data_preparator import DataPreparator
import numpy as np
from analysis.function_analysis import FunctionAnalysis
from analysis.empty_rows_deletion_evaluation import EmptyRowsDeletionEvaluation
class DimensionalityEvaluation:

    def __init__(self):
        self.set_configurations_to_test()
    
    def set_configurations_to_test(self):
        self.DESIRED_EXPLAINED_VARIANCE_RATIO = 0.95
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS")
        both_config = DataConfiguration()
        both_config.set_to_default_configuration("BOTH")
        self.configurations_to_test = {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH":both_config}

    def run_evaluation(self,data_source,col_emptiness_thresholds=None):
        ideal_dimensionalities = {}
        for config_name in self.configurations_to_test:
            data = DataPreparator(self.configurations_to_test[config_name], data_source).apply_configuration(col_emptiness_thresholds[config_name] if col_emptiness_thresholds and config_name in col_emptiness_thresholds else None)
            analyser = PrincipalComponentAnalysisPerformanceMeasurement(data,extra_title_precision=config_name)
            min_nb_dimensions_tested, explained_variance_ratios = analyser.compute_and_plot_explained_variance_ratio_to_components_count()
            ideal_dimensionalities[config_name] = self.compute_index_first_element_above_threshold(explained_variance_ratios) + min_nb_dimensions_tested
        return ideal_dimensionalities
    
    def compute_index_first_element_above_threshold(self, array):
        for i in range(len(array)):
            if array[i] > self.DESIRED_EXPLAINED_VARIANCE_RATIO:
                return i
        return array[len(array)-1]