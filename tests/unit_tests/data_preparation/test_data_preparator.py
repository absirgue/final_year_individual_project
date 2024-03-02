import unittest
from main import DataPreparator,DataConfiguration
from analysis.data_configuration import DataSource
class TestDataPreparator(unittest.TestCase):
    
    def test_configuration_with_all_encodings_is_executed_correctly(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted([])
        configuration.set_country_risk_score_encoding_preference(True)
        configuration.set_business_diversification_encoding_preference(True,0)
        configuration.set_industry_name_encoding_preference(True)
        configuration.set_geography_diversification_encoding_preference(True,0)
        configuration.set_indutry_outlooks_encoding_preference(True,{'buy':1,'high':1,'highest':1,'hold':1,'low':1,'lowest':1,'neutral':1})
        dp = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening"))
        dp.apply_configuration()
        result = dp.get_intermediary_dataframe()
        # Business diversification encoding happened
        self.assertIn("CUSTOMBusiness Encoding",result.columns)
        # Geography diversification encoding happened
        self.assertIn("CUSTOMGeography Encoding",result.columns)
        # Country risk score one-hot encoding happened
        self.assertIn("aa+ ",result.columns)
        # Ratios not demanded are not present
        self.assertNotIn("State Owner  % Owned [Latest Quarter] (%)",result.columns)
        # Raw numbers not demanded are not present
        self.assertNotIn("AsReported Total Revenue  Capital IQ [LTM] ($USD, Historical rate)",result.columns)
        # Core data not demanded are not present
        self.assertNotIn("Exchange:Ticker",result.columns)

    def test_encodings_not_demanded_are_not_executed(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted([])
        configuration.set_country_risk_score_encoding_preference(True)
        configuration.set_business_diversification_encoding_preference(False,0)
        configuration.set_industry_name_encoding_preference(True)
        configuration.set_geography_diversification_encoding_preference(True,0)
        configuration.set_indutry_outlooks_encoding_preference(True,{'buy':1,'high':1,'highest':1,'hold':1,'low':1,'lowest':1,'neutral':1})
        dp = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening"))
        dp.apply_configuration()
        result = dp.get_intermediary_dataframe()
        self.assertNotIn("CUSTOMBusiness Encoding",result.columns)
    
    def test_data_types_not_demanded_are_not_kept(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted(["RATIO"])
        dp = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening"))
        dp.apply_configuration()
        result = dp.get_intermediary_dataframe()
        self.assertNotIn("Number of Geographic Segments [Annual]",result.columns)
        self.assertNotIn("# of Analyst Lowest (5) Industry Recommendations  Capital IQ [Latest]",result.columns)
        self.assertNotIn("Industry Classifications",result.columns)
        self.assertNotIn("Earnings from Cont. Ops.  Capital IQ [LTM] ($USDmm, Historical rate)",result.columns)
    