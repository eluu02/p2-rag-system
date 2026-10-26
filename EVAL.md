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

- My corpus is the answer pages of Ask CFPB, the Consumer Financial Protection Bureau's question and answer pages on credit, mortgages, debt collection, bank accounts and similar topics. This comes from the pages listed in consumerfinance.gov's sitemap. The corpus contains 672 documents at 1.6 megabytes. The license basis comes from CFPB's privacy page saying: "Information created by the CFPB is in the public domain and you may reproduce, publish, or otherwise use it without the Bureau's permission.", and is found at https://www.consumerfinance.gov/privacy/website-privacy-policy/.

- The first document I was unsure about was a-deposit-was-credited-to-my-account-by-mistake-can-the-bankcred, which contained one word for its answer. This would add noise to the gold set and relevance would be decided by how close the query is to the title, so I decided to remove this document from the corpus. The second document was do-joint-credit-card-accounts-with-my-spouse-affect-my-credit-sc, which contains 30 words and was flagged by INGEST.md as very short. I decided to keep this document after reading it since it has a complete answer unlike the first document.

- A search of all documents found none of the following search terms: "©", "copyright", "all rights reserved". Ask CFPB answers are the Bureau's own guidance, not reports written by a contractor. This corpus falls under the US federal government works (us-gov-public-domain) category for allowed sources.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

- There are a total of 30 queries, 12 written by hand and 18 written by Claude. There are 10 queries per class for an even split, otherwise MRR@10 would be weighted toward whichever class has the most queries. I used three classes, identifier to test an exact term, paraphrase to test meaning without shared words, and mixed to test a combination of identifier and paraphrase. These match the shared set's classes, making the cross-corpus comparison fair.

- A document is relevant to a query if it answers the question the query asks. A document that only mentions the query's term is not relevant. The answer may be anywhere in the document and the document counts even if its title asks something else as long as some passage answers the query.

- To find candidates, Claude built a pool of documents using bm25 and dense top 10, hybrid's top 20, and keyword search for all queries, as well as the page I wrote the query from only for the handwritten queries. I used several sources since a gold set built from one system's results favors that system. I read the full text if the title shares a word with the query that appears in no more than 2% of titles, or if the document is in dense's top 5, then I read a small excerpt if the key term appears in the text but not in the title and screened the rest from their titles only. Additionally, I opened the full page whenever an excerpt or a screened-out title might answer the query, and every label was decided from the full page.

- My labels are binary since there is no second level to grade, resulting in one boundary to apply instead of two as well as being comparable with the shared corpus. Every line in qrels.txt has rel 1. A document without a line in qrels.txt counts as not relevant.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.756 | 0.758 | 0.721 |
| dense | 0.947 | 0.898 | 0.880 |
| hybrid | 0.897 | 0.860 | 0.836 |
| rerank | 0.942 | 0.983 | 0.907 |
| ablation/dense_potion | 0.850 | 0.721 | 0.720 |

30 judged queries; nDCG uses binary labels; a random ranking of the 672 documents would get recall@10 near 0.015.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | identifier (n=10) | paraphrase (n=10) | mixed (n=10) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.350 | 0.917 |
| bm25 | MRR@10 | 1.000 | 0.425 | 0.850 |
| bm25 | nDCG@10 | 0.976 | 0.332 | 0.854 |
| dense | Recall@10 | 1.000 | 0.842 | 1.000 |
| dense | MRR@10 | 1.000 | 0.743 | 0.950 |
| dense | nDCG@10 | 0.981 | 0.709 | 0.952 |
| hybrid | Recall@10 | 1.000 | 0.692 | 1.000 |
| hybrid | MRR@10 | 1.000 | 0.631 | 0.950 |
| hybrid | nDCG@10 | 0.993 | 0.566 | 0.947 |
| rerank | Recall@10 | 1.000 | 0.825 | 1.000 |
| rerank | MRR@10 | 1.000 | 1.000 | 0.950 |
| rerank | nDCG@10 | 0.977 | 0.814 | 0.928 |
| ablation/dense_potion | Recall@10 | 0.900 | 0.650 | 1.000 |
| ablation/dense_potion | MRR@10 | 1.000 | 0.438 | 0.725 |
| ablation/dense_potion | nDCG@10 | 0.915 | 0.447 | 0.797 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=12) | claude (n=18) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 0.750 | 0.759 | -0.009 | [-0.287, +0.269] | not distinguishable |
| bm25 | MRR@10 | 0.792 | 0.736 | +0.056 | [-0.236, +0.333] | not distinguishable |
| bm25 | nDCG@10 | 0.720 | 0.721 | -0.001 | [-0.282, +0.267] | not distinguishable |
| dense | Recall@10 | 0.924 | 0.963 | -0.039 | [-0.139, +0.069] | not distinguishable |
| dense | MRR@10 | 0.958 | 0.857 | +0.101 | [-0.042, +0.257] | not distinguishable |
| dense | nDCG@10 | 0.892 | 0.873 | +0.019 | [-0.102, +0.154] | not distinguishable |
| hybrid | Recall@10 | 0.896 | 0.898 | -0.002 | [-0.213, +0.183] | not distinguishable |
| hybrid | MRR@10 | 0.847 | 0.869 | -0.022 | [-0.272, +0.206] | not distinguishable |
| hybrid | nDCG@10 | 0.830 | 0.839 | -0.010 | [-0.234, +0.192] | not distinguishable |
| rerank | Recall@10 | 0.951 | 0.935 | +0.016 | [-0.083, +0.130] | not distinguishable |
| rerank | MRR@10 | 1.000 | 0.972 | +0.028 | [+0.000, +0.083] | not distinguishable |
| rerank | nDCG@10 | 0.926 | 0.894 | +0.032 | [-0.063, +0.131] | not distinguishable |
| ablation/dense_potion | Recall@10 | 0.806 | 0.880 | -0.074 | [-0.297, +0.148] | not distinguishable |
| ablation/dense_potion | MRR@10 | 0.812 | 0.660 | +0.152 | [-0.114, +0.398] | not distinguishable |
| ablation/dense_potion | nDCG@10 | 0.732 | 0.712 | +0.020 | [-0.207, +0.241] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | -0.204 | -0.174 | -0.030 | [-0.278, +0.222] | not distinguishable |
| MRR@10 | -0.121 | -0.167 | +0.045 | [-0.159, +0.268] | not distinguishable |
| nDCG@10 | -0.152 | -0.172 | +0.020 | [-0.193, +0.232] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.70 (12 queries), claude 0.69 (18 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 12 hand and 18 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | +0.192 | [+0.081, +0.317] | 0.178 | dense higher |
| dense minus bm25 | MRR@10 | +0.139 | [+0.051, +0.245] | 0.146 | dense higher |
| dense minus bm25 | nDCG@10 | +0.160 | [+0.065, +0.267] | 0.151 | dense higher |
| hybrid minus bm25 | Recall@10 | +0.142 | [+0.044, +0.258] | 0.158 | hybrid higher |
| hybrid minus bm25 | MRR@10 | +0.102 | [+0.026, +0.197] | 0.127 | hybrid higher |
| hybrid minus bm25 | nDCG@10 | +0.115 | [+0.045, +0.198] | 0.114 | hybrid higher |
| hybrid minus dense | Recall@10 | -0.050 | [-0.139, +0.022] | 0.121 | not distinguishable |
| hybrid minus dense | MRR@10 | -0.037 | [-0.142, +0.058] | 0.145 | not distinguishable |
| hybrid minus dense | nDCG@10 | -0.045 | [-0.121, +0.021] | 0.103 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.186 | [+0.072, +0.314] | 0.182 | rerank higher |
| rerank minus bm25 | MRR@10 | +0.225 | [+0.091, +0.375] | 0.213 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.186 | [+0.070, +0.313] | 0.181 | rerank higher |
| rerank minus dense | Recall@10 | -0.006 | [-0.050, +0.033] | 0.057 | not distinguishable |
| rerank minus dense | MRR@10 | +0.086 | [+0.000, +0.182] | 0.135 | not distinguishable |
| rerank minus dense | nDCG@10 | +0.026 | [-0.018, +0.073] | 0.067 | not distinguishable |
| rerank minus hybrid | Recall@10 | +0.044 | [-0.011, +0.122] | 0.107 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.123 | [+0.011, +0.251] | 0.177 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.071 | [-0.013, +0.170] | 0.136 | not distinguishable |
| ablation/dense_potion minus bm25 | Recall@10 | +0.094 | [-0.033, +0.233] | 0.197 | not distinguishable |
| ablation/dense_potion minus bm25 | MRR@10 | -0.037 | [-0.150, +0.081] | 0.167 | not distinguishable |
| ablation/dense_potion minus bm25 | nDCG@10 | -0.001 | [-0.111, +0.117] | 0.168 | not distinguishable |
| ablation/dense_potion minus dense | Recall@10 | -0.097 | [-0.203, -0.008] | 0.143 | dense higher |
| ablation/dense_potion minus dense | MRR@10 | -0.177 | [-0.278, -0.083] | 0.142 | dense higher |
| ablation/dense_potion minus dense | nDCG@10 | -0.161 | [-0.252, -0.077] | 0.127 | dense higher |
| ablation/dense_potion minus hybrid | Recall@10 | -0.047 | [-0.111, +0.006] | 0.084 | not distinguishable |
| ablation/dense_potion minus hybrid | MRR@10 | -0.139 | [-0.264, -0.017] | 0.180 | hybrid higher |
| ablation/dense_potion minus hybrid | nDCG@10 | -0.116 | [-0.201, -0.031] | 0.124 | hybrid higher |
| ablation/dense_potion minus rerank | Recall@10 | -0.092 | [-0.189, -0.011] | 0.132 | rerank higher |
| ablation/dense_potion minus rerank | MRR@10 | -0.262 | [-0.392, -0.139] | 0.189 | rerank higher |
| ablation/dense_potion minus rerank | nDCG@10 | -0.187 | [-0.294, -0.089] | 0.150 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

- At 30 queries, the MDDs run from 0.057 (rerank minus dense, Recall@10) to 0.213 (rerank minus bm25, MRR@10), for example, hybrid minus dense on MRR@10 is -0.037 with an MDD of 0.145, so a true gap of about 0.14 could go undetected. Every system minus bm25 is distinguishable and beats bm25 on every metric, for example, dense minus bm25 on MRR@10 has interval [+0.051, +0.245] with a mean difference of +0.139. Among dense, hybrid, and rerank, only rerank minus hybrid on MRR@10 is distinguishable, for example, rerank minus hybrid has interval [+0.011, +0.251] with a mean difference of +0.123.

- Every hand minus claude interval includes 0 so no system differs distinguishably. bm25 trails dense in both groups (-0.121 claude, -0.167 hand) and the interval [-0.159, +0.268] with a mean difference of +0.045 isn't distinguishable. This is consistent with the overlap of shared terms from the query to document where hand got a score of 0.70 and claude 0.69. The similar results are likely due to the shared class split and the shared source page method for writing queries. With 12 hand written and 18 claude queries, the unpaired intervals are wide, so a real difference could be hidden.

- My prediction on dense beating bm25 and bm25 being the worst system held but not for the reason of a lack of identifiers since bm25 scored 1.000 on identifier queries and lost on paraphrase (0.425). My prediction on rerank being the best system partially held since the rerank minus dense on MRR@10 interval is [+0.000, +0.182] which is not distinguishable, but was the best in point estimates yet not enough to separate from dense. My hedge prediction that rerank could fall below dense is neither confirmed nor ruled out.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.
- I expect dense with potion to have a lower MRR@10 compared to dense with bge-small on my corpus. Due to the existing ceiling for dense, potion could only improve on paraphrase, and leaves potential for loss on identifier and mixed queries. Since potion averages fixed word vectors, losing the context a reworded question depends on, it will likely drop overall MRR@10.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/dense_potion minus bm25 | Recall@10 | +0.094 | [-0.033, +0.233] | 0.197 | not distinguishable |
| ablation/dense_potion minus bm25 | MRR@10 | -0.037 | [-0.150, +0.081] | 0.167 | not distinguishable |
| ablation/dense_potion minus bm25 | nDCG@10 | -0.001 | [-0.111, +0.117] | 0.168 | not distinguishable |
| ablation/dense_potion minus dense | Recall@10 | -0.097 | [-0.203, -0.008] | 0.143 | dense higher |
| ablation/dense_potion minus dense | MRR@10 | -0.177 | [-0.278, -0.083] | 0.142 | dense higher |
| ablation/dense_potion minus dense | nDCG@10 | -0.161 | [-0.252, -0.077] | 0.127 | dense higher |
| ablation/dense_potion minus hybrid | Recall@10 | -0.047 | [-0.111, +0.006] | 0.084 | not distinguishable |
| ablation/dense_potion minus hybrid | MRR@10 | -0.139 | [-0.264, -0.017] | 0.180 | hybrid higher |
| ablation/dense_potion minus hybrid | nDCG@10 | -0.116 | [-0.201, -0.031] | 0.124 | hybrid higher |
| ablation/dense_potion minus rerank | Recall@10 | -0.092 | [-0.189, -0.011] | 0.132 | rerank higher |
| ablation/dense_potion minus rerank | MRR@10 | -0.262 | [-0.392, -0.139] | 0.189 | rerank higher |
| ablation/dense_potion minus rerank | nDCG@10 | -0.187 | [-0.294, -0.089] | 0.150 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/dense_potion against dense (BASE = "dense" in p2/retrievers/dense_potion.py): it helped 0 queries, hurt 10 and left 20 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_potion RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| o21 | paraphrase | claude | 1.000 | 0.200 | -0.800 | hurt |
| o10 | mixed | hand | 1.000 | 0.250 | -0.750 | hurt |
| o24 | paraphrase | claude | 1.000 | 0.250 | -0.750 | hurt |
| o07 | paraphrase | hand | 0.500 | 0.000 | -0.500 | hurt |
| o09 | mixed | hand | 1.000 | 0.500 | -0.500 | hurt |
| o23 | paraphrase | claude | 1.000 | 0.500 | -0.500 | hurt |
| o28 | mixed | claude | 1.000 | 0.500 | -0.500 | hurt |
| o29 | mixed | claude | 1.000 | 0.500 | -0.500 | hurt |
| o19 | paraphrase | claude | 0.500 | 0.100 | -0.400 | hurt |
| o22 | paraphrase | claude | 0.100 | 0.000 | -0.100 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

- I changed the model that dense uses from bge-small to potion. This performed worse compared to bge-small on all three metrics, resulting in 10 queries hurt by this change. Paraphrase took the most losses at 6 of 10 and mixed lost on 4 of 10. Since all intervals exclude 0 (MRR@10: -0.177 [-0.278, -0.083], Recall@10: -0.097 [-0.203, -0.008], nDCG@10: -0.161 [-0.252, -0.077]), the drop is distinguishable on all three metrics. On MRR@10, the drop of 0.177 is also larger than its MDD of 0.142, so the gold set was big enough to see this drop. My hypothesis of lower overall MRR@10 than dense with bge-small is supported.

- My change does explain the change in query ranking as potion kept a relevant page in the top 5 but pushed it down to rank 4 or 5 for the three queries at the top of the list by matching the query's words without its meaning. For example, potion's top pages for o21 all share "card" but aren't about who is responsible for fraudulent charges.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| o22 | The relevant page at rank 1, then 9 unlabeled pages |"How long will it take before I'll face foreclosure...?" (rank 1). Missing: "How does foreclosure work?" and "What happens after I complete an application to determine my options to avoid foreclosure?" both outside hybrid's top 20 | Dense found one missing page and fusion with bm25 dropped it outside of rerank's candidates, and the other was missed by every system | Let rerank see more candidates or rerank dense's top 20 instead of hybrid. For the one true miss, I would try a stronger embedding model. To know it works, the first missing page enters the candidates and the true miss moves into the top 20 |
| o19 | The relevant page at rank 1, then 9 unlabeled pages | "I wrote a check, but it was stolen and cashed by the thief..." (rank 1). Missing: "I wrote a check and someone forged the endorsement and cashed the check..." outside hybrid's top 20 | Dense found the missing page and fusion with bm25 dropped it just outside of rerank's candidates | Let rerank see more candidates or rerank dense's top 20 instead of hybrid. To know it works, the missing page enters the candidates and rerank places it in the top 10 |
| o06 | The relevant pages at ranks 1 and 5, then 8 unlabeled pages | "Can a debt collector contact me through social media?" (rank 1) and "What is an unfair, deceptive or abusive practice by a debt collector (rank 5). Missing: "What laws limit what debt collectors can say or do?", which was hybrid rank 2 | The missing page was in hybrid's top 20, but since the first mention of key terms appears after 600 characters, rerank pushed it out of the top 10 | Raise the character window for rerank or send Claude each page's best matching chunk instead of its opening. To know it works, rerunning rerank brings the missing page into the top 10 |
| o05 | Two relevant pages at ranks 1 and 2, then 8 unlabeled pages | "Does requesting my credit report hurt my credit score?" (rank 1), "What is a credit inquiry?" (rank 2), and "What happens when a mortgage lender checks my credit?" (rank 8). Missing: "Does my credit score affect my ability to get a mortgage loan or the mortgage rate I pay?", which was hybrid rank 6 | The missing page was in hybrid's top 20, but since the first mention of key terms appears after 600 characters, rerank pushed it out of the top 10 | Raise the character window for rerank or send Claude each page's best matching chunk instead of its opening. To know it works, rerunning rerank brings the missing page into the top 10 |
| o28 | "What happens to my federal student loans if my income drops?" (rank 1, unlabeled), then the relevant pages at ranks 2 and 5, then 7 other unlabeled pages | "What are income-driven repayment (IDR) plans, and how do I qualify?" (rank 2) and "What is an Extended Repayment Plan for federal student loans?" (rank 5) | Label error, the page was read and rejected but answers the query and correcting it would raise rerank's MRR@10 by about 0.017 | Rejudge the candidate pool and check other queries for the same inconsistency, including queries where hybrid or dense failed so the correction isn't one sided |

- Across these failures, two are in the first stage, mostly from fusion, two in the reranker's 600 character window, and one in the gold set. Most failures were in paraphrase queries at 4 of 5, and no identifier query failed. 4 of 5 already have a relevant page at rank 1, so the failures are mostly additional relevant pages missing or pushed down in ranks.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

- The winner didn't change between the corpora with rerank winning on both corpora (rerank's MRR@10: 0.800 shared, 0.983 own). On the shared corpus, rerank is distinguishably above all other systems whereas on my corpus, rerank is distinguishable from hybrid and bm25, but not dense (rerank minus dense: +0.086 [+0.000, +0.182]).

- The differences between the two corpora are as follows. First, fusion pulled down dense's finds shown query by query on my corpus. For example, on o19, dense ranked the missing page 5th, bm25 140th, and hybrid 21st so a page dense finds can be fused out of rerank's candidates. On paraphrase queries, hybrid trails dense on both corpora (0.152 against 0.714 on shared, 0.631 against 0.743 on own). Second, dense's strength comes from context which is why dense ties rerank on my corpus. Swapping bge-small for potion, which loses context, dropped MRR@10 by -0.177 [-0.278, -0.083], with the losses mostly in paraphrase queries. This was tested on my corpus only. Lastly, my queries' overlap is about 0.70 against the shared practice set's 0.95/0.11/0.51 by class, with the biggest gap on paraphrase. This fits bm25 scoring much higher on my own corpus (0.758 against 0.507 overall and 0.425 against 0.000 on paraphrase). The query sets differ in other ways, so overlap can't be isolated as the cause. The median document length is 68 words on the shared corpus against 274 on mine, which is a difference I measured but never varied, so its effect is a guess.

- The sample sizes can't support a cross-corpus interval since the interval compares systems within a corpus. The two rerank minus hybrid intervals, [+0.164, +0.504] and [+0.011, +0.251] overlap so I can't claim the gain changed size. The shared set's MDDs range from 0.166 to 0.415 so not distinguishable results could hide large gaps and mine ranges from 0.057 to 0.213 which would show smaller gaps. The per-class rows have no intervals, so class patterns like dense's 0.333 on shared identifiers are descriptive only. Finally, document length, identifier type, and query style all change together between the two corpora so no explanation can be separated from the others.

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
| traces/answers-rerank.r1.jsonl | rerank | 12 | 24 | 0 | 159,648 | 4,339 | 83.5 | 13,304 | 362 | 7.0 |
| traces/answers-rerank.r2.jsonl | rerank | 12 | 24 | 0 | 141,833 | 4,006 | 75.9 | 11,819 | 334 | 6.3 |
| traces/answers-rerank.r3.jsonl | rerank | 12 | 24 | 0 | 163,968 | 4,560 | 85.1 | 13,664 | 380 | 7.1 |
| traces/own-own-rerank.jsonl | rerank | 30 | 30 | 2 | 235,682 | 2,730 | 78.2 | 7,856 | 91 | 2.6 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 20 | 183,301 | 2,040 | 56.7 | 9,165 | 102 | 2.8 |
| traces/shared-practice-rerank.r1.jsonl | rerank | 20 | 20 | 0 | 166,257 | 1,932 | 55.2 | 8,313 | 97 | 2.8 |
| traces/shared-practice-rerank.r2.jsonl | rerank | 20 | 20 | 0 | 142,324 | 2,047 | 54.8 | 7,116 | 102 | 2.7 |
| traces/shared-practice-rerank.r3.jsonl | rerank | 20 | 20 | 0 | 155,448 | 1,985 | 54.3 | 7,772 | 99 | 2.7 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 40 | 355,224 | 4,290 | 111.3 | 8,881 | 107 | 2.8 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.293 | [-0.533, -0.043] | 9,165 | 2.8 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.237 | [-0.408, -0.083] | 9,165 | 2.8 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.329 | [-0.504, -0.164] | 9,165 | 2.8 | rerank higher |
| own: bm25 minus rerank | 30 | -0.225 | [-0.375, -0.091] | 7,856 | 2.6 | rerank higher |
| own: dense minus rerank | 30 | -0.086 | [-0.182, +0.000] | 7,856 | 2.6 | not distinguishable |
| own: hybrid minus rerank | 30 | -0.123 | [-0.251, -0.011] | 7,856 | 2.6 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Every two answers files on the same questions, the one with fewer input tokens per question first:

| Cheaper minus dearer | Questions | Passing share difference | 95% interval | Input tokens saved per question | Seconds saved per question | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared: hybrid minus rerank | 12 | -0.083 | [-0.250, +0.000] | 9,570 | 3.8 | not distinguishable |

A question passes when its `p2 verify` line is a PASS: every quote is in a chunk that was retrieved, and the question is declined exactly when it should be.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-dense_potion.jsonl | dense_potion | 30 | 0.03 | 0.9 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 30 | 0.02 | 0.8 |
| traces/retrieval/own-own-dense.jsonl | dense | 30 | 0.16 | 5.3 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 30 | 0.23 | 7.5 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.04 | 2.0 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.17 | 8.4 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.22 | 11.1 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.08 | 2.0 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.27 | 6.7 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.44 | 11.0 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.
- Rider

- The rider has two parts, PREREG.md filled in before the first judgment, and repeats where rerank was rerun 3 times on the shared practice queries, and the 12 shared questions answered 3 times, each with its trace in traces/ as well as runs in runs/shared/rerank.practice.r1 to .r3.trec and answers in answers/shared/rerank.r1 to .r3.json.

- Tables p2 score wrote: repeats is the repeats in section 9, own-pairs is the preregistered test in section 4.

- The intervals let me claim rerank's gain over hybrid on the shared practice queries survives run-to-run variation with a range of 0.000 against +0.329 for the repeats, but doesn't let me claim that answer rates are high since true rates can be as low as about 68% and 51%, nor does it cover my own corpus. It also lets me claim rerank minus hybrid with interval +0.123 [+0.011, +0.251] falls in row 1 in section 4 of PREREG.md but doesn't let me claim that the gain reaches Δ or that my near-duplicate mechanism explains it.

- One thing I'd do next is growing the gold set toward the original 60. An MDD at or below 0.15 so the interval can tell whether the gain clears Δ would show it worked.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
Repeated runs of rerank on shared/practice:

| Run | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| rerank.r1 | 0.758 | 0.800 | 0.763 |
| rerank.r2 | 0.758 | 0.800 | 0.769 |
| rerank.r3 | 0.758 | 0.800 | 0.763 |
| range (max minus min) | 0.000 | 0.000 | 0.006 |

| Comparison | Metric | Mean difference | 95% interval | Reading |
| --- | --- | ---: | ---: | --- |
| rerank.r1 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r1 higher |
| rerank.r2 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r2 higher |
| rerank.r3 minus hybrid | Recall@10 | +0.167 | [+0.058, +0.292] | rerank.r3 higher |
| rerank.r1 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r1 higher |
| rerank.r2 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r2 higher |
| rerank.r3 minus hybrid | MRR@10 | +0.329 | [+0.164, +0.504] | rerank.r3 higher |
| rerank.r1 minus hybrid | nDCG@10 | +0.320 | [+0.195, +0.448] | rerank.r1 higher |
| rerank.r2 minus hybrid | nDCG@10 | +0.326 | [+0.199, +0.454] | rerank.r2 higher |
| rerank.r3 minus hybrid | nDCG@10 | +0.320 | [+0.195, +0.448] | rerank.r3 higher |

Repeated answers shared/rerank:

| File | Verified (in) | 95% interval | Declined (out) | 95% interval |
| --- | ---: | ---: | ---: | ---: |
| rerank.r1 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r2 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| rerank.r3 | 8 of 8 (100%) | [0.676, 1.000] | 4 of 4 (100%) | [0.510, 1.000] |
| range (max minus min) | 0.000 |  | 0.000 |  |

Each repeat answers the same questions, so the repeats are not independent trials and their counts are not pooled into one interval.
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

- The reranker's gain over its first stage survived. Rerank was rerun 3 times on the 20 shared practice queries with fresh Claude replies where the MRR@10 was 0.800 in every repeat, so the range is 0.000 against a gain of +0.329. Each repeat minus hybrid is +0.329 [+0.164, +0.504], so the gain is distinguishable in every repeat.  

- From comparing the four run files, the three repeats and the original run, 0 of 20 queries had the same top 10 in every run. 17 of 20 queries kept the same rank 1. Since MRR@10 only depends on the rank of the first relevant page and that rank never changed, reorderings below it didn't move the score.

- Every repeat verified 8 of 8 and declined 4 of 4. The Wilson interval for verified is [0.676, 1.000] and declined is [0.510, 1.000]. A perfect score on a few questions still allows a true rate as low as about 68% for verified and 51% for declined since the intervals are wide because n is small. The repeats don't narrow the intervals since they answer the same 12 questions, but adding more questions would.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

- I mostly followed the plan with one deviation. The hypothesis (rerank > hybrid), the metric (MRR@10), Δ = 0.15, and the default decision rule all stayed the same. The deviation is changing the number of queries in the gold set from 60 to 30 through the amendment in PREREG.md section 6. This was done before any own-corpus run or score existed so it couldn't have been influenced by the result. With this change, the MDD rose from about 0.14 to 0.177, above delta.

- The resulting interval for rerank minus hybrid on MRR@10 is +0.123 [+0.011, +0.251]. This interval falls into row 1 of section 4 in PREREG.md (entirely above zero in the predicted direction), whose verdict is supported. The full results can be seen in PREREG.md section 5.

- Since Δ = 0.15 is inside the interval, the gain is distinguishable from zero, but may be smaller than what justifies rerank's cost. In the failure analysis, a relevant page was found with no line in qrels.txt. Correcting this would raise rerank's o28 RR from 0.5 to 1.0, moving the result to about +0.140 which is still in row 1 of section 4 in PREREG.md. I kept the gold set as is since I only looked for errors in rerank's failures and changing judgements after scoring would bias the test toward rerank. Additionally, my hypothesis said rerank wins by separating near-duplicate questions, but the failure analysis found no clear near-duplicate case. The gain is concentrated in 6 of 30 queries (5 up, 1 down), consisting of mostly paraphrases, so this suggests rerank fixes paraphrase queries that hybrid ranks too low.
