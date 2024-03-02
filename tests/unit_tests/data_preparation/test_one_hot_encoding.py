import unittest
from data_preparation.one_hot_encoding import CountryRiskScoreOneHotEncoding
import pandas as pd

class TestCountryRiskScoreOneHotEncoding(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({ "PD Fundamental  Country/Region Risk Score [Latest Quarter] (Model Version 1.0)": ["aaa", "aa+", "","not a risk score"]})
        super().__init__(methodName)
        
    def test_one_hot_encoding_is_as_expected(self):
        result = CountryRiskScoreOneHotEncoding(self.data).encode()
        # Check first line
        self.assertEqual(result.loc[0,"No Country Risk Score Known"],0)
        self.assertEqual(result.loc[0,"aa+"],0)
        self.assertEqual(result.loc[0,"aaa"],1)
        # Check second line
        self.assertEqual(result.loc[1,"No Country Risk Score Known"],0)
        self.assertEqual(result.loc[1,"aa+"],1)
        self.assertEqual(result.loc[1,"aaa"],0)

    def test_behaves_as_expected_when_no_country_risk_score(self):
        result = CountryRiskScoreOneHotEncoding(self.data).encode()
        self.assertEqual(result.loc[2,"No Country Risk Score Known"],1)
        self.assertEqual(result.loc[2,"aa+"],0)
        self.assertEqual(result.loc[2,"aaa"],0)

    def test_behaves_as_expected_when_invalid(self):
        result = CountryRiskScoreOneHotEncoding(self.data).encode()
        self.assertEqual(result.loc[3,"No Country Risk Score Known"],1)
        self.assertEqual(result.loc[3,"aa+"],0)
        self.assertEqual(result.loc[3,"aaa"],0)
