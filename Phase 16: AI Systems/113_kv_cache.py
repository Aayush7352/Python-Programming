"""
KV Cache implementation for efficient transformer inference.

Requires: pip install torch
"""
import sys


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import numpy as np
        import time
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== KV Cache for Efficient Inference ===\n")

    class AttentionWithKVCache(nn.Module):
        """Attention with KV cache for autoregressive generation."""

        def __init__(self, d_model: int, n_heads: int):
            super().__init__()
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads

            self.w_q = nn.Linear(d_model, d_model, bias=False)
            self.w_k = nn.Linear(d_model, d_model, bias=False)
            self.w_v = nn.Linear(d_model, d_model, bias=False)
            self.w_o = nn.Linear(d_model, d_model, bias=False)

        def forward(self, x, past_kv=None, use_cache=True):
            batch_size, seq_len, _ = x.shape

            Q = self.w_q(x).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            K = self.w_k(x).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)
            V = self.w_v(x).view(batch_size, -1, self.n_heads, self.d_k).transpose(1, 2)

            if past_kv is not None and use_cache:
                past_K, past_V = past_kv
                K = torch.cat([past_K, K], dim=2)
                V = torch.cat([past_V, V], dim=2)

            current_kv = (K, V) if use_cache else None

            scores = torch.matmul(Q, K.transpose(-2, -1)) / (self.d_k ** 0.5)
            attn = F.softmax(scores, dim=-1)
            output = torch.matmul(attn, V)
            output = output.transpose(1, 2).contiguous().view(batch_size, -1, self.d_model)
            output = self.w_o(output)

            return output, current_kv

    d_model = 64
    n_heads = 4
    attn = AttentionWithKVCache(d_model, n_heads)

    # Simulate autoregressive generation
    print("1. Autoregressive Generation without KV Cache")

    def generate_without_cache(attn, start_token, n_tokens):
        """Generate tokens without KV cache (recomputes all)."""
        generated = [start_token]
        times = []

        for step in range(n_tokens):
            t0 = time.time()
            x = torch.randn(1, len(generated), d_model)
            output, _ = attn(x, use_cache=False)
            next_token = output[:, -1:, :]
            generated.append(next_token)
            times.append(time.time() - t0)

        return generated, times

    generated, times_no_cache = generate_without_cache(attn, torch.randn(1, 1, d_model), 10)
    print(f"  Total time: {sum(times_no_cache):.4f}s")
    print(f"  Average per token: {sum(times_no_cache) / len(times_no_cache):.6f}s")

    print("\n2. Autoregressive Generation WITH KV Cache")

    def generate_with_cache(attn, start_token, n_tokens):
        """Generate tokens with KV cache (only computes new)."""
        past_kv = None
        generated = [start_token]
        times = []

        for step in range(n_tokens):
            t0 = time.time()

            if step == 0:
                x = start_token
            else:
                x = generated[-1]

            output, past_kv = attn(x, past_kv=past_kv, use_cache=True)
            next_token = output[:, -1:, :]
            generated.append(next_token)
            times.append(time.time() - t0)

        return generated, times

    generated, times_with_cache = generate_with_cache(
        attn, torch.randn(1, 1, d_model), 10
    )
    print(f"  Total time: {sum(times_with_cache):.4f}s")
    print(f"  Average per token: {sum(times_with_cache) / len(times_with_cache):.6f}s")

    # Speed comparison
    print("\n3. Speed Comparison")
    print(f"  Without cache: {sum(times_no_cache):.4f}s")
    print(f"  With cache:    {sum(times_with_cache):.4f}s")
    print(f"  Speedup:       {sum(times_no_cache) / max(sum(times_with_cache), 0.001):.1f}x")

    # KV cache size
    print("\n4. KV Cache Memory Analysis")
    batch_size = 1
    n_layers = 12
    n_heads = 12
    d_k = 64
    seq_len = 2048

    kv_per_layer = 2 * batch_size * seq_len * n_heads * d_k * 4  # 4 bytes per float32
    total_kv = kv_per_layer * n_layers
    print(f"  KV cache per token: {kv_per_layer // seq_len // 1024:.1f}KB per layer")
    print(f"  Total KV cache ({seq_len} tokens): {total_kv / 1024 / 1024:.1f}MB")

    print("\n=== KV Cache Benefits ===")
    print("  - Eliminates redundant recomputation")
    print("  - O(1) time per token vs O(n)")
    print("  - Memory-efficiency trade-off: store K,V states")
    print("  - Essential for production LLM inference")
    print("  - Used by: GPT, LLaMA, Mistral, etc.")


if __name__ == "__main__":
    main()
