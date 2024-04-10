import math
class CreditRatingEncoding:
    """
    Centralizes operations to encode and decode credit ratings.
    """

    def __init__(self, data=[], credit_rating_col_name=""):
        self.NAME_COL_TO_ENCODE  = credit_rating_col_name
        self.data = data
        self.CR_NUMBER_MAPPING = {"AAA":1,
                                  "AA+":2,
                                  "AA":3,
                                  "AA-":4,
                                  "A+":5,
                                  "A":6,
                                  "A-":7,
                                  "BBB+":8,
                                  "BBB":9,
                                  "BBB-":10,
                                  "BB+":11,
                                  "BB":12,
                                  "BB-":13,
                                  "B+":14,
                                  "B":15,
                                  "B-":16,
                                  "CCC+":17,
                                  "CCC":18,
                                  "CCC-":19,
                                  "CC":20,
                                  "C":21,
                                  "D":22}
    
    """
    Performs the encoding. There is only one credit rating for each row and it is defined for 
    every row.
    """
    def encode(self):
        for index, row in self.data.iterrows():
            cell_content = str(row[self.NAME_COL_TO_ENCODE])
            encoding = self.compute_numeric_encoding_of_credit_rating(cell_content)
            if "CUSTOM Credit Rating" not in self.data.columns:
                self.data["CUSTOM Credit Rating"] = None
            self.data.at[index, "CUSTOM Credit Rating"] = encoding
        self.data.drop(self.NAME_COL_TO_ENCODE, axis=1,inplace=True)
        self.data["CUSTOM Credit Rating"] = self.data["CUSTOM Credit Rating"].astype(float)
        return self.data, "CUSTOM Credit Rating"
    
    # Returns the numerical encoding of a given credit rating if it exists in our mapping.
    def compute_numeric_encoding_of_credit_rating(self, rating):
        if rating in self.CR_NUMBER_MAPPING.keys():
            return self.CR_NUMBER_MAPPING[rating]
        else:
            return math.nan
    
    """
    Performs the reverse operation to encoding and returns the letter grade associated 
    with a given numerical encoding.
    """ 
    def compute_letter_grade_from_numeric_encoding(self, encoding):
        try:
            encoding = int(encoding)
            for key, value in self.CR_NUMBER_MAPPING.items():
                if value == encoding:
                    return key
            return encoding
        except:
            return encoding
    
    # Returns the numerical encoding of the first "non-invetment grade" (aka "junk") rating. 
    def get_encoding_first_junk_rating(self):
        return self.CR_NUMBER_MAPPING["BB+"]

    # Returns the numerical encoding of the B- rating.
    def get_b_minus_encoding(self):
        return self.CR_NUMBER_MAPPING["B-"]