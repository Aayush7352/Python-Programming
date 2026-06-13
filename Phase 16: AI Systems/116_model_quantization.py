"""
Model quantization techniques.

Requires: pip install torch
"""
import sys


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import numpy as np
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== Model Quantization ===\n")

    # 1. Post-Training Dynamic Quantization
    print("1. Post-Training Dynamic Quantization")

    class SimpleModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(128, 64)
            self.fc2 = nn.Linear(64, 32)
            self.fc3 = nn.Linear(32, 10)

        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            return self.fc3(x)

    model_fp32 = SimpleModel()
    model_fp32.eval()

    print(f"  Original (FP32):")
    print(f"    fc1.weight dtype: {model_fp32.fc1.weight.dtype}")

    # Quantize
    model_quantized = torch.quantization.quantize_dynamic(
        model_fp32, {nn.Linear}, dtype=torch.qint8
    )
    print(f"  Quantized (INT8):")
    print(f"    fc1.weight dtype: {model_quantized.fc1.weight().dtype}")

    # Compare sizes
    def get_model_size(model):
        return sum(p.numel() * p.element_size() for p in model.parameters())

    fp32_size = get_model_size(model_fp32)
    quantized_size = get_model_size(model_quantized)
    print(f"  FP32 size: {fp32_size:,} bytes")
    print(f"  INT8 size: {quantized_size:,} bytes")
    print(f"  Compression: {fp32_size / quantized_size:.1f}x")

    # 2. Weight Quantization (from scratch)
    print("\n2. Manual Weight Quantization")

    def quantize_tensor(tensor, n_bits=8):
        """Quantize a tensor to n_bits."""
        qmin = 0
        qmax = 2 ** n_bits - 1

        min_val = tensor.min()
        max_val = tensor.max()

        scale = (max_val - min_val) / (qmax - qmin)
        zero_point = qmin - min_val / scale if scale > 0 else 0

        q_tensor = torch.round(tensor / scale + zero_point).clamp(qmin, qmax)
        return q_tensor, scale, zero_point

    def dequantize_tensor(q_tensor, scale, zero_point):
        """Dequantize a tensor."""
        return (q_tensor - zero_point) * scale

    weights = torch.randn(10, 10)
    q_weights, scale, zp = quantize_tensor(weights, n_bits=8)
    dq_weights = dequantize_tensor(q_weights, scale, zp)

    mse = ((weights - dq_weights) ** 2).mean()
    print(f"  Original weights: {weights.flatten()[:4]}")
    print(f"  Quantized weights: {q_weights.flatten()[:4]}")
    print(f"  Dequantized weights: {dq_weights.flatten()[:4]}")
    print(f"  Quantization MSE: {mse:.6f}")

    # 3. Effect on Model Accuracy
    print("\n3. Impact on Accuracy")
    with torch.no_grad():
        x = torch.randn(32, 128)

        fp32_output = model_fp32(x)
        q_output = model_quantized(x)

        mse_diff = ((fp32_output - q_output) ** 2).mean()
        max_diff = (fp32_output - q_output).abs().max()
        print(f"  Mean squared diff: {mse_diff:.6f}")
        print(f"  Max absolute diff: {max_diff:.6f}")

    # 4. Different quantization levels
    print("\n4. Quantization Levels Comparison")
    bit_widths = [4, 8, 16, 32]
    for bits in bit_widths:
        q, scale, zp = quantize_tensor(weights, bits)
        dq = dequantize_tensor(q, scale, zp)
        mse = ((weights - dq) ** 2).mean()
        compression = 32 / bits
        print(f"  {bits:2d}-bit: MSE={mse:.8f}, Compression={compression:.1f}x")

    # 5. K-bit quantization example
    print("\n5. K-bit Quantization")
    w = torch.randn(1000)
    q4, s4, zp4 = quantize_tensor(w, 4)
    q8, s8, zp8 = quantize_tensor(w, 8)

    print(f"  FP32 unique values: {len(w.unique())}")
    print(f"  INT4 unique values: {len(q4.unique())}")
    print(f"  INT8 unique values: {len(q8.unique())}")

    print("\n=== Quantization Methods ===")
    print("  1. Post-Training Dynamic Quantization")
    print("  2. Post-Training Static Quantization")
    print("  3. Quantization-Aware Training")
    print("  4. Weight-only Quantization (GPTQ, AWQ)")
    print("  5. FP8 Training (H100+)")
    print("  6. NF4 (NormalFloat4 - QLoRA)")
    print("  7. SmoothQuant (activation quantization)")


if __name__ == "__main__":
    main()
