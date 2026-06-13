import re


def main():
    # Basic pattern matching
    text = "The quick brown fox jumps over the lazy dog."
    print("=== Basic Matching ===")
    pattern = r"fox"
    match = re.search(pattern, text)
    if match:
        print(f"Found '{pattern}' at index {match.start()}-{match.end()}")
        print(f"Matched text: {match.group()}")

    # findall
    print("\n=== findall ===")
    emails = "Contact: alice@example.com, bob@test.org, or charlie@company.co.uk"
    pattern = r"\b[\w.]+@[\w.]+\.\w+\b"
    found = re.findall(pattern, emails)
    print(f"Emails found: {found}")

    # finditer
    print("\n=== finditer ===")
    for match in re.finditer(r"\w+", text):
        print(f"  Word: '{match.group()}' at {match.start()}")

    # Groups
    print("\n=== Groups ===")
    phone = "Phone: (555) 123-4567"
    pattern = r"\((\d{3})\)\s(\d{3})-(\d{4})"
    match = re.search(pattern, phone)
    if match:
        print(f"Full match: {match.group()}")
        print(f"Area code: {match.group(1)}")
        print(f"Exchange: {match.group(2)}")
        print(f"Number: {match.group(3)}")
        print(f"All groups: {match.groups()}")

    # Named groups
    print("\n=== Named Groups ===")
    pattern = r"(?P<area>\d{3})-(?P<exchange>\d{3})-(?P<number>\d{4})"
    match = re.search(pattern, "123-456-7890")
    if match:
        print(f"Area: {match.group('area')}")
        print(f"Exchange: {match.group('exchange')}")

    # sub (replace)
    print("\n=== sub (Replace) ===")
    text = "Hello, my name is John. John is a programmer."
    result = re.sub(r"John", "Jane", text)
    print(f"Substituted: {result}")
    result = re.sub(r"John", "Jane", text, count=1)
    print(f"Count=1: {result}")

    # split
    print("\n=== split ===")
    text = "apple, banana; cherry | date"
    parts = re.split(r"[,;|]\s*", text)
    print(f"Split: {parts}")

    # Compilation
    print("\n=== Compiled Patterns ===")
    pattern = re.compile(r"\b[A-Z][a-z]*\b")
    capitalized = pattern.findall("The Quick Brown Fox Jumps Over The Lazy Dog")
    print(f"Capitalized words: {capitalized}")

    # Character classes
    print("\n=== Character Classes ===")
    text = "Password: Pass123! @#$%"
    print(f"Digits: {re.findall(r'\d', text)}")
    print(f"Non-digits: {re.findall(r'\D', text)}")
    print(f"Word chars: {re.findall(r'\w', text)}")
    print(f"Non-word: {re.findall(r'\W', text)}")
    print(f"Whitespace: {re.findall(r'\s', text)}")


if __name__ == "__main__":
    main()
