"""Hybrid retrieval: reciprocal rank fusion (RRF) of two systems' full rankings.

Ported from the 13 lab's pipeline.py (rrf and command_fuse). Each document scores

    RRF(d) = sum over the fused systems s of 1 / (k + rank_s(d)),    rank 1 = best, k = 60

Only ranks count, never raw scores, so bm25's scores (0 to about 20) and dense's cosines (about 0.2 to 0.7)
need no rescaling. Every document is ranked by both systems, not just their top 10, because a document
that is 11th in both lists can belong in the fused top 10.

search_chunks fuses the systems' chunk rankings the same way, so `p2 answer` can use hybrid.

Settings, all optional, in a [hybrid] table of p2.toml:
    systems = ["bm25", "dense"]   the systems to fuse (any in p2/retrievers/ that do not call Claude)
    k = 60                        the RRF constant; a larger k flattens the gap between rank 1 and rank 10
"""

from __future__ import annotations

from p2 import retrievers
from p2.runfile import order

NEEDS_CLAUDE = False


def rrf(rankings, k):
    """Fuse lists of (id, score), each best first, into one list of (id, RRF score), best first."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item, _) in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        settings = cfg.table("hybrid")
        self.k = settings.get("k", 60)
        names = settings.get("systems", ["bm25", "dense"])
        self.systems = [retrievers.build(name, corpus, cfg) for name in names]
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text, k):
        return rrf([s.search(text, self.n_docs) for s in self.systems], self.k)[:k]

    def search_chunks(self, text, k):
        return rrf([s.search_chunks(text, self.n_chunks) for s in self.systems], self.k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
