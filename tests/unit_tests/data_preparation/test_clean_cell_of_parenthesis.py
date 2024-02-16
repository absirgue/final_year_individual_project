import unittest
from data_preparation.cell_cleaning import CleanCellOfParenthesis

class TestCleanCellOfParenthesis(unittest.TestCase):

    def test_can_remove_a_parenthetical_statement(self):
        result = CleanCellOfParenthesis().clean("I hold one statement (here)")
        self.assertEqual(result.strip(), "I hold one statement")
    
    def test_can_remove_two_parenthetical_statements(self):
        result = CleanCellOfParenthesis().clean("9.18 (spec 1) (spec 2)")
        self.assertEqual(result.strip(), "9.18")
    
    def test_does_not_fail_when_no_parenthetical_statement(self):
        try:
            result = CleanCellOfParenthesis().clean("9.18")
        except:
            self.fail("Error was raised when no parenthetical statement.")
        