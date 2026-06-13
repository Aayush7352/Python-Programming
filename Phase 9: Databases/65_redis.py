"""
Redis demonstration.

Requires: pip install redis
"""
import sys
import time


def main():
    """Redis operations demonstration."""
    try:
        import redis
    except ImportError:
        print("redis-py is not installed.")
        print("Install with: pip install redis")
        print("\nThis file demonstrates Redis patterns using redis-py.")
        sys.exit(1)

    print("=== Redis Demo ===")

    try:
        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.ping()
        print("  Connected to Redis!")
    except redis.ConnectionError:
        print("  Could not connect to Redis.")
        print("  Make sure Redis is running on localhost:6379")
        return

    # String operations
    print("\n=== String Operations ===")
    r.set("user:1:name", "Alice")
    r.set("user:1:email", "alice@example.com")
    r.set("user:1:count", 0)

    name = r.get("user:1:name")
    print(f"  Name: {name}")

    # Increment/Decrement
    r.incr("user:1:count")
    r.incr("user:1:count")
    r.incr("user:1:count")
    count = r.get("user:1:count")
    print(f"  Count after 3 increments: {count}")

    # Set with expiry
    r.setex("temp:session", 5, "active")
    print(f"  Session TTL: {r.ttl('temp:session')}s")

    # List operations
    print("\n=== List Operations ===")
    r.rpush("queue:tasks", "task1", "task2", "task3")
    print(f"  Queue length: {r.llen('queue:tasks')}")
    print(f"  Pop from left: {r.lpop('queue:tasks')}")
    print(f"  Queue range: {r.lrange('queue:tasks', 0, -1)}")

    # Set operations
    print("\n=== Set Operations ===")
    r.sadd("user:1:skills", "Python", "Docker", "Redis")
    r.sadd("user:2:skills", "Python", "Kubernetes", "AWS")

    print(f"  User 1 skills: {r.smembers('user:1:skills')}")
    print(f"  Common skills: {r.sinter('user:1:skills', 'user:2:skills')}")
    print(f"  All skills: {r.sunion('user:1:skills', 'user:2:skills')}")

    # Sorted sets
    print("\n=== Sorted Set Operations ===")
    r.zadd("leaderboard", {"Alice": 100, "Bob": 85, "Charlie": 95, "Diana": 80})
    print(f"  Leaderboard: {r.zrevrange('leaderboard', 0, -1, withscores=True)}")
    print(f"  Bob's rank: {r.zrevrank('leaderboard', 'Bob') + 1}")

    # Hash operations
    print("\n=== Hash Operations ===")
    r.hset("user:1", mapping={
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "city": "New York",
    })
    print(f"  User hash: {r.hgetall('user:1')}")
    print(f"  User age: {r.hget('user:1', 'age')}")

    # Pipeline
    print("\n=== Pipeline ===")
    pipe = r.pipeline()
    pipe.incr("stats:page_views")
    pipe.incr("stats:page_views")
    pipe.incr("stats:page_views")
    pipe.set("stats:last_update", time.strftime("%Y-%m-%d %H:%M:%S"))
    pipe.execute()
    print(f"  Page views: {r.get('stats:page_views')}")

    # Pub/Sub
    print("\n=== Pub/Sub ===")
    pub = r.pubsub()
    pub.subscribe("notifications")
    r.publish("notifications", "Hello from Redis!")
    message = pub.get_message(timeout=2)
    if message:
        print(f"  Received: {message['data']}")
    pub.unsubscribe("notifications")

    # Expiry and TTL
    print("\n=== Expiry ===")
    r.set("temp:key", "will expire", ex=10)
    print(f"  TTL: {r.ttl('temp:key')}s")
    r.expire("temp:key", 60)
    print(f"  TTL after expire: {r.ttl('temp:key')}s")

    # Cleanup keys
    print("\n=== Cleanup ===")
    keys = r.keys("user:*") + r.keys("queue:*") + r.keys("temp:*") + \
           r.keys("stats:*") + r.keys("leaderboard")
    if keys:
        r.delete(*keys)
        print(f"  Deleted {len(keys)} demo keys")

    r.close()


if __name__ == "__main__":
    main()
