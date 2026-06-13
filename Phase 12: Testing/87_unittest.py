import unittest
import math


class Calculator:
    """Simple calculator to test."""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, a, b):
        return a ** b

    def sqrt(self, a):
        if a < 0:
            raise ValueError("Cannot sqrt negative number")
        return math.sqrt(a)


class TestCalculator(unittest.TestCase):
    """Unit tests for Calculator."""

    def setUp(self):
        """Set up test fixtures."""
        self.calc = Calculator()
        print(f"\n  setUp: created Calculator")

    @classmethod
    def setUpClass(cls):
        print("\n  setUpClass: Calculator test suite starting")

    @classmethod
    def tearDownClass(cls):
        print("\n  tearDownClass: Calculator test suite done")

    def tearDown(self):
        print(f"  tearDown: cleanup after test")

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1, 1), 0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5, 3), 2)
        self.assertEqual(self.calc.subtract(3, 5), -2)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(4, 3), 12)
        self.assertEqual(self.calc.multiply(0, 5), 0)
        self.assertEqual(self.calc.multiply(-2, 3), -6)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(7, 2), 3.5)
        self.assertAlmostEqual(self.calc.divide(1, 3), 0.3333, places=4)
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)

    def test_sqrt(self):
        self.assertEqual(self.calc.sqrt(16), 4)
        self.assertAlmostEqual(self.calc.sqrt(2), 1.4142, places=4)
        with self.assertRaises(ValueError):
            self.calc.sqrt(-1)

    @unittest.skip("Demonstrating skip")
    def test_skip(self):
        self.fail("This should be skipped")

    @unittest.skipIf(1 == 1, "Always skipped")
    def test_skip_conditional(self):
        pass


def suite():
    """Create a test suite."""
    suite = unittest.TestSuite()
    suite.addTest(TestCalculator("test_add"))
    suite.addTest(TestCalculator("test_divide"))
    return suite


def main():
    print("=== unittest Framework ===")
    print("  Run tests with: python -m unittest 87_unittest.py")
    print("  Or run this file directly\n")

    # Run using test runner
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())


if __name__ == "__main__":
    main()
