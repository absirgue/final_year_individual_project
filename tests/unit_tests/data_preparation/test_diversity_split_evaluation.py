import unittest
from data_preprocessing.diversification_split_evaluations import EntropyCalculator,SegmentsCount

class TestEntropyCalculator(unittest.TestCase):

    def test_entropy_can_be_calculated_in_perfect_situations(self):
        result = EntropyCalculator().encode("Element 1: 12 (45%);Element 2: 12 (12.6%);Element 3: 12 (42.40%)")
        self.assertEqual(result,1.4198072055186346)
    
    def test_entropy_can_be_calculated_with_line_breaks(self):
        result = EntropyCalculator().encode("Element 1: 12 (45%);\nElement 2: 12 (12.6%);\nElement 3: 12 (42.40%)")
        self.assertEqual(result,1.4198072055186346)

    def test_entropy_can_be_calculated_with_some_unknown_proportions(self):
        result = EntropyCalculator().encode("Element 1: 12 (45%);\nElement 2: 12 (12.6%);\nElement 3: 12 (32.40%);\nElement 4:")
        self.assertEqual(result,1.4277254052800652)
    
    def test_entropy_can_be_calculated_with_some_mistyped_proportions(self):
        result = EntropyCalculator().encode("Element 1: 12 (45%);\nElement 2:(12.6%);\nElement 3: 12 (32.40%);\nElement 4: ()")
        self.assertEqual(result,0.9807983646944296)

    def test_no_split_information_fails_gracisouly(self):
        try:
            result = EntropyCalculator().encode("Element 1: 12 ();Element 2:;Element 3: 12 ()")
        except Exception:
            self.fail("Does not fail graciously")

    def test_cell_structured_without_semi_colons_fails_graciously(self):
        try:
            result = EntropyCalculator().encode("Element 1: (),Element 2: Element 3: ()")
        except Exception:
            self.fail("Does not fail graciously")

class TestSegmentsCount (unittest.TestCase):
    def test_returns_as_expected(self):
        result = SegmentsCount().encode("12")
        self.assertEqual("12",result)
