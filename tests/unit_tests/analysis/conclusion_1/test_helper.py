import unittest
from analysis.hyperparameters_optimisation.helper import create_floats_list,create_ints_list

class TestConc1Helper(unittest.TestCase):


    def test_create_floats_list_creates_list_as_expected(self):
        list = create_floats_list(0.1,0.6,0.2)
        self.assertAlmostEqual(list[0],0.1)
        self.assertAlmostEqual(list[1],0.3)
        self.assertAlmostEqual(list[2],0.5)
    
    def test_create_ints_list_creates_list_as_expected(self):
        self.assertEqual(create_floats_list(0,10,2),[0,2,4,6,8,10])