"""Ablation of dense: the same retriever with the lab's static embedder instead of bge-small.

One change against dense.py: the model is potion-retrieval-32M (POTION, through model2vec), a static
model that looks each token's vector up and averages them, where bge-small (through fastembed) runs a
transformer over the whole text. Chunking, the query prefix and the best-chunk lift stay the same.
"""

from __future__ import annotations

from p2 import embed
from p2.retrievers import ChunkScorer
from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"


class DensePotion(Dense):
    def __init__(self, corpus, cfg):
        ChunkScorer.__init__(self, corpus, cfg)
        self.model = embed.POTION
        self.query_prefix = cfg.table("dense").get("query_prefix", "")
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)


def build(corpus, cfg):
    return DensePotion(corpus, cfg)
