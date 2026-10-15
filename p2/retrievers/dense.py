"""Dense retrieval: embed every chunk once, embed the query, and rank chunks by cosine similarity.

Ported from the 12 lab's retrieve.py (dense_rankings), with two changes:
- it scores chunks (the [chunking] settings of p2.toml), not whole documents, and ChunkScorer lifts
  them to documents by each document's best chunk;
- the chunk vectors are cached per text in .cache/vectors/ by p2/embed.py, so only new or changed
  chunks are encoded again.

Every vector has length 1, so for query vector q and chunk vector c the score is
    cos(q, c) = q . c
and one matrix-vector product scores every chunk at once.

Settings, all optional, in a [dense] table of p2.toml:
    model = "BAAI/bge-small-en-v1.5"   the embedder (default bge-small; "minishlab/potion-retrieval-32M" is the lab's other one)
    query_prefix = ""                  text put before every query, such as bge's search instruction
"""

from __future__ import annotations

import numpy as np

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        settings = cfg.table("dense")
        self.model = settings.get("model", embed.BGE)
        self.query_prefix = settings.get("query_prefix", "")
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str) -> np.ndarray:
        if not len(self.chunks):
            return np.zeros(0, dtype=np.float32)
        query = self.embedder.encode([self.query_prefix + text])[0]
        return self.vectors @ query


def build(corpus, cfg):
    return Dense(corpus, cfg)
