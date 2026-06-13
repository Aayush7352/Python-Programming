"""
PyTorch basics.

Requires: pip install torch torchvision
"""
import sys


def main():
    try:
        import torch
    except ImportError:
        print("PyTorch not installed.")
        print("Install with: pip install torch torchvision")
        sys.exit(1)

    print(f"  PyTorch version: {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  CUDA device: {torch.cuda.get_device_name(0)}")
        print(f"  Device count: {torch.cuda.device_count()}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Using device: {device}")

    # Tensor creation
    print("\n=== Tensor Creation ===")
    t1 = torch.tensor([1, 2, 3, 4, 5])
    t2 = torch.zeros(3, 4)
    t3 = torch.ones(2, 3)
    t4 = torch.eye(4)
    t5 = torch.randn(3, 3)
    t6 = torch.arange(10)
    t7 = torch.linspace(0, 1, 5)
    t8 = torch.full((2, 3), 7)

    print(f"  From list: {t1}")
    print(f"  Zeros (3x4):\n{t2}")
    print(f"  Eye (4x4):\n{t4}")
    print(f"  Random normal:\n{t5}")
    print(f"  Full of 7s:\n{t8}")

    # Tensor operations
    print("\n=== Tensor Operations ===")
    a = torch.tensor([1, 2, 3])
    b = torch.tensor([4, 5, 6])

    print(f"  a = {a}, b = {b}")
    print(f"  a + b = {a + b}")
    print(f"  a * b = {a * b}")
    print(f"  a @ b (dot product) = {a @ b}")
    print(f"  torch.matmul(a, b) = {torch.matmul(a, b)}")
    print(f"  a.mean() = {a.mean():.2f}")
    print(f"  a.sum() = {a.sum()}")

    # Reshaping
    print("\n=== Reshaping ===")
    x = torch.arange(12)
    print(f"  Original: {x}")
    print(f"  Reshape (3,4):\n{x.reshape(3, 4)}")
    print(f"  View (2,6):\n{x.view(2, 6)}")

    # Indexing
    print("\n=== Indexing ===")
    x = torch.randn(4, 4)
    print(f"  Tensor:\n{x}")
    print(f"  [0, 0]: {x[0, 0]:.4f}")
    print(f"  First row: {x[0]}")
    print(f"  Column 1: {x[:, 1]}")
    print(f"  Boolean mask (x > 0): {x[x > 0]}")

    # Type conversion
    print("\n=== Type Conversion ===")
    x = torch.tensor([1, 2, 3], dtype=torch.float32)
    print(f"  Float: {x}, dtype: {x.dtype}")
    x_int = x.to(torch.int32)
    print(f"  Int: {x_int}, dtype: {x_int.dtype}")

    # NumPy <-> Torch
    print("\n=== NumPy Interop ===")
    import numpy as np
    np_array = np.array([1, 2, 3, 4, 5])
    torch_tensor = torch.from_numpy(np_array)
    print(f"  NumPy -> Torch: {torch_tensor}")
    back_to_numpy = torch_tensor.numpy()
    print(f"  Torch -> NumPy: {back_to_numpy}")


if __name__ == "__main__":
    main()
