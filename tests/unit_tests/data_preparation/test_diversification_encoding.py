import unittest
import pandas as pd
from data_preparation.diversification_encoding import DiversificationEncoding

class TestDiversificationEncoding(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({'Number of Geographic Segments [Annual]':["12"],"Number of Business Segments [Annual]":["30"],"Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]":["US: 12 (12%);UK: 34 (24%); FR: 52 (42%); Unknwon (20%)"],"Business Segments (Screen by Sum) (Details): % of Revenue [LTM]":["Cosmetics: 12 (12%);Variation: 34 (24%); Variation (again): 52 (42%); Unknwon (20%)"]})
        super().__init__(methodName)
    
    def test_encoding_with_geographic_segment_count_is_successful(self):
        result = DiversificationEncoding(self.data).encode(1,"Geography")
        self.assertEqual(result.loc[0,'CUSTOMGeography Encoding'], '12')
    
    def test_encoding_with_business_segment_count_is_successful(self):
        result = DiversificationEncoding(self.data).encode(1,"Business")
        self.assertEqual(result.loc[0,'CUSTOMBusiness Encoding'], '30')
    
    def test_encoding_with_geographic_segment_entropy_is_successful(self):
        result = DiversificationEncoding(self.data).encode(0,"Geography")
        self.assertEqual(result.loc[0,'CUSTOMGeography Encoding'],1.419556298571613)
    
    def test_encoding_with_business_segment_entropy_is_successful(self):
        result = DiversificationEncoding(self.data).encode(0,"Business")
        self.assertEqual(result.loc[0,'CUSTOMBusiness Encoding'],1.419556298571613)