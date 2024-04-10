import unittest
import pandas as pd
from data_preprocessing.country_economic_encoding import CountryEconomicEncoding

class TestCountryEconomicEncoding(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({'Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]':["Adjustment: 20 (20%); France: 40 (40%); United States: 40 (40%)","Adjustment: 20 (20%); Unexisting Country: 80 (80%)"]})
        super().__init__(methodName)

    def test_country_correctly_encoded_when_all_economic_variables_exist(self):
        result = CountryEconomicEncoding(self.data,normalise_columns=False).encode()
        self.assertEqual(result.loc[0,'CUSTOMPPPPC'],57896.081999999995)
        self.assertEqual(result.loc[0,'CUSTOMPPPGDP'],12824.204000000002)
        self.assertEqual(result.loc[0,'CUSTOMPCPI'],193.7405)
        self.assertEqual(result.loc[0,'CUSTOMPCPIE'],195.2995)
        self.assertEqual(result.loc[0,'CUSTOMNGDPPC'],53067.034499999994)
        self.assertEqual(result.loc[0,'CUSTOMLP'],198.94650000000001)
        self.assertEqual(result.loc[0,'CUSTOMGGX'],4651.705)
        self.assertEqual(result.loc[0,'CUSTOMBCA'],-300.00550000000004)
    

    def test_fails_graciously_when_no_economic_variable_for_country(self):
        result = CountryEconomicEncoding(self.data,normalise_columns=False).encode()
        self.assertEqual(result.loc[1,'CUSTOMPPPPC'],None)
        self.assertEqual(result.loc[1,'CUSTOMPPPGDP'],None)
        self.assertEqual(result.loc[1,'CUSTOMPCPI'],None)
        self.assertEqual(result.loc[1,'CUSTOMPCPIE'],None)
        self.assertEqual(result.loc[1,'CUSTOMNGDPPC'],None)
        self.assertEqual(result.loc[1,'CUSTOMLP'],None)
        self.assertEqual(result.loc[1,'CUSTOMGGX'],None)
        self.assertEqual(result.loc[1,'CUSTOMBCA'],None)

    def test_fails_graciously_when_no_country_column(self):
        try:
            result = CountryEconomicEncoding(pd.DataFrame({"Useless column:":[12]}),normalise_columns=False).encode()
        except Exception as e:
            print(e)
            self.fail("Failed ungraciously when geographic split column was missing.")