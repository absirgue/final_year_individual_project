class DataSource:
    def __init__(self,path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
class DataConfiguration:

    def __init__(self) -> None:
        self.normalise_economic_variables = False
        self.encode_country = False
        self.encode_industry_outlooks = False
        self.encode_industry_name = False
        self.encode_geography_diversification = False
        self.encode_business_diversification = False
        self.encode_country_risk_score = False
        self.average_by_cr_factor = False
        self.data_source = None
        self.data_types=[]
        self.default_configurations = {"CREDIT MODEL":["CREDIT MODEL"],"CREDIT HEALTH":["CREDIT HEALTH"],"BOTH RATIOS AND RAW NUMBERS":["RATIO","RAW NUMBER"],"BOTH CREDIT HEALTH AND CREDIT MODEL":["CREDIT HEALTH","CREDIT MODEL"],"RAW NUMBERS":["RAW NUMBER"],"RATIOS":["RATIO"]}
        cr_and_ch_ds = DataSource(path = "./data/sp_credit_health_and_model_data.xls", sheet_name = "Screening")
        rn_and_ra_ds = DataSource(path = "./data/Jan download.xls", sheet_name = "Screening")
        self.default_data_sources = {"CREDIT MODEL":cr_and_ch_ds,"CREDIT HEALTH":cr_and_ch_ds,"BOTH RATIOS AND RAW NUMBERS":rn_and_ra_ds,"BOTH CREDIT HEALTH AND CREDIT MODEL":cr_and_ch_ds,"RAW NUMBERS":rn_and_ra_ds,"RATIOS":rn_and_ra_ds}
        self.default_outlooks_weight_distribution = {'buy':2,'high':1,'highest':2,'hold':0,'low':-1,'lowest':-2,'neutral':0}
        self.average_by_cr_factor = 0

    def get_data_source(self):
        return self.data_source

    # 1 is mean, 2 ....
    def set_to_default_configuration(self, default_configuration_id,mixed_data = False,average_by_category=0):
        self.data_source=  self.default_data_sources[default_configuration_id]
        data_types_wanted = self.default_configurations[default_configuration_id]
        if mixed_data:
            data_types_wanted.append("INDUSTRY NAMES")
            # TO DO: encode differently for mixed
            data_types_wanted.append('DIVERSIFICATION - GEOGRAPHIC SEGMENTS - REVENUE')
            data_types_wanted.append('DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE')
            data_types_wanted.append('COUNTRY RISK SCORE')
        self.set_data_types_wanted(data_types_wanted)
        self.set_indutry_outlooks_encoding_preference(True,self.default_outlooks_weight_distribution)
        if not mixed_data:
            # We always normalise except when the configuration wanted is "Raw Numbers"
            self.set_country_economic_data_encoding_preference(True,default_configuration_id!="RAW NUMBERS")
            self.set_geography_diversification_encoding_preference(True, 0)
            self.set_business_diversification_encoding_preference(True,0)
        self.average_by_cr_factor = average_by_category

    def set_data_types_wanted(self,data_types_wanted):
        self.data_types = data_types_wanted

    def set_country_economic_data_encoding_preference(self,encode_industry_outlooks,normalise_economic_variables):   
        if encode_industry_outlooks and "COUNTRY RISK SCORE" not in self.data_types:
            self.data_types.append('DIVERSIFICATION - GEOGRAPHIC SEGMENTS - REVENUE')
        if normalise_economic_variables:
            self.normalise_economic_variables = True
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
            self.data_types.append('DIVERSIFICATION - GEOGRAPHIC SEGMENTS - REVENUE')

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

    def get_appendix_for_averager_modif_of_config(self):
        match self.average_by_cr_factor:
            case 1:
                return " - Factors by Mean"
            case 2:
                return " - Factors by Median"
            case 3:
                return " - Factors by Normalized Mean"
            case _:
                return ""