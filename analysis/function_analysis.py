import numpy as np

class FunctionAnalysis:

    def get_first_inflection_point_x_coordinate_with_list_of_y_values(self,y_values_list):
        first_derivative = np.diff(y_values_list)
        inflection_point_index = np.where(np.diff(np.sign(first_derivative)))[0]
        return inflection_point_index
    
    def get_inflection_points_from_x_y_2d_array(self,x_y_mapping):
        second_derivatives = []
        for i in range(1, len(x_y_mapping) - 1):
            second_derivatives.append(self.get_second_derivative_of_point_at_index(i,x_y_mapping))
        inflection_points = []
        for i in range(1, len(second_derivatives) - 1):
            if second_derivatives[i - 1] * second_derivatives[i + 1] < 0:
                inflection_points.append(x_y_mapping[i])
        return inflection_points
    
    def get_second_derivative_of_point_at_index(self, idx, arr):
        x1, y1 = arr[idx - 1]
        x2, y2 = arr[idx]
        x3, y3 = arr[idx + 1]
        second_derivative = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        return second_derivative

    def extract_x_values_2d_array_of_points(self, array):
        x_vals = []
        for point in array:
            x_vals.append(point[0])
        return x_vals
    
    def extract_y_values_2d_array_of_points(self, array):
        y_vals = []
        for point in array:
            y_vals.append(point[1])
        return y_vals