"""
Multi-Head Attention implementation from scratch.
"""
import math
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

    print("=== Multi-Head Attention ===\n")

    class MultiHeadAttention(nn.Module):
        """Multi-Head Attention from 'Attention is All You Need'."""

        def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
            super().__init__()
            assert d_model % n_heads == 0, "d_model must be divisible by n_heads"

            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads

            self.w_q = nn.Linear(d_model, d_model, bias=False)
            self.w_k = nn.Linear(d_model, d_model, bias=False)
            self.w_v = nn.Linear(d_model, d_model, bias=False)
            self.w_o = nn.Linear(d_model, d_model, bias=False)
            self.dropout = nn.Dropout(dropout)

        def forward(self, query, key, value, mask=None, return_weights=False):
            batch_size = query.size(0)

            # Linear projections and split into heads
            Q = self.w_q(query).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = self.w_k(key).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = self.w_v(value).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)

            # Scaled dot-product attention
            scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

            if mask is not None:
                scores = scores.masked_fill(mask == 0, float("-inf"))

            attn_weights = F.softmax(scores, dim=-1)
            attn_weights = self.dropout(attn_weights)

            # Apply attention to values
            attn_output = torch.matmul(attn_weights, V)

            # Concatenate heads
            attn_output = attn_output.transpose(1, 2).contiguous()
            attn_output = attn_output.view(batch_size, -1, self.d_model)

            # Final projection
            output = self.w_o(attn_output)

            if return_weights:
                return output, attn_weights
            return output

    # Demonstrate Multi-Head Attention
    d_model = 512
    n_heads = 8
    batch_size = 2
    seq_len = 10

    mha = MultiHeadAttention(d_model, n_heads)
    print(f"  d_model={d_model}, n_heads={n_heads}, d_k={d_model // n_heads}")

    # Self-attention
    x = torch.randn(batch_size, seq_len, d_model)
    output = mha(x, x, x)
    print(f"\n  Input shape: {x.shape}")
    print(f"  Output shape: {output.shape}")

    # With attention weights
    output, weights = mha(x, x, x, return_weights=True)
    print(f"  Attention weights shape: {weights.shape}")
    print(f"  (batch, heads, seq_len, seq_len)")

    # Cross-attention
    encoder_output = torch.randn(batch_size, 15, d_model)
    decoder_input = torch.randn(batch_size, 8, d_model)
    cross_output = mha(decoder_input, encoder_output, encoder_output)
    print(f"\n  Cross-attention:")
    print(f"  Query (decoder): {decoder_input.shape}")
    print(f"  Key/Value (encoder): {encoder_output.shape}")
    print(f"  Output: {cross_output.shape}")

    # Masked attention (causal)
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
    mask = mask.unsqueeze(0).unsqueeze(0)  # (1, 1, seq_len, seq_len)
    masked_output, masked_weights = mha(
        x, x, x, mask=~mask, return_weights=True
    )
    print(f"\n  Causal masking:")
    print(f"  First head attention (lower triangular):")
    print(f"  {masked_weights[0, 0].round(3)}")

    # Attention patterns visualization
    print("\n=== Head Analysis ===")
    x = torch.randn(1, 5, d_model)
    _, weights = mha(x, x, x, return_weights=True)

    for h in range(min(4, n_heads)):
        print(f"  Head {h}:")
        print(f"    {weights[0, h].round(3)}")

    # Parameter count
    total_params = sum(p.numel() for p in mha.parameters())
    print(f"\n  Total parameters: {total_params:,}")
    print(f"  Q/K/V/O projections: {4 * d_model * d_model:,}")

    print("\n=== Multi-Head Attention Summary ===")
    print("  1. Project Q, K, V with learned weights")
    print("  2. Split into h heads")
    print("  3. Compute scaled dot-product attention per head")
    print("  4. Concatenate all heads")
    print("  5. Final output projection")
    print("  Benefits: captures different relationship types")


if __name__ == "__main__":
    main()
