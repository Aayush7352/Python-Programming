"""
Retrieval-Augmented Generation (RAG) Pipeline.

Requires: pip install numpy
"""
import sys
import numpy as np
from typing import List


class SimpleEmbedder:
    """Simple embedding function (simulated)."""

    def __init__(self, dim: int = 384):
        self.dim = dim

    def embed(self, text: str) -> np.ndarray:
        np.random.seed(hash(text) % (2 ** 31))
        return np.random.randn(self.dim)


class VectorStore:
    """Simple vector store for RAG."""

    def __init__(self, dim: int):
        self.dim = dim
        self.chunks: List[str] = []
        self.embeddings: List[np.ndarray] = []
        self.metadata: List[dict] = []

    def add(self, chunk: str, embedding: np.ndarray, metadata: dict = None):
        self.chunks.append(chunk)
        self.embeddings.append(embedding / np.linalg.norm(embedding))
        self.metadata.append(metadata or {})

    def search(self, query_emb: np.ndarray, k: int = 3) -> List[dict]:
        query_emb = query_emb / np.linalg.norm(query_emb)
        similarities = [np.dot(e, query_emb) for e in self.embeddings]
        top_k = np.argsort(similarities)[-k:][::-1]

        results = []
        for idx in top_k:
            results.append({
                "chunk": self.chunks[idx],
                "score": float(similarities[idx]),
                "metadata": self.metadata[idx],
            })
        return results


class SimpleLLM:
    """Simulated LLM for RAG demonstration."""

    def generate(self, prompt: str) -> str:
        return f"[Generated response based on context: {prompt[:50]}...]"


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline."""

    def __init__(self, embedder, vector_store, llm):
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm = llm

    def index_document(self, text: str, doc_id: str = None):
        """Split and index a document."""
        chunks = self._chunk_text(text)
        for i, chunk in enumerate(chunks):
            emb = self.embedder.embed(chunk)
            self.vector_store.add(chunk, emb, {
                "doc_id": doc_id or "unknown",
                "chunk_idx": i,
            })
        print(f"  Indexed {len(chunks)} chunks")

    def _chunk_text(self, text: str, chunk_size: int = 200) -> List[str]:
        """Simple text chunking by character count."""
        words = text.split()
        chunks = []
        current = []
        current_len = 0

        for word in words:
            if current_len + len(word) > chunk_size:
                chunks.append(" ".join(current))
                current = [word]
                current_len = len(word)
            else:
                current.append(word)
                current_len += len(word) + 1

        if current:
            chunks.append(" ".join(current))
        return chunks

    def query(self, question: str, k: int = 3) -> dict:
        """Answer a question using RAG."""
        # Retrieve
        query_emb = self.embedder.embed(question)
        relevant_chunks = self.vector_store.search(query_emb, k=k)

        # Augment
        context = "\n\n".join([
            f"[Source {i + 1}]: {r['chunk']}"
            for i, r in enumerate(relevant_chunks)
        ])

        prompt = f"""Context:
{context}

Question: {question}

Answer based on the context above:"""

        # Generate
        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {"chunk": r["chunk"], "score": r["score"]}
                for r in relevant_chunks
            ],
        }


def main():
    print("=== RAG Pipeline ===\n")

    # Initialize components
    embedder = SimpleEmbedder(384)
    vector_store = VectorStore(384)
    llm = SimpleLLM()
    rag = RAGPipeline(embedder, vector_store, llm)

    # Index sample documents
    print("1. Indexing Documents")
    documents = [
        "Python is a high-level programming language known for its readability. "
        "It supports multiple programming paradigms including procedural, "
        "object-oriented, and functional programming. Python's design philosophy "
        "emphasizes code readability with its notable use of significant whitespace. "
        "It was created by Guido van Rossum and first released in 1991.",

        "Machine learning is a subset of artificial intelligence that enables systems "
        "to learn and improve from experience without being explicitly programmed. "
        "It focuses on developing computer programs that can access data and use it "
        "to learn for themselves. Common algorithms include linear regression, "
        "decision trees, neural networks, and support vector machines.",

        "PyTorch is an open-source machine learning framework developed by Facebook's "
        "AI Research lab. It provides two high-level features: tensor computation "
        "with strong GPU acceleration, and deep neural networks built on a "
        "tape-based autograd system. PyTorch is widely used for research and "
        "production deep learning applications.",
    ]

    for i, doc in enumerate(documents):
        rag.index_document(doc, doc_id=f"doc_{i}")

    # Query
    print("\n2. Querying")
    questions = [
        "Who created Python?",
        "What is machine learning?",
        "What is PyTorch used for?",
    ]

    for question in questions:
        print(f"\n  Q: {question}")
        result = rag.query(question)
        print(f"  A: {result['answer']}")
        print(f"  Sources: {len(result['sources'])}")
        for s in result['sources']:
            print(f"    Score: {s['score']:.4f} | Chunk: {s['chunk'][:50]}...")

    print("\n=== RAG Architecture ===")
    print("  1. Document -> Chunking -> Embedding -> Index")
    print("  2. Query -> Embedding -> Similarity Search")
    print("  3. Retrieved Chunks + Query -> LLM Prompt")
    print("  4. LLM generates answer with citations")
    print("\n  Key improvements:")
    print("    - Chunking: semantic, overlap")
    print("    - Embedding: fine-tuned for domain")
    print("    - Retrieval: hybrid (dense + sparse)")
    print("    - Reranking: improve relevance")
    print("    - Prompt engineering: better answers")


if __name__ == "__main__":
    main()
