import pandas as pd
import numpy as np

class CreditRatingFactorAveragesCalculator:

    def __init__(self, data,entity_id_col_name):
        self.entity_id_col_name =entity_id_col_name
        self.data = data
        self.credit_rating_factors_to_col_names_mapping = {
            "Leverage":["Total Equity to Total Assets - Capital IQ [LTM] (%)","FFO/Debt (%) - Credit Stats Direct [LTM]","Debt/Debt And Equity (%) - Credit Stats Direct [LTM]","CreditModel - Current Liabilities / Net Worth [Latest Quarter] (Model Version 2.6)","CreditModel - Common Equity / Total Assets [Latest Quarter] (Model Version 2.6)","CreditModel - Loans / Deposits [Latest Quarter] (Model Version 2.6)","CreditModel - EBT Interest Coverage [Latest Quarter] (Model Version 2.6)","CreditModel - Retained Earnings / (Debt + Equity) [Latest Quarter] (Model Version 2.6)","CreditModel - Gearing Ratio [Latest Quarter] (Model Version 2.6)","CreditModel - PPE/ Assets [Latest Quarter] (Model Version 2.6)","CreditModel - Free Operating Cash Flow / Debt [Latest Quarter] (Model Version 2.6)","CreditModel - EBIT Interest Coverage [Latest Quarter] (Model Version 2.6)","CreditModel - Cash to Total Debt [Latest Quarter] (Model Version 2.6)","CreditModel - Cash from Operations Interest Coverage [Latest Quarter] (Model Version 2.6)","(FFO + Cash) to Short Term Debt - Capital IQ [LTM]","Total Debt/Revenue - Capital IQ [LTM]","Total Debt/Total Liabilities % - Capital IQ [LTM]","Total Debt to Capital - Capital IQ [LTM]","Net Debt/EBITDA - Capital IQ [LTM]","FFO to Total Debt - Capital IQ [LTM]","EBITDA / Interest Exp. - Capital IQ [LTM]","FFO Interest Coverage - Capital IQ [LTM]",],
            "Profitability":["CreditModel - Net Income / Total Revenue [Latest Quarter] (Model Version 2.6)",
                             "CreditModel - Net Operating Income After Loan Loss Provisions / Revenues [Latest Quarter] (Model Version 2.6)","CreditModel - Sales Growth [Latest Quarter] (Model Version 2.6)","CreditModel - Operating Income (after D&A) / Revenues [Latest Quarter] (Model Version 2.6)","FFO to Gross Profit - Capital IQ [LTM]","EBITDA Margin % - Capital IQ [LTM]","Gross Margin % - Capital IQ [LTM]","Return on Capital - Capital IQ [LTM]","Recurring Earnings / Total Assets - Capital IQ [LTM]"],
            "Financial Statement Lines":["As-Reported Total Revenue - Capital IQ [LTM] ($USD, Historical rate)","Total Equity - Capital IQ [Latest Annual] ($USDmm, Historical rate)","Total Revenue - Capital IQ [LTM] ($USDmm, Historical rate)","Total Equity - Capital IQ [LTM] ($USDmm, Historical rate)"],
            "Liquidity":["CreditModel - Acid Test Ratio [Latest Quarter] (Model Version 2.6)","Quick Ratio - Capital IQ [LTM]","Current Ratio - Capital IQ [LTM]","Basic Defense Interval - Capital IQ [LTM] (Days)","Net Working Capital / Revenue - Capital IQ [LTM]","Net Working Capital/ Total Assets - Capital IQ [LTM]"],
            "Efficiency":["CreditModel - Operating Expense / Total Assets [Latest Quarter] (Model Version 2.6)","CreditModel - Nonperforming assets / Total Assets  [Latest Quarter] (Model Version 2.6)","CreditModel - Operating Cash Flow / Total Assets [Latest Quarter] (Model Version 2.6)","CreditModel - Receivable Turnover [Latest Quarter] (Model Version 2.6)","Asset Turnover - Capital IQ [LTM]","Intangible Assets / Revenue - Capital IQ [LTM]","Payables / Receivables - Capital IQ [LTM]"],
            "Performance":["Management Rate of Return (%) - Capital IQ [LTM]"],
            "Industry Risk":["CUSTOM Industry Outlook Weighted Average","# of Analyst Neutral (3) Industry Recommendations - Capital IQ [Latest]","# of Analyst Lowest (5) Industry Recommendations - Capital IQ [Latest]","# of Analyst Low (4) Industry Recommendations - Capital IQ [Latest]","# of Analyst Highest (1) Industry Recommendations - Capital IQ [Latest]","# of Analyst High (2) Industry Recommendations - Capital IQ [Latest]","Business Segments (Screen by Sum) (Details): % of Revenue [LTM]","Industry Classifications"],
            "Risk":["CreditModel - Loan Loss Provisions / Loans [Latest Quarter] (Model Version 2.6)","CreditModel - Deposits Growth [Latest Quarter] (%) (Model Version 2.6)","CreditModel - Tier 1 Ratio  [Latest Quarter] (Model Version 2.6)"],
            "Country Risk":["CUSTOMPCPIE","CUSTOMBCA","CUSTOMGGX","CUSTOMGGXWDN_NGDP","CUSTOMGGX_NGDP","CUSTOMLP","CUSTOMNGDPPC","CUSTOMLUR","CUSTOMNGDP_FY","CUSTOMPCPI","CUSTOMPPPGDP","CUSTOMPPPPC","Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]","CreditModel - CPI Growth [Latest Quarter] (%) (Model Version 2.6)"],
            "Country Diversification":["CUSTOMGeography Encoding","Number of Geographic Segments [Annual]"],
            "Industry Diversification":["CUSTOMBusiness Encoding","Number of Business Segments [Annual]"],
            "Government Intervention Adjustment":["CreditModel - Revenue/GDP [Latest Quarter] (%) (Model Version 2.6)","CreditModel - Likelihood of Government Support [Latest Quarter] (Model Version 2.6)"],
        }
    
    def encode(self,encoding_type=1):
        match encoding_type:
            case 1:
                return self.encode_using_average()
            case 2:
                return self.encode_using_median()
            case 3:
                return self.encode_using_normalized_average()
        raise ValueError  

    def encode_using_average(self):
        new_dataframe = pd.DataFrame()

        for factor, columns in self.credit_rating_factors_to_col_names_mapping.items():
            valid_columns = [col for col in columns if col in self.data.columns]

            if valid_columns:
                new_dataframe[factor] = self.data[valid_columns].apply(
                    lambda row: np.nanmean([float(val) for val in row if isinstance(val, (int, float))]),
                    axis=1
                )
        if "CUSTOM Credit Rating" in self.data.columns :
            new_dataframe["CUSTOM Credit Rating"] = self.data["CUSTOM Credit Rating"]
        if self.entity_id_col_name in self.data.columns :
            new_dataframe[self.entity_id_col_name] = self.data[self.entity_id_col_name]
        return new_dataframe

    def encode_using_median(self):
        new_dataframe = pd.DataFrame()

        for factor in self.credit_rating_factors_to_col_names_mapping.keys():
            valid_columns = [col for col in self.credit_rating_factors_to_col_names_mapping[factor] if col in self.data.columns]
            if valid_columns:
                new_dataframe[factor] = self.data[valid_columns].apply(
                    lambda row: np.nanmedian([float(val) for val in row if isinstance(val, (int, float))]),
                    axis=1
                )
        if "CUSTOM Credit Rating" in  self.data.columns :
            new_dataframe["CUSTOM Credit Rating"] = self.data["CUSTOM Credit Rating"]
        if self.entity_id_col_name in self.data.columns :
            new_dataframe[self.entity_id_col_name] = self.data[self.entity_id_col_name]
        return new_dataframe
    
    def precompute_column_ranges(self, column_names):
        column_ranges = {}
        for col in column_names:
            col_values = self.data[col]
            numeric_col_values = col_values.apply(pd.to_numeric, errors='coerce').dropna()
            range = numeric_col_values.max() - numeric_col_values.min()
            min = numeric_col_values.min()
            if pd.notna(range):
                column_ranges[col] = [range,min]
        return column_ranges
    
    def calculate_custom_average(self, row, valid_columns, column_ranges):
        normalized_values = []
        for col in valid_columns:
            col_data = column_ranges.get(col)
            if col_data is not None and pd.notna(row[col]):
                numeric_value = pd.to_numeric(row[col], errors='coerce')
                if col_data[0]:
                    normalized_value = (numeric_value - col_data[1]) / col_data[0]
                    normalized_values.append(normalized_value)
                else:
                    normalized_values.append(0)
        return np.nanmean(normalized_values)
    
    def encode_using_normalized_average(self):
        new_dataframe = pd.DataFrame()

        for factor, columns in self.credit_rating_factors_to_col_names_mapping.items():
            valid_columns = [col for col in columns if col in self.data.columns]

            if valid_columns:
                # Precompute column ranges outside the loop
                column_ranges = self.precompute_column_ranges(valid_columns)
                # Apply the custom average calculation using precomputed ranges
                new_dataframe[factor] = self.data.apply(
                    lambda row: self.calculate_custom_average(row, valid_columns,column_ranges),
                    axis=1
                )
        if "CUSTOM Credit Rating" in  self.data.columns :
            new_dataframe["CUSTOM Credit Rating"] = self.data["CUSTOM Credit Rating"]
        if self.entity_id_col_name in self.data.columns :
            new_dataframe[self.entity_id_col_name] = self.data[self.entity_id_col_name]
        return new_dataframe
