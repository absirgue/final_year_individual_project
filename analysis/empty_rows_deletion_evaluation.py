from analysis.data_configuration import DataConfiguration
from data_preparation.data_preparator import DataPreparator
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
class EmptyRowsDeletionEvaluation:

    def __init__(self):
        self.set_configurations_to_test()
        self.IDEAL_MIN_ROW_COUNT = 500
    
    def set_configurations_to_test(self):
        ratios_config = DataConfiguration()
        ratios_config.set_to_default_configuration("RATIOS")
        raw_nbs_config = DataConfiguration()
        raw_nbs_config.set_to_default_configuration("RAW NUMBERS")
        both_config = DataConfiguration()
        both_config.set_to_default_configuration("BOTH")
        self.configurations_to_test = {"RATIOS":ratios_config,"RAW NUMBERS":raw_nbs_config,"BOTH":both_config}
    
    def run_evaluation(self,data_source):
        self.ideal_empty_col_thresholds = {}
        for config_name in self.configurations_to_test:
            # mappings_nb_columns_nb_rows = []
            point_product_thresh_map = {}
            points = []
            for i in range(0, 21):
                empty_col_threshold = i * 0.05
                preparator = DataPreparator(self.configurations_to_test[config_name], data_source)
                data = preparator.apply_configuration(empty_col_threshold)
                number_added_columns = preparator.get_number_added_columns()
                points.append([data.shape[0],data.shape[1]-number_added_columns])
                point_product_thresh_map[data.shape[0]*(data.shape[1]-number_added_columns)] = empty_col_threshold
            GraphingHelper().plot_2d_array_of_points(points,"Number of rows","Number of columns","Rows and Columns for Data Cleaning of Default Configuration "+config_name)
            inflection_points = FunctionAnalysis().get_inflection_points_from_x_y_2d_array(points)
            favored_point = self.get_best_inflection_point(inflection_points,points)
            self.ideal_empty_col_thresholds[config_name] = point_product_thresh_map[favored_point[0]*favored_point[1]]
        return self.ideal_empty_col_thresholds

    def get_best_inflection_point(self, inflection_points,points):
        if not inflection_points:
            for point in points:
                if point[0] >= self.IDEAL_MIN_ROW_COUNT:
                    return point
        for i in range(len(inflection_points)):
            if inflection_points[i][0] >= self.IDEAL_MIN_ROW_COUNT:
                return inflection_points[i]
        return inflection_points[len(inflection_points)-1]

    def get_optimal_col_emptiness_threshold(self, config_name):
        if config_name in self.ideal_empty_col_thresholds:
            return self.ideal_empty_col_thresholds[config_name]
        else:
            return None