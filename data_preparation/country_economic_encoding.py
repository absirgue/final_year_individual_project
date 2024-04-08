import pandas as pd
import csv
import csv
from data_preparation.number_from_string_extractor import NumberFromStringExtractor
class CountryEconomicEncoding:
    """
    Centralizes all necessary operations for the encoding of a company's country(ies) of operation
    based on the value of its macroeconomic indicators.
    """

    """
    Params:
        - data - the data to encode
        - normalise_columns - True if the encoded values should be normalize so that they all lie in 
        [-1,1].
    """
    def __init__(self, data,normalise_columns):
        self.normalise_columns = normalise_columns
        self.data = data
        self.ECONOMIC_VARIABLES = ["PPPPC","PPPGDP","PCPIE","PCPI","NGDP_FY","NGDPPC","LUR","LP","GGX_NGDP","GGXWDN_NGDP","GGX","BCA"]
        self.generate_country_letters_mapping()
        self.generate_economic_variables_mapping()

    # Orchestrates all actions needed for the encoding at hand.
    def encode(self):
        self.add_averaged_economic_data_columns()
        if self.normalise_columns:
            self.normalise_added_column()
        return self.data

    # Normalize all columns we have added.
    def normalise_added_column(self):
        for eco_variable in self.ECONOMIC_VARIABLES:
            max_value = self.data["CUSTOM"+eco_variable].max()
            self.data["CUSTOM"+eco_variable] = self.data["CUSTOM"+eco_variable] / max_value
    
    # Generates and stores a dictionary associating a country with its 3 letters abbreviation.
    def generate_country_letters_mapping(self):
        self.country_letters_mapping = {}
        with open('./data/country_letter_symbols.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = row.get('\ufeffCountryName'.strip())
                if key is not None:
                    self.country_letters_mapping[key] = row['ThreeLettersSymbol']

    # Performs the actual encoding.
    def add_averaged_economic_data_columns(self):
        # A set of countries we were unable to encode because we didn't know the 3 letters 
        # abbreviation for them 
        forgotten_countries = set()
        for index, row in self.data.iterrows():
            try:
                countries_by_share_of_rev = str(row['Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]'])
            except:
                return
            if countries_by_share_of_rev and not pd.isna(countries_by_share_of_rev):
                total_share = 0
                # Stores the sum value of each macroeconomic indicators across all of a company's
                # country(ies) of operation.
                totals = {}
                # Iterating over all countries a company is operating in.
                for country_by_share_of_rev in countries_by_share_of_rev.split(";"):
                    country_name = NumberFromStringExtractor().extract_value_name(country_by_share_of_rev)
                    if not (country_name  in self.country_letters_mapping):
                        # We couldn't find the 3 letter abbreviation for this country name.
                        forgotten_countries.add(country_name)
                    if country_name in self.country_letters_mapping:
                        share = NumberFromStringExtractor().extract_share_value(country_by_share_of_rev)
                        total_share+=share
                        for variable in self.ECONOMIC_VARIABLES:
                            # We add the value for each of the economic variables, weigthe by
                            # the share of revenue made in this given country.
                            value_of_economic_variable = self.get_latest_value_economic_variable(self.country_letters_mapping[country_name], variable)
                            if value_of_economic_variable:
                                if variable in totals:
                                    totals[variable] += float(value_of_economic_variable)*float(share)
                                else:
                                    totals[variable] = float(value_of_economic_variable)*float(share)
                # We divide by the total revenue accounted for by all the countries we could encode.
                if total_share:
                    for variable in totals:
                        totals[variable] = totals[variable]/total_share
                self.set_avg_economic_indicators(index,totals)

    """
    Writes our computed weighted average values of each macroeconomic indicator to our data set. 
    Adds dedicated columns if they do not already exist.
    """
    def set_avg_economic_indicators(self,index,economic_indicators_value):
        for eco_variable in economic_indicators_value:
            if "CUSTOM"+eco_variable not in self.data.columns:
                self.data["CUSTOM"+eco_variable] = None
            self.data.loc[index, "CUSTOM"+eco_variable] = economic_indicators_value[eco_variable]

    """
    Retrieves the most recent value of a given macroeconomic indicator for a given country.
    """
    def get_latest_value_economic_variable(self, country_ticker, eco_variable):
        return self.economic_variables_values[country_ticker+"_"+eco_variable]

    """
    Generates a mapping of each country and macroeconomic indicator name pair with its value.
    """
    def generate_economic_variables_mapping(self):
        self.economic_variables_values = {}
        with open('./data/country_economic_variables.csv', 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                self.economic_variables_values[row[0]] = row[1]