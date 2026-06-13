"""
Attention mechanism implementation from scratch.
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

    print("=== Attention Mechanism ===\n")

    # 1. Simple Dot-Product Attention
    print("1. Dot-Product Attention")
    query = torch.tensor([[1.0, 0.0, 1.0]])
    keys = torch.tensor([[1.0, 0.0, 0.0],
                         [0.0, 1.0, 0.0],
                         [1.0, 1.0, 1.0],
                         [0.0, 0.0, 1.0]])
    values = torch.tensor([[10.0], [20.0], [30.0], [40.0]])

    # Compute attention scores
    scores = torch.matmul(query, keys.T)
    weights = F.softmax(scores, dim=-1)
    output = torch.matmul(weights, values)

    print(f"  Query: {query}")
    print(f"  Keys:\n{keys}")
    print(f"  Attention weights: {weights}")
    print(f"  Output: {output}")

    # 2. Scaled Dot-Product Attention
    print("\n2. Scaled Dot-Product Attention")
    d_k = query.size(-1)
    scaled_scores = torch.matmul(query, keys.T) / math.sqrt(d_k)
    scaled_weights = F.softmax(scaled_scores, dim=-1)
    scaled_output = torch.matmul(scaled_weights, values)

    print(f"  Scaled scores: {scaled_scores}")
    print(f"  Scaled weights: {scaled_weights}")
    print(f"  Scaled output: {scaled_output}")

    # 3. Self-Attention
    print("\n3. Self-Attention")
    n = 5
    d = 8
    X = torch.randn(1, n, d)  # (batch, seq_len, d_model)

    W_q = torch.randn(d, d)
    W_k = torch.randn(d, d)
    W_v = torch.randn(d, d)

    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v

    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d)
    attn = F.softmax(scores, dim=-1)
    output = torch.matmul(attn, V)

    print(f"  Input shape: {X.shape}")
    print(f"  Q shape: {Q.shape}")
    print(f"  K shape: {K.shape}")
    print(f"  V shape: {V.shape}")
    print(f"  Attention matrix shape: {attn.shape}")
    print(f"  Output shape: {output.shape}")
    print(f"\n  Attention matrix (row-wise):")
    print(f"  {attn[0].round(3)}")

    # 4. Masked Self-Attention (for decoders)
    print("\n4. Masked Self-Attention")
    seq_len = 5
    mask = torch.triu(torch.ones(seq_len, seq_len) * float("-inf"), diagonal=1)
    print(f"  Causal mask:\n{mask}")

    scores = torch.randn(1, seq_len, seq_len)
    masked_scores = scores + mask
    masked_attn = F.softmax(masked_scores, dim=-1)
    print(f"  Masked attention:\n{masked_attn[0].round(3)}")

    # 5. Cross-Attention (Encoder-Decoder)
    print("\n5. Cross-Attention")
    encoder_output = torch.randn(1, 7, d)  # (batch, src_len, d_model)
    decoder_input = torch.randn(1, 3, d)  # (batch, tgt_len, d_model)

    Q = decoder_input @ W_q  # queries from decoder
    K = encoder_output @ W_k  # keys from encoder
    V = encoder_output @ W_v  # values from encoder

    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d)
    cross_attn = F.softmax(scores, dim=-1)
    output = torch.matmul(cross_attn, V)

    print(f"  Encoder output: {encoder_output.shape}")
    print(f"  Decoder input: {decoder_input.shape}")
    print(f"  Cross-attention shape: {cross_attn.shape}")

    # 6. Attention Visualization
    print("\n6. Attention Interpretation")
    n = 4
    X = torch.randn(1, n, d)
    Q = X @ W_q
    K = X @ W_k
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d)
    attn = F.softmax(scores, dim=-1)

    print(f"  Attention patterns (each row sums to 1):")
    for i in range(n):
        print(f"    Token {i} attends to: {attn[0, i].round(3)}")

    print("\n=== Attention Variants ===")
    print("  1. Dot-product: score = Q·K")
    print("  2. Scaled dot-product: score = Q·K / sqrt(d)")
    print("  3. Additive (Bahdanau): score = v·tanh(W1·Q + W2·K)")
    print("  4. Bi-linear: score = Q·W·K")
    print("  5. Self-attention: Q=K=V=X")
    print("  6. Cross-attention: Q from decoder, K=V from encoder")
    print("  7. Causal/masked: prevent looking ahead")


if __name__ == "__main__":
    main()
