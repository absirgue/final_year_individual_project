import unittest
import math
import numpy as np
from analysis.function_analysis import FunctionAnalysis

class TestFunctionAnalysis(unittest.TestCase):

    def test_get_elbow_point_from_x_y_2d_array_gives_expected_value(self): 
        x_y_arr = []
        for i in range(-5,50):
            x_y_arr.append([i,math.exp(-1*i)])
        result = FunctionAnalysis().get_elbow_point_from_x_y_2d_array(x_y_arr)    
        self.assertEqual(result[0],-1)
    
    def test_get_elbow_point_from_x_y_2d_array_gives_expected_value_in_flatter_config(self): 
        x_y_arr = []
        for i in range(-40,50):
            x_y_arr.append([i,math.exp(-0.1*i)])
        result = FunctionAnalysis().get_elbow_point_from_x_y_2d_array(x_y_arr)    
        self.assertEqual(result[0],-18)
