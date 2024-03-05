from analysis.data_configuration import DataConfiguration
from data_preparation.data_preparator import DataPreparator
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis

class EmptyRowsDeletionEvaluation:

    def __init__(self,configuration_to_test):
        self.configurations_to_test = configuration_to_test
        self.IDEAL_MIN_ROW_COUNT = 500
    
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