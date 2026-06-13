"""
Vector database implementation concepts.

Requires: pip install numpy
"""
import sys
import numpy as np
from typing import List, Tuple, Optional


class VectorStore:
    """Simple in-memory vector database with cosine similarity."""

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors: List[np.ndarray] = []
        self.metadata: List[dict] = []
        self.ids: List[int] = []
        self._next_id = 1

    def add(self, vector: np.ndarray, metadata: dict = None) -> int:
        """Add a vector to the store."""
        assert vector.shape == (self.dimension,), \
            f"Expected dimension {self.dimension}, got {vector.shape}"
        vector_id = self._next_id
        self._next_id += 1
        self.vectors.append(vector / np.linalg.norm(vector))  # normalize
        self.metadata.append(metadata or {})
        self.ids.append(vector_id)
        return vector_id

    def add_batch(self, vectors: List[np.ndarray],
                  metadatas: List[dict] = None) -> List[int]:
        """Add multiple vectors."""
        if metadatas is None:
            metadatas = [{}] * len(vectors)
        return [self.add(v, m) for v, m in zip(vectors, metadatas)]

    def search(self, query: np.ndarray, k: int = 10,
               return_scores: bool = True) -> List[Tuple]:
        """Search for k nearest neighbors using cosine similarity."""
        query = query / np.linalg.norm(query)
        similarities = np.dot(self.vectors, query)

        top_k = np.argsort(similarities)[-k:][::-1]

        results = []
        for idx in top_k:
            result = {
                "id": self.ids[idx],
                "metadata": self.metadata[idx],
                "score": float(similarities[idx]),
            }
            results.append(result)

        return results

    def delete(self, vector_id: int) -> bool:
        """Delete a vector by ID."""
        if vector_id in self.ids:
            idx = self.ids.index(vector_id)
            self.vectors.pop(idx)
            self.metadata.pop(idx)
            self.ids.pop(idx)
            return True
        return False

    @property
    def size(self):
        return len(self.vectors)


class IVFFlatIndex:
    """Simple IVF (Inverted File) index for approximate search."""

    def __init__(self, dimension: int, n_clusters: int = 5):
        self.dimension = dimension
        self.n_clusters = n_clusters
        self.centroids: np.ndarray = None
        self.vectors: List[np.ndarray] = []
        self.metadata: List[dict] = []
        self.ids: List[int] = []
        self._next_id = 1

    def train(self, vectors: List[np.ndarray]):
        """Train the index (k-means clustering)."""
        from sklearn.cluster import KMeans

        X = np.array([v / np.linalg.norm(v) for v in vectors])
        kmeans = KMeans(n_clusters=min(self.n_clusters, len(vectors)),
                       random_state=42, n_init=10)
        kmeans.fit(X)
        self.centroids = kmeans.cluster_centers_

    def add(self, vector: np.ndarray, metadata: dict = None) -> int:
        vector = vector / np.linalg.norm(vector)
        vid = self._next_id
        self._next_id += 1
        self.vectors.append(vector)
        self.metadata.append(metadata or {})
        self.ids.append(vid)
        return vid

    def search(self, query: np.ndarray, k: int = 5, n_probe: int = 2) -> List[dict]:
        """Search with approximate nearest neighbors."""
        query = query / np.linalg.norm(query)

        if self.centroids is not None:
            dists = np.linalg.norm(self.centroids - query, axis=1)
            top_clusters = np.argsort(dists)[:n_probe]

            candidates = []
            for cid in top_clusters:
                for v, meta, vid in zip(self.vectors, self.metadata, self.ids):
                    candidates.append((v, meta, vid))

            if candidates:
                candidate_vectors = np.array([c[0] for c in candidates])
                similarities = np.dot(candidate_vectors, query)
                top_k = np.argsort(similarities)[-k:][::-1]

                results = []
                for idx in top_k:
                    results.append({
                        "id": candidates[idx][2],
                        "metadata": candidates[idx][1],
                        "score": float(similarities[idx]),
                    })
                return results

        return []


def main():
    print("=== Vector Database Implementation ===\n")

    # Create vector store
    dimension = 128
    store = VectorStore(dimension)

    # Add random vectors
    print("1. Adding vectors")
    for i in range(100):
        vec = np.random.randn(dimension)
        store.add(vec, {"label": f"doc_{i}", "category": i % 5})
    print(f"   Store size: {store.size}")

    # Search
    print("\n2. Search")
    query = np.random.randn(dimension)
    results = store.search(query, k=5)

    print("   Top 5 results:")
    for r in results:
        print(f"     ID={r['id']}, Score={r['score']:.4f}, "
              f"Label={r['metadata']['label']}")

    # IVF index
    print("\n3. IVF (Approximate) Index")
    ivf = IVFFlatIndex(dimension, n_clusters=5)

    for i in range(100):
        vec = np.random.randn(dimension)
        ivf.add(vec, {"id": i})

    ivf.train(ivf.vectors[:50])
    results = ivf.search(query, k=5, n_probe=2)

    print("   IVF Search results:")
    for r in results:
        print(f"     ID={r['id']}, Score={r['score']:.4f}")

    # Comparison: exact vs approximate
    print("\n4. Exact vs Approximate Search")
    exact = store.search(query, k=5)
    approx = ivf.search(query, k=5, n_probe=3)

    exact_ids = {r["id"] for r in exact}
    approx_ids = {r["id"] for r in approx}
    overlap = exact_ids & approx_ids
    print(f"   Exact IDs: {sorted(exact_ids)[:5]}")
    print(f"   Approx IDs: {sorted(approx_ids)[:5]}")
    print(f"   Overlap: {len(overlap)} / {len(exact)}")

    print("\n=== Vector Database Concepts ===")
    print("  1. Embedding models convert data to vectors")
    print("  2. Exact search: O(n) linear scan")
    print("  3. Approximate: IVF, HNSW, PQ")
    print("  4. Similarity: cosine, euclidean, dot product")
    print("  5. Used in: semantic search, RAG, recommendations")
    print("  Popular: Pinecone, Weaviate, Qdrant, Milvus, Chroma")


if __name__ == "__main__":
    main()
