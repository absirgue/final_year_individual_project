import pandas as pd
from data_preparation.credit_rating_encoding import CreditRatingEncoding
from analysis.data_configuration import DataSource
from analysis.json_helper import JSONHelper
class RatingChangesIdentifier:
    """
    Coordinates all actions needed to identify the differences in credit ratings between 2 data sets.
    """

    def __init__(self, data_source):
        # The data source we want to use as the historic reference point.
        self.data_source = data_source
        # The default source of the most recent set of credit rating values we have access to.
        self.most_recent_source = DataSource("./data/all_cr_and_ch_most_recent_download.xls","Screening")
    
    # Coordinates all actions.
    def identify_changes(self):
        original_mapping_sp_identifier_to_credit_rating = self.generate_sp_identifier_to_credit_rating_mapping_from_data_configuration()
        differences,count_up, count_significant = self.identify_changes_in_mapping_with_most_recent_file(original_mapping_sp_identifier_to_credit_rating)
        self.save_analysis(differences,list(original_mapping_sp_identifier_to_credit_rating.keys()),count_up,count_significant)
        return differences
    
    """
    Save an anlysis presenting some key information about the changes which occured between 
    the two data sets. This information include:
    - the number and share of changes
    - the number and share of chanhes to or from B-
    - the number and share of upgrades
    - the number and share of downgrades
    """
    def save_analysis(self,changes, original_companies,count_up,count_significant):
        analysis = {"Number of changes":len(changes),"Share of companies that changed":len(changes)/len(original_companies),"Number of upgrades":count_up,"Share of upgrades":count_up/len(changes) if len(changes)>0 else 0,"Number of jumps from or to B-":count_significant}
        JSONHelper().save("./credit_rating_changes", self.data_source.path.split('/')[-1],analysis)

    def identify_changes_in_mapping_with_most_recent_file(self,original_mapping):
        changes = []
        count_upgrade = 0
        count_jumps_to_from_below_b_minus = 0
        data = self.get_data_frame_for_spreadhseet( self.most_recent_source.path,  self.most_recent_source.sheet_name)
        for index, row in data.iterrows():
            # Companies are uniquely identified by their S&P Entity ID.
            if str(row['S&P Entity ID']) in original_mapping.keys():
                if row['S&P Entity Credit Rating - Issuer Credit Rating - Local Currency LT [Latest] (Rating)'] != original_mapping[str(row['S&P Entity ID'])]:
                    rating_was = original_mapping[str(row['S&P Entity ID'])]
                    rating_is = row['S&P Entity Credit Rating - Issuer Credit Rating - Local Currency LT [Latest] (Rating)']
                    difference = self.compute_rating_numerical_difference(rating_was, rating_is)
                    is_jump_to_or_from_below_b_minus = self.get_is_jump_to_or_from_below_b_minus(rating_was,rating_is)
                    if is_jump_to_or_from_below_b_minus:
                        count_jumps_to_from_below_b_minus += 1
                    changes.append({str(row['S&P Entity ID']):{"was":rating_was,"is":rating_is,"difference":difference,"is_jump_from_or_to_below_b_minus":is_jump_to_or_from_below_b_minus}})
                    if difference <0:
                        count_upgrade += 1
        return changes,count_upgrade,count_jumps_to_from_below_b_minus

    # Returns true if an identified change corresponds to a jump to or from a rating below B-.
    def get_is_jump_to_or_from_below_b_minus(self, past_rating, present_rating):
        numeric_rating_was = CreditRatingEncoding().compute_numeric_encoding_of_credit_rating(past_rating)
        numeric_rating_is = CreditRatingEncoding().compute_numeric_encoding_of_credit_rating(present_rating)
        b_minus_encoding = CreditRatingEncoding().get_b_minus_encoding()
        return (numeric_rating_was < b_minus_encoding and numeric_rating_is >= b_minus_encoding) or (numeric_rating_was >= b_minus_encoding and numeric_rating_is < b_minus_encoding)
    
    # Returns the numerical difference between 2 credit ratings based on our encoding.
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
            mapping[row['S&P Entity ID']] = row["S&P Entity Credit Rating - Issuer Credit Rating - Local Currency LT [Latest] (Rating)"]
        return mapping
    
    def get_data_frame_for_spreadhseet(self, path, sheet_name):
        return pd.read_excel(path, sheet_name=sheet_name)