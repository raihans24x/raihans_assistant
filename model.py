# ai_core/model.py

import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, embed_size, heads):
        super().__init__()
        self.embed_size = embed_size
        self.heads = heads
        self.head_dim = embed_size // heads

        assert self.head_dim * heads == embed_size

        self.values = nn.Linear(embed_size, embed_size)
        self.keys = nn.Linear(embed_size, embed_size)
        self.queries = nn.Linear(embed_size, embed_size)
        self.fc_out = nn.Linear(embed_size, embed_size)

    def forward(self, values, keys, queries, mask=None):
        N, query_len, _ = queries.shape
        values = self.values(values)
        keys = self.keys(keys)
        queries = self.queries(queries)

        energy = torch.einsum("nqd,nkd->nqk", [queries, keys])
        attention = F.softmax(energy / (self.embed_size ** 0.5), dim=2)

        out = torch.einsum("nqk,nvd->nqv", [attention, values])
        out = self.fc_out(out)
        return out

class TransformerBlock(nn.Module):
    def __init__(self, embed_size, heads, dropout):
        super().__init__()
        self.attention = SelfAttention(embed_size, heads)
        self.norm1 = nn.LayerNorm(embed_size)
        self.norm2 = nn.LayerNorm(embed_size)

        self.feed_forward = nn.Sequential(
            nn.Linear(embed_size, embed_size * 4),
            nn.ReLU(),
            nn.Linear(embed_size * 4, embed_size)
        )

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        attention = self.attention(x, x, x)
        x = self.norm1(attention + x)
        forward = self.feed_forward(x)
        x = self.norm2(forward + x)
        return x

class GPTMini(nn.Module):
    def __init__(self, vocab_size, embed_size=128, heads=4, depth=2, max_length=100, dropout=0.1):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, embed_size)
        self.pos_embed = nn.Embedding(max_length, embed_size)
        self.blocks = nn.ModuleList(
            [TransformerBlock(embed_size, heads, dropout) for _ in range(depth)]
        )
        self.fc_out = nn.Linear(embed_size, vocab_size)

    def forward(self, x):
        N, seq_length = x.shape
        positions = torch.arange(0, seq_length).unsqueeze(0).expand(N, seq_length).to(x.device)
        out = self.token_embed(x) + self.pos_embed(positions)

        for block in self.blocks:
            out = block(out)

        out = self.fc_out(out)
        return out
