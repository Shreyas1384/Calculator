"""
Unit tests for Shrey's Calc core arithmetic and scientific engine.
"""

import unittest
import math
from calculator import Calculator


class TestShreysCalculatorOperations(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    # --- Basic Operations ---
    def test_addition(self):
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.add(-3, 8), 5)
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=7)

    def test_subtraction(self):
        self.assertEqual(self.calc.subtract(20, 7), 13)
        self.assertEqual(self.calc.subtract(5, 12), -7)

    def test_multiplication(self):
        self.assertEqual(self.calc.multiply(6, 7), 42)
        self.assertEqual(self.calc.multiply(-4, 5), -20)

    def test_division(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    # --- Scientific Operations ---
    def test_trigonometry_degrees(self):
        # sin(30 deg) = 0.5
        self.assertAlmostEqual(self.calc.sin(30, mode="DEG"), 0.5, places=7)
        # cos(60 deg) = 0.5
        self.assertAlmostEqual(self.calc.cos(60, mode="DEG"), 0.5, places=7)
        # tan(45 deg) = 1.0
        self.assertAlmostEqual(self.calc.tan(45, mode="DEG"), 1.0, places=7)

    def test_trigonometry_radians(self):
        self.assertAlmostEqual(self.calc.sin(math.pi / 2, mode="RAD"), 1.0, places=7)
        self.assertAlmostEqual(self.calc.cos(math.pi, mode="RAD"), -1.0, places=7)

    def test_inverse_trigonometry(self):
        # asin(0.5) in deg = 30
        self.assertAlmostEqual(self.calc.asin(0.5, mode="DEG"), 30.0, places=7)
        # acos(0.5) in deg = 60
        self.assertAlmostEqual(self.calc.acos(0.5, mode="DEG"), 60.0, places=7)
        # atan(1) in deg = 45
        self.assertAlmostEqual(self.calc.atan(1, mode="DEG"), 45.0, places=7)

    def test_logarithms_and_exp(self):
        # ln(e) = 1
        self.assertAlmostEqual(self.calc.ln(math.e), 1.0, places=7)
        # log10(1000) = 3
        self.assertAlmostEqual(self.calc.log10(1000), 3.0, places=7)
        # exp(1) = e
        self.assertAlmostEqual(self.calc.exp(1), math.e, places=7)
        # log of <= 0 raises ValueError
        with self.assertRaises(ValueError):
            self.calc.ln(0)

    def test_powers_and_roots(self):
        self.assertEqual(self.calc.power(2, 4), 16)
        self.assertEqual(self.calc.square_root(49), 7)
        self.assertEqual(self.calc.cube_root(27), 3)
        self.assertEqual(self.calc.cube_root(-27), -3)

    def test_factorial(self):
        self.assertEqual(self.calc.factorial(0), 1)
        self.assertEqual(self.calc.factorial(5), 120)
        self.assertEqual(self.calc.factorial(6), 720)
        with self.assertRaises(ValueError):
            self.calc.factorial(-3)
        with self.assertRaises(ValueError):
            self.calc.factorial(3.5)

    def test_reciprocal_and_abs(self):
        self.assertEqual(self.calc.reciprocal(4), 0.25)
        self.assertEqual(self.calc.abs_val(-42), 42)
        with self.assertRaises(ZeroDivisionError):
            self.calc.reciprocal(0)

    def test_scientific_expression_evaluation(self):
        # sin(30) + cos(60) = 1 in DEG mode
        self.assertAlmostEqual(self.calc.evaluate_expression("sin(30) + cos(60)", angle_mode="DEG"), 1.0, places=7)
        # log(100) * 5 = 10
        self.assertEqual(self.calc.evaluate_expression("log(100) * 5"), 10)
        # fact(5) + sqrt(16) = 120 + 4 = 124
        self.assertEqual(self.calc.evaluate_expression("fact(5) + sqrt(16)"), 124)
        # Constants: pi and e
        self.assertAlmostEqual(self.calc.evaluate_expression("pi"), math.pi, places=7)
        self.assertAlmostEqual(self.calc.evaluate_expression("2 * e"), 2 * math.e, places=7)

    def test_history(self):
        self.calc.clear_history()
        self.calc.evaluate_expression("12 * 12")
        hist = self.calc.get_history()
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["result"], 144)


if __name__ == "__main__":
    unittest.main()
