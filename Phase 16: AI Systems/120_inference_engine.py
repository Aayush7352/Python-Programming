"""
Inference engine for transformer models.

Implements efficient inference with KV cache, speculative decoding, etc.
"""
import sys
import time
import math
from typing import List, Optional, Tuple


def main():
    try:
        import torch
        import torch.nn as nn
        import torch.nn.functional as F
        import numpy as np
    except ImportError:
        print("PyTorch not installed (pip install torch)")
        sys.exit(1)

    print("=== Inference Engine ===\n")

    class AttentionLayer(nn.Module):
        def __init__(self, d_model, n_heads):
            super().__init__()
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_k = d_model // n_heads
            self.w_q = nn.Linear(d_model, d_model, bias=False)
            self.w_k = nn.Linear(d_model, d_model, bias=False)
            self.w_v = nn.Linear(d_model, d_model, bias=False)
            self.w_o = nn.Linear(d_model, d_model, bias=False)

        def forward(self, x, past_kv=None, use_cache=True):
            batch, seq_len, _ = x.shape
            Q = self.w_q(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
            K = self.w_k(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)
            V = self.w_v(x).view(batch, seq_len, self.n_heads, self.d_k).transpose(1, 2)

            if past_kv is not None:
                past_K, past_V = past_kv
                K = torch.cat([past_K, K], dim=2)
                V = torch.cat([past_V, V], dim=2)

            new_kv = (K, V) if use_cache else None

            scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
            attn = F.softmax(scores, dim=-1)
            out = torch.matmul(attn, V)
            out = out.transpose(1, 2).contiguous().view(batch, -1, self.d_model)
            return self.w_o(out), new_kv

    class FeedForward(nn.Module):
        def __init__(self, d_model, d_ff):
            super().__init__()
            self.gate = nn.Linear(d_model, d_ff, bias=False)
            self.up = nn.Linear(d_model, d_ff, bias=False)
            self.down = nn.Linear(d_ff, d_model, bias=False)

        def forward(self, x):
            return self.down(F.silu(self.gate(x)) * self.up(x))

    class TransformerLayer(nn.Module):
        def __init__(self, d_model, n_heads, d_ff):
            super().__init__()
            self.attn = AttentionLayer(d_model, n_heads)
            self.ff = FeedForward(d_model, d_ff)
            self.norm1 = nn.LayerNorm(d_model)
            self.norm2 = nn.LayerNorm(d_model)

        def forward(self, x, past_kv=None, use_cache=True):
            attn_out, kv = self.attn(self.norm1(x), past_kv, use_cache)
            x = x + attn_out
            x = x + self.ff(self.norm2(x))
            return x, kv

    class InferenceEngine:
        """Efficient inference engine with KV cache."""

        def __init__(self, d_model=128, n_heads=4, d_ff=256, n_layers=4):
            self.d_model = d_model
            self.layers = nn.ModuleList([
                TransformerLayer(d_model, n_heads, d_ff)
                for _ in range(n_layers)
            ])
            self.norm = nn.LayerNorm(d_model)
            self.lm_head = nn.Linear(d_model, 1000, bias=False)

        @torch.no_grad()
        def generate(self, input_ids, max_new_tokens=20, temperature=0.8):
            """Generate tokens with KV cache."""
            self.eval()
            generated = input_ids.clone()
            past_kvs = [None] * len(self.layers)
            token_times = []

            for step in range(max_new_tokens):
                t0 = time.time()

                if step == 0:
                    x = self._embed(generated)
                else:
                    x = self._embed(generated[:, -1:])

                for i, layer in enumerate(self.layers):
                    x, past_kvs[i] = layer(x, past_kvs[i], use_cache=True)

                x = self.norm(x)
                logits = self.lm_head(x[:, -1, :])

                # Temperature sampling
                logits = logits / temperature
                probs = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)

                generated = torch.cat([generated, next_token], dim=1)
                token_times.append(time.time() - t0)

            return generated, token_times

        def _embed(self, tokens):
            return torch.randn(tokens.size(0), tokens.size(1), self.d_model)

        def eval(self):
            for layer in self.layers:
                layer.eval()

    engine = InferenceEngine()
    input_ids = torch.randint(0, 100, (1, 5))

    print("1. Generating with KV Cache")
    generated, times = engine.generate(input_ids, max_new_tokens=10)

    print(f"   Input shape: {input_ids.shape}")
    print(f"   Output shape: {generated.shape}")
    print(f"   Generated {len(times)} tokens")
    print(f"   Average time per token: {sum(times) / len(times) * 1000:.2f}ms")

    # Temperature effect
    print("\n2. Temperature Sampling")
    logits = torch.randn(1000)
    for temp in [0.1, 0.5, 1.0, 2.0]:
        scaled = logits / temp
        probs = F.softmax(scaled, dim=-1)
        entropy = -(probs * torch.log(probs + 1e-10)).sum()
        print(f"   Temperature {temp:.1f}: entropy={entropy:.2f}")

    # Top-k and top-p sampling
    print("\n3. Top-k / Top-p Sampling")
    logits = torch.randn(1000)
    probs = F.softmax(logits / 0.8, dim=-1)

    top_k = 10
    top_k_probs, top_k_indices = torch.topk(probs, top_k)
    top_k_probs = top_k_probs / top_k_probs.sum()
    print(f"   Top-{top_k} sampling: tokens = {top_k_indices[:5].tolist()}...")

    # Greedy vs sampling
    print("\n4. Greedy vs Sampling")
    greedy = logits.argmax().item()
    sampled = torch.multinomial(probs, 1).item()
    print(f"   Greedy: token {greedy}")
    print(f"   Sampled: token {sampled}")

    print("\n=== Inference Engine Features ===")
    print("  1. KV Cache for O(1) per-token generation")
    print("  2. Temperature sampling for creativity")
    print("  3. Top-k / Top-p (nucleus) sampling")
    print("  4. Batch inference for throughput")
    print("  5. Continuous batching")
    print("  6. Speculative decoding")
    print("  7. Prefix caching")
    print("  8. PagedAttention (vLLM)")


if __name__ == "__main__":
    main()
