from collections import (
    namedtuple, deque, defaultdict, Counter, OrderedDict,
    ChainMap, UserDict, UserList, UserString
)


def demonstrate_namedtuple():
    """Named tuples for readable data structures."""
    Point = namedtuple("Point", ["x", "y", "z"])
    p = Point(10, 20, 30)
    print(f"Point: {p}")
    print(f"p.x = {p.x}, p[0] = {p[0]}")
    print(f"As dict: {p._asdict()}")
    p2 = p._replace(x=100)
    print(f"After replace: {p2}")


def demonstrate_deque():
    """Double-ended queue for fast appends/pops from both ends."""
    dq = deque(maxlen=5)
    for i in range(7):
        dq.append(i)
        print(f"After append({i}): {list(dq)}")
    print(f"\nDeque: {list(dq)}")
    print(f"Pop right: {dq.pop()}")
    print(f"Pop left: {dq.popleft()}")
    dq.extendleft([-1, -2])
    print(f"After extendleft: {list(dq)}")
    dq.rotate(2)
    print(f"After rotate(2): {list(dq)}")


def demonstrate_defaultdict():
    """Dictionary with default factory for missing keys."""
    dd = defaultdict(int)
    for char in "mississippi":
        dd[char] += 1
    print(f"Char count: {dict(dd)}")

    grouped = defaultdict(list)
    for name in ["alice", "bob", "charlie", "adam"]:
        grouped[name[0]].append(name)
    print(f"Grouped by first letter: {dict(grouped)}")


def demonstrate_counter():
    """Count hashable objects."""
    cnt = Counter("abracadabra")
    print(f"Counter: {cnt}")
    print(f"Most common 3: {cnt.most_common(3)}")
    print(f"Elements: {''.join(sorted(cnt.elements()))}")

    cnt2 = Counter("abracadabraaa")
    print(f"\nCounter operations:")
    print(f"Sum: {cnt + cnt2}")
    print(f"Difference: {cnt - cnt2}")
    print(f"Intersection: {cnt & cnt2}")
    print(f"Union: {cnt | cnt2}")


def demonstrate_ordereddict():
    """Dictionary that remembers insertion order (regular dicts also do this in 3.7+)."""
    od = OrderedDict()
    od["z"] = 1
    od["a"] = 2
    od["b"] = 3
    print(f"OrderedDict: {od}")
    od.move_to_end("z")
    print(f"After move_to_end('z'): {od}")
    od.move_to_end("z", last=False)
    print(f"After move_to_end('z', last=False): {od}")


def demonstrate_chainmap():
    """Combine multiple dictionaries into a single view."""
    defaults = {"theme": "dark", "language": "en", "show_sidebar": True}
    user_prefs = {"language": "fr", "font_size": 14}
    session_prefs = {"show_sidebar": False}

    config = ChainMap(session_prefs, user_prefs, defaults)
    print(f"\nChainMap: {config}")
    print(f"Language: {config['language']}")  # from user_prefs
    print(f"Theme: {config['theme']}")  # from defaults
    config["language"] = "de"
    print(f"After setting language: {config}")


def main():
    print("=== namedtuple ===")
    demonstrate_namedtuple()

    print("\n=== deque ===")
    demonstrate_deque()

    print("\n=== defaultdict ===")
    demonstrate_defaultdict()

    print("\n=== Counter ===")
    demonstrate_counter()

    print("\n=== OrderedDict ===")
    demonstrate_ordereddict()

    print("\n=== ChainMap ===")
    demonstrate_chainmap()


if __name__ == "__main__":
    main()
