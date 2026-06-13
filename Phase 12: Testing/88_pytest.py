"""
pytest demonstration.

Requires: pip install pytest

Run with: pytest 88_pytest.py -v
"""
import math
import pytest


# Fixtures
@pytest.fixture
def calculator():
    """Create a calculator instance."""
    return Calculator()


@pytest.fixture(params=[(2, 3, 5), (0, 0, 0), (-1, 1, 0)])
def add_data(request):
    """Parameterized fixture for add tests."""
    return request.param


# Class to test
class Calculator:
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

    def is_even(self, n):
        return n % 2 == 0

    def fibonacci(self, n):
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


# Tests
def test_add(calculator):
    assert calculator.add(2, 3) == 5
    assert calculator.add(-1, 1) == 0


def test_subtract(calculator):
    assert calculator.subtract(5, 3) == 2
    assert calculator.subtract(3, 5) == -2


def test_multiply(calculator):
    assert calculator.multiply(4, 3) == 12
    assert calculator.multiply(0, 5) == 0


def test_divide(calculator):
    assert calculator.divide(10, 2) == 5
    assert calculator.divide(7, 2) == 3.5
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(10, 0)


def test_power(calculator):
    assert calculator.power(2, 3) == 8
    assert calculator.power(5, 0) == 1


def test_sqrt(calculator):
    assert calculator.sqrt(16) == 4
    assert calculator.sqrt(2) == pytest.approx(1.4142, rel=1e-3)
    with pytest.raises(ValueError):
        calculator.sqrt(-1)


# Parameterized test
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add_parametrized(calculator, a, b, expected):
    assert calculator.add(a, b) == expected


# Using fixture with parameterized data
def test_add_with_fixture(calculator, add_data):
    a, b, expected = add_data
    assert calculator.add(a, b) == expected


# Test grouping with class
class TestCalculatorAdvanced:
    def test_is_even(self, calculator):
        assert calculator.is_even(2) == True
        assert calculator.is_even(3) == False
        assert calculator.is_even(0) == True

    def test_fibonacci(self, calculator):
        assert calculator.fibonacci(0) == 0
        assert calculator.fibonacci(1) == 1
        assert calculator.fibonacci(10) == 55
        with pytest.raises(ValueError):
            calculator.fibonacci(-1)


# Skip tests
@pytest.mark.skip(reason="Demonstrating skip")
def test_skipped():
    assert False


@pytest.mark.skipif(1 == 1, reason="Always skipped")
def test_skip_conditional():
    pass


# Expected failures
@pytest.mark.xfail(reason="Known bug")
def test_expected_failure():
    assert 1 + 1 == 3  # This will fail but is expected


# Custom markers
@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(0.2)
    assert True


# Conftest-like setup
@pytest.fixture(scope="session", autouse=True)
def global_setup():
    print("\n  (Global setup: runs once per session)")
    yield
    print("  (Global teardown)")


def main():
    print("=== pytest Framework ===")
    print("  Run with: pytest 88_pytest.py -v")
    print("  Run with coverage: pytest --cov=.")
    print("\n  Or use python to run:")
    import subprocess
    subprocess.run(["pytest", __file__, "-v", "--tb=short"], check=False)


if __name__ == "__main__":
    main()
