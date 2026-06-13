"""
PyTorch tensor operations.

Requires: pip install torch
"""
import sys


def main():
    try:
        import torch
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Using device: {device}")

    # Math operations
    print("=== Math Operations ===")
    x = torch.tensor([1.0, 2.0, 3.0, 4.0])
    print(f"  x = {x}")
    print(f"  exp(x) = {torch.exp(x)}")
    print(f"  log(x) = {torch.log(x)}")
    print(f"  sqrt(x) = {torch.sqrt(x)}")
    print(f"  sin(x) = {torch.sin(x)}")
    print(f"  abs(x) = {torch.abs(x)}")
    print(f"  ceil(x/2) = {torch.ceil(x / 2)}")
    print(f"  floor(x/2) = {torch.floor(x / 2)}")

    # Reduction operations
    print("\n=== Reduction Operations ===")
    x = torch.randn(3, 4)
    print(f"  Tensor:\n{x}")
    print(f"  Sum: {x.sum()}")
    print(f"  Mean: {x.mean():.4f}")
    print(f"  Std: {x.std():.4f}")
    print(f"  Max: {x.max()}, Min: {x.min()}")
    print(f"  Sum dim=0: {x.sum(dim=0)}")
    print(f"  Sum dim=1: {x.sum(dim=1)}")
    print(f"  Argmax: {x.argmax()}")
    print(f"  Cumsum: {x.cumsum(dim=0)}")

    # Matrix operations
    print("\n=== Matrix Operations ===")
    A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
    print(f"  A = {A}")
    print(f"  B = {B}")
    print(f"  A @ B = \n{A @ B}")
    print(f"  A.T = \n{A.T}")
    print(f"  A.trace() = {A.trace()}")
    print(f"  A.det() = {A.det():.2f}")
    print(f"  A.inverse() = \n{A.inverse()}")

    # Broadcasting
    print("\n=== Broadcasting ===")
    a = torch.tensor([[1.0], [2.0], [3.0]])
    b = torch.tensor([4.0, 5.0, 6.0])
    print(f"  a shape: {a.shape}")
    print(f"  b shape: {b.shape}")
    print(f"  a + b:\n{a + b}")

    # Tensor concatenation
    print("\n=== Concatenation ===")
    a = torch.ones(2, 3)
    b = torch.zeros(2, 3)
    c = torch.ones(2, 3) * 2

    cat0 = torch.cat([a, b, c], dim=0)
    cat1 = torch.cat([a, b, c], dim=1)
    print(f"  Concat dim=0 shape: {cat0.shape}")
    print(f"  Concat dim=1 shape: {cat1.shape}")
    print(f"  Stack:\n{torch.stack([a, b, c]).shape}")

    # Einsum
    print("\n=== Einsum ===")
    A = torch.randn(3, 4)
    B = torch.randn(4, 5)
    C = torch.einsum("ij,jk->ik", A, B)
    print(f"  Einsum matmul: {C.shape}")

    # Scatter and gather
    print("\n=== Scatter/Gather ===")
    x = torch.tensor([[1, 2], [3, 4], [5, 6]])
    index = torch.tensor([[0, 1], [0, 0], [1, 1]])
    gathered = torch.gather(x, 1, index)
    print(f"  Gather: {gathered}")

    # Slicing and strides
    print("\n=== Advanced Slicing ===")
    x = torch.arange(24).reshape(2, 3, 4)
    print(f"  Shape: {x.shape}")
    print(f"  Strides: {x.stride()}")
    print(f"  Contiguous: {x.is_contiguous()}")

    # Move to GPU
    print("\n=== Device Transfer ===")
    if torch.cuda.is_available():
        x_cpu = torch.randn(3, 3)
        x_gpu = x_cpu.to("cuda")
        print(f"  CPU tensor: {x_cpu.device}")
        print(f"  GPU tensor: {x_gpu.device}")
    else:
        print("  CUDA not available for device transfer demo")


if __name__ == "__main__":
    main()
