"""
Transformer model from scratch with PyTorch.

Requires: pip install torch
"""
import sys
import math


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import torch.optim as optim
        import numpy as np
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== Transformer Model ===\n")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Scaled Dot-Product Attention
    class ScaledDotProductAttention(nn.Module):
        def forward(self, query, key, value, mask=None):
            d_k = query.size(-1)
            scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
            if mask is not None:
                scores = scores.masked_fill(mask == 0, -1e9)
            attn = F.softmax(scores, dim=-1)
            output = torch.matmul(attn, value)
            return output, attn

    # Multi-Head Attention
    class MultiHeadAttention(nn.Module):
        def __init__(self, d_model, n_heads):
            super().__init__()
            assert d_model % n_heads == 0
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads

            self.w_q = nn.Linear(d_model, d_model)
            self.w_k = nn.Linear(d_model, d_model)
            self.w_v = nn.Linear(d_model, d_model)
            self.w_o = nn.Linear(d_model, d_model)
            self.attention = ScaledDotProductAttention()

        def forward(self, query, key, value, mask=None):
            batch_size = query.size(0)

            Q = self.w_q(query).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = self.w_k(key).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = self.w_v(value).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)

            output, attn = self.attention(Q, K, V, mask)
            output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
            output = self.w_o(output)
            return output

    # Feed Forward
    class FeedForward(nn.Module):
        def __init__(self, d_model, d_ff):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(d_model, d_ff),
                nn.ReLU(),
                nn.Linear(d_ff, d_model),
            )

        def forward(self, x):
            return self.net(x)

    # Transformer Block
    class TransformerBlock(nn.Module):
        def __init__(self, d_model, n_heads, d_ff, dropout=0.1):
            super().__init__()
            self.attention = MultiHeadAttention(d_model, n_heads)
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)
            self.ff = FeedForward(d_model, d_ff)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, mask=None):
            attn_output = self.attention(x, x, x, mask)
            x = self.norm1(x + self.dropout(attn_output))
            ff_output = self.ff(x)
            x = self.norm2(x + self.dropout(ff_output))
            return x

    # Transformer Encoder
    class TransformerEncoder(nn.Module):
        def __init__(self, vocab_size, d_model, n_heads, d_ff, n_layers, max_len, dropout=0.1):
            super().__init__()
            self.embedding = nn.Embedding(vocab_size, d_model)
            self.pos_encoding = nn.Embedding(max_len, d_model)
            self.layers = nn.ModuleList([
                TransformerBlock(d_model, n_heads, d_ff, dropout)
                for _ in range(n_layers)
            ])
            self.dropout = nn.Dropout(dropout)

        def forward(self, x, mask=None):
            seq_len = x.size(1)
            positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
            x = self.embedding(x) + self.pos_encoding(positions)
            x = self.dropout(x)
            for layer in self.layers:
                x = layer(x, mask)
            return x

    # Simple classifier using transformer
    class TransformerClassifier(nn.Module):
        def __init__(self, vocab_size, d_model=128, n_heads=4, d_ff=256, n_layers=3, max_len=50, num_classes=2):
            super().__init__()
            self.encoder = TransformerEncoder(vocab_size, d_model, n_heads, d_ff, n_layers, max_len)
            self.pool = nn.AdaptiveAvgPool1d(1)
            self.classifier = nn.Linear(d_model, num_classes)

        def forward(self, x, mask=None):
            x = self.encoder(x, mask)
            x = x.transpose(1, 2)
            x = self.pool(x).squeeze(-1)
            x = self.classifier(x)
            return x

    print("  Model components defined:")
    print("  - ScaledDotProductAttention")
    print("  - MultiHeadAttention")
    print("  - FeedForward")
    print("  - TransformerBlock")
    print("  - TransformerEncoder")
    print("  - TransformerClassifier")

    # Create model and test
    d_model = 128
    model = TransformerClassifier(
        vocab_size=1000, d_model=d_model, n_heads=4,
        d_ff=256, n_layers=3, max_len=50, num_classes=2
    ).to(device)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"\n  Total parameters: {total_params:,}")

    # Generate synthetic data
    torch.manual_seed(42)
    batch_size, seq_len = 4, 20
    X = torch.randint(0, 100, (batch_size, seq_len)).to(device)
    y = torch.randint(0, 2, (batch_size,)).to(device)

    # Forward pass
    output = model(X)
    print(f"\n  Input shape: {X.shape}")
    print(f"  Output shape: {output.shape}")
    print(f"  Output sample:\n{output}")

    # Training step
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("\n=== Training Step ===")
    model.train()
    optimizer.zero_grad()
    output = model(X)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()
    print(f"  Loss: {loss.item():.4f}")

    # Compare with PyTorch's built-in transformer
    print("\n=== PyTorch Built-in Transformer ===")
    transformer = nn.Transformer(
        d_model=128, nhead=4, num_encoder_layers=3,
        num_decoder_layers=3, dim_feedforward=256
    )
    src = torch.randn(10, 32, 128)
    tgt = torch.randn(20, 32, 128)
    out = transformer(src, tgt)
    print(f"  PyTorch Transformer output shape: {out.shape}")

    print("\n=== Transformer Architecture ===")
    print("  Key components:")
    print("  1. Multi-Head Attention")
    print("  2. Position-wise Feed Forward")
    print("  3. Layer Normalization")
    print("  4. Residual Connections")
    print("  5. Positional Encoding")
    print("  Used in: BERT, GPT, ViT, T5")


if __name__ == "__main__":
    main()
