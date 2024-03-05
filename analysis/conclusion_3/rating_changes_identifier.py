import pandas as pd
from data_preparation.credit_rating_encoding import CreditRatingEncoding

class RatingChangesIdentifier:

    def __init__(self, data_source):
        self.data_source = data_source
    
    def identify_changes(self):
        original_mapping_sp_identifier_to_credit_rating = self.generate_sp_identifier_to_credit_rating_mapping_from_data_configuration()
        differences = self.identify_changes_in_mapping_with_most_recent_file(original_mapping_sp_identifier_to_credit_rating)

    def identify_changes_in_mapping_with_most_recent_file(self,original_mapping):
        changes = {}
        count_upgrade = 0
        data = self.get_data_frame_for_spreadhseet("./data/most_recent_download.xls","Screening")
        for index, row in data.iterrows():
            if str(row['S&P Entity ID']) in original_mapping.keys():
                if row['S&P Entity Credit Rating - Issuer Credit Rating - Foreign Currency LT [Latest] (Rating)'] != original_mapping[str(row['S&P Entity ID'])]:
                    rating_was = original_mapping[str(row['S&P Entity ID'])]
                    rating_is = row['S&P Entity Credit Rating - Issuer Credit Rating - Foreign Currency LT [Latest] (Rating)']
                    difference = self.compute_rating_numerical_difference(rating_was, rating_is)
                    changes[str(row['S&P Entity ID'])] = {"was":rating_was,"is":rating_is,"difference":difference}
                    if difference <0:
                        count_upgrade += 1
        return changes
    
    def compute_rating_numerical_difference(self, old_rating, new_rating):
        old_rating_val = CreditRatingEncoding().compute_numeric_encoding_of_credit_rating(old_rating)
        new_rating_val = CreditRatingEncoding().compute_numeric_encoding_of_credit_rating(new_rating)
        return new_rating_val - old_rating_val

    def generate_sp_identifier_to_credit_rating_mapping_from_data_configuration(self):
        mapping = {}
        data = self.get_data_frame_for_spreadhseet(self.data_source.path,self.data_source.sheet_name)
        data.columns = data.iloc[0]
        data = data.drop(0)
        for index, row in data.iterrows():
            mapping[row['S&P Entity ID']] = row['S&P Entity Credit Rating  Issuer Credit Rating  Foreign Currency LT [Latest] (Rating)']
        return mapping
    
    def get_data_frame_for_spreadhseet(self, path, sheet_name):
        return pd.read_excel(path, sheet_name=sheet_name)