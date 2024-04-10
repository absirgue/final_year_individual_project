import sys

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from data_preprocessing.data_preparator import DataPreparator

import numpy as np
from analysis.clusters_analysis.clustering_results_analyzer import ClusteringResultsAnalyzer
# from analysis.clusters_analysis.manual_analysis_helper import ManualAnalysisHelper
from analysis.hyperparameters_optimisation.algorithms_performances_evaluation import AlgorithmsPerformancesEvaluation
from analysis.data_configuration import DataConfiguration
from interface_beautifier import InterfaceBeautifier
np.seterr(over='ignore')

class DataConfigurationWrapper:

    """
    Provides several combinations (packages) of different data configurations.
    """

    def __init__(self):
        self.create_config_packages()

    # Returns the list of configurations for a given combination name.
    def get_config_package(self, pkg_id):
        return self.config_packages[pkg_id]

    # Creates a dictionary of all default packages of data configurations. 
    def create_config_packages(self):
        self.config_packages = {}
        self.config_packages["ALL"] = self.get_all_configs()
        self.config_packages["RAW NUMBERS AND RATIOS"] = self.get_raw_nb_and_ratios_configs()
        self.config_packages["CREDIT HEALTH AND CREDIT MODEL"] = self.get_credit_health_and_credit_model()
        self.config_packages["ALL - COMPLEX"] = self.get_all_configs(complex=True)
        self.config_packages["CREDIT HEALTH AND CREDIT MODEL - COMPLEX"] = self.get_credit_health_and_credit_model(complex=True)
        self.config_packages["INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL"] = self.get_industry_specific_credit_health_and_credit_model()
        self.config_packages["INDUSTRY SPECIFIC CREDIT HEALTH AND CREDIT MODEL - COMPLEX"] = self.get_industry_specific_credit_health_and_credit_model(complex=True)
        self.config_packages["INDUSTRY SPECIFIC & CREDIT HEALTH AND CREDIT MODEL - COMPLEX"] = self.get_industry_specific_and_credit_health_and_credit_model(complex=True)
        self.config_packages["INDUSTRY SPECIFIC & CREDIT HEALTH AND CREDIT MODEL"] = self.get_industry_specific_and_credit_health_and_credit_model(complex=False)

    """
    Helper method to assemble data configurations related to both credit health and credit models
    both for industry-specific and general data sets.
    """
    def get_industry_specific_and_credit_health_and_credit_model(self, complex=False):
        cr_and_ch = self.get_credit_health_and_credit_model(complex=True)
        industry_specific = self.get_industry_specific_credit_health_and_credit_model(complex=True)
        industry_specific.update(cr_and_ch)
        return industry_specific
    
    # Returns a list of all default data configurations. 
    def get_all_configs(self,complex=False):
        raw_nb_and_ratios_configs = self.get_raw_nb_and_ratios_configs()
        credit_health_and_credit_model = self.get_credit_health_and_credit_model(complex)
        industry_specific_credit_health_and_credit_model = self.get_industry_specific_credit_health_and_credit_model(complex)
        credit_health_and_credit_model.update(raw_nb_and_ratios_configs)
        credit_health_and_credit_model.update(industry_specific_credit_health_and_credit_model)
        return credit_health_and_credit_model

    # Returns a list of all default data configurations related to raw numbers and ratios.
    def get_raw_nb_and_ratios_configs(self):
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS","RATIOS AND RAW NUMBERS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS","RATIOS AND RAW NUMBERS")
        both_config_ratios_and_raw_numbers = DataConfiguration()
        both_config_ratios_and_raw_numbers.set_to_default_configuration("BOTH RATIOS AND RAW NUMBERS","RATIOS AND RAW NUMBERS")
        return {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH RATIOS AND RAW NUMBERS":both_config_ratios_and_raw_numbers}
    
    """
    Returns a list of all default data configurations related to credit healh and credit model
    for general data sets.
    """
    def get_credit_health_and_credit_model(self,complex=False):
        configs = {}
        credit_model_config = DataConfiguration()
        credit_model_config.set_to_default_configuration("CREDIT MODEL","CREDIT MODEL AND CREDIT HEALTH")
        configs["CREDIT MODEL"] = credit_model_config
        credit_health_config = DataConfiguration()
        credit_health_config.set_to_default_configuration("CREDIT HEALTH","CREDIT MODEL AND CREDIT HEALTH")
        configs["CREDIT HEALTH"] = credit_health_config
        both_config_credit_health_and_credit_model = DataConfiguration()
        both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL","CREDIT MODEL AND CREDIT HEALTH")
        configs["BOTH CREDIT HEALTH AND CREDIT MODEL"] = both_config_credit_health_and_credit_model
        # If we want the features to be aggregated based on a pilar of credit rating, 
        # create 3 additional configurations for each basic one, one for aggregation using mean,
        # one for using median, and one for using normalized mean.
        if complex:
            for config_nb in range(1,4):
                credit_health_config = DataConfiguration()
                credit_health_config.set_to_default_configuration("CREDIT HEALTH","CREDIT MODEL AND CREDIT HEALTH",average_by_category=config_nb)
                configs["CREDIT HEALTH"+credit_health_config.get_appendix_for_averager_modif_of_config()] = credit_health_config
                credit_model_config = DataConfiguration()
                credit_model_config.set_to_default_configuration("CREDIT MODEL","CREDIT MODEL AND CREDIT HEALTH",average_by_category=config_nb)
                configs["CREDIT MODEL"+credit_model_config.get_appendix_for_averager_modif_of_config()] = credit_model_config
                both_config_credit_health_and_credit_model = DataConfiguration()
                both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL","CREDIT MODEL AND CREDIT HEALTH",average_by_category=config_nb)
                configs["BOTH CREDIT HEALTH AND CREDIT MODEL"+both_config_credit_health_and_credit_model.get_appendix_for_averager_modif_of_config()] = both_config_credit_health_and_credit_model
        return configs

    """
    Returns a list of all default data configurations related to credit healh and credit model
    for industry-specific data sets.
    """
    def get_industry_specific_credit_health_and_credit_model(self,complex=False):
        configs = {}
        industries_to_add = ["RENEWABLE ENERGY INDUSTRY","FOOD PRODUCTS INDUSTRY","OIL AND GAS INDUSTRY"]
        for industry in industries_to_add:
            credit_model_config = DataConfiguration()
            credit_model_config.set_to_default_configuration("CREDIT MODEL",industry+" CREDIT MODEL AND CREDIT HEALTH")
            configs[industry+" - CREDIT MODEL"] = credit_model_config
            credit_health_config = DataConfiguration()
            credit_health_config.set_to_default_configuration("CREDIT HEALTH",industry+" CREDIT MODEL AND CREDIT HEALTH")
            configs[industry+" - CREDIT HEALTH"] = credit_health_config
            both_config_credit_health_and_credit_model = DataConfiguration()
            both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",industry+" CREDIT MODEL AND CREDIT HEALTH")
            configs[industry+" - BOTH CREDIT HEALTH AND CREDIT MODEL"] = both_config_credit_health_and_credit_model
            # If we want the features to be aggregated based on a pilar of credit rating, 
            # create 3 additional configurations for each basic one, one for aggregation using mean,
            # one for using median, and one for using normalized mean.
            if complex:
                for config_nb in range(1,4):
                    credit_health_config = DataConfiguration()
                    credit_health_config.set_to_default_configuration("CREDIT HEALTH",industry+" CREDIT MODEL AND CREDIT HEALTH",average_by_category=config_nb)
                    configs[industry+" - CREDIT HEALTH"+credit_health_config.get_appendix_for_averager_modif_of_config()] = credit_health_config
                    credit_model_config = DataConfiguration()
                    credit_model_config.set_to_default_configuration("CREDIT MODEL",industry+" CREDIT MODEL AND CREDIT HEALTH",average_by_category=config_nb)
                    configs[industry+" - CREDIT MODEL"+credit_model_config.get_appendix_for_averager_modif_of_config()] = credit_model_config
                    both_config_credit_health_and_credit_model = DataConfiguration()
                    both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",industry+" CREDIT MODEL AND CREDIT HEALTH",average_by_category=config_nb)
                    configs[industry+" - BOTH CREDIT HEALTH AND CREDIT MODEL"+both_config_credit_health_and_credit_model.get_appendix_for_averager_modif_of_config()] = both_config_credit_health_and_credit_model
        return configs

"""
Executes a custom run of the program.
Params:
    config_name_pca - the name of the package of default configurations to be used for analysis 
    after PCA
    config_name_non_pca - the name of the package of default configurations to be used for 
    analysis without PCA
    analysis_only - True if we should ignore the hyperparameter optimisation step
    run_pca - False if we should not run any analysis after application of PCA
"""
def run_demanded_program(config_name_pca, config_name_non_pca, analysis_only, run_pca):
    configuration = DataConfigurationWrapper().get_config_package(config_name_non_pca)
    if not analysis_only:
        AlgorithmsPerformancesEvaluation(configuration).run_evaluation()
        InterfaceBeautifier().print_major_annoucement("algorithms hyperparameters optimization done with non-pca")
    ClusteringResultsAnalyzer("./hyperparameter_optimisation_results/algorithms_comparisons/without_pca/performance_metrics.json", "./clusters_content_analyses/",False,configuration).analyse()
    InterfaceBeautifier().print_major_annoucement("analysis of non-pca clusters done")
    if run_pca:
        if not analysis_only:
            configuration = DataConfigurationWrapper().get_config_package(config_name_pca)
            AlgorithmsPerformancesEvaluation(configuration,run_pca=True).run_evaluation()
            InterfaceBeautifier().print_major_annoucement("algorithms hyperparameters optimization done with pca")
        ClusteringResultsAnalyzer("./hyperparameter_optimisation_results/algorithms_comparisons/with_pca/performance_metrics.json", "./clusters_content_analyses/",True,configuration).analyse()
        InterfaceBeautifier().print_major_annoucement("analysis of pca clusters done")
    InterfaceBeautifier().print_major_annoucement("finished all tasks")

def main():
    args = sys.argv[1:]
    analysis_only = False
    run_pca = True
    if "-pca_configs" in args:
        config_name_pca = args[args.index("-pca_configs")+1]
    else:
        config_name_pca = "INDUSTRY SPECIFIC & CREDIT HEALTH AND CREDIT MODEL"
    if "-non_pca_configs" in args:
        config_name_non_pca = args[args.index("-non_pca_configs")+1]
    else:
        config_name_non_pca = "INDUSTRY SPECIFIC & CREDIT HEALTH AND CREDIT MODEL - COMPLEX"
    if "-analysis_only" in args:
        analysis_only = True
    if "-skip_pca" in args:
        run_pca = False
    run_demanded_program(config_name_pca=config_name_pca, config_name_non_pca=config_name_non_pca,analysis_only=analysis_only,run_pca=run_pca)

# Allow main method to operate.
if __name__ == "__main__":
    main()