import json
import os
from datetime import datetime


class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder for datetime objects."""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def serialize_basics() -> dict:
    """Serialize Python objects to JSON-compatible dicts."""
    data = {
        "name": "Alice",
        "age": 30,
        "is_student": False,
        "grades": [85, 92, 78, 95],
        "address": {
            "city": "New York",
            "zip": "10001",
        },
        "courses": ["Math", "Physics", "CS"],
        "graduated": None,
    }
    return data


def write_json(filepath: str, data: dict) -> None:
    """Write JSON to file with formatting."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Written to {filepath}")


def read_json(filepath: str) -> dict:
    """Read JSON from file."""
    with open(filepath, "r") as f:
        return json.load(f)


def json_with_custom_types(filepath: str) -> None:
    """Serialize objects with custom types."""
    data = {
        "event": "Conference",
        "date": datetime.now(),
        "sessions": ["AI", "Web", "Mobile"],
    }
    with open(filepath, "w") as f:
        json.dump(data, f, cls=DateTimeEncoder, indent=2)
    print(f"  Custom JSON written to {filepath}")


def json_streaming(filepath: str, records: list) -> None:
    """Stream JSON records line by line (JSONL format)."""
    with open(filepath, "w") as f:
        for record in records:
            f.write(json.dumps(record) + "\n")
    print(f"  Written {len(records)} JSONL records to {filepath}")


def read_jsonl(filepath: str) -> list:
    """Read JSONL file."""
    records = []
    with open(filepath, "r") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def manipulate_json(data: dict) -> None:
    """JSON manipulation in Python."""
    print("=== JSON Manipulation ===")
    json_str = json.dumps(data, indent=2)
    print(f"  JSON string:\n{json_str}")

    parsed = json.loads(json_str)
    print(f"  Parsed back: {parsed['name']}")

    # Compact JSON
    compact = json.dumps(data, separators=(",", ":"))
    print(f"  Compact: {compact[:60]}...")

    # Sorted keys
    sorted_json = json.dumps(data, sort_keys=True, indent=2)
    print(f"  Sorted keys:\n{sorted_json}")


def main():
    tmpdir = "/tmp/json_demo"
    os.makedirs(tmpdir, exist_ok=True)

    print("=== Basic JSON Serialization ===")
    data = serialize_basics()
    path = os.path.join(tmpdir, "data.json")
    write_json(path, data)

    print("\n=== Read JSON Back ===")
    loaded = read_json(path)
    print(f"  Name: {loaded['name']}")
    print(f"  Grades: {loaded['grades']}")
    print(f"  Courses: {', '.join(loaded['courses'])}")

    print("\n=== Custom Type Serialization ===")
    custom_path = os.path.join(tmpdir, "custom.json")
    json_with_custom_types(custom_path)
    with open(custom_path, "r") as f:
        print(f"  Content: {f.read()}")

    print("\n=== JSONL Streaming ===")
    records = [
        {"id": 1, "name": "Record 1", "value": 100},
        {"id": 2, "name": "Record 2", "value": 200},
        {"id": 3, "name": "Record 3", "value": 300},
    ]
    jsonl_path = os.path.join(tmpdir, "data.jsonl")
    json_streaming(jsonl_path, records)
    loaded_records = read_jsonl(jsonl_path)
    print(f"  Loaded {len(loaded_records)} records: {loaded_records}")

    manipulate_json(data)

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
