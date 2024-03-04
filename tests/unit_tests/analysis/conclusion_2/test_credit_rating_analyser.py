import unittest
import numpy as np
from analysis.conclusion_2.credit_rating_analyzer import CreditRatingAnalyzer
from analysis.conclusion_2.credit_rating_cluster import CreditRatingCluster
from analysis.conclusion_2.clusters_analyzer import ClustersAnalyzer

class TestCreditRatingAnalyser(unittest.TestCase):

    def test_insert_company_has_intended_effect_on_empty_cr_analyser(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.insert_company("1",["data 1"])
        self.assertEqual(cr_analyser.credit_rating,"1")
        self.assertEqual(cr_analyser.get_companies_count(),1)
        self.assertEqual(cr_analyser.data,[["data 1"]])

    def test_insert_company_has_intended_effect_on_non_empty_cr_analyser(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.insert_company("1",["data 1"])
        cr_analyser.insert_company("1",["data 2"])
        cr_analyser.insert_company("1",["data 3"])
        self.assertEqual(cr_analyser.credit_rating,"1")
        self.assertEqual(cr_analyser.get_companies_count(),3)
        self.assertEqual(cr_analyser.data,[["data 1"],["data 2"],["data 3"]])
    
    def test_insert_company_gives_intended_response_when_rating_differs(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.insert_company("1",["data 1"])
        response = cr_analyser.insert_company("2",["data 2"])
        self.assertEqual(response,None)
        self.assertEqual(cr_analyser.get_companies_count(),1)

    def test_get_measure_of_location_and_dispersion_gives_expected_results(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_measures_of_location_and_dispersion(0)
        self.assertEqual(result["Mean"],2.5)
        self.assertEqual(result["Median"],2.5)
        self.assertEqual(result["1st Quartile"],0.5)
        self.assertEqual(result["3rd Quartile"],4.5)
        self.assertAlmostEqual(result["Standard Deviation"],2.6925824035)
    
    def test_get_col_normalized_range_gives_expected_result_scenar_1(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_col_normalized_range(0,np.array([[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8],[10,20,30]]))
        self.assertEqual(result,7/11)
    
    def test_get_col_normalized_range_gives_expected_result_scenar_2(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_col_normalized_range(1,np.array([[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8],[10,20,30]]))
        self.assertEqual(result,9/22)
    
    def test_get_col_normalized_range_gives_expected_result_scenar_3(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_col_normalized_range(2,np.array([[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8],[10,20,30]]))
        self.assertEqual(result,11/33)

    def test_get_col_normalized_range_fails_graciously_inexisting_col(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_col_normalized_range(12,np.array([[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8],[10,20,30]]))
        self.assertEqual(result,0)

    def test_get_top_X_most_important_columns_gives_expected_result(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_top_X_most_important_columns(2,np.array([[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8],[10,20,30]]))
        self.assertEqual(len(result),2)
        self.assertTrue(1 in result)
        self.assertTrue(0 in result)
    
    def test_get_top_X_most_important_columns_when_nb_columns_inferior_X(self):
        cr_analyser = CreditRatingAnalyzer()
        cr_analyser.data = [[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8]]
        result = cr_analyser.get_top_X_most_important_columns(12,np.array([[1,2,3],[-1,-2,-3],[4,5,6],[6,7,8],[10,20,30]]))
        self.assertEqual(len(result),3)
        self.assertTrue(1 in result)
        self.assertTrue(0 in result)
        self.assertTrue(2 in result)