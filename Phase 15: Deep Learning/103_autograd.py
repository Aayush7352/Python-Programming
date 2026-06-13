"""
PyTorch autograd - automatic differentiation.

Requires: pip install torch
"""
import sys


def main():
    try:
        import torch
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== Autograd: Automatic Differentiation ===\n")

    # Basic gradient computation
    print("1. Basic Gradient")
    x = torch.tensor(3.0, requires_grad=True)
    y = x ** 2 + 2 * x + 1
    y.backward()
    print(f"   x = {x}, y = x^2 + 2x + 1 = {y}")
    print(f"   dy/dx at x=3: {x.grad} (expected 2*3+2=8)")

    # Multi-variable gradient
    print("\n2. Multi-variable Gradient")
    x = torch.tensor(2.0, requires_grad=True)
    y = torch.tensor(3.0, requires_grad=True)
    z = x ** 2 + y ** 3 + x * y
    z.backward()
    print(f"   x = {x}, y = {y}")
    print(f"   z = x^2 + y^3 + xy = {z}")
    print(f"   dz/dx = {x.grad} (expected 2x + y = 2*2 + 3 = 7)")
    print(f"   dz/dy = {y.grad} (expected 3y^2 + x = 3*9 + 2 = 29)")

    # Gradient of a vector
    print("\n3. Vector Gradient")
    x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
    y = x ** 2
    # y is a vector, need to provide gradient
    grad_output = torch.ones_like(y)
    y.backward(grad_output)
    print(f"   x = {x}")
    print(f"   y = x^2 = {y}")
    print(f"   dy/dx = {x.grad} (expected 2*x = {2 * torch.tensor([1.0, 2.0, 3.0])})")

    # Gradient accumulation
    print("\n4. Gradient Accumulation")
    x = torch.tensor(2.0, requires_grad=True)
    y = x ** 2
    y.backward()
    print(f"   After first backward: {x.grad}")
    # Accumulates!
    y = x ** 3
    y.backward()
    print(f"   After second backward (accumulated): {x.grad}")
    x.grad.zero_()
    y = x ** 2
    y.backward()
    print(f"   After zero_grad and backward: {x.grad}")

    # Disabling gradient tracking
    print("\n5. Disabling Gradient Tracking")
    x = torch.tensor(3.0, requires_grad=True)
    y1 = x ** 2
    with torch.no_grad():
        y2 = x ** 3
    print(f"   y1 (requires grad): {y1.requires_grad}")
    print(f"   y2 (no grad): {y2.requires_grad}")

    # Using torch.no_grad for inference
    print("\n6. Neural Network Style")
    torch.manual_seed(42)
    w = torch.randn(2, 3, requires_grad=True)
    b = torch.randn(3, requires_grad=True)
    x = torch.randn(1, 2)

    # Forward pass
    z = x @ w + b
    loss = z.sum()

    # Backward pass
    loss.backward()

    print(f"   Input shape: {x.shape}")
    print(f"   Weight shape: {w.shape}")
    print(f"   Output shape: {z.shape}")
    print(f"   Loss: {loss.item():.4f}")
    print(f"   w.grad shape: {w.grad.shape}")
    print(f"   b.grad: {b.grad}")

    # Computational graph
    print("\n7. Computational Graph")
    x = torch.tensor(2.0, requires_grad=True)
    y = torch.tensor(3.0, requires_grad=True)
    z1 = x ** 2 + y ** 2
    z2 = x * y
    z = z1 + z2
    print(f"   Grad function: {z.grad_fn}")
    print(f"   Grad fn next: {z.grad_fn.next_functions}")

    # Higher-order gradients
    print("\n8. Higher-order Gradients")
    x = torch.tensor(2.0, requires_grad=True)

    def f(x):
        return x ** 3 + 2 * x ** 2 + x

    # First derivative
    y = f(x)
    grad = torch.autograd.grad(y, x, create_graph=True)[0]
    print(f"   f(x) = x^3 + 2x^2 + x")
    print(f"   f'({x.item()}) = {grad.item()} ({3*x**2 + 4*x + 1})")

    # Second derivative
    y2 = grad.sum()
    grad2 = torch.autograd.grad(y2, x)[0]
    print(f"   f''({x.item()}) = {grad2.item()} ({6*x + 4})")


if __name__ == "__main__":
    main()
