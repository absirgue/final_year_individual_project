import numpy as np
from data_treatment.principal_component_analysis import PrincipalComponentAnalysisPerformanceMeasurement
from data_preparation.data_preparator import DataPreparator
from interface_beautifier import InterfaceBeautifier

class DimensionalityEvaluation:
    """
    Coordinates all actions required to obtain the minimum numper of Principal Components we can 
    reduce a data set to while conserving a given share of total explained variance ratio. 
    """

    def __init__(self,configuration_to_test):
        self.configurations_to_test = configuration_to_test
        # the minimum total explained variance ratio is set to 95% by default.
        self.DESIRED_EXPLAINED_VARIANCE_RATIO = 0.95
    
    def run_evaluation(self,col_emptiness_thresholds=None):
        ideal_dimensionalities = {}
        nb_configs_tested = 0
        for config_name in self.configurations_to_test:
            config = self.configurations_to_test[config_name]
            nb_configs_tested += 1
            data = DataPreparator(config, config.get_data_source()).apply_configuration(col_emptiness_thresholds[config_name] if col_emptiness_thresholds and config_name in col_emptiness_thresholds else None)
            analyser = PrincipalComponentAnalysisPerformanceMeasurement(data,extra_title_precision=config_name)
            min_nb_dimensions_tested, explained_variance_ratios = analyser.compute_and_plot_explained_variance_ratio_to_components_count()
            ideal_dimensionalities[config_name] = self.compute_index_first_element_above_threshold(explained_variance_ratios) + min_nb_dimensions_tested
            InterfaceBeautifier().print_percentage_progress("Progress on Optimal Dimensionality Evaluation",nb_configs_tested*100/len(self.configurations_to_test))
        return ideal_dimensionalities
    
    def compute_index_first_element_above_threshold(self, array):
        for i in range(len(array)):
            if array[i] > self.DESIRED_EXPLAINED_VARIANCE_RATIO:
                return i
        return array[len(array)-1]