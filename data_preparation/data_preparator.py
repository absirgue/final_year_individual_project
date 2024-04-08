import pandas as pd
import xlrd
from data_preparation.data_type_isolator import DataTypeIsolator
from data_preparation.one_hot_encoding import CountryRiskScoreOneHotEncoding
from data_preparation.country_economic_encoding import CountryEconomicEncoding
from data_preparation.industry_outlook_encoder import IndustryOutlookEncode
from data_preparation.diversification_encoding import DiversificationEncoding
from data_preparation.data_frame_cleaner import DataFrameCleaner
from data_preparation.industry_name_encoding import IndustryNameHashEncoding
from data_preparation.credit_rating_encoding import CreditRatingEncoding
from data_preparation.credit_rating_factor_averages_calculator import CreditRatingFactorAveragesCalculator
class DataPreparator:
    """
    Coordinates all operations of our Data Preprocessing subsystem. 
    """

    def __init__(self,configuration,data_source):
        self.intermediary_dataframe = None
        self.NAME_CREDIT_RATING_ABSTRACT_COL = "CREDIT RATING"
        self.NAME_CREDIT_RATING_COL = "S&P Entity Credit Rating - Issuer Credit Rating - Local Currency LT [Latest] (Rating)"
        self.NAME_SP_ENTITY_ID_ABSTRACT_COL = "ENTITY ID"
        self.NAME_SP_ENTITY_ID_COL = "S&P Entity ID"
        self.configuration = configuration 
        self.data_source = data_source
        self.col_names = None
        self.credit_ratings = None
        self.entity_ids = None
        self.data = self.read_data_from_csv()

    def read_data_from_csv(self):
        return pd.read_excel(self.data_source.path, sheet_name=self.data_source.sheet_name)
    
    """
    Coordinates the application of all preprocessing technqiues specified in a given data 
    configuration. The encoded data set is then cleaned and striped of empty values. 
    We however save ordered lists of encoded credit rating values, column names, and 
    S&P Entity ID values (a unique identified for each company.)

    Returns: the modified data set in the form of a 2D array of numbers. 
    """
    def apply_configuration(self,threshold_of_column_emptiness=0.05):
        data = DataTypeIsolator(self.data,self.NAME_CREDIT_RATING_ABSTRACT_COL,self.NAME_SP_ENTITY_ID_ABSTRACT_COL).isolate_data_types(self.configuration.data_types)
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
            data = CreditRatingFactorAveragesCalculator(data,self.NAME_SP_ENTITY_ID_COL).encode(self.configuration.average_by_cr_factor)
        self.intermediary_dataframe = data
        # Note: Entity ID is a number and it is defined for all lines, it therefore will not be affected
        # by the dataframe cleaner
        data = DataFrameCleaner(data).clean(threshold_of_column_emptiness)
        data = self.extract_and_delete_credit_ratings(data)
        data = self.extract_and_delete_entity_ids(data)
        self.col_names = data.columns
        data = data.values
        data = data.astype(float)
        return data

    # Useful only to provide insights on the encoded data frame before it is cleaned. 
    def get_intermediary_dataframe(self):
        return self.intermediary_dataframe
    
    # Extracts and stores an ordered list of S&P Entity ID values before deleting the related feature.
    def extract_and_delete_entity_ids(self, data):
        if self.NAME_SP_ENTITY_ID_COL in data.columns:
            self.entity_ids = []
            for index, row in data.iterrows():
                cell_content = data.loc[index,self.NAME_SP_ENTITY_ID_COL]
                if type(cell_content) == pd.core.series.Series:
                    cell_content = cell_content.iloc[0]
                self.entity_ids.append(cell_content)
            data.drop(self.NAME_SP_ENTITY_ID_COL, axis=1,inplace=True)
        else:
            print("NO COLUMN NAMED CORRECTLY FOR DATA TYPE EXTRACTION")
        return data

    # Returns the S&P Entity ID value of a given row of our encoded data set.
    def get_entity_id_of_row(self,row_idx):
        return self.entity_ids[row_idx]

    # Returns the ordered list of S&P Entity IDs.
    def get_entity_ids(self):
        return self.entity_ids

    # Extracts and stores an ordered list of Credit Ratin values before deleting the related feature.
    def extract_and_delete_credit_ratings(self,data):
        if "CUSTOM Credit Rating" in data.columns:
            self.credit_ratings = []
            for index, row in data.iterrows():
                cell_content = data.loc[index,self.NAME_CREDIT_RATING_COL]
                if type(cell_content) == pd.core.series.Series:
                    cell_content = cell_content.iloc[0]
                self.credit_ratings.append(float(cell_content))
            data.drop(self.NAME_CREDIT_RATING_COL, axis=1,inplace=True)
        return data
    
    # Returns an ordered list of column names
    def get_column_names(self):
        return list(self.col_names)

    # Returns an ordered list of credit rating values.
    def get_credit_ratings(self):
        return self.credit_ratings
    
    # Returns the number of columns that was added by our encoding operations.
    def get_number_added_columns(self):
        return self.number_added_columns