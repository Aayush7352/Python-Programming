"""
Simple search engine implementation with inverted index.
"""
import re
import math
from collections import defaultdict, Counter
from typing import List, Dict, Set
import heapq


class Document:
    """Represents a document in the search index."""

    def __init__(self, doc_id: int, title: str, content: str):
        self.doc_id = doc_id
        self.title = title
        self.content = content
        self.terms = self._tokenize(title + " " + content)

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        return re.findall(r"\b\w+\b", text)


class InvertedIndex:
    """Inverted index for search."""

    def __init__(self):
        self.index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.documents: Dict[int, Document] = {}
        self.doc_count = 0

    def add_document(self, doc: Document):
        """Add a document to the index."""
        self.documents[doc.doc_id] = doc
        self.doc_count += 1

        term_counts = Counter(doc.terms)
        for term, count in term_counts.items():
            self.index[term][doc.doc_id] = count

    def _compute_tfidf(self, term: str, doc_id: int, freq: int) -> float:
        """Compute TF-IDF score."""
        tf = 1 + math.log10(freq) if freq > 0 else 0
        df = len(self.index.get(term, {}))
        idf = math.log10(self.doc_count / (1 + df))

        # Title boost
        doc = self.documents[doc_id]
        if term in doc.title.lower():
            idf *= 1.5

        return tf * idf

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        """Search for documents matching the query."""
        query_terms = re.findall(r"\b\w+\b", query.lower())
        if not query_terms:
            return []

        scores = defaultdict(float)

        for term in query_terms:
            if term in self.index:
                for doc_id, freq in self.index[term].items():
                    scores[doc_id] += self._compute_tfidf(term, doc_id, freq)

        # Get top-k
        top_docs = heapq.nlargest(top_k, scores.items(), key=lambda x: x[1])
        results = []

        for doc_id, score in top_docs:
            doc = self.documents[doc_id]
            snippet = self._generate_snippet(doc.content, query_terms)
            results.append({
                "doc_id": doc_id,
                "title": doc.title,
                "snippet": snippet,
                "score": round(score, 4),
            })

        return results

    def _generate_snippet(self, content: str, query_terms: List[str], max_len: int = 150) -> str:
        """Generate a search snippet around matching terms."""
        content_lower = content.lower()
        positions = []

        for term in query_terms:
            idx = content_lower.find(term)
            if idx >= 0:
                positions.append(idx)

        if not positions:
            return content[:max_len] + "..."

        best_pos = min(positions)
        start = max(0, best_pos - 50)
        end = min(len(content), start + max_len)

        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."

        return snippet

    def print_stats(self):
        """Print index statistics."""
        print(f"  Documents: {self.doc_count}")
        print(f"  Unique terms: {len(self.index)}")
        print(f"  Avg postings per term: {sum(len(p) for p in self.index.values()) / max(len(self.index), 1):.1f}")


def main():
    print("=== Search Engine ===\n")

    index = InvertedIndex()

    # Add documents
    documents = [
        (1, "Python Programming Guide",
         "Python is a high-level programming language. It is widely used for web "
         "development, data analysis, artificial intelligence, and scientific computing."),

        (2, "Machine Learning Basics",
         "Machine learning is a subset of artificial intelligence. It enables systems "
         "to learn and improve from experience without being explicitly programmed."),

        (3, "Web Development with Python",
         "Python web development is popular with frameworks like Django and Flask. "
         "These frameworks make it easy to build scalable web applications."),

        (4, "Data Science Tools",
         "Python is the most popular language for data science. Libraries like NumPy, "
         "Pandas, and Scikit-learn make data analysis powerful and accessible."),

        (5, "Artificial Intelligence Overview",
         "Artificial intelligence encompasses machine learning, deep learning, and "
         "other techniques that enable machines to simulate human intelligence."),
    ]

    print("Indexing documents...")
    for doc_id, title, content in documents:
        doc = Document(doc_id, title, content)
        index.add_document(doc)

    index.print_stats()

    # Search queries
    queries = [
        "Python programming",
        "machine learning",
        "artificial intelligence",
        "data science with Python",
        "web development",
    ]

    print("\nSearch Results:")
    for query in queries:
        results = index.search(query, top_k=3)
        print(f"\n  Query: '{query}' ({len(results)} results)")
        for r in results:
            print(f"    [{r['score']:.3f}] {r['title']}")
            print(f"      {r['snippet'][:80]}...")

    # Boolean query
    print("\n=== Boolean Search ===")
    query = "Python AI"
    term1, term2 = query.lower().split()
    docs_with_both = set(index.index.get(term1, {}).keys()) & \
                     set(index.index.get(term2, {}).keys())
    docs_with_either = set(index.index.get(term1, {}).keys()) | \
                       set(index.index.get(term2, {}).keys())
    print(f"  Documents with '{term1}' AND '{term2}': {len(docs_with_both)}")
    print(f"  Documents with '{term1}' OR '{term2}': {len(docs_with_either)}")

    print("\n=== Search Engine Architecture ===")
    print("  1. Crawling: web crawlers discover pages")
    print("  2. Indexing: inverted index of terms")
    print("  3. Ranking: TF-IDF, BM25, PageRank")
    print("  4. Query: tokenization, expansion")
    print("  5. Retrieval: top-k from inverted index")
    print("  6. Distributed: sharding, replication")


if __name__ == "__main__":
    main()
