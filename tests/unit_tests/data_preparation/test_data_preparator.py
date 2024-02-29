import unittest
from main import DataPreparator,DataConfiguration,DataSource
class TestDataPreparator(unittest.TestCase):
    
    def test_configuration_with_all_encodings_is_executed_correctly(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted([])
        configuration.set_country_risk_score_encoding_preference(True)
        configuration.set_business_diversification_encoding_preference(True,0)
        configuration.set_industry_name_encoding_preference(True)
        configuration.set_geography_diversification_encoding_preference(True,0)
        configuration.set_indutry_outlooks_encoding_preference(True,{'buy':1,'high':1,'highest':1,'hold':1,'low':1,'lowest':1,'neutral':1})
        result = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")).apply_configuration()
        # Business diversification encoding happened
        self.assertIn("Business Encoding",result.columns)
        # Geography diversification encoding happened
        self.assertIn("Geography Encoding",result.columns)
        # Country risk score one-hot encoding happened
        self.assertIn("aa+ ",result.columns)
        # Industry name one-hot encoding happened
        self.assertIn("Electric Power Distribution (Primary)",result.columns)
        # Industry outlook encoding happened
        self.assertIn("Electric Power Distribution (Primary)",result.columns)
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
        result = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")).apply_configuration()
        self.assertNotIn("Business Encoding",result.columns)
        self.assertIn("Geography Encoding",result.columns)
    
    def test_data_types_not_demanded_are_not_kept(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted(["RATIO"])
        result = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")).apply_configuration()
        self.assertNotIn("Number of Geographic Segments [Annual]",result.columns)
        self.assertNotIn("# of Analyst Lowest (5) Industry Recommendations  Capital IQ [Latest]",result.columns)
        self.assertNotIn("Industry Classifications",result.columns)
        self.assertNotIn("Earnings from Cont. Ops.  Capital IQ [LTM] ($USDmm, Historical rate)",result.columns)
    
    def test_non_numerical_columns_are_left_out(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted(["RATIO","DIVERSIFICATION - GEOGRAPHIC SEGMENTS - REVENUE"])
        result = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")).apply_configuration()
        self.assertNotIn("Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]",result.columns)
    
