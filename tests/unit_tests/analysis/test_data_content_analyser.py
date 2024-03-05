import unittest
import pandas as pd
from analysis.data_content_analyser import DataContentAnalyser

class TestDataContentAnalyser(unittest.TestCase):

    def __init__(self, methodName: str = "runTest"):
        self.data = pd.DataFrame({"col 1":[1,2,3,4,-4],"col 2":[4,5,6,3,2]})
        super().__init__(methodName)

    def test_data_content_analyser_produces_accurate_analysis(self):
        result = DataContentAnalyser(self.data,"",[1,1,2,2,3]).analyse_data()
        self.assertEqual(result["Number of Companies"],5)
        self.assertEqual(result["Number of Columns"],2)
        self.assertEqual(result["Share of each Credit Rating"][1],0.4)
        self.assertEqual(result["Share of each Credit Rating"][2],0.4)
        self.assertEqual(result["Share of each Credit Rating"][3],0.2)
        self.assertTrue("col 1" in result["List of Columns"])
        self.assertTrue("col 2" in result["List of Columns"])
        self.assertEqual(len(result["List of Columns"]),2)
    
    def test_fails_graciously_when_no_credit_ratings_info(self):
        result = DataContentAnalyser(self.data,"",[]).analyse_data()
        self.assertEqual(result["Number of Companies"],5)
        self.assertEqual(result["Number of Columns"],2)
        self.assertEqual(len(result["Share of each Credit Rating"].keys()),0)
        self.assertTrue("col 1" in result["List of Columns"])
        self.assertTrue("col 2" in result["List of Columns"])
        self.assertEqual(len(result["List of Columns"]),2)