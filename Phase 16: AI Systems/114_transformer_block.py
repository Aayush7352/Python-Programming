"""
Complete Transformer block implementation.

Requires: pip install torch
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

    print("=== Complete Transformer Block ===\n")

    class MultiHeadAttention(nn.Module):
        def __init__(self, d_model, n_heads, dropout=0.1):
            super().__init__()
            assert d_model % n_heads == 0
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads
            self.w_q = nn.Linear(d_model, d_model)
            self.w_k = nn.Linear(d_model, d_model)
            self.w_v = nn.Linear(d_model, d_model)
            self.w_o = nn.Linear(d_model, d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, query, key, value, mask=None):
            batch = query.size(0)
            Q = self.w_q(query).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = self.w_k(key).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = self.w_v(value).view(batch, -1, self.n_heads, self.d_k).transpose(1, 2)
            scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
            if mask is not None:
                scores = scores.masked_fill(mask == 0, float("-inf"))
            attn = self.dropout(F.softmax(scores, dim=-1))
            out = torch.matmul(attn, V)
            out = out.transpose(1, 2).contiguous().view(batch, -1, self.d_model)
            return self.w_o(out)

    class FeedForward(nn.Module):
        def __init__(self, d_model, d_ff, dropout=0.1):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(d_ff, d_model),
                nn.Dropout(dropout),
            )

        def forward(self, x):
            return self.net(x)

    class TransformerBlock(nn.Module):
        """One transformer block with pre-layer norm."""

        def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
            super().__init__()
            self.self_attn = MultiHeadAttention(d_model, n_heads, dropout)
            self.cross_attn = MultiHeadAttention(d_model, n_heads, dropout)
            self.ff = FeedForward(d_model, d_ff, dropout)
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)
            self.norm3 = nn.LayerNorm(d_model)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, encoder_output=None, self_mask=None, cross_mask=None):
            # Self-attention with residual
            attn_out = self.self_attn(self.norm1(x), self.norm1(x), self.norm1(x), self_mask)
            x = x + self.dropout(attn_out)

            # Cross-attention (if encoder output available)
            if encoder_output is not None:
                cross_out = self.cross_attn(
                    self.norm2(x), self.norm2(encoder_output),
                    self.norm2(encoder_output), cross_mask
                )
                x = x + self.dropout(cross_out)

            # Feed forward with residual
            ff_out = self.ff(self.norm3(x))
            x = x + self.dropout(ff_out)

            return x

    class TransformerDecoder(nn.Module):
        """Complete transformer decoder."""

        def __init__(self, vocab_size, d_model, n_heads, d_ff, n_layers, max_len, dropout=0.1):
            super().__init__()
            self.token_embedding = nn.Embedding(vocab_size, d_model)
            self.pos_embedding = nn.Embedding(max_len, d_model)
            self.layers = nn.ModuleList([
                TransformerBlock(d_model, n_heads, d_ff, dropout)
                for _ in range(n_layers)
            ])
            self.norm = nn.LayerNorm(d_model)
            self.output = nn.Linear(d_model, vocab_size)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, encoder_output=None):
            seq_len = x.size(1)
            positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
            x = self.dropout(self.token_embedding(x) + self.pos_embedding(positions))

            # Causal mask
            mask = torch.triu(torch.ones(seq_len, seq_len, device=x.device), diagonal=1).bool()

            for layer in self.layers:
                x = layer(x, encoder_output, self_mask=~mask)

            x = self.norm(x)
            return self.output(x)

    print("  Component layers:")
    print("  - Token Embedding + Positional Embedding")
    print("  - Dropout")
    print("  - N x TransformerBlock (Self-Attn + Cross-Attn + FF)")
    print("  - LayerNorm")
    print("  - Output projection\n")

    # Build and test
    d_model = 128
    n_heads = 4
    d_ff = 256
    n_layers = 3
    vocab_size = 1000

    decoder = TransformerDecoder(vocab_size, d_model, n_heads, d_ff, n_layers, max_len=50)
    total_params = sum(p.numel() for p in decoder.parameters())
    print(f"  Total parameters: {total_params:,}")

    # Forward pass
    x = torch.randint(0, vocab_size, (2, 10))
    encoder_out = torch.randn(2, 15, d_model)
    output = decoder(x, encoder_out)
    print(f"  Input shape: {x.shape}")
    print(f"  Encoder output shape: {encoder_out.shape}")
    print(f"  Output shape: {output.shape}")

    # Inference
    logits = output[0, -1, :]
    probs = F.softmax(logits, dim=-1)
    top_k = torch.topk(probs, 5)
    print(f"\n  Top-5 predictions:")
    for i in range(5):
        print(f"    Token {top_k.indices[i]}: {top_k.values[i]:.4f}")

    print("\n=== Transformer Block Architecture ===")
    print("  Input -> LayerNorm -> Multi-Head Self-Attention")
    print("  -> Residual -> LayerNorm -> Cross-Attention")
    print("  -> Residual -> LayerNorm -> Feed Forward")
    print("  -> Residual -> Output")
    print("  Key features: Pre-norm, GELU activation")
    print("  Used in: GPT-2, LLaMA, Mistral")


if __name__ == "__main__":
    main()
