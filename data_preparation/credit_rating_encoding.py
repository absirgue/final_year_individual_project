import math
class CreditRatingEncoding:

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
                                  "CCC":17,
                                  "CCC-":17,
                                  "CC":18,
                                  "C":19,
                                  "D":20}
    
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
    
    def compute_numeric_encoding_of_credit_rating(self, rating):
        if rating in self.CR_NUMBER_MAPPING.keys():
            return self.CR_NUMBER_MAPPING[rating]
        else:
            return math.nan
    
    def get_encoding_first_junk_rating(self):
        return self.CR_NUMBER_MAPPING["BB+"]

    def get_b_minus_encoding(self):
        return self.CR_NUMBER_MAPPING["B-"]