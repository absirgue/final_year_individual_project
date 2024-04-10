from data_preprocessing.number_from_string_extractor import NumberFromStringExtractor

class IndustryNameHashEncoding:
    """
    Coordinates actions required for the hash-based encoding of the names of companies' industry(ies)
    of operation.
    """

    def __init__(self,data_frame):
        self.data = data_frame

    def encode(self):
        row_industry_share_mapping = []
        max_nb_industries = 0
        for index, row in self.data.iterrows():
            cell_content = str(row['Business Segments (Screen by Sum) (Details): % of Revenue [LTM]'])
            industry_share_mapping = {}
            for industry_and_share in cell_content.split(";"):
                if ":" in industry_and_share and len(industry_and_share.split(":"))==2:
                    share = NumberFromStringExtractor().extract_share_value(industry_and_share)
                    name = industry_and_share.split(":")[0]
                    industry_share_mapping[share] = name
            if len(cell_content.split(";")) > max_nb_industries:
                max_nb_industries = len(cell_content.split(";"))
            row_industry_share_mapping.append(industry_share_mapping)
        for i in range(max_nb_industries):
            self.data["CUSTOM - INDUSTRY NAME ENCODING "+str(i)] = None
        for index, row in self.data.iterrows():
            if index < len(row_industry_share_mapping):
                industry_share_mapping = row_industry_share_mapping[index]
                ordered_industries = sorted(industry_share_mapping.keys())
                for i in range(len(ordered_industries)):
                    self.data.loc[index,"CUSTOM - INDUSTRY NAME ENCODING "+str(i)] = self.hash_to_strictly_numerical(industry_share_mapping[ordered_industries[i]])
                for i in range(len(ordered_industries),max_nb_industries):
                    self.data.loc[index,"CUSTOM - INDUSTRY NAME ENCODING "+str(i)] = 0
        return self.data
    
    def hash_to_strictly_numerical(self,str):
        return hash(str)