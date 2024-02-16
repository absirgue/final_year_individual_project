import pandas as pd
import xlrd
from data_preparation.data_type_isolator import DataTypeIsolator
from data_preparation.one_hot_encoding import CountryRiskScoreOneHotEncoding
from data_preparation.country_economic_encoding import CountryEconomicEncoding
from data_preparation.industry_outlooks_encoder import IndustryOutlookEncode
from data_preparation.diversification_encoding import DiversificationEncoding
from data_preparation.data_frame_cleaner import DataFrameCleaner
from data_preparation.industry_name_encoding import IndustryNameHashEncoding

class DataPreparator:

    def __init__(self,configuration,data_source):
        self.configuration = configuration 
        self.data_source = data_source
        self.data = self.read_data_from_csv()

    def read_data_from_csv(self):
        return pd.read_excel(self.data_source.path, sheet_name=self.data_source.sheet_name)
    
    def apply_configuration(self,threshold_of_column_emptiness=0):
        data = DataTypeIsolator(self.data).isolate_data_types(self.configuration.data_types)
        # We can now remove the data "categories"
        data.columns = data.iloc[0]
        data = data.drop(0)
        initial_columns_count = data.shape[1]
        if self.configuration.encode_geography_diversification:
            data = DiversificationEncoding(data).encode(self.configuration.geography_encoding_type,"Geography")
        if self.configuration.encode_business_diversification:
            data = DiversificationEncoding(data).encode(self.configuration.business_encoding_type,"Business")
        if self.configuration.encode_country_risk_score:
            data = CountryRiskScoreOneHotEncoding(data).encode()
        if self.configuration.encode_industry_name:
            data = IndustryNameHashEncoding(data).encode()
        if self.configuration.encode_industry_outlooks:
            data = IndustryOutlookEncode(data).encode(self.configuration.outlooks_weight_distribution)
        if self.configuration.encode_country:
            data = CountryEconomicEncoding(data).encode()
        self.number_added_columns = data.shape[1] - initial_columns_count
        data = DataFrameCleaner(data).clean(threshold_of_column_emptiness)
        self.write_to_csv(data)
        return data
    
    def get_number_added_columns(self):
        return self.number_added_columns
    
    def write_to_csv(self,data):
        df = pd.DataFrame(data)
        excel_filename = 'data_preparator_output.csv'
        df.to_csv(excel_filename, index=False)
        return data
