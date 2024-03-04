from analysis.data_configuration import DataConfiguration
from data_preparation.data_preparator import DataPreparator
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
class EmptyRowsDeletionEvaluation:

    def __init__(self,configuration_to_test = None):
        if configuration_to_test:
            self.configurations_to_test = configuration_to_test
        else:
            self.set_configurations_to_test()
        self.IDEAL_MIN_ROW_COUNT = 500
    
    def set_configurations_to_test(self):
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS")
        both_config_ratios_and_raw_numbers = DataConfiguration()
        both_config_ratios_and_raw_numbers.set_to_default_configuration("BOTH RATIOS AND RAW NUMBERS")
        credit_health__config = DataConfiguration()
        credit_health__config.set_to_default_configuration("CREDIT HEALTH")
        credit_model_config = DataConfiguration()
        credit_model_config.set_to_default_configuration("CREDIT MODEL")
        both_config_credit_health_and_credit_model = DataConfiguration()
        both_config_credit_health_and_credit_model.set_to_default_configuration("BOTH CREDIT HEALTH AND CREDIT MODEL")
        self.configurations_to_test = {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH RATIOS AND RAW NUMBERS":both_config_ratios_and_raw_numbers,"CREDIT MODEL":credit_model_config,"CREDIT HEALTH":credit_health__config,"BOTH CREDIT HEALTH AND CREDIT MODEL":both_config_credit_health_and_credit_model}
    
    def run_evaluation(self):
        self.ideal_empty_col_thresholds = {}
        for config_name in self.configurations_to_test:
            point_product_thresh_map = {}
            points = []
            for i in range(0, 21):
                empty_col_threshold = i * 0.05
                config = self.configurations_to_test[config_name]
                preparator = DataPreparator(config, config.get_data_source())
                data = preparator.apply_configuration(empty_col_threshold)
                number_added_columns = preparator.get_number_added_columns()
                points.append([data.shape[0],data.shape[1]-number_added_columns])
                point_product_thresh_map[data.shape[0]*(data.shape[1]-number_added_columns)] = empty_col_threshold
            GraphingHelper().plot_2d_array_of_points(points,folder_name="empty_rows_deletion_evaluation_graphs",x_label="Number of rows",y_label="Number of columns",title=config_name+": Rows and Columns for Data Cleaning of Default Configuration")
            elbow_point = FunctionAnalysis().get_elbow_point_from_x_y_2d_array(points)
            self.ideal_empty_col_thresholds[config_name] = point_product_thresh_map[elbow_point[0]*elbow_point[1]]
        return self.ideal_empty_col_thresholds

    def get_optimal_col_emptiness_threshold(self, config_name):
        if config_name in self.ideal_empty_col_thresholds:
            return self.ideal_empty_col_thresholds[config_name]
        else:
            return None