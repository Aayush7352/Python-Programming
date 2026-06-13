class TrieNode:
    """Node in a trie data structure."""

    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0  # number of words passing through


class Trie:
    """Trie (prefix tree) implementation."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.count += 1
        node.is_end = True

    def search(self, word: str) -> bool:
        """Search for a complete word."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix."""
        return self._find_node(prefix) is not None

    def count_prefix(self, prefix: str) -> int:
        """Count words with given prefix."""
        node = self._find_node(prefix)
        return node.count if node else 0

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Find node corresponding to prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def get_all_words(self) -> list:
        """Get all words in the trie."""
        words = []

        def dfs(node, path):
            if node.is_end:
                words.append("".join(path))
            for char, child in sorted(node.children.items()):
                path.append(char)
                dfs(child, path)
                path.pop()

        dfs(self.root, [])
        return words

    def autocomplete(self, prefix: str, limit: int = 5) -> list:
        """Autocomplete suggestions for a prefix."""
        node = self._find_node(prefix)
        if not node:
            return []

        suggestions = []

        def dfs(node, path):
            if len(suggestions) >= limit:
                return
            if node.is_end:
                suggestions.append(prefix + "".join(path))
            for char, child in sorted(node.children.items()):
                path.append(char)
                dfs(child, path)
                path.pop()
                if len(suggestions) >= limit:
                    return

        dfs(node, [])
        return suggestions

    def delete(self, word: str) -> bool:
        """Delete a word from the trie."""
        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0

            char = word[depth]
            if char not in node.children:
                return False

            should_delete = _delete(node.children[char], word, depth + 1)
            if should_delete:
                node.children[char].count -= 1
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            node.children[char].count -= 1
            return False

        return _delete(self.root, word, 0)


def main():
    print("=== Trie Basics ===")
    trie = Trie()
    words = ["apple", "app", "application", "apt", "bat", "batch", "battery"]

    for word in words:
        trie.insert(word)

    print(f"  Words in trie: {trie.get_all_words()}")

    print("\n=== Search ===")
    tests = ["apple", "app", "apt", "appl", "batman"]
    for t in tests:
        print(f"  search('{t}'): {trie.search(t)}")

    print("\n=== Prefix Check ===")
    prefixes = ["ap", "app", "bat", "cat"]
    for p in prefixes:
        print(f"  starts_with('{p}'): {trie.starts_with(p)}")

    print("\n=== Count Prefix ===")
    for p in ["ap", "app", "ba", "x"]:
        print(f"  count_prefix('{p}'): {trie.count_prefix(p)}")

    print("\n=== Autocomplete ===")
    for prefix in ["ap", "app", "ba", "cat"]:
        suggestions = trie.autocomplete(prefix, 3)
        print(f"  autocomplete('{prefix}'): {suggestions}")

    print("\n=== Delete ===")
    trie = Trie()
    for word in ["apple", "app", "application"]:
        trie.insert(word)
    print(f"  Before delete: {trie.get_all_words()}")
    trie.delete("app")
    print(f"  After delete 'app': {trie.get_all_words()}")
    print(f"  search('apple'): {trie.search('apple')}")

    # Practical example: spell checker
    print("\n=== Spell Checker ===")
    dictionary = Trie()
    valid_words = ["hello", "world", "python", "programming", "code"]
    for w in valid_words:
        dictionary.insert(w)

    test_words = ["helo", "world", "pyton", "codex"]
    for w in test_words:
        if dictionary.search(w):
            print(f"  '{w}': correct")
        else:
            suggestions = dictionary.autocomplete(w[:2], 3)
            print(f"  '{w}': incorrect, suggestions: {suggestions}")


if __name__ == "__main__":
    main()
