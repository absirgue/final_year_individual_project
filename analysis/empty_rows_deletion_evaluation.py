from data_preparation.data_preparator import DataPreparator
from graph.graphing_helper import GraphingHelper
from analysis.function_analysis import FunctionAnalysis
from interface_beautifier import InterfaceBeautifier

class EmptyRowsDeletionEvaluation:
    """
    Coordinates all actions required to compute the optimal column emptiness threshold 
    for a given data set. 
    """

    def __init__(self,configuration_to_test):
        self.configurations_to_test = configuration_to_test
        self.IDEAL_MIN_ROW_COUNT = 500
        # The maximum number of credit ratings present in any data set + 10. 
        self.MINIMUM_NUMBER_OF_ROWS = 32
    
    def run_evaluation(self):
        self.ideal_empty_col_thresholds = {}
        count_config_tested = 0
        for config_name in self.configurations_to_test:
            count_config_tested+=1
            point_product_thresh_map = {}
            points = []
            for i in range(21):
                empty_col_threshold = i * 0.05
                config = self.configurations_to_test[config_name]
                preparator = DataPreparator(config, config.get_data_source())
                data = preparator.apply_configuration(empty_col_threshold)
                number_added_columns = preparator.get_number_added_columns()
                points.append([data.shape[0],data.shape[1]-number_added_columns])
                point_product_thresh_map[data.shape[0]*(data.shape[1]-number_added_columns)] = empty_col_threshold
            GraphingHelper().plot_2d_array_of_points(points,folder_name="empty_rows_deletion_evaluation_graphs",x_label="Number of rows",y_label="Number of columns",title=config_name+": Rows and Columns for Data Cleaning of Default Configuration")
            inflection_points = FunctionAnalysis().get_inflection_points_from_x_y_2d_array(points)
            favored_point = self.get_best_inflection_point(inflection_points,points)
            self.ideal_empty_col_thresholds[config_name] = point_product_thresh_map[favored_point[0]*favored_point[1]]
            InterfaceBeautifier().print_percentage_progress("Progress on Optimal Empty Column Deletion Threshold Evaluation",(count_config_tested)*100/len(self.configurations_to_test))
        return self.ideal_empty_col_thresholds

    def get_best_inflection_point(self, inflection_points,points):
        if not inflection_points:
            for point in points:
                if point[0] >= self.IDEAL_MIN_ROW_COUNT:
                    return point
        for i in range(len(inflection_points)-1,-1,-1):
            if inflection_points[i][0] >= self.IDEAL_MIN_ROW_COUNT:
                return inflection_points[i]
        for i in range(len(inflection_points)-1,-1,-1):
            if inflection_points[i][0] >= self.MINIMUM_NUMBER_OF_ROWS:
                return inflection_points[i]

    def get_optimal_col_emptiness_threshold(self, config_name):
        if config_name in self.ideal_empty_col_thresholds:
            return self.ideal_empty_col_thresholds[config_name]
        else:
            return None