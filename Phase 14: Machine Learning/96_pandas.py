"""
Pandas fundamentals.

Requires: pip install pandas numpy
"""
import sys


def main():
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        print("pandas not installed (pip install pandas)")
        sys.exit(1)

    print("=== Series ===")
    s1 = pd.Series([1, 3, 5, np.nan, 6, 8])
    s2 = pd.Series({"a": 10, "b": 20, "c": 30})
    print(f"  Series from list:\n{s1}")
    print(f"\n  Series from dict:\n{s2}")

    print("\n=== DataFrame Creation ===")
    df = pd.DataFrame({
        "Name": ["Alice", "Bob", "Charlie", "Diana"],
        "Age": [25, 30, 35, 28],
        "City": ["NYC", "LA", "Chicago", "Houston"],
        "Salary": [70000, 85000, 65000, 90000],
    })
    print(f"  DataFrame:\n{df}")

    # From numpy array
    df2 = pd.DataFrame(
        np.random.randn(4, 3),
        columns=["A", "B", "C"],
        index=["Row1", "Row2", "Row3", "Row4"]
    )
    print(f"\n  From NumPy:\n{df2}")

    # Reading data
    print("\n=== DataFrame Info ===")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Dtypes:\n{df.dtypes}")
    print(f"  Describe:\n{df.describe()}")

    # Accessing data
    print("\n=== Accessing Data ===")
    print(f"  Head:\n{df.head(2)}")
    print(f"  By column 'Name':\n{df['Name']}")
    print(f"  By iloc [0, 1]: {df.iloc[0, 1]}")
    print(f"  By loc:\n{df.loc[0:1, ['Name', 'Salary']]}")
    print(f"  Boolean filter (Age > 28):\n{df[df['Age'] > 28]}")

    # Operations
    print("\n=== Operations ===")
    print(f"  Mean age: {df['Age'].mean()}")
    print(f"  Max salary: {df['Salary'].max()}")
    print(f"  Sum all numeric: \n{df.select_dtypes(include=[np.number]).sum()}")
    print(f"  Value counts:\n{df['City'].value_counts()}")

    # Grouping
    print("\n=== Grouping ===")
    data = pd.DataFrame({
        "Department": ["Eng", "Eng", "Sales", "Sales", "HR"],
        "Employee": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
        "Salary": [100000, 90000, 80000, 85000, 70000],
    })
    grouped = data.groupby("Department")["Salary"].agg(["mean", "min", "max", "count"])
    print(f"  Grouped by department:\n{grouped}")

    # Handling missing data
    print("\n=== Missing Data ===")
    df_missing = pd.DataFrame({
        "A": [1, 2, np.nan, 4],
        "B": [5, np.nan, np.nan, 8],
        "C": [9, 10, 11, 12],
    })
    print(f"  Original:\n{df_missing}")
    print(f"  Is null:\n{df_missing.isnull()}")
    print(f"  Drop rows:\n{df_missing.dropna()}")
    print(f"  Fill:\n{df_missing.fillna(0)}")
    print(f"  Forward fill:\n{df_missing.fillna(method='ffill')}")

    # Merge and join
    print("\n=== Merging ===")
    df1 = pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
    df2 = pd.DataFrame({"id": [1, 2, 4], "score": [85, 92, 78]})

    merged = pd.merge(df1, df2, on="id", how="inner")
    print(f"  Inner merge:\n{merged}")
    left_merge = pd.merge(df1, df2, on="id", how="left")
    print(f"  Left merge:\n{left_merge}")

    # Apply functions
    print("\n=== Apply ===")
    df["Age Category"] = df["Age"].apply(lambda x: "Young" if x < 30 else "Senior")
    print(f"  With category:\n{df}")

    # Pivot tables
    print("\n=== Pivot Table ===")
    sales = pd.DataFrame({
        "Month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar"],
        "Product": ["A", "B", "A", "B", "A", "B"],
        "Sales": [100, 150, 120, 130, 110, 160],
    })
    pivot = pd.pivot_table(sales, values="Sales", index="Month", columns="Product")
    print(f"  Pivot table:\n{pivot}")

    # Read CSV
    print("\n=== I/O ===")
    import tempfile, os
    path = os.path.join(tempfile.gettempdir(), "sample.csv")
    df.to_csv(path, index=False)
    df_read = pd.read_csv(path)
    print(f"  Read CSV:\n{df_read}")
    os.remove(path)


if __name__ == "__main__":
    main()
