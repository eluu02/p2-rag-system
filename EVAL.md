# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

- dense: The embedding model used is bge-small-en-v1.5 seen in lab 12 and documents were chunked by splitting them into 300 word chunks with neighbors sharing 50 words for documents longer than 300 words. The difference from lab 12 is chunks are 300 word windows and each document takes its best chunk's score and only new or modified chunks are re-encoded.

- hybrid: Each query asks bm25 and dense to rank 2,484 documents each, then scores each document with reciprocal rank fusion, then ranks them based on their scores. The difference from lab 13 is the bm25 and dense indexes are each built once per run.

- rerank: Takes hybrid's top 20 documents and reorders them using Claude (Sonnet). The reranker saw 20 candidates per query with each candidate shown to Claude as its first 600 characters and the difference from lab 13 is using hybrid for the first stage instead of a run file as well as the schema limiting each number from 1 to 20.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.592 | 0.471 | 0.443 |
| rerank | 0.758 | 0.800 | 0.765 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.405 | 0.917 |
| hybrid | MRR@10 | 0.514 | 0.152 | 0.792 |
| hybrid | nDCG@10 | 0.397 | 0.202 | 0.779 |
| rerank | Recall@10 | 0.714 | 0.595 | 1.000 |
| rerank | MRR@10 | 0.714 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.714 | 0.626 | 0.987 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.033 | [-0.250, +0.192] | 0.324 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.037 | [-0.178, +0.083] | 0.192 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.075 | [-0.238, +0.075] | 0.228 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.033 | [-0.125, +0.192] | 0.231 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.092 | [-0.306, +0.109] | 0.301 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.036 | [-0.200, +0.113] | 0.227 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.100, +0.358] | 0.340 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.293 | [+0.043, +0.533] | 0.353 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.247 | [+0.019, +0.463] | 0.323 | rerank higher |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.367] | 0.224 | rerank higher |
| rerank minus dense | MRR@10 | +0.237 | [+0.083, +0.408] | 0.239 | rerank higher |
| rerank minus dense | nDCG@10 | +0.285 | [+0.146, +0.439] | 0.214 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | 0.166 | rerank higher |
| rerank minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | 0.247 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.322 | [+0.196, +0.451] | 0.184 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

- A difference is distinguishable when its 95% interval excludes 0. The distinguishable comparisons consist of the following: rerank minus hybrid on all metrics, rerank minus dense on all metrics, and rerank minus bm25 on MRR@10 and nDCG@10. The nondistinguishable comparisons consist of the following: rerank minus bm25 on Recall@10, dense minus bm25 on all metrics, hybrid minus bm25 on all metrics, and hybrid minus dense on all metrics.

- The MDD at 20 queries ranges from 0.166 (rerank minus hybrid, Recall@10) to 0.415 (dense minus bm25, Recall@10). Smaller gaps have a much lower chance of detection and are invisible to this gold set but not absent. Here, on hybrid minus dense with MRR@10, a gap of .301 has 80% chance of detection, 0.15 has about 28%, 0.10 has about 15%, and 0.05 has about 7%.

- The main supported claim from lab 13 is that reranking only improves on its first stage which is supported in rerank minus hybrid having a gap of +0.329 with an interval of [+0.164, +0.504] and no practice query got worse. The main claim left open from lab 12 is that fusion helps a weaker retriever and hurts a strong retriever since all six hybrid intervals include 0. On 7 paraphrase queries with no interval, hybrid (0.152) fell below the stronger retriever, dense (0.714), but rose above the weaker retriever, bm25 (0.000), on MRR@10. This is consistent with the claim from the lab but left open since no interval excludes 0.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| hybrid | hybrid | 7 of 8 (88%) | [0.529, 0.978] | 1 of 8 (12%) | 4 of 4 (100%) | [0.510, 1.000] | 11 of 11 |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 12 of 12 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

- For the 12 shared questions, I used rerank since it beat hybrid with an interval excluding 0 on the practice queries. Here, it recovered one chunk that hybrid missed, but since the intervals overlap almost entirely, it is difficult to determine which system is better in this case. The missed question was a06 since document 62.101 wasn't in the top 5. For prompts/answer.txt, no changes were made so both runs used lab 13's prompt and the only difference was the retrieval system. The verified share moved due to a06's retrieval with rerank which verified 8 of 8 against hybrid's 7 of 8. The decline share didn't move since both systems declined all 4 unanswerable questions.

- a01: The quote partially supports the claim since it supports the time frame to contact MSHA but does not include applicable accidents and the mention of death as stated in the claim. The chunk directly supports the claim with the list of accidents in which MSHA must be contacted with the death of an individual as the first item.
- a02: The quote partially supports the claim since it supports the 80%, but it does not mention methane or the increase in percentage when methane is present. The chunk directly supports the claim by stating that an increase occurs when methane is present by 0.4% for each 0.1% of methane. The support for the claim is just outside of what Claude quoted.
- a06: The quote partially supports the claim since it does answer the question, but does not support the 8-hour average part. The chunk also partially supports the claim as it answers the question but does not mention an 8-hour average.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

TODO: describe your corpus and its license basis.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

TODO: describe your gold set and your relevance rule.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
_No scored runs here yet: run `uv run p2 run --corpus own --system bm25` (or `--all`), then `uv run p2 score`._
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

TODO: write what your own-corpus intervals let you claim.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

<!-- p2:begin own-ablation -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
_No ablation runs yet: `uv run p2 run --corpus own --system NAME --ablation` writes one to runs/own/ablation/, then `uv run p2 score` fills this table._
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

TODO: write the ablation: the one change, the hypothesis, the result and the claim.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|

TODO: add one row for each failure you analyzed, and write two or three sentences on the pattern you see across them.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

TODO: write the cross-corpus comparison.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-hybrid.jsonl | hybrid | 12 | 12 | 0 | 64,240 | 3,202 | 51.1 | 5,353 | 267 | 4.3 |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 179,085 | 4,225 | 96.2 | 14,924 | 352 | 8.0 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 183,301 | 2,040 | 56.7 | 9,165 | 102 | 2.8 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 355,224 | 4,290 | 111.3 | 8,881 | 107 | 2.8 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 9,165 | 2.8 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 9,165 | 2.8 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 9,165 | 2.8 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Every two answers files on the same questions, the one with fewer input tokens per question first:

| Cheaper minus dearer | Questions | Passing share difference | 95% interval | Input tokens saved per question | Seconds saved per question | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared: hybrid minus rerank | 12 | -0.083 | [-0.250, +0.000] | 9,570 | 3.8 | not distinguishable |

A question passes when its `p2 verify` line is a PASS: every quote is in a chunk that was retrieved, and the question is declined exactly when it should be.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.04 | 1.9 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.16 | 8.2 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.22 | 10.9 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.08 | 1.9 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.32 | 7.9 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.43 | 10.8 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
