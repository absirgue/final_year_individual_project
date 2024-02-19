import pandas as pd
import csv
import json
import csv
from data_preparation.number_from_string_extractor import NumberFromStringExtractor
class CountryEconomicEncoding:

    def __init__(self, data):
        self.data = data
        self.ECONOMIC_VARIABLES = ["PPPPC","PPPGDP","PCPIE","PCPI","NGDP_FY","NGDPPC","LUR","LP","GGX_NGDP","GGXWDN_NGDP","GGX","BCA"]
        self.generate_country_letters_mapping()
        self.generate_economic_variables_mapping()

    def encode(self):
        print("CALLED THE COUNTRY")
        self.add_averaged_economic_data_columns()
        return self.data

    def generate_country_letters_mapping(self):
        self.country_letters_mapping = {}
        with open('./data/country_letter_symbols.csv', mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = row.get('\ufeffCountryName'.strip())
                if key is not None:
                    self.country_letters_mapping[key] = row['ThreeLettersSymbol']
        
    def add_averaged_economic_data_columns(self):
        forgotten_countries = set()
        for index, row in self.data.iterrows():
            try:
                countries_by_share_of_rev = str(row['Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]'])
            except:
                # print("COUNTRY ECONOMIC ENCODING: Missing split column")
                return
            if countries_by_share_of_rev and not pd.isna(countries_by_share_of_rev):
                total_share = 0
                totals = {}
                for country_by_share_of_rev in countries_by_share_of_rev.split(";"):
                    country_name = NumberFromStringExtractor().extract_country_name(country_by_share_of_rev)
                    if not (country_name  in self.country_letters_mapping):
                        forgotten_countries.add(country_name)
                    if country_name in self.country_letters_mapping:
                        share = NumberFromStringExtractor().extract_share_value(country_by_share_of_rev)
                        total_share+=share
                        for variable in self.ECONOMIC_VARIABLES:
                            value_of_economic_variable = self.get_latest_value_economic_variable(self.country_letters_mapping[country_name], variable)
                            if value_of_economic_variable:
                                if variable in totals:
                                    totals[variable] += float(value_of_economic_variable)*float(share)
                                else:
                                    totals[variable] = float(value_of_economic_variable)*float(share)
                if total_share:
                    for variable in totals:
                        totals[variable] = totals[variable]/total_share
                self.set_avg_economic_indicators(index,totals)
        # print("Countries formulations unconsidered counts: "+str(len(forgotten_countries)))

    def set_avg_economic_indicators(self,index,economic_indicators_value):
        for eco_variable in economic_indicators_value:
            if "CUSTOM"+eco_variable not in self.data.columns:
                self.data["CUSTOM"+eco_variable] = None
            self.data.loc[index, "CUSTOM"+eco_variable] = economic_indicators_value[eco_variable]

    def get_latest_value_economic_variable(self, country_ticker, eco_variable):
        return self.economic_variables_values[country_ticker+"_"+eco_variable]

    def generate_economic_variables_mapping(self):
        self.economic_variables_values = {}
        with open('./data/country_economic_variables.csv', 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            for row in csv_reader:
                self.economic_variables_values[row[0]] = row[1]