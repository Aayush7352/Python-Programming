"""
URL Shortener service implementation.
"""
import hashlib
import json
import time
from typing import Optional


class URLShortener:
    """URL shortener with analytics."""

    BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def __init__(self):
        self.url_map = {}
        self.reverse_map = {}
        self.stats = {}
        self.counter = 1000000

    def _encode(self, num: int) -> str:
        """Convert number to base62 string."""
        if num == 0:
            return self.BASE62[0]
        encoded = []
        while num > 0:
            encoded.append(self.BASE62[num % 62])
            num //= 62
        return "".join(reversed(encoded))

    def shorten(self, long_url: str, custom_alias: str = None) -> str:
        """Shorten a URL."""
        if custom_alias:
            if custom_alias in self.url_map:
                raise ValueError(f"Alias '{custom_alias}' already in use")
            short_url = custom_alias
        else:
            if long_url in self.reverse_map:
                return self.reverse_map[long_url]
            self.counter += 1
            short_url = self._encode(self.counter)

        self.url_map[short_url] = long_url
        self.reverse_map[long_url] = short_url
        self.stats[short_url] = {"created": time.time(), "clicks": 0}

        return short_url

    def resolve(self, short_url: str) -> Optional[str]:
        """Resolve a shortened URL to the original."""
        long_url = self.url_map.get(short_url)
        if long_url:
            self.stats[short_url]["clicks"] += 1
        return long_url

    def get_stats(self, short_url: str) -> Optional[dict]:
        return self.stats.get(short_url)

    def delete(self, short_url: str) -> bool:
        if short_url in self.url_map:
            long_url = self.url_map.pop(short_url)
            self.reverse_map.pop(long_url, None)
            self.stats.pop(short_url, None)
            return True
        return False


def main():
    print("=== URL Shortener ===\n")

    shortener = URLShortener()

    # Shorten URLs
    urls = [
        "https://example.com/very/long/url/that/needs/shortening",
        "https://docs.python.org/3/tutorial/index.html",
        "https://github.com/username/repository/pull/123",
    ]

    print("Shortened URLs:")
    short_codes = []
    for url in urls:
        short = shortener.shorten(url)
        short_codes.append(short)
        print(f"  {url[:50]:50} -> {short}")

    # Custom alias
    custom = shortener.shorten("https://my-site.com/about", "about-us")
    print(f"\nCustom alias: {'https://my-site.com/about':50} -> {custom}")
    print(f"Duplicate check: {shortener.shorten('https://my-site.com/about')}")

    # Resolve
    print("\nResolving URLs:")
    for short in short_codes:
        original = shortener.resolve(short)
        print(f"  {short:10} -> {original[:50]}...")

    # Stats
    print("\nAccess Statistics:")
    for short in short_codes:
        for _ in range(3):
            shortener.resolve(short)
        stats = shortener.get_stats(short)
        print(f"  {short:10} clicks={stats['clicks']}")

    # Delete
    print(f"\nDelete '{short_codes[0]}': {shortener.delete(short_codes[0])}")
    print(f"Resolve after delete: {shortener.resolve(short_codes[0])}")

    # Error handling
    try:
        shortener.shorten("https://example.com", custom_alias="about-us")
    except ValueError as e:
        print(f"\nError: {e}")

    print("\n=== Design Considerations ===")
    print("  Storage: Redis (cache) + PostgreSQL (persistent)")
    print("  Encoding: Base62 (6-7 chars for billions of URLs)")
    print("  Redirection: 301/302 HTTP redirect")
    print("  Analytics: click tracking, geolocation")
    print("  Scaling: consistent hashing, read replicas")
    print("  Rate limiting: per-user API limits")


if __name__ == "__main__":
    main()
