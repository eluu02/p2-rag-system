"""Listwise reranking: Claude reorders a first-stage system's top 20.

Ported from the 13 lab's pipeline.py (rerank_one, RERANK_SCHEMA, RERANK_PROMPT):
- the first stage's top `candidates` documents are shown to Claude as numbered passages, each cut to
  its first `passage_chars` characters, and Claude replies with the best order of their numbers;
- the reply is forced into {"order": [n integers, each 1 to n]} with a JSON schema;
- a reply that is not each number once (or a failed call) keeps the first-stage order for that query,
  with a warning;
- documents below the candidates keep their first-stage order underneath, and a document outside
  the candidates can never be rescued.

Changes from the lab: the prompt names this corpus instead of a help center, the schema bounds every
number to 1..n (the stub's advice), the first stage is a p2 system, every call goes through
p2.claude.call (model from p2.toml, cached replies, tokens recorded in the trace), and the run file's
score is 1 / rank, since Claude returns an order and no score.

search_chunks reranks the first stage's top chunks the same way, for `p2 answer`.

One claude -p call per query. Settings, all optional, in a [rerank] table of p2.toml:
    first_stage = "hybrid"   the system whose top candidates are reranked
    candidates = 20          how many of its top results Claude sees
    passage_chars = 600      each passage is cut to this many characters
"""

from __future__ import annotations

import sys

from p2 import claude, retrievers

NEEDS_CLAUDE = True

PROMPT = """Below are {n} passages from Title 30 of the US Code of Federal Regulations, Chapter I (the federal mine safety and health regulations), numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n):
    return {
        "type": "object",
        "properties": {"order": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": n}, "minItems": n, "maxItems": n}},
        "required": ["order"],
    }


class Rerank:
    def __init__(self, corpus, cfg):
        settings = cfg.table("rerank")
        self.first_stage = settings.get("first_stage", "hybrid")
        self.candidates = settings.get("candidates", 20)
        self.passage_chars = settings.get("passage_chars", 600)
        self.model = cfg.model
        self.cache_dir = claude.cache_folder(cfg)
        self.first = retrievers.build(self.first_stage, corpus, cfg)
        self.doc_text = {docid: doc.text for docid, doc in corpus.docs.items()}
        self.chunk_text = {c.id: c.text for c in corpus.chunks(cfg.chunk_words, cfg.chunk_overlap)}

    def rerank(self, query, ranked, texts, k):
        """ranked: the first stage's ids, best first. Returns k (id, 1 / rank) pairs."""
        top, rest = ranked[: self.candidates], ranked[self.candidates :]
        n = len(top)
        passages = "\n\n".join(f"[{i}] {texts[item][: self.passage_chars]}" for i, item in enumerate(top, 1))
        reply = claude.call(PROMPT.format(n=n, query=query, passages=passages), schema(n), model=self.model, cache_dir=self.cache_dir)
        order = (reply.output or {}).get("order")
        if reply.error or not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
            print(f"WARNING: {reply.error or f'reply was not each of 1 to {n} once: {order}'}; kept the {self.first_stage} order", file=sys.stderr)
        else:
            top = [top[i - 1] for i in order]
        return [(item, 1 / rank) for rank, item in enumerate((top + rest)[:k], 1)]

    def search(self, text, k):
        ranked = [docid for docid, _ in self.first.search(text, max(k, self.candidates))]
        return self.rerank(text, ranked, self.doc_text, k)

    def search_chunks(self, text, k):
        ranked = [chunk_id for chunk_id, _ in self.first.search_chunks(text, max(k, self.candidates))]
        return self.rerank(text, ranked, self.chunk_text, k)


def build(corpus, cfg):
    return Rerank(corpus, cfg)
