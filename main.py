import sys
import numpy as np
from analysis.conclusion_2.clustering_results_analyzer import ClusteringResultsAnalyzer
from analysis.conclusion_2.manual_analysis_helper import ManualAnalysisHelper
from analysis.data_configuration import DataConfiguration
from interface_beautifier import InterfaceBeautifier
np.seterr(over='ignore')

class DataConfigurationWrapper:

    def __init__(self):
        self.create_config_packages()

    def get_config_package(self, pkg_id):
        return self.config_packages[pkg_id]

    def create_config_packages(self):
        self.config_packages = {}
        self.config_packages["ALL"] = self.get_all_configs()
        self.config_packages["RAW NUMBERS AND RATIOS"] = self.get_raw_nb_and_ratios_configs()
        self.config_packages["CREDIT HEALTH AND CREDIT MODEL"] = self.get_credit_health_and_credit_model()
        self.config_packages["ALL - COMPLEX"] = self.get_all_configs(complex=True)
        self.config_packages["CREDIT HEALTH AND CREDIT MODEL - COMPLEX"] = self.get_credit_health_and_credit_model(complex=True)

    def get_all_configs(self,complex=False):
        raw_nb_and_ratios_configs = self.get_raw_nb_and_ratios_configs()
        credit_health_and_credit_model = self.get_credit_health_and_credit_model(complex)
        credit_health_and_credit_model.update(raw_nb_and_ratios_configs)
        return credit_health_and_credit_model

    def get_raw_nb_and_ratios_configs(self):
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS")
        both_config_ratios_and_raw_numbers = DataConfiguration()
        both_config_ratios_and_raw_numbers.set_to_default_configuration("BOTH RATIOS AND RAW NUMBERS")
        return {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH RATIOS AND RAW NUMBERS":both_config_ratios_and_raw_numbers}
    
    def get_credit_health_and_credit_model(self,complex=False):
        configs = {}
        credit_model_config = DataConfiguration()
        credit_model_config.set_to_default_configuration("CREDIT MODEL")
        configs["CREDIT MODEL"] = credit_model_config
        credit_health_config = DataConfiguration()
        credit_health_config.set_to_default_configuration("CREDIT HEALTH")
        configs["CREDIT HEALTH"] = credit_health_config
        both_config_credit_health_and_credit_model = DataConfiguration()
        both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL")
        configs["BOTH CREDIT HEALTH AND CREDIT MODEL"] = both_config_credit_health_and_credit_model
        if complex:
            for config_nb in range(1,4):
                credit_health_config = DataConfiguration()
                credit_health_config.set_to_default_configuration("CREDIT HEALTH",average_by_category=config_nb)
                configs["CREDIT HEALTH"+credit_health_config.get_appendix_for_averager_modif_of_config()] = credit_health_config
                credit_model_config = DataConfiguration()
                credit_model_config.set_to_default_configuration("CREDIT MODEL",average_by_category=config_nb)
                configs["CREDIT MODEL"+credit_model_config.get_appendix_for_averager_modif_of_config()] = credit_model_config
                both_config_credit_health_and_credit_model = DataConfiguration()
                both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL",average_by_category=config_nb)
                configs["BOTH CREDIT HEALTH AND CREDIT MODEL"+both_config_credit_health_and_credit_model.get_appendix_for_averager_modif_of_config()] = both_config_credit_health_and_credit_model
        return configs

def run_demanded_program(config_name_pca, config_name_non_pca, analysis_only, run_pca):
    configuration = DataConfigurationWrapper().get_config_package(config_name_non_pca)
    # if not analysis_only:
    #     # AlgorithmsPerformancesEvaluation(configuration).run_evaluation()
    #     InterfaceBeautifier().print_major_annoucement("algorithms hyperparameters optimization done with non-pca")
    ClusteringResultsAnalyzer("./conclusion_1_graphs/algorithms_comparisons/without_pca/performance_metrics.json", "./conclusion_2_results/",False,configuration).analyse()
    InterfaceBeautifier().print_major_annoucement("analysis of non-pca clusters done")
    if run_pca:
        pass
        # if not analysis_only:
        #     configuration = DataConfigurationWrapper().get_config_package(config_name_pca)
        #     AlgorithmsPerformancesEvaluation(configuration,run_pca=True).run_evaluation()
        #     InterfaceBeautifier().print_major_annoucement("algorithms hyperparameters optimization done with pca")
        # RE RUN 
        ClusteringResultsAnalyzer("./conclusion_1_graphs/algorithms_comparisons/with_pca/performance_metrics.json", "./conclusion_2_results/",True,configuration).analyse()
        # InterfaceBeautifier().print_major_annoucement("analysis of pca clusters done")
    ManualAnalysisHelper()
    InterfaceBeautifier().print_major_annoucement("finished all tasks")

def main():
    # both_config_credit_health_and_credit_model = DataConfiguration()
    # both_config_credit_health_and_credit_model.set_to_default_configuration("CREDIT MODEL")
    # dp = DataPreparator(configuration=both_config_credit_health_and_credit_model,data_source=both_config_credit_health_and_credit_model.get_data_source())
    # data = dp.apply_configuration(0.65)
    # print(dp.get_entity_ids())
    # print(data.shape[1])
    # print(data.shape[0])
    # it = DBSCANIterator(data)
    # print(it.iterate())
    # it.graph()
    # RatingChangesIdentifier(None).identify_changes()
    args = sys.argv[1:]
    analysis_only = False
    run_pca = True
    if "-pca_configs" in args:
        config_name_pca = args[args.index("-pca_configs")+1]
    else:
        config_name_pca = "CREDIT HEALTH AND CREDIT MODEL"
    if "-non_pca_configs" in args:
        config_name_non_pca = args[args.index("-non_pca_configs")+1]
    else:
        config_name_non_pca = "CREDIT HEALTH AND CREDIT MODEL - COMPLEX"
    if "-analysis_only" in args:
        analysis_only = True
    if "-skip_pca" in args:
        run_pca = False
    run_demanded_program(config_name_pca=config_name_pca, config_name_non_pca=config_name_non_pca,analysis_only=analysis_only,run_pca=run_pca)

# Allow main method to operate.
if __name__ == "__main__":
    main()