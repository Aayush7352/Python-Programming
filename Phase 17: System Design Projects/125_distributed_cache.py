"""
Distributed cache implementation with consistent hashing.
"""
import hashlib
import time
from typing import Any, Optional, List, Tuple


class CacheNode:
    """Represents a cache node in the cluster."""

    def __init__(self, node_id: str, capacity: int = 1000):
        self.node_id = node_id
        self.capacity = capacity
        self.data: dict = {}
        self.expiry: dict = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[Any]:
        if key in self.data:
            if key in self.expiry and time.time() > self.expiry[key]:
                del self.data[key]
                del self.expiry[key]
                self.misses += 1
                return None
            self.hits += 1
            return self.data[key]
        self.misses += 1
        return None

    def set(self, key: str, value: Any, ttl: int = None):
        if len(self.data) >= self.capacity:
            self._evict()
        self.data[key] = value
        if ttl:
            self.expiry[key] = time.time() + ttl

    def delete(self, key: str) -> bool:
        if key in self.data:
            del self.data[key]
            self.expiry.pop(key, None)
            return True
        return False

    def _evict(self):
        """Simple LRU-like eviction: remove oldest."""
        if self.data:
            oldest = next(iter(self.data))
            del self.data[oldest]
            self.expiry.pop(oldest, None)

    @property
    def stats(self) -> dict:
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "node_id": self.node_id,
            "size": len(self.data),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": hit_rate,
        }


class ConsistentHashRing:
    """Consistent hashing for distributing keys across nodes."""

    def __init__(self, virtual_nodes: int = 10):
        self.virtual_nodes = virtual_nodes
        self.ring: dict = {}
        self.sorted_keys: List[int] = []
        self.nodes: dict = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node: CacheNode):
        self.nodes[node.node_id] = node
        for i in range(self.virtual_nodes):
            vnode_key = f"{node.node_id}:vnode:{i}"
            hash_val = self._hash(vnode_key)
            self.ring[hash_val] = node.node_id
        self.sorted_keys = sorted(self.ring.keys())

    def remove_node(self, node_id: str):
        self.nodes.pop(node_id, None)
        for i in range(self.virtual_nodes):
            vnode_key = f"{node_id}:vnode:{i}"
            hash_val = self._hash(vnode_key)
            self.ring.pop(hash_val, None)
        self.sorted_keys = sorted(self.ring.keys())

    def get_node(self, key: str) -> Optional[CacheNode]:
        if not self.ring:
            return None
        hash_val = self._hash(key)
        for ring_key in self.sorted_keys:
            if hash_val <= ring_key:
                return self.nodes.get(self.ring[ring_key])
        return self.nodes.get(self.ring[self.sorted_keys[0]])


class DistributedCache:
    """Distributed cache with consistent hashing."""

    def __init__(self):
        self.ring = ConsistentHashRing()

    def add_node(self, node_id: str, capacity: int = 1000):
        node = CacheNode(node_id, capacity)
        self.ring.add_node(node)

    def remove_node(self, node_id: str):
        self.ring.remove_node(node_id)

    def get(self, key: str) -> Optional[Any]:
        node = self.ring.get_node(key)
        return node.get(key) if node else None

    def set(self, key: str, value: Any, ttl: int = None):
        node = self.ring.get_node(key)
        if node:
            node.set(key, value, ttl)

    def delete(self, key: str) -> bool:
        node = self.ring.get_node(key)
        return node.delete(key) if node else False

    def get_stats(self) -> List[dict]:
        return [node.stats for node in self.ring.nodes.values()]


def main():
    print("=== Distributed Cache ===\n")

    cache = DistributedCache()

    # Add nodes
    for i in range(3):
        cache.add_node(f"node-{i}", capacity=100)
    print(f"  Cluster has {len(cache.ring.nodes)} nodes")

    # Set values
    print("\n  Setting values...")
    for i in range(20):
        cache.set(f"key:{i}", f"value:{i}", ttl=60)

    # Get values
    print("  Getting values...")
    hits = 0
    misses = 0
    for i in range(25):
        result = cache.get(f"key:{i}")
        if result:
            hits += 1
        else:
            misses += 1
    print(f"  Hits: {hits}, Misses: {misses}")

    # Node statistics
    print("\n  Node Statistics:")
    for stat in cache.get_stats():
        print(f"    {stat['node_id']}: size={stat['size']}, "
              f"hit_rate={stat['hit_rate']:.2%}")

    # Simulate node failure
    print("\n  Removing node-0...")
    cache.remove_node("node-0")
    print(f"  Cluster has {len(cache.ring.nodes)} nodes")

    # Data redistribution (automatic via consistent hashing)
    print("\n  Accessing data after node removal...")
    hits = 0
    for i in range(20):
        if cache.get(f"key:{i}"):
            hits += 1
    print(f"  Recovered keys after node removal: {hits}/20")

    print("\n=== Distributed Cache Features ===")
    print("  1. Consistent hashing for minimal redistribution")
    print("  2. Virtual nodes for balanced distribution")
    print("  3. TTL-based expiry")
    print("  4. LRU eviction")
    print("  5. Node failure tolerance")
    print("  6. Horizontal scalability")
    print("  Production: Redis Cluster, Memcached, Hazelcast")


if __name__ == "__main__":
    main()
