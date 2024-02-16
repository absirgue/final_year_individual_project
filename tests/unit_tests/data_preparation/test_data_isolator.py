import unittest
from data_preparation.data_type_isolator import DataTypeIsolator
import pandas as pd

class DataIsolatorUnitTests(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.read_excel("./data/Jan download.xls", sheet_name="Screening")
        super().__init__(methodName)

    def test_can_isolate_ratios(self):
        result = self.run_data_preparation(["RATIO"])
        self.assertIn("Debt Fixed Charge Coverage (%)  Credit Stats Direct [LTM]",result.columns)
        self.assertIn("(EBITDACAPEX) / Interest Exp.  Capital IQ [LTM]",result.columns)
        self.assertNotIn("Interest Expense  Finance Division  Capital IQ [LTM] ($USDmm, Historical rate)",result.columns)
        self.assertNotIn("Industry Classifications",result.columns)

    def test_can_isolate_ratios_and_country_credit_rating(self):
        result = self.run_data_preparation(["RATIO","COUNTRY RISK SCORE"])
        self.assertIn("Debt Fixed Charge Coverage (%)  Credit Stats Direct [LTM]",result.columns)
        self.assertIn("(EBITDACAPEX) / Interest Exp.  Capital IQ [LTM]",result.columns)
        self.assertNotIn("Interest Expense  Finance Division  Capital IQ [LTM] ($USDmm, Historical rate)",result.columns)
        self.assertNotIn("Industry Classifications",result.columns)
        self.assertIn("PD Fundamental  Country/Region Risk Score [Latest Quarter] (Model Version 1.0)",result.columns)
    
    def test_isolate_unexisting_category_fails_graciously(self):
        try:
            result = self.run_data_preparation(["I DON'T EXIST"])
        except Exception:
            self.fail("Error was raised with non-existing category.")
    
    def test_can_keep_no_data_category(self):
        try:
            result = self.run_data_preparation([])
        except Exception:
            self.fail("Error was raised with no category.")

    def run_data_preparation(self, data_types_wanted):
        raw_return =  DataTypeIsolator(self.data).isolate_data_types(data_types_wanted)
        raw_return.columns = raw_return.iloc[0]
        raw_return = raw_return.drop(0)
        return raw_return