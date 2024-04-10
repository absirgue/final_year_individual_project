import unittest
from analysis.hyperparameters_optimisation.list_transformations import ListTransformations

class TestListTransformations(unittest.TestCase):

    def test_extract_3d_list_from_list_of_dics_gives_expected_result(self):
        result = ListTransformations().extract_3d_list_from_list_of_dics([{"A":1,"B":2,"C":4,"D":8},{"A":4,"B":5,"C":6,"D":7}],"A","B","D")
        self.assertEqual(result,[[1,2,8],[4,5,7]])
    
    def test_extract_2d_list_from_list_of_dics_gives_expected_result(self):
        result = ListTransformations().extract_2d_list_from_list_of_dics([{"A":1,"B":2,"C":4,"D":8},{"A":4,"B":5,"C":6,"D":7}],"A","D")
        self.assertEqual(result,[[1,8],[4,7]])
    
    def test_extract_list_from_list_of_dics_gives_expected_result(self):
        result = ListTransformations().extract_list_from_list_of_dics([{"A":1,"B":2,"C":4,"D":8},{"A":4,"B":5,"C":6,"D":7}],"A")
        self.assertEqual(result,[1,4])
