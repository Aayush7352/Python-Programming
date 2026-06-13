"""
Recommendation system implementation.

Collaborative filtering + content-based filtering.
"""
import math
import random
from collections import defaultdict
from typing import List, Dict, Tuple


class User:
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.ratings: Dict[int, float] = {}  # item_id -> rating


class Item:
    def __init__(self, item_id: int, title: str, genres: List[str]):
        self.item_id = item_id
        self.title = title
        self.genres = genres


class RecommenderSystem:
    """Hybrid recommendation system."""

    def __init__(self):
        self.users: Dict[int, User] = {}
        self.items: Dict[int, Item] = {}
        self.similarity_cache: Dict[Tuple[int, int], float] = {}

    def add_user(self, user_id: int, name: str) -> User:
        user = User(user_id, name)
        self.users[user_id] = user
        return user

    def add_item(self, item_id: int, title: str, genres: List[str]) -> Item:
        item = Item(item_id, title, genres)
        self.items[item_id] = item
        return item

    def rate_item(self, user_id: int, item_id: int, rating: float):
        if user_id in self.users and item_id in self.items:
            self.users[user_id].ratings[item_id] = max(1.0, min(5.0, rating))

    def _cosine_similarity(self, ratings_a: Dict[int, float],
                           ratings_b: Dict[int, float]) -> float:
        common = set(ratings_a.keys()) & set(ratings_b.keys())
        if not common:
            return 0.0

        dot_product = sum(ratings_a[i] * ratings_b[i] for i in common)
        norm_a = math.sqrt(sum(r ** 2 for r in ratings_a.values()))
        norm_b = math.sqrt(sum(r ** 2 for r in ratings_b.values()))

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def _user_similarity(self, u1: int, u2: int) -> float:
        if (u1, u2) in self.similarity_cache:
            return self.similarity_cache[(u1, u2)]
        similarity = self._cosine_similarity(
            self.users[u1].ratings, self.users[u2].ratings
        )
        self.similarity_cache[(u1, u2)] = similarity
        self.similarity_cache[(u2, u1)] = similarity
        return similarity

    def collaborative_filtering(self, user_id: int, k: int = 5) -> List[Tuple[int, float]]:
        """User-based collaborative filtering."""
        user = self.users[user_id]
        scores = defaultdict(float)

        for other_id, other_user in self.users.items():
            if other_id == user_id:
                continue

            similarity = self._user_similarity(user_id, other_id)
            if similarity <= 0:
                continue

            for item_id, rating in other_user.ratings.items():
                if item_id not in user.ratings:
                    scores[item_id] += similarity * rating

        # Normalize
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]

    def content_based_filtering(self, user_id: int, k: int = 5) -> List[Tuple[int, float]]:
        """Content-based: recommend similar items to user's liked items."""
        user = self.users[user_id]
        liked_genres = defaultdict(float)

        for item_id, rating in user.ratings.items():
            if rating >= 4.0:  # Liked items
                item = self.items[item_id]
                for genre in item.genres:
                    liked_genres[genre] += rating

        if not liked_genres:
            return []

        # Score unseen items by genre overlap
        scores = {}
        for item_id, item in self.items.items():
            if item_id in user.ratings:
                continue
            score = sum(liked_genres[g] for g in item.genres if g in liked_genres)
            if score > 0:
                scores[item_id] = score

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]

    def hybrid_recommend(self, user_id: int, k: int = 5) -> List[Tuple[int, float]]:
        """Hybrid: combine collaborative and content-based."""
        collab = dict(self.collaborative_filtering(user_id, k))
        content = dict(self.content_based_filtering(user_id, k))

        all_items = set(collab.keys()) | set(content.keys())
        scores = {}

        for item_id in all_items:
            collab_score = collab.get(item_id, 0)
            content_score = content.get(item_id, 0)

            # Normalize and combine
            max_collab = max(collab.values()) if collab else 1
            max_content = max(content.values()) if content else 1

            normalized = collab_score / max_collab + content_score / max_content
            scores[item_id] = normalized

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]


def main():
    print("=== Recommendation System ===\n")

    rs = RecommenderSystem()

    # Add items
    items_data = [
        (1, "The Matrix", ["Action", "Sci-Fi"]),
        (2, "Inception", ["Action", "Thriller", "Sci-Fi"]),
        (3, "The Shawshank Redemption", ["Drama"]),
        (4, "Pulp Fiction", ["Crime", "Drama"]),
        (5, "The Dark Knight", ["Action", "Thriller", "Drama"]),
        (6, "Interstellar", ["Sci-Fi", "Drama"]),
        (7, "Fight Club", ["Drama", "Thriller"]),
        (8, "Forrest Gump", ["Drama", "Romance"]),
        (9, "The Lord of the Rings", ["Fantasy", "Action"]),
        (10, "Star Wars", ["Sci-Fi", "Action"]),
    ]

    for id_, title, genres in items_data:
        rs.add_item(id_, title, genres)

    # Add users and ratings
    alice = rs.add_user(1, "Alice")
    bob = rs.add_user(2, "Bob")
    charlie = rs.add_user(3, "Charlie")

    alice_ratings = {1: 5, 2: 4, 6: 5, 10: 3}
    bob_ratings = {1: 4, 5: 5, 7: 4, 9: 5}
    charlie_ratings = {3: 5, 4: 4, 5: 3, 8: 4}

    for uid, ratings in [(1, alice_ratings), (2, bob_ratings), (3, charlie_ratings)]:
        for item_id, rating in ratings.items():
            rs.rate_item(uid, item_id, rating)

    # Recommendations for Alice
    print("Alice's ratings:")
    for item_id, rating in alice.ratings.items():
        print(f"  {rs.items[item_id].title}: {rating}")

    print("\nCollaborative Filtering:")
    for item_id, score in rs.collaborative_filtering(1, 5):
        print(f"  {rs.items[item_id].title}: score={score:.3f}")

    print("\nContent-Based Filtering:")
    for item_id, score in rs.content_based_filtering(1, 5):
        print(f"  {rs.items[item_id].title}: score={score:.3f}")

    print("\nHybrid Recommendation:")
    for item_id, score in rs.hybrid_recommend(1, 5):
        print(f"  {rs.items[item_id].title}: score={score:.3f}")

    print("\n=== Recommendation Approaches ===")
    print("  1. Collaborative Filtering: user-based, item-based")
    print("  2. Content-Based: based on item features")
    print("  3. Hybrid: combine multiple approaches")
    print("  4. Matrix Factorization: SVD, ALS")
    print("  5. Deep Learning: NeuMF, Two-Tower")
    print("  6. Contextual: time, location, device")


if __name__ == "__main__":
    main()
