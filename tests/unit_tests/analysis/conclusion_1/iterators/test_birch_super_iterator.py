import unittest
import numpy as np
from analysis.conclusion_1.iterators.birch_super_iterator import BIRCHSuperIterator
from tests.unit_tests.analysis.conclusion_1.iterators.helper import get_random_2d_array
from sklearn.cluster import Birch
from sklearn.metrics import calinski_harabasz_score,silhouette_score

class TestBIRCHSuperIterator(unittest.TestCase):

    def test_get_optimal_gives_expected_result(self):
        iterator = BIRCHSuperIterator(np.array([[]]))
        iterator.calinski_harabasz_data = [[1,1.1,0,0,0],[2,1.5,0.9,0,0],[3,2,0,0,0]]
        iterator.silhouette_score_data = [[1,0.7,0,0,0],[2,0.9,1,0,0],[3,0.8,0,0,0]]
        result = iterator.get_optimal()
        self.assertEqual(result["Calinski Harabasz Index Optimum"]["K"],3)
        self.assertEqual(result["Calinski Harabasz Index Optimum"]["Calinski Harabasz Index"],2)
        self.assertEqual(result["Silhouette Score Optimum"]["K"],2)
        self.assertEqual(result["Silhouette Score Optimum"]["Silhouette Score"],0.9)
    
    def test_get_performance_on_given_K_gives_expected_result(self):
        iterator = BIRCHSuperIterator(np.array([[]]))
        iterator.calinski_harabasz_data = [[1,1.1,0,0,0],[2,1.5,0.9,0,0],[3,2,0,0,0]]
        iterator.silhouette_score_data = [[1,0.7,0,0,0],[2,0.9,1,1,0],[3,0.8,0,0,0]]
        result = iterator.get_performance_on_given_K(2)
        self.assertEqual(result["Branching Factor"]["Silhouette Score Optimum"],1)
        self.assertEqual(result["Branching Factor"]["Calinski Harabasz Index Optimum"],0)
        self.assertEqual(result["Calinski Harabasz Index"],1.5)
        self.assertEqual(result["Silhouette Score"],0.9)