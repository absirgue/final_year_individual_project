from data_preprocessing.diversification_split_evaluations import EntropyCalculator,SegmentsCount

class DiversificationEncoding:
    """
    Coordinates all actions to encode either busienss or geography diversification.
    """

    def __init__(self,data):
        self.data = data
    
    def encode(self,encoding_type,diversity_evaluated):
        self.result_col_name = diversity_evaluated+" Encoding"
        if encoding_type == 1:
            if diversity_evaluated == "Geography":
                column_name = "Number of Geographic Segments [Annual]"
            else:
                column_name = "Number of Business Segments [Annual]"
            return self.segment_counts_encoding(column_name)
        else:
            if diversity_evaluated == "Geography":
                column_name = "Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]"
            else:
                column_name = "Business Segments (Screen by Sum) (Details): % of Revenue [LTM]"
            return self.entropy_encoding(column_name)
    
    def segment_counts_encoding(self,column_name):
        for index, row in self.data.iterrows():
            cell_content = str(row[column_name])
            encoding = SegmentsCount().encode(cell_content)
            if "CUSTOM"+self.result_col_name not in self.data.columns:
                self.data["CUSTOM"+self.result_col_name] = None
            self.data.loc[index, "CUSTOM"+self.result_col_name] = encoding
        return self.data
    
    def entropy_encoding(self,column_name):
        for index, row in self.data.iterrows():
            cell_content = str(row[column_name])
            encoding = EntropyCalculator().encode(cell_content)
            if "CUSTOM"+self.result_col_name not in self.data.columns:
                self.data["CUSTOM"+self.result_col_name] = None
            self.data.loc[index, "CUSTOM"+self.result_col_name] = encoding
        return self.data

        