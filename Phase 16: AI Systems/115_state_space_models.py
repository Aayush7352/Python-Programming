"""
State Space Models (SSM) / Mamba implementation concepts.

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

    print("=== State Space Models (Mamba-style) ===\n")

    class SSMCell(nn.Module):
        """Basic State Space Model cell.
        
        State: h' = A @ h + B @ x
        Output: y = C @ h + D @ x (skip connection)
        """
        def __init__(self, d_model, d_state=16):
            super().__init__()
            self.d_model = d_model
            self.d_state = d_state

            # Parameters (simplified - real Mamba has HiPPO initialization)
            self.A = nn.Parameter(torch.randn(d_state, d_state) * 0.1)
            self.B = nn.Parameter(torch.randn(d_model, d_state) * 0.1)
            self.C = nn.Parameter(torch.randn(d_state, d_model) * 0.1)
            self.D = nn.Parameter(torch.randn(d_model) * 0.1)

        def forward(self, x, h=None):
            batch, seq_len, _ = x.shape

            if h is None:
                h = torch.zeros(batch, self.d_state, device=x.device)

            outputs = []
            for t in range(seq_len):
                xt = x[:, t, :]
                # h = A @ h + B @ x
                h = h @ self.A.T + xt @ self.B
                # y = C @ h + D * x (skip)
                yt = h @ self.C + self.D * xt
                outputs.append(yt)

            return torch.stack(outputs, dim=1), h

    class MambaBlock(nn.Module):
        """Simplified Mamba-style block."""

        def __init__(self, d_model, d_state=16, expand=2):
            super().__init__()
            self.d_model = d_model
            inner_dim = d_model * expand

            self.norm = nn.LayerNorm(d_model)
            self.proj_in = nn.Linear(d_model, inner_dim)
            self.ssm = SSMCell(inner_dim, d_state)
            self.proj_out = nn.Linear(inner_dim, d_model)
            self.activation = nn.SiLU()

        def forward(self, x):
            residual = x
            x = self.norm(x)
            x = self.activation(self.proj_in(x))
            x, _ = self.ssm(x)
            x = self.proj_out(x)
            return x + residual

    # Test the SSM
    print("1. SSM Cell")
    d_model = 32
    d_state = 8
    batch, seq_len = 2, 10

    ssm = SSMCell(d_model, d_state)
    x = torch.randn(batch, seq_len, d_model)
    output, final_h = ssm(x)

    print(f"  Input shape: {x.shape}")
    print(f"  Output shape: {output.shape}")
    print(f"  Final state shape: {final_h.shape}")

    # Test Mamba block
    print("\n2. Mamba Block")
    mamba = MambaBlock(d_model, d_state)
    x = torch.randn(batch, seq_len, d_model)
    output = mamba(x)
    print(f"  Input shape: {x.shape}")
    print(f"  Output shape: {output.shape}")

    # Compare with Transformer
    print("\n3. SSM vs Transformer")
    print(f"  SSM: O(L * d^2) compute, O(d^2) memory")
    print(f"  Transformer: O(L^2 * d) compute, O(L^2) memory")
    print(f"  Where L = sequence length, d = model dimension")

    # Sequence length scaling
    print("\n4. Scaling Comparison")
    for L in [512, 1024, 2048, 4096]:
        ssm_compute = L * d_model ** 2
        transformer_compute = L ** 2 * d_model
        ratio = transformer_compute / ssm_compute
        print(f"  L={L:5d}: SSM={ssm_compute:10d}, Transformer={transformer_compute:12d}, "
              f"Ratio={ratio:.1f}x")

    print("\n=== SSM/Mamba Advantages ===")
    print("  - Linear complexity O(L) vs O(L^2)")
    print("  - Better long-range dependencies")
    print("  - Constant memory (state-based)")
    print("  - Fast inference (recurrent)")
    print("  - Selective state space (Mamba v2)")
    print("  - Used in: Mamba, Mamba-2, Jamba")
    print("  - Competitive with Transformers on many tasks")

    print("\n=== SSM Variants ===")
    print("  1. S4: Structured State Space")
    print("  2. Mamba: Selective SSM")
    print("  3. Mamba-2: State Space Dual")
    print("  4. Jamba: Hybrid SSM + Transformer")
    print("  5. Griffin: Gated Linear Recurrence")


if __name__ == "__main__":
    main()
