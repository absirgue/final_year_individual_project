import unittest
import pandas as pd
from data_preparation.data_frame_cleaner import DataFrameCleaner
from data_preparation.data_type_isolator import DataTypeIsolator

class TestDataFrameCleaner(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.read_excel("./data/raw_financial_data_and_ratios.xls", sheet_name="Screening")
        super().__init__(methodName)

    def test_numerical_columns_are_kept(self):
        data = self.run_data_preparation(["INDUSTRY OUTLOOK","CORE"])
        result = DataFrameCleaner(data).clean(threshold_of_column_emptiness=1)
        self.assertIn("# of Analyst Buy (1) Industry Recommendations  Capital IQ [Latest]",result)
        self.assertIn("# of Analyst High (2) Industry Recommendations  Capital IQ [Latest]",result)
        self.assertIn("# of Analyst Highest (1) Industry Recommendations  Capital IQ [Latest]",result)
        self.assertIn("# of Analyst Hold (3) Industry Recommendations  Capital IQ [Latest]",result)
        self.assertIn("# of Analyst Low (4) Industry Recommendations  Capital IQ [Latest]",result)
        self.assertIn("# of Analyst Lowest (5) Industry Recommendations  Capital IQ [Latest]",result)
        self.assertIn("# of Analyst Neutral (3) Industry Recommendations  Capital IQ [Latest]",result)  		

    def test_non_numerical_columns_are_left_out(self):
        data = self.run_data_preparation(["INDUSTRY OUTLOOK","CORE"])
        result = DataFrameCleaner(data).clean(threshold_of_column_emptiness=1)
        self.assertNotIn("Company Name",result)
        self.assertNotIn("Exchange:Ticker",result)
    
    def test_parenthetical_statements_are_removed(self):
        data = self.run_data_preparation(["PROBABILITY OF DEFAULT"])
        result = DataFrameCleaner(data).clean(threshold_of_column_emptiness=1)
        self.assertEqual("0.2055 ",result.loc[1,"Market Signal Probability of Default (NonRatings) [Latest]"])
    
    def run_data_preparation(self, data_types_wanted):
        raw_return =  DataTypeIsolator(self.data,"","").isolate_data_types(data_types_wanted)
        raw_return.columns = raw_return.iloc[0]
        raw_return = raw_return.drop(0)
        return raw_return