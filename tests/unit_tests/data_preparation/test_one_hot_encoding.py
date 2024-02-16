import unittest
from data_preparation.one_hot_encoding import CountryRiskScoreOneHotEncoding,IndustryOneHotEncoding
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


class TestIndustryOneHotEncoding(unittest.TestCase):
      
    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({ 'Industry Classifications': ["industry 1 (Primary); industry 2 (Primary); industry 3 (not primary)","industry 1 (Secondary); industry 2 (Minor); industry 3 (Primary)", "industry 1 (Primary); industry 2 (Primary); industry 3 ", "","not an industry classification", "industry 1 (); industry 2 (); industry ()"]})
        super().__init__(methodName)
        
    def test_behave_as_expected_in_perfect_conditions(self):
        result = IndustryOneHotEncoding(self.data).encode()
        # Check first line
        self.assertEqual(result.loc[0,"industry 1 (Primary)"],1)
        self.assertEqual(result.loc[0,"industry 2 (Primary)"],1)
        self.assertEqual(result.loc[0,"industry 3 (Primary)"],0)
        # Check second line
        self.assertEqual(result.loc[1,"industry 1 (Primary)"],0)
        self.assertEqual(result.loc[1,"industry 2 (Primary)"],0)
        self.assertEqual(result.loc[1,"industry 3 (Primary)"],1)
    
    def test_behaves_correctly_when_no_parenthetical_statement(self):
        result = IndustryOneHotEncoding(self.data).encode()
        self.assertEqual(result.loc[2,"industry 1 (Primary)"],1)
        self.assertEqual(result.loc[2,"industry 2 (Primary)"],1)
        self.assertEqual(result.loc[2,"industry 3 (Primary)"],0)
    
    def test_behaves_correctly_on_empty_cell(self):
        result = IndustryOneHotEncoding(self.data).encode()
        self.assertEqual(result.loc[3,"industry 1 (Primary)"],0)
        self.assertEqual(result.loc[3,"industry 2 (Primary)"],0)
        self.assertEqual(result.loc[3,"industry 3 (Primary)"],0)
    
    def test_behaves_correctly_on_unstructured_cell(self):
        result = IndustryOneHotEncoding(self.data).encode()
        self.assertEqual(result.loc[4,"industry 1 (Primary)"],0)
        self.assertEqual(result.loc[4,"industry 2 (Primary)"],0)
        self.assertEqual(result.loc[4,"industry 3 (Primary)"],0)
    
    def test_behaves_correctly_on_all_empty_parenthesis(self):
        result = IndustryOneHotEncoding(self.data).encode()
        self.assertEqual(result.loc[5,"industry 1 (Primary)"],0)
        self.assertEqual(result.loc[5,"industry 2 (Primary)"],0)
        self.assertEqual(result.loc[5,"industry 3 (Primary)"],0)