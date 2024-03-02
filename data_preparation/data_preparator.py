import pandas as pd
import xlrd
from data_preparation.data_type_isolator import DataTypeIsolator
from data_preparation.one_hot_encoding import CountryRiskScoreOneHotEncoding
from data_preparation.country_economic_encoding import CountryEconomicEncoding
from data_preparation.industry_outlooks_encoder import IndustryOutlookEncode
from data_preparation.diversification_encoding import DiversificationEncoding
from data_preparation.data_frame_cleaner import DataFrameCleaner
from data_preparation.industry_name_encoding import IndustryNameHashEncoding
from data_preparation.credit_rating_encoding import CreditRatingEncoding
from data_preparation.credit_rating_factor_averages_calculator import CreditRatingFactorAveragesCalculator
class DataPreparator:

    def __init__(self,configuration,data_source):
        self.intermediary_dataframe = None
        self.NAME_CREDIT_RATING_ABSTRACT_COL = "CREDIT RATING"
        self.NAME_CREDIT_RATING_COL = "S&P Entity Credit Rating - Issuer Credit Rating - Local Currency LT [Latest] (Rating)"
        self.configuration = configuration 
        self.data_source = data_source
        self.col_names = None
        self.credit_ratings = None
        self.data = self.read_data_from_csv()

    def read_data_from_csv(self):
        return pd.read_excel(self.data_source.path, sheet_name=self.data_source.sheet_name)
    
    def apply_configuration(self,threshold_of_column_emptiness=0):
        data = DataTypeIsolator(self.data,self.NAME_CREDIT_RATING_ABSTRACT_COL).isolate_data_types(self.configuration.data_types)
        data.columns = data.iloc[0]
        data = data.drop(0)
        initial_columns_count = data.shape[1]
        data,self.NAME_CREDIT_RATING_COL = CreditRatingEncoding(data,self.NAME_CREDIT_RATING_COL).encode()
        data = data.drop_duplicates()
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
            data = CountryEconomicEncoding(data,self.configuration.normalise_economic_variables).encode()
        self.number_added_columns = data.shape[1] - initial_columns_count
        if self.configuration.average_by_cr_factor:
            data = CreditRatingFactorAveragesCalculator(data).encode()
        self.write_to_csv_1(data)
        self.intermediary_dataframe = data
        data = DataFrameCleaner(data).clean(threshold_of_column_emptiness)
        data = self.extract_and_delete_product_ratings(data)
       
        self.write_to_csv(data)
        self.col_names = data.columns
        data = data.values
        data = data.astype(float)
        return data

    def get_intermediary_dataframe(self):
        return self.intermediary_dataframe
    
    def extract_and_delete_product_ratings(self,data):
        if "CUSTOM Credit Rating" in data.columns:
            self.credit_ratings = []
            for index, row in data.iterrows():
                cell_content = data.loc[index,self.NAME_CREDIT_RATING_COL]
                if type(cell_content) == pd.core.series.Series:
                    cell_content = cell_content.iloc[0]
                self.credit_ratings.append(cell_content)
            data.drop(self.NAME_CREDIT_RATING_COL, axis=1,inplace=True)
        return data
    
    def remove_custom_columns(self,dataframe):
        columns_to_remove = [col for col in dataframe.columns if col.startswith("CUSTOM")]
        dataframe.drop(columns=columns_to_remove, inplace=True)
        return dataframe
    
    def get_encoding_of_first_junk_rating(self):
        return CreditRatingEncoding().get_encoding_first_junk_rating()

    def get_column_names(self):
        return self.col_names

    def get_credit_ratings(self):
        return self.credit_ratings
    
    def get_number_added_columns(self):
        return self.number_added_columns
    
    def write_to_csv(self,data):
        df = pd.DataFrame(data)
        excel_filename = 'data_preparator_output.csv'
        df.to_csv(excel_filename, index=False)
        return data

    def write_to_csv_1(self,data):
        df = pd.DataFrame(data)
        excel_filename = 'data_preparator_output_1.csv'
        df.to_csv(excel_filename, index=False)
        return data