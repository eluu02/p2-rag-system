# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

- For stage 2, I chose the Consumer Financial Protection Bureau (CFPB) question and answers pages from the Ask CFPB section. I chose this set of documents as I am also taking an Accounting & Finance course where I discovered financial documents and help pages are generally difficult to navigate and dense which makes it difficult to read or search for specific articles. This document set contains about 673 documents, at an estimated 314,000 tokens which is comfortably within the recommended token and document limit.
- Between bm25 and dense, dense will likely outperform bm25 due to the lack of identifiers in the corpus and embedding models are largely trained on question and answer pairs so this document set should be close to that training data. Bm25 will likely be the worst of all systems unless the gold set is written using the exact vocabulary seen in a document. Since rerank only reorders the top 20 from hybrid's ranking, it should be the best system based on previous labs and practice runs, but it's possible for rerank to underperform dense since hybrid is fusing a weak system (bm25) with a strong one (dense).

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

- One document (A deposit was credited to my account by mistake. Can the bank/credit union take it back?) exists where the CFPB answer is a single word, "Yes". The options were to remove this document or keep it in the corpus.

- I chose to remove this document so that every document has a real, readable answer. Removing this would also never allow a single "Yes" to be cited as evidence. This leaves the corpus with 672 documents instead of 673. The downside is that one real answer leaves the corpus so a user asking exactly this question would only get related pages. If I had kept this document, relevance would be decided by how close the query is to the title. This would add noise to the gold set and similar queries could be judged differently since closeness is a spectrum while labels are binary.

- The alternative was rejected without measuring since it was only one document out of 673 and it was removed before any query, judgement, or run existed so nothing had to be redone.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

TODO: your answer to prompt 3.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

TODO: your answer to prompt 4.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

TODO: your answer to prompt 5.
