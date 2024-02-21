import unittest
from data_treatment.principal_component_analysis import PrincipalComponentAnalysis
import pandas as pd
import numpy as np
class TestPrincipalComponentAnalysis(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        self.data = pd.DataFrame({"col 1":[1,-4,-3.14],"col 2":[-30,6.789,0.1],"col 3": [12,30,-12],"col 4":[-1,0.01,98]})
        super().__init__(methodName)

    def test_principal_component_analysis_gives_expected_result(self):
        obtained_components = PrincipalComponentAnalysis(self.data,2).get_principal_components()
        self.assertTrue(np.array_equal(obtained_components,[[1.9917240408405805,-0.6723157797872941],
                                                            [-0.32398847423276017,1.8309341493965197],
                                                            [-1.66773556660782,-1.1586183696092256]]))
    
    def test_total_explained_variance_ratio_is_as_expected(self):
        total_explained_variance = PrincipalComponentAnalysis(self.data,2).get_total_explained_variance_ratio()
        self.assertEqual(total_explained_variance,1)
    
    def test_fails_as_expected_when_no_data(self):
        with self.assertRaises(ValueError):
            PrincipalComponentAnalysis(pd.DataFrame(),0)
    
    def test_fails_as_expected_when_data_can_not_be_further_reduced(self):
        with self.assertRaises(ValueError):
            PrincipalComponentAnalysis(pd.DataFrame({"col 1":[1,2,3]}),0)

    def test_explained_variance_ratio_is_as_expected(self):
        explained_variance_ratios = PrincipalComponentAnalysis(self.data,2).get_explained_variance_ratios()
        self.assertTrue(np.array_equal(explained_variance_ratios,[0.5711062588688923,0.4288937411311077]))
    
    def test_fails_as_expected_when_number_of_components_greater_than_number_of_features(self):
        with self.assertRaises(ValueError):
            PrincipalComponentAnalysis(self.data,5) 