"""
NumPy fundamentals.

Requires: pip install numpy
"""
import sys


def main():
    try:
        import numpy as np
    except ImportError:
        print("NumPy is not installed.")
        print("Install with: pip install numpy")
        sys.exit(1)

    print("=== NumPy Arrays ===")

    # Creating arrays
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.zeros((3, 4))
    arr3 = np.ones((2, 3))
    arr4 = np.eye(4)
    arr5 = np.arange(10)
    arr6 = np.linspace(0, 1, 5)
    arr7 = np.random.randn(3, 3)

    print(f"  From list: {arr1}")
    print(f"  Zeros (3x4):\n{arr2}")
    print(f"  Identity (4x4):\n{arr4}")
    print(f"  arange: {arr5}")
    print(f"  linspace: {arr6}")

    # Array attributes
    print("\n=== Array Attributes ===")
    arr = np.random.randn(4, 5)
    print(f"  Shape: {arr.shape}")
    print(f"  Dimensions: {arr.ndim}")
    print(f"  Size (elements): {arr.size}")
    print(f"  Data type: {arr.dtype}")
    print(f"  Item size: {arr.itemsize} bytes")

    # Indexing and slicing
    print("\n=== Indexing & Slicing ===")
    arr = np.arange(12).reshape(3, 4)
    print(f"  Array:\n{arr}")
    print(f"  Element [1,2]: {arr[1, 2]}")
    print(f"  Row 1: {arr[1]}")
    print(f"  Column 2: {arr[:, 2]}")
    print(f"  Slice [0:2, 1:3]:\n{arr[0:2, 1:3]}")
    print(f"  Boolean mask (arr > 5): {arr[arr > 5]}")

    # Fancy indexing
    print(f"  Fancy indexing [[0,2], [1,3]]: {arr[[0, 2], [1, 3]]}")

    # Operations
    print("\n=== Array Operations ===")
    a = np.array([1, 2, 3, 4])
    b = np.array([5, 6, 7, 8])

    print(f"  a = {a}, b = {b}")
    print(f"  a + b = {a + b}")
    print(f"  a * b = {a * b}")
    print(f"  a ** 2 = {a ** 2}")
    print(f"  np.sin(a) = {np.sin(a)}")
    print(f"  np.dot(a, b) = {np.dot(a, b)}")

    # Broadcasting
    print("\n=== Broadcasting ===")
    matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    vector = np.array([1, 0, 1])
    print(f"  Matrix:\n{matrix}")
    print(f"  Vector: {vector}")
    print(f"  Matrix + Vector:\n{matrix + vector}")

    # Statistical operations
    print("\n=== Statistics ===")
    data = np.random.randn(1000)
    print(f"  Mean: {np.mean(data):.4f}")
    print(f"  Std: {np.std(data):.4f}")
    print(f"  Min: {np.min(data):.4f}")
    print(f"  Max: {np.max(data):.4f}")
    print(f"  Median: {np.median(data):.4f}")
    print(f"  Percentile 25: {np.percentile(data, 25):.4f}")

    # Reshaping
    print("\n=== Reshaping ===")
    arr = np.arange(12)
    print(f"  Original: {arr}")
    print(f"  Reshape (3,4):\n{arr.reshape(3, 4)}")
    print(f"  Reshape (2,2,3):\n{arr.reshape(2, 2, 3)}")

    # Linear Algebra
    print("\n=== Linear Algebra ===")
    A = np.array([[3, 1], [1, 2]])
    b = np.array([9, 8])
    x = np.linalg.solve(A, b)
    print(f"  Solve Ax = b: x = {x}")
    print(f"  Verify: A @ x = {A @ x}")
    print(f"  Determinant of A: {np.linalg.det(A):.2f}")
    print(f"  Inverse of A:\n{np.linalg.inv(A)}")
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"  Eigenvalues: {eigenvalues}")

    # Performance comparison
    print("\n=== Performance ===")
    import time
    n = 10_000_000

    start = time.time()
    python_sum = sum(range(n))
    python_time = time.time() - start

    start = time.time()
    numpy_sum = np.sum(np.arange(n))
    numpy_time = time.time() - start

    print(f"  Python sum: {python_time:.4f}s")
    print(f"  NumPy sum: {numpy_time:.4f}s")
    print(f"  NumPy is {python_time / numpy_time:.1f}x faster")


if __name__ == "__main__":
    main()
