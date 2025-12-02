import unittest
from src.calculator import parse_expression, validate_expression, CalculatorError

class TestValidation(unittest.TestCase):

    def test_parse_expression_basic(self):
        self.assertEqual(parse_expression("1+2"), ['1', '+', '2'])
        self.assertEqual(parse_expression("10-5"), ['10', '-', '5'])
        self.assertEqual(parse_expression("3*4"), ['3', '*', '4'])
        self.assertEqual(parse_expression("10/2"), ['10', '/', '2'])
        self.assertEqual(parse_expression("(1+2)*3"), ['(', '1', '+', '2', ')', '*', '3'])
        self.assertEqual(parse_expression("1.5+2.5"), ['1.5', '+', '2.5'])

    def test_validate_expression_balanced_parentheses(self):
        self.assertTrue(validate_expression(['(', '1', '+', '2', ')']))
        with self.assertRaises(CalculatorError):
            validate_expression(['(', '1', '+', '2'])
        with self.assertRaises(CalculatorError):
            validate_expression(['1', '+', '2', ')'])

    def test_validate_expression_consecutive_operators(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['1', '+', '+', '2'])
        with self.assertRaises(CalculatorError):
            validate_expression(['1', '*', '/', '2'])

    def test_validate_expression_operator_at_start_end(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['+', '1', '2'])
        with self.assertRaises(CalculatorError):
            validate_expression(['1', '2', '-'])

    def test_validate_expression_empty(self):
        with self.assertRaises(CalculatorError):
            validate_expression([])

    def test_validate_expression_operator_after_opening_parenthesis(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['(', '*', '2', ')'])
        self.assertTrue(validate_expression(['(', '-', '2', ')'])) # Unary minus is allowed

    def test_validate_expression_operator_before_closing_parenthesis(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['(', '2', '+', ')'])

    def test_validate_expression_missing_operator_between_parentheses(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['(', '2', ')', '(', '3', ')'])

    def test_validate_expression_missing_operator_number_parenthesis(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['2', '(', '3', ')'])
        with self.assertRaises(CalculatorError):
            validate_expression(['(', '2', ')', '3'])

    def test_validate_expression_division_by_zero(self):
        with self.assertRaises(CalculatorError):
            validate_expression(['1', '/', '0'])
        with self.assertRaises(CalculatorError):
            validate_expression(['(', '10', '-', '5', ')', '/', '0'])

