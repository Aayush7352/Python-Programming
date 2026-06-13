import os


def read_entire_file(filepath: str) -> str:
    """Read entire file as a single string."""
    with open(filepath, "r") as f:
        return f.read()


def read_line_by_line(filepath: str) -> list:
    """Read file line by line into a list."""
    with open(filepath, "r") as f:
        return [line.strip() for line in f]


def read_with_iterator(filepath: str) -> None:
    """Read file using iteration (memory efficient for large files)."""
    with open(filepath, "r") as f:
        for line in f:
            print(f"  Line: {line.strip()}")


def read_with_readlines(filepath: str) -> list:
    """Read using readlines() method."""
    with open(filepath, "r") as f:
        return f.readlines()


def read_chunks(filepath: str, chunk_size: int = 1024) -> None:
    """Read file in fixed-size chunks (great for binary files)."""
    with open(filepath, "r") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            print(f"  Chunk ({len(chunk)} chars): {chunk[:50]}...")


def read_with_seek(filepath: str) -> None:
    """Demonstrate seeking within a file."""
    with open(filepath, "r") as f:
        print(f"Position: {f.tell()}")
        content = f.read(10)
        print(f"Read 10 chars: '{content}'")
        print(f"Position: {f.tell()}")
        f.seek(0)
        print(f"After seek(0), position: {f.tell()}")
        content = f.read(5)
        print(f"Read 5 chars from start: '{content}'")


def main():
    # Create a sample file
    sample_path = "/tmp/sample_read.txt"
    with open(sample_path, "w") as f:
        f.write("Hello, World!\n")
        f.write("This is line 2.\n")
        f.write("Line 3: Python file handling.\n")
        f.write("Line 4: Reading files is easy.\n")
        f.write("Line 5: End of file.\n")

    print("=== Read Entire File ===")
    content = read_entire_file(sample_path)
    print(f"  Content:\n{content}")

    print("\n=== Read Line by Line ===")
    lines = read_line_by_line(sample_path)
    for i, line in enumerate(lines, 1):
        print(f"  {i}: {line}")

    print("\n=== Iterate Over File ===")
    read_with_iterator(sample_path)

    print("\n=== Read with readlines() ===")
    raw_lines = read_with_readlines(sample_path)
    print(f"  Raw lines: {raw_lines}")

    print("\n=== Seek and Tell ===")
    read_with_seek(sample_path)

    # Cleanup
    os.remove(sample_path)


if __name__ == "__main__":
    main()
