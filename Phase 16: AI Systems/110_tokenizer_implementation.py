"""
Tokenizer implementation from scratch.

Demonstrates BPE (Byte-Pair Encoding) tokenization.
"""
import re
from collections import defaultdict, Counter


class BPETokenizer:
    """Byte-Pair Encoding tokenizer implementation."""

    def __init__(self, vocab_size: int = 300):
        self.vocab_size = vocab_size
        self.merges = {}
        self.vocab = {}
        self.pattern = r"""'(?i:[sdmt]|ll|ve|re)| ?\w+| ?\W+"""

    def _get_stats(self, words: list) -> Counter:
        """Count adjacent byte pairs."""
        pairs = Counter()
        for word, freq in words:
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs

    def _merge_vocab(self, pair, words):
        """Merge a pair of tokens."""
        new_words = []
        pattern = " ".join(pair)
        replacement = "".join(pair)
        for word, freq in words:
            new_word = word.replace(pattern, replacement, 1)
            new_words.append((new_word, freq))
        return new_words

    def train(self, corpus: str):
        """Train the tokenizer on a corpus."""
        # Pre-tokenize
        words = re.findall(self.pattern, corpus)
        word_freqs = Counter(words)
        words = [(" ".join(list(w)) + " </w>", freq) for w, freq in word_freqs.items()]

        # Learn merges
        num_merges = min(self.vocab_size - 256, len(set(" ".join(w) for w, _ in words)))
        # Simple BPE
        self.vocab = {i: chr(i) for i in range(256)}
        next_id = 256

        for i in range(num_merges):
            pairs = self._get_stats(words)
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            self.merges[best] = next_id
            self.vocab[next_id] = "".join(best)
            next_id += 1
            words = self._merge_vocab(best, words)

        print(f"  Trained vocabulary size: {len(self.vocab)}")
        print(f"  Number of merges: {len(self.merges)}")

    def encode(self, text: str) -> list:
        """Encode text to token IDs."""
        words = re.findall(self.pattern, text)
        tokens = []
        for word in words:
            symbols = list(word) + ["</w>"]
            while len(symbols) > 1:
                pairs = [(symbols[i], symbols[i + 1]) for i in range(len(symbols) - 1)]
                can_merge = [p for p in pairs if p in self.merges]
                if not can_merge:
                    break
                best = min(can_merge, key=lambda p: self.merges[p])
                idx = pairs.index(best)
                symbols = symbols[:idx] + ["".join(best)] + symbols[idx + 2:]
            tokens.append(symbols[0])
        return [self.vocab.get(t, ord(t[0])) for t in tokens]

    def decode(self, ids: list) -> str:
        """Decode token IDs back to text."""
        rev_vocab = {v: k for k, v in self.vocab.items()}
        text = "".join(rev_vocab.get(i, "") for i in ids)
        return text.replace("</w>", " ").strip()


class SimpleCharTokenizer:
    """Simple character-level tokenizer."""

    def __init__(self):
        self.char_to_id = {}
        self.id_to_char = {}

    def fit(self, texts: list):
        chars = set("".join(texts))
        self.char_to_id = {c: i + 1 for i, c in enumerate(sorted(chars))}
        self.char_to_id["[PAD]"] = 0
        self.char_to_id["[UNK]"] = len(self.char_to_id)
        self.id_to_char = {v: k for k, v in self.char_to_id.items()}

    def encode(self, text: str, max_len: int = None) -> list:
        ids = [self.char_to_id.get(c, self.char_to_id["[UNK]"]) for c in text]
        if max_len:
            ids = ids[:max_len] + [0] * (max_len - len(ids))
        return ids

    def decode(self, ids: list) -> str:
        return "".join(self.id_to_char.get(i, "") for i in ids if i != 0)


def main():
    print("=== Tokenizer Implementation ===\n")

    corpus = "Hello, world! This is a tokenizer implementation. "
    corpus += "Tokenization is the first step in NLP pipelines. "
    corpus += "Byte-Pair Encoding is a popular subword tokenization algorithm."

    print("1. BPE Tokenizer")
    tokenizer = BPETokenizer(vocab_size=350)
    tokenizer.train(corpus)

    test_sentences = [
        "Hello, world!",
        "Tokenization is important.",
        "Subword tokenization works well.",
    ]

    for sent in test_sentences:
        encoded = tokenizer.encode(sent)
        decoded = tokenizer.decode(encoded)
        print(f"\n  Input: '{sent}'")
        print(f"  Encoded: {encoded[:10]}{'...' if len(encoded) > 10 else ''}")
        print(f"  Decoded: '{decoded}'")

    print("\n\n2. Character Tokenizer")
    char_tokenizer = SimpleCharTokenizer()
    char_tokenizer.fit([
        "Hello, world!",
        "Tokenization is fun.",
    ])

    for sent in test_sentences:
        encoded = char_tokenizer.encode(sent, max_len=20)
        decoded = char_tokenizer.decode(encoded)
        print(f"\n  Input: '{sent}'")
        print(f"  Encoded: {encoded}")
        print(f"  Decoded: '{decoded}'")

    print("\n=== Tokenization Types ===")
    print("  Word-level: splits on whitespace/punctuation")
    print("  Character-level: each char is a token")
    print("  Subword (BPE): most common (GPT, BERT)")
    print("  SentencePiece: language-independent")
    print("  WordPiece: used in BERT")


if __name__ == "__main__":
    main()
