class DataSource:
    def __init__(self,path, sheet_name):
        self.path = path
        self.sheet_name = sheet_name
class DataConfiguration:
    """
    Defines DataConfiguration objects and enables a series of default data configurations.
    """

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
        rn_and_ra_ds = DataSource(path = "./data/raw_financial_data_and_ratios.xls", sheet_name = "Screening")
        renewables_cr_and_ch_ds = DataSource(path = "./data/renewable_energy_credit_model_and_credit_health.xls", sheet_name = "Screening")
        oil_and_gas_cr_and_ch_ds = DataSource(path = "./data/oil_and_gas_credit_model_and_credit_health.xls", sheet_name = "Screening")
        food_products_cr_and_ch_ds = DataSource(path = "./data/food_products_credit_model_and_health.xls", sheet_name = "Screening")
        self.default_data_sources = {"CREDIT MODEL AND CREDIT HEALTH":cr_and_ch_ds,"RATIOS AND RAW NUMBERS":rn_and_ra_ds,"RENEWABLE ENERGY INDUSTRY CREDIT MODEL AND CREDIT HEALTH":renewables_cr_and_ch_ds,"FOOD PRODUCTS INDUSTRY CREDIT MODEL AND CREDIT HEALTH":food_products_cr_and_ch_ds,"OIL AND GAS INDUSTRY CREDIT MODEL AND CREDIT HEALTH":oil_and_gas_cr_and_ch_ds}
        self.default_outlooks_weight_distribution = {'buy':2,'high':1,'highest':2,'hold':0,'low':-1,'lowest':-2,'neutral':0}
        self.average_by_cr_factor = 0

    def get_data_source(self):
        return self.data_source

    """
    Handles setting the data configuration's parameters according to a given default configuration
    name.
    Params:
        - data_types_wanted - the data types wanted
        - data_source_wanted - the data source wanted
        - average_by_category - takes value 0 if we do not want the features to be aggregated 
        on key pillars of credit ratings, 1 if we want this aggregation to be made using the mean
        technique, 2 for the median technique, and 3 for the normalized mean one.
    """
    def set_to_default_configuration(self, data_types_wanted,data_source_wanted,average_by_category=0):
        self.data_source=  self.default_data_sources[data_source_wanted]
        data_types_wanted = self.default_configurations[data_types_wanted]
        self.set_data_types_wanted(data_types_wanted)
        self.set_indutry_outlooks_encoding_preference(True,self.default_outlooks_weight_distribution)
        self.set_country_economic_data_encoding_preference(True,data_types_wanted!="RAW NUMBERS")
        self.set_geography_diversification_encoding_preference(True, 0)
        self.set_business_diversification_encoding_preference(True,0)
        self.average_by_cr_factor = average_by_category

    def set_data_types_wanted(self,data_types_wanted):
        self.data_types = data_types_wanted

    # Sets custom preference for the encoding of companies' country(ies) of operation and their 
    # macroeconomic indicators.
    def set_country_economic_data_encoding_preference(self,encode_industry_outlooks,normalise_economic_variables):   
        if encode_industry_outlooks and "COUNTRY RISK SCORE" not in self.data_types:
            self.data_types.append('DIVERSIFICATION - GEOGRAPHIC SEGMENTS - REVENUE')
        if normalise_economic_variables:
            self.normalise_economic_variables = True
        self.encode_country = True
    
    # Sets custom preference for the encoding of analysts' outlooks on companies' industry(ies)
    # of operation.
    def set_indutry_outlooks_encoding_preference(self, encode_industry_outlooks, outlooks_weight_distribution):
        if encode_industry_outlooks and ("INDUSTRY OUTLOOK" not in self.data_types):
            self.data_types.append("INDUSTRY OUTLOOK")
        self.encode_industry_outlooks = encode_industry_outlooks
        self.outlooks_weight_distribution = outlooks_weight_distribution

    # Sets custom preference for the encoding of companies' industry(ies) of operation.
    def set_industry_name_encoding_preference(self, encode_industry_name):
        if encode_industry_name and "DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE" not in self.data_types:
            self.data_types.append("DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE")
        self.encode_industry_name = encode_industry_name
    
    # Sets custom preference for the encoding of companies' geography diversification.
    def set_geography_diversification_encoding_preference(self,encode_geopgraphy,encoding_type):
        self.encode_geography_diversification = encode_geopgraphy
        self.geography_encoding_type = encoding_type
        if encoding_type == 1:
            self.data_types.append("DIVERSIFICATION - GEOGRAPHIC SEGMENTS COUNT")
        elif encoding_type == 0:
            self.data_types.append('DIVERSIFICATION - GEOGRAPHIC SEGMENTS - REVENUE')

    # Sets custom preference for the encoding of companies' business diversification.
    def set_business_diversification_encoding_preference(self,encode_industry,encoding_type):
        self.encode_business_diversification = encode_industry
        self.business_encoding_type = encoding_type
        if encoding_type == 1:
            self.data_types.append("DIVERSIFICATION - BUSINESS SEGMENTS COUNT")
        elif encoding_type == 0:
            self.data_types.append('DIVERSIFICATION - BUSINESS SEGMENTS - REVENUE')
    
    # Sets custom preference for the encoding of companies' country risk score.
    def set_country_risk_score_encoding_preference(self,encode_country_risk_score):
        self.encode_country_risk_score = encode_country_risk_score
        if encode_country_risk_score and ("COUNTRY RISK SCORE" not in self.data_types):
            self.data_types.append("COUNTRY RISK SCORE")

    # Returns the spelled out appendix to our data configuration name based on the desired setting
    # of aggregation on key pillars of credit ratings.
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