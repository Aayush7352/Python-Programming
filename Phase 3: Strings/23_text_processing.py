import textwrap
import string
import re
from collections import Counter


def word_frequency(text: str, top_n: int = 5):
    """Count word frequencies in a text."""
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words).most_common(top_n)


def wrap_text(text: str, width: int = 40):
    """Wrap text to specified width."""
    wrapped = textwrap.fill(text, width=width)
    return wrapped


def extract_sentences(text: str):
    """Split text into sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def remove_punctuation(text: str):
    """Remove all punctuation from text."""
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def caesar_cipher(text: str, shift: int = 3):
    """Simple Caesar cipher encryption/decryption."""
    result = []
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26
            result.append(chr(shifted + ascii_offset))
        else:
            result.append(char)
    return "".join(result)


def main():
    sample_text = """
    Python is a powerful programming language. It is widely used for
    web development, data analysis, artificial intelligence, and more.
    Python's simple syntax makes it easy to learn. Many developers
    love Python for its versatility and readability.
    """

    print("=== Word Frequency ===")
    freq = word_frequency(sample_text)
    for word, count in freq:
        print(f"  {word}: {count}")

    print("\n=== Text Wrapping ===")
    print(wrap_text(sample_text.strip(), width=50))

    print("\n=== Sentence Extraction ===")
    sentences = extract_sentences(sample_text)
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}: {sent}")

    print("\n=== Remove Punctuation ===")
    text_with_punct = "Hello, world! How's it going? (Great!)"
    print(f"  Original: {text_with_punct}")
    print(f"  Clean: {remove_punctuation(text_with_punct)}")

    print("\n=== Caesar Cipher ===")
    original = "Hello, Python!"
    encrypted = caesar_cipher(original, 3)
    decrypted = caesar_cipher(encrypted, -3)
    print(f"  Original: {original}")
    print(f"  Encrypted: {encrypted}")
    print(f"  Decrypted: {decrypted}")

    # Template strings
    print("\n=== Template Strings ===")
    template = string.Template("Hello, $name! You are $age years old.")
    result = template.substitute(name="Alice", age=30)
    print(f"  Template: {result}")


if __name__ == "__main__":
    main()
