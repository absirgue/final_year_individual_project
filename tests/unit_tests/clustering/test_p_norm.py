import unittest
from clustering_algorithms.p_norm import PNorm
import pandas as pd
import numpy as np

class TestPNormDistance(unittest.TestCase):

    def test_p_can_not_be_0(self):
        with self.assertRaises(ValueError):
            PNorm(0)
    
    def test_p_can_not_be_negative(self):
        with self.assertRaises(ValueError):
            PNorm(-12)
    
    def test_1_norm_of_2D_points_calculates_Euclidian_distance(self):
        result = PNorm(1).calculate_norm([1,5],[2,3])
        self.assertEqual(result,3)
    
    def test_2_norm_of_2D_points_calculates_Manhattan_distance(self):
        result = PNorm(2).calculate_norm([1,5],[2,3])
        self.assertEqual(result,5**(1/2))
    
    def test_5_norm_of_5D_points_result_is_as_expected(self):
        result = PNorm(5).calculate_norm([1,5,-3,2,3.14],[2,3,3,4,5])
        self.assertEqual(result,6.013406318514255)
    
    def test_5_norm_of_2D_points_result_is_as_expected(self):
        result = PNorm(5).calculate_norm([1,5],[2,3])
        self.assertEqual(result,2.0123466170855586)