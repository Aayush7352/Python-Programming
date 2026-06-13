import os
import tempfile


def write_text(filepath: str, content: str) -> None:
    """Write text to a file (overwrites)."""
    with open(filepath, "w") as f:
        f.write(content)
    print(f"  Wrote {len(content)} chars to {filepath}")


def write_lines(filepath: str, lines: list) -> None:
    """Write multiple lines to a file."""
    with open(filepath, "w") as f:
        for line in lines:
            f.write(line + "\n")
    print(f"  Wrote {len(lines)} lines to {filepath}")


def append_to_file(filepath: str, content: str) -> None:
    """Append content to an existing file."""
    with open(filepath, "a") as f:
        f.write(content)
    print(f"  Appended to {filepath}")


def write_with_writelines(filepath: str, lines: list) -> None:
    """Write using writelines() method."""
    with open(filepath, "w") as f:
        f.writelines(line + "\n" for line in lines)


def write_binary(filepath: str, data: bytes) -> None:
    """Write binary data to a file."""
    with open(filepath, "wb") as f:
        f.write(data)
    print(f"  Wrote {len(data)} bytes to {filepath}")


def write_formatted(filepath: str, data: dict) -> None:
    """Write formatted output."""
    with open(filepath, "w") as f:
        f.write("Configuration File\n")
        f.write("=" * 40 + "\n")
        for key, value in data.items():
            f.write(f"{key:20}: {value}\n")


def main():
    # Using temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        print("=== Write Text ===")
        path = os.path.join(tmpdir, "output.txt")
        write_text(path, "Hello, File!")

        print("\n=== Write Lines ===")
        lines_path = os.path.join(tmpdir, "lines.txt")
        write_lines(lines_path, ["Line 1", "Line 2", "Line 3"])

        print("\n=== Append to File ===")
        append_to_file(lines_path, "\nAppended line")

        print("\n=== Read Back ===")
        with open(lines_path, "r") as f:
            print(f.read())

        print("\n=== Write Binary ===")
        bin_path = os.path.join(tmpdir, "binary.bin")
        write_binary(bin_path, bytes(range(256)))

        print("\n=== Write Formatted ===")
        config_path = os.path.join(tmpdir, "config.txt")
        config = {
            "host": "localhost",
            "port": "8080",
            "debug": "true",
            "database": "testdb",
        }
        write_formatted(config_path, config)

        print("\n=== Read Formatted Config ===")
        with open(config_path, "r") as f:
            print(f.read())

        # Read binary back
        print("=== Read Binary Back ===")
        with open(bin_path, "rb") as f:
            data = f.read()
        print(f"  First 10 bytes: {list(data[:10])}")
        print(f"  Last 5 bytes: {list(data[-5:])}")

        # Cleanup happens automatically


if __name__ == "__main__":
    main()
