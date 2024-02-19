
class DataConfiguration:

    def __init__(self) -> None:
        self.encode_country = False
        self.encode_industry_outlooks = False
        self.encode_industry_name = False
        self.encode_geography_diversification = False
        self.encode_business_diversification = False
        self.encode_country_risk_score = False
        self.data_types=[]
        self.default_configurations = {"RATIOS":["RATIO"],"RAW NUMBERS":["RAW NUMBER"],"BOTH":["RATIO","RAW NUMBER"]}
        self.default_outlooks_weight_distribution = {'buy':2,'high':1,'highest':2,'hold':0,'low':-1,'lowest':-2,'neutral':0}

    def set_to_default_configuration(self, default_configuration_id,mixed_data = False):
        data_types_wanted = self.default_configurations[default_configuration_id]
        if mixed_data:
            # data_types_wanted.append("INDUSTRY NAMES")
            # TO DO: encode differently for mixed
            data_types_wanted.append('DIVERSIFICATION - GEOGRAPHY - REVENUE')
            data_types_wanted.append('DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE')
            data_types_wanted.append('COUNTRY RISK SCORE')
        self.set_indutry_outlooks_encoding_preference(True,self.default_outlooks_weight_distribution)
        self.set_data_types_wanted(data_types_wanted)
        if not mixed_data:
            # self.set_industry_name_encoding_preference(True)
            self.set_country_economic_data_encoding_preference(True)
            self.set_country_risk_score_encoding_preference(True)
            self.set_geography_diversification_encoding_preference(True, 0)
            self.set_business_diversification_encoding_preference(True,0)

    def set_data_types_wanted(self,data_types_wanted):
        self.data_types = data_types_wanted

    def set_country_economic_data_encoding_preference(self,encode_industry_outlooks):   
        if encode_industry_outlooks and "COUNTRY RISK SCORE" not in self.data_types:
            self.data_types.append('DIVERSIFICATION - GEOGRAPHY - REVENUE')
        self.encode_country = True
    
    def set_indutry_outlooks_encoding_preference(self, encode_industry_outlooks, outlooks_weight_distribution):
        if encode_industry_outlooks and ("INDUSTRY OUTLOOK" not in self.data_types):
            self.data_types.append("INDUSTRY OUTLOOK")
        self.encode_industry_outlooks = encode_industry_outlooks
        self.outlooks_weight_distribution = outlooks_weight_distribution

    def set_industry_name_encoding_preference(self, encode_industry_name):
        if encode_industry_name and "DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE" not in self.data_types:
            self.data_types.append("DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE")
        self.encode_industry_name = encode_industry_name

    def set_geography_diversification_encoding_preference(self,encode_geopgraphy,encoding_type):
        self.encode_geography_diversification = encode_geopgraphy
        self.geography_encoding_type = encoding_type
        if encoding_type == 1:
            self.data_types.append("DIVERSIFICATION - GEOGRAPHIC SEGMENTS COUNT")
        elif encoding_type == 0:
            self.data_types.append('DIVERSIFICATION - GEOGRAPHY - REVENUE')

    def set_business_diversification_encoding_preference(self,encode_industry,encoding_type):
        self.encode_business_diversification = encode_industry
        self.business_encoding_type = encoding_type
        if encoding_type == 1:
            self.data_types.append("DIVERSIFICATION - BUSINESS SEGMENTS COUNT")
        elif encoding_type == 0:
            self.data_types.append('DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE')
    
    def set_country_risk_score_encoding_preference(self,encode_country_risk_score):
        self.encode_country_risk_score = encode_country_risk_score
        if encode_country_risk_score and ("COUNTRY RISK SCORE" not in self.data_types):
            self.data_types.append("COUNTRY RISK SCORE")
