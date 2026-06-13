import csv
import io
import os


def write_csv_basic(filepath: str) -> None:
    """Basic CSV writing."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Age", "City"])
        writer.writerow(["Alice", 30, "New York"])
        writer.writerow(["Bob", 25, "London"])
        writer.writerow(["Charlie", 35, "Paris"])


def write_csv_dict(filepath: str) -> None:
    """Write CSV using DictWriter."""
    with open(filepath, "w", newline="") as f:
        fieldnames = ["Name", "Age", "City", "Salary"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({"Name": "David", "Age": 28, "City": "Berlin", "Salary": 75000})
        writer.writerow({"Name": "Eve", "Age": 32, "City": "Tokyo", "Salary": 85000})


def read_csv_basic(filepath: str) -> None:
    """Read CSV using reader."""
    print(f"  Reading {filepath}:")
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            print(f"    Row {i}: {row}")


def read_csv_dict(filepath: str) -> None:
    """Read CSV using DictReader."""
    print(f"\n  Reading {filepath} as dict:")
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(f"    {row['Name']}: Age {row['Age']}, City {row['City']}")


def csv_in_memory() -> None:
    """Work with CSV in memory."""
    print("\n=== In-Memory CSV ===")
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Product", "Price", "Quantity"])
    writer.writerow(["Laptop", 999.99, 10])
    writer.writerow(["Mouse", 25.50, 50])
    writer.writerow(["Keyboard", 79.99, 30])

    csv_content = output.getvalue()
    print(f"  CSV Content:\n{csv_content}")

    # Read back
    input_stream = io.StringIO(csv_content)
    reader = csv.reader(input_stream)
    for row in reader:
        print(f"  Parsed: {row}")


def csv_with_custom_delimiter(filepath: str) -> None:
    """CSV with custom delimiter (e.g., semicolon)."""
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Name", "Age", "Country"])
        writer.writerow(["Frank", 40, "Canada"])
        writer.writerow(["Grace", 22, "Australia"])

    print(f"\n  Reading semicolon-delimited CSV:")
    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            print(f"    {row}")


def main():
    tmpdir = "/tmp/csv_demo"
    os.makedirs(tmpdir, exist_ok=True)

    print("=== Write/Read Basic CSV ===")
    path = os.path.join(tmpdir, "people.csv")
    write_csv_basic(path)
    read_csv_basic(path)

    print("\n=== Write/Read Dict CSV ===")
    dict_path = os.path.join(tmpdir, "employees.csv")
    write_csv_dict(dict_path)
    read_csv_dict(dict_path)

    csv_in_memory()

    print("\n=== Custom Delimiter ===")
    custom_path = os.path.join(tmpdir, "custom.csv")
    csv_with_custom_delimiter(custom_path)

    # Cleanup
    import shutil
    shutil.rmtree(tmpdir)


if __name__ == "__main__":
    main()
