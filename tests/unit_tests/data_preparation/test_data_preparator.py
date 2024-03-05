import unittest
from analysis.data_configuration import DataConfiguration
from data_preparation.data_preparator import DataPreparator
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
    
    def test_col_names_order_is_maintained_and_returned_accurately(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted(["RATIO"])
        dp = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening"))
        dp.apply_configuration()
        col_names = dp.get_column_names()
        expected_col_names = ["Cost of Borrowing  Capital IQ [Latest Annual] (%)",
            "Recurring Earnings / Total Assets  Capital IQ [LTM]",
            "EBITDA Margin %  Capital IQ [LTM]",
            "FFO Interest Coverage  Capital IQ [LTM]",
            "EBITDA / Interest Exp.  Capital IQ [LTM]",
            "Current Ratio  Capital IQ [LTM]",
            "State Owner  % Owned [Latest Quarter] (%)",
            "(EBITDACAPEX) / Interest Exp.  Capital IQ [LTM]",
            "Debt Fixed Charge Coverage (%)  Credit Stats Direct [LTM]",
            "Efficiency Ratio  Capital IQ [Latest Quarter]",
            "Annual Revenue Growth (%), Adj.  Credit Stats Direct [Latest Annual]",
            "Avg. Interest Bearing Liabilities, 1 Yr Growth %  Capital IQ [Latest Annual] (%)",
            "(FFO + Cash) to Short Term Debt  Capital IQ [LTM]",
            "Cash from Ops. to Curr. Liab.  Capital IQ [Latest Quarter]",
            "Total Debt/Equity %  Capital IQ [Latest Quarter]",
            "Total Debt/Capital %  Capital IQ [Latest Quarter]",
            "Total Liabilities/Total Assets %  Capital IQ [Latest Quarter]",
            "EBIT / Interest Exp.  Capital IQ [LTM]",
            "Total Debt/EBITDA  Capital IQ [LTM]",
            "Net Debt/EBITDA  Capital IQ [LTM]",
            "EBITDA, Excl. Operating Leases/Interest Expense  Capital IQ [LTM]",
            "(EBITDA, Excl. Operating LeasesCAPEX)/Interest Exp.  Capital IQ [LTM]",
            "Total Debt / EBITDA, Excl. Operating Leases  Capital IQ [LTM]",
            "Altman Z Score  Capital IQ [LTM]",
            "Capex as % of Revenues  Capital IQ [Latest Annual] (%)",
            "EBITDA, 1 Yr Growth %  Capital IQ [LTM] (%)",
            "Normalized Net Income, 1 Yr Growth %  Capital IQ [LTM] (%)",
            "Return on Assets %  Capital IQ [LTM]",
            "Return on Capital %  Capital IQ [LTM]",
            "Return on Equity %  Capital IQ [LTM]",
            "EBITA Margin %  Capital IQ [LTM]",
            "EBIT Margin %  Capital IQ [LTM]",
            "Net Income Margin %  Capital IQ [LTM]",
            "Levered Free Cash Flow Margin %  Capital IQ [LTM]",
            "Unlevered Free Cash Flow Margin %  Capital IQ [LTM]",
            "Inventory Turnover  Capital IQ [Latest Quarter]",
            "Current Ratio  Capital IQ [Latest Quarter]",
            "Quick Ratio  Capital IQ [Latest Quarter]",
            "Avg. Cash Conversion Cycle  Capital IQ [Latest Quarter] (Days)"]
        order_is_kept = True
        for i in range(1,len(col_names)):
            prior_col = col_names[i-1]
            col = col_names[i]
            if not expected_col_names.index(prior_col) < expected_col_names.index(col):
                order_is_kept = False
        self.assertTrue(order_is_kept)
    
    def test_credit_rating_order_is_maintained_and_returned_accurately(self):
        configuration = DataConfiguration()
        configuration.set_data_types_wanted(["RATIO"])
        dp = DataPreparator(configuration,DataSource(path = "./data/Jan download.xls", sheet_name = "Screening"))
        dp.apply_configuration(0.05)
        credit_ratings = dp.get_credit_ratings()
        expected_10_first_credit_ratings = [9.0,9.0,6.0,8.0,12.0,6.0,9.0,12.0,12.0,9.0]
        self.assertEqual(credit_ratings[:10],expected_10_first_credit_ratings)