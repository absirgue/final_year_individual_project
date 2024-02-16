import unittest
from data_preparation.industry_outlooks_encoder import IndustryOutlookEncode
import pandas as pd

class TestIndustryOutlookEncoder(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({'# of Analyst Buy (1) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst High (2) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst Highest (1) Industry Recommendations  Capital IQ [Latest]':[2],'# of Analyst Hold (3) Industry Recommendations  Capital IQ [Latest]':[3],'# of Analyst Low (4) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst Lowest (5) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst Neutral (3) Industry Recommendations  Capital IQ [Latest]':[1]})
        super().__init__(methodName)

    def test_successful_with_equal_weights(self):
        result = IndustryOutlookEncode(self.data).encode({'buy':1,'high':1,'highest':1,'hold':1,'low':1,'lowest':1,'neutral':1})
        self.assertEqual(result.loc[0,'Industry Outlook Weighted Average'],10)

    def test_successful_with_different_weights(self):
        result = IndustryOutlookEncode(self.data).encode({'buy':1,'high':1,'highest':2,'hold':7,'low':1,'lowest':1,'neutral':1})
        self.assertEqual(result.loc[0,'Industry Outlook Weighted Average'],30)

    def test_fails_graciously_when_no_weight(self):
        try:
            result = IndustryOutlookEncode(self.data).encode({})
        except:
            self.fail("Weight missing fails ungraciously")
    
    def test_fails_graciously_when_one_column_is_missing(self):
        try:
            result = IndustryOutlookEncode(pd.DataFrame({'# of Analyst High (2) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst Highest (1) Industry Recommendations  Capital IQ [Latest]':[2],'# of Analyst Hold (3) Industry Recommendations  Capital IQ [Latest]':[3],'# of Analyst Low (4) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst Lowest (5) Industry Recommendations  Capital IQ [Latest]':[1],'# of Analyst Neutral (3) Industry Recommendations  Capital IQ [Latest]':[1]})).encode({'buy':1,'high':1,'highest':2,'hold':7,'low':1,'lowest':1,'neutral':1})
        except:
            self.fail("Column missing fails ungraciously")
    
    def test_fails_graciously_when_one_weight_is_missing(self):
        try:
            result = IndustryOutlookEncode(self.data).encode({'high':1,'highest':2,'hold':7,'low':1,'lowest':1,'neutral':1})
        except:
            self.fail("Weights missing fails ungraciously")
    
    def test_fails_graciously_when_all_columns_are_missing(self):
        try:
            result = IndustryOutlookEncode(pd.DataFrame({})).encode({'buy':1,'high':1,'highest':2,'hold':7,'low':1,'lowest':1,'neutral':1})
        except:
            self.fail("Columns missing fails ungraciously")
