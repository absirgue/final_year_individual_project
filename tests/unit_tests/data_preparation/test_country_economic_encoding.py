import unittest
import pandas as pd
from data_preparation.country_economic_encoding import CountryEconomicEncoding

class TestCountryEconomicEncoding(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({'Geographic Segments (Screen by Sum) (Details): % of Revenue [LTM]':["Adjustment: 20 (20%); France: 40 (40%); United States: 40 (40%)","Adjustment: 20 (20%); Unexisting Country: 80 (80%)"]})
        super().__init__(methodName)

    def test_country_correctly_encoded_when_all_economic_variables_exist(self):
        result = CountryEconomicEncoding(self.data).encode()
        self.assertEqual(result.loc[0,'PPPPC'],57896.081999999995)
        self.assertEqual(result.loc[0,'PPPGDP'],12824.204000000002)
        self.assertEqual(result.loc[0,'PCPI'],193.7405)
        self.assertEqual(result.loc[0,'PCPIE'],195.2995)
        self.assertEqual(result.loc[0,'NGDPPC'],53067.034499999994)
        self.assertEqual(result.loc[0,'LP'],198.94650000000001)
        self.assertEqual(result.loc[0,'GGX'],4651.705)
        self.assertEqual(result.loc[0,'BCA'],-300.00550000000004)
    

    def test_fails_graciously_when_no_economic_variable_for_country(self):
        result = CountryEconomicEncoding(self.data).encode()
        self.assertEqual(result.loc[1,'PPPPC'],None)
        self.assertEqual(result.loc[1,'PPPGDP'],None)
        self.assertEqual(result.loc[1,'PCPI'],None)
        self.assertEqual(result.loc[1,'PCPIE'],None)
        self.assertEqual(result.loc[1,'NGDPPC'],None)
        self.assertEqual(result.loc[1,'LP'],None)
        self.assertEqual(result.loc[1,'GGX'],None)
        self.assertEqual(result.loc[1,'BCA'],None)

    def test_fails_graciously_when_no_country_column(self):
        try:
            result = CountryEconomicEncoding(pd.DataFrame({"Useless column:":[12]})).encode()
        except:
            self.fail("Failed ungraciously when geographic split column was missing.")