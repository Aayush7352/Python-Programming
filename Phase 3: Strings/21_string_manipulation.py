def main():
    # String creation
    s1 = "Hello"
    s2 = 'World'
    s3 = """Multi-line
string"""
    s4 = "Python " * 3

    print("=== String Creation ===")
    print(f"s1: {s1}")
    print(f"s2: {s2}")
    print(f"s3: {s3}")
    print(f"s4: {s4}")

    # String indexing and slicing
    text = "Python Programming"
    print(f"\n=== Indexing & Slicing ===")
    print(f"Original: {text}")
    print(f"First char: {text[0]}")
    print(f"Last char: {text[-1]}")
    print(f"Slice [0:6]: '{text[0:6]}'")
    print(f"Slice [7:]: '{text[7:]}'")
    print(f"Step [::2]: '{text[::2]}'")
    print(f"Reverse: '{text[::-1]}'")

    # String methods
    print("\n=== String Methods ===")
    s = "  Hello, Python World!  "
    print(f"Original: '{s}'")
    print(f"strip(): '{s.strip()}'")
    print(f"lower(): '{s.lower()}'")
    print(f"upper(): '{s.upper()}'")
    print(f"title(): '{s.title()}'")
    print(f"capitalize(): '{s.capitalize()}'")
    print(f"swapcase(): '{s.swapcase()}'")
    print(f"replace('Python', 'Java'): '{s.replace('Python', 'Java')}'")

    # Searching
    print(f"\n=== Searching ===")
    s = "Hello, World!"
    print(f"find('World'): {s.find('World')}")
    print(f"index('World'): {s.index('World')}")
    print(f"startswith('Hello'): {s.startswith('Hello')}")
    print(f"endswith('!'): {s.endswith('!')}")
    print(f"count('l'): {s.count('l')}")

    # Splitting and joining
    print(f"\n=== Splitting & Joining ===")
    csv_line = "apple,banana,cherry,date"
    parts = csv_line.split(",")
    print(f"split(','): {parts}")
    print(f"rsplit(',', 2): {csv_line.rsplit(',', 2)}")
    print(f"join(): {', '.join(parts)}")
    print(f"partition(','): {csv_line.partition(',')}")

    # Padding and alignment
    print(f"\n=== Padding & Alignment ===")
    s = "Python"
    print(f"ljust(10): '{s.ljust(10)}'")
    print(f"rjust(10): '{s.rjust(10)}'")
    print(f"center(10): '{s.center(10)}'")
    print(f"zfill(10): '{s.zfill(10)}'")

    # Character checks
    print(f"\n=== Character Checks ===")
    print(f"'Hello'.isalpha(): {'Hello'.isalpha()}")
    print(f"'123'.isdigit(): {'123'.isdigit()}")
    print(f"'Hello123'.isalnum(): {'Hello123'.isalnum()}")
    print(f"'   '.isspace(): {'   '.isspace()}")
    print(f"'Title Case'.istitle(): {'Title Case'.istitle()}")


if __name__ == "__main__":
    main()
