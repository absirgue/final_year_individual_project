import unittest
import pandas as pd
from data_preparation.credit_rating_factor_averages_calculator import CreditRatingFactorAveragesCalculator

class TestCreditRatigFactorAveragesCalculator(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        self.data = pd.DataFrame({"CreditModel - Acid Test Ratio [Latest Quarter] (Model Version 2.6)":[0.5,0.4,0.9],
                                  "Net Working Capital / Revenue - Capital IQ [LTM]":[0.5,0.5,0.5],
                                 "CreditModel - Operating Expense / Total Assets [Latest Quarter] (Model Version 2.6)":[0,1,0.4],
                                 "Net Working Capital/ Total Assets - Capital IQ [LTM]":[0.2,0.3,0.04],
                                 "CreditModel - Nonperforming assets / Total Assets  [Latest Quarter] (Model Version 2.6)":[-0.1,0.5,0.4]
                                 })
        # Liquidity
        # Liquidity
        # Efficiency
        # Liquidity
         # Efficiency
        super().__init__(methodName)

    def test_mean_averager_gives_expected_result(self):
        result = CreditRatingFactorAveragesCalculator(self.data).encode(1)
        expected_efficiency = [-0.05,0.75,0.4]
        expected_liquidity = [0.4,0.4,0.48]
        for i in range(3):
            self.assertAlmostEqual(expected_efficiency[i],list(result["Efficiency"])[i])
            self.assertAlmostEqual(expected_liquidity[i],list(result["Liquidity"])[i])

    def test_median_averager_gives_expected_result(self):
        result = CreditRatingFactorAveragesCalculator(self.data).encode(2)
        expected_efficiency = [-0.05,0.75,0.4]
        expected_liquidity = [0.5,0.4,0.5]
        for i in range(3):
            self.assertAlmostEqual(expected_efficiency[i],list(result["Efficiency"])[i])
            self.assertAlmostEqual(expected_liquidity[i],list(result["Liquidity"])[i])

        
    def test_normalized_mean_averager_gives_expected_result(self):
        result = CreditRatingFactorAveragesCalculator(self.data).encode(3)
        expected_efficiency = [0,1,0.616666666666]
        expected_liquidity = [0.2717948717,0.33333333333333,0.333333333333]
        for i in range(3):
            self.assertAlmostEqual(expected_efficiency[i],list(result["Efficiency"])[i])
            self.assertAlmostEqual(expected_liquidity[i],list(result["Liquidity"])[i])