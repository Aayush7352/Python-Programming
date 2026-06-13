from decimal import Decimal
from fractions import Fraction
from datetime import datetime, date, time
import sys


def main():
    # Numeric types
    integer_num = 42
    float_num = 3.14159
    complex_num = 3 + 4j
    decimal_num = Decimal("19.99")
    fraction_num = Fraction(1, 3)

    print("=== Numeric Types ===")
    print(f"int: {integer_num}")
    print(f"float: {float_num:.2f}")
    print(f"complex: {complex_num}, Real: {complex_num.real}, Imag: {complex_num.imag}")
    print(f"decimal: {decimal_num}")
    print(f"fraction: {fraction_num}, Float: {float(fraction_num):.3f}")

    # Sequence types
    string_val = "Python"
    list_val = [1, 2, 3, 4, 5]
    tuple_val = (10, 20, 30)
    range_val = range(5)

    print("\n=== Sequence Types ===")
    print(f"str: {string_val}")
    print(f"list: {list_val}")
    print(f"tuple: {tuple_val}")
    print(f"range: {list(range_val)}")

    # Mapping type
    dict_val = {"name": "Bob", "age": 30}

    # Set types
    set_val = {1, 2, 3, 4, 5}
    frozenset_val = frozenset([1, 2, 3])

    print("\n=== Mapping & Set Types ===")
    print(f"dict: {dict_val}")
    print(f"set: {set_val}")
    print(f"frozenset: {frozenset_val}")

    # Boolean and None
    print("\n=== Boolean & None ===")
    print(f"bool: {True}, {False}")
    print(f"NoneType: {None}")

    # Type checking
    print("\n=== Type Checking ===")
    print(f"Is 42 an int? {isinstance(42, int)}")
    print(f"Size of int 42: {sys.getsizeof(42)} bytes")


if __name__ == "__main__":
    main()
