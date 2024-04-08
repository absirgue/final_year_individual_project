import math

class FunctionAnalysis:

    # Returns the slope of a line based on the list of x and y values of the different points it is made off. 
    def get_straight_line_coefficient(self, x_values, y_values):
        return (y_values[len(y_values)-1] - y_values[0])/(x_values[len(x_values)-1]-x_values[0])
    
    """
    Returns the coordinates of the elbow point in a graph based on a 2D array of points.
    The elbow point is mathematically characterized as the point where the distance between the 
    curve and the line from its start and end point is the greatest.
    """
    def get_elbow_point_from_x_y_2d_array(self,x_y_mapping):
        x_values = self.extract_x_values_2d_array_of_points(x_y_mapping)
        y_values = self.extract_y_values_2d_array_of_points(x_y_mapping)
        straight_line_coeff = self.get_straight_line_coefficient(x_values,y_values)
        perpendicular_coeff = 1/(-1*straight_line_coeff)
        straight_line_y_intercept = self.get_straight_line_y_intercept(straight_line_coeff,x_values[0],y_values[0])
        elbow_point = None
        greatest_distance_to_straight_line = -10**9
        for i in range(len(x_y_mapping)):
            perpendicular_y_intercept = self.get_straight_line_y_intercept(perpendicular_coeff,x_values[i],y_values[i])
            intercept_of_direct_straight_line_x_value = self.get_x_value_of_2_lines_intercept(straight_line_coeff,straight_line_y_intercept,perpendicular_coeff,perpendicular_y_intercept)
            intercept_of_direct_straight_line_y_value = intercept_of_direct_straight_line_x_value*perpendicular_coeff+ perpendicular_y_intercept
            distance = math.sqrt((y_values[i] - intercept_of_direct_straight_line_y_value)**2 + (x_values[i] - intercept_of_direct_straight_line_x_value)**2)
            if distance > greatest_distance_to_straight_line:
                elbow_point = x_y_mapping[i]
                greatest_distance_to_straight_line = distance
        return elbow_point
    
    """
    Returns the x-coordinate of the point where 2 lines intersect. The lines are each specified 
    by their slope and y-intercept.
    """
    def get_x_value_of_2_lines_intercept(self,line_1_coeff,line_1_intercept,line_2_coeff,line_2_intercept):
        return (line_1_intercept-line_2_intercept)/(line_2_coeff-line_1_coeff)

    # Returns the y-interecept of a line based on its slope and on the coordinates of 1 of its points.
    def get_straight_line_y_intercept(self, straight_line_coeff, x_value, y_value):
        return y_value - (x_value*straight_line_coeff)
    
    # Returns the x-coordinate values of all points in a list of points
    def extract_x_values_2d_array_of_points(self, array):
        x_vals = []
        for point in array:
            x_vals.append(point[0])
        return x_vals
    
    # Returns the y-coordinate values of all points in a list of points
    def extract_y_values_2d_array_of_points(self, array):
        y_vals = []
        for point in array:
            y_vals.append(point[1])
        return y_vals

    # Returns a list of all inflection points on a graph.
    def get_inflection_points_from_x_y_2d_array(self,x_y_mapping):
        second_derivatives = []
        for i in range(1, len(x_y_mapping) - 1):
            second_derivatives.append(self.get_second_derivative_of_point_at_index(i,x_y_mapping))
        inflection_points = []
        for i in range(1, len(second_derivatives) - 1):
            if second_derivatives[i - 1] * second_derivatives[i + 1] <= 0:
                inflection_points.append(x_y_mapping[i])
        return inflection_points

    """
    Returns the value of the second derivative of a function at a given point. The function 
    is characterized by a list of pointsand the point by its index in this list.
    """
    def get_second_derivative_of_point_at_index(self, idx, arr):
        x1, y1 = arr[idx - 1]
        x2, y2 = arr[idx]
        x3, y3 = arr[idx + 1]
        second_derivative = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
        return second_derivative