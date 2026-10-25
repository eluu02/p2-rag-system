# Pre-registration (598E)

This file is for 598E students; it is the second half of the 598E rider, and 498E students can ignore it or delete it.

A pre-registration is a claim you write down, with the test that will judge it, before you can see the answer.
Its value is that the claim can be wrong in a way anyone can check, and that you cannot adjust it afterwards to fit the numbers.
A well-powered result that says "no effect as large as the one I cared about" scores as well as a confirmation, so you have no reason to bend the claim.

**Git history is how I will know the order.**
Commit this file, filled in through section 4, before the first commit that puts a judgment line into `eval/own/qrels.txt` (or any other file under `eval/own/`).
`uv run p2 check` reads `git log` to find the first commit in which sections 1 to 4 have no TODO marker left and some words of yours in each, and confirms that it comes before your first judgment; a copy that was filled in afterwards fails.
Right after that commit, `p2 check` names it and waits for your first judgment; it asks for section 5 separately, once you have scored your own corpus.
You may ingest your corpus and write queries first, but not the relevance judgments.
After that first commit, do not edit sections 1 to 4, because `p2 check` compares them with the commit where you filled them in.
If something must change, add a dated entry in section 6 and leave the original as it was.

You need your stage 1 scores for section 3, so score the shared corpus first.

---

## 1. Hypothesis

One sentence, about your own corpus, naming two of your systems and a direction.
For example: "On my corpus of Kubernetes documentation, `rerank` has a higher MRR@10 than `hybrid`, because the queries are paraphrases that a first-stage fusion ranks too low."
It should be something you could be wrong about.

- On my CFPB corpus, rerank has a higher MRR@10 compared to hybrid, since the corpus contains many near-duplicate questions, the RRF scores are similar which gives hybrid little evidence to distinguish them, while rerank using Claude can separate questions by intent. 

---

## 2. The smallest effect that matters

Name one metric, MRR@10 or nDCG@10, and choose it now so you cannot pick the better one afterwards.
Then say how large a difference between the two systems would matter to a person using the search, and why that size.
A difference of 0.02 is usually not worth a reranker's cost in time and tokens.
In this course, choose a Δ of at least 0.15 unless you argue for a larger one, because a smaller gap takes more queries than one project can judge.
Call your number Δ (delta).

- I choose MRR@10 with a delta of 0.15. Since rerank adds time and about 9,000 input tokens per query, a gain smaller than 0.15 wouldn't be noticeable enough to justify the extra wait time. Additionally, on this corpus, a wrong page at rank 1 is often a similar question that looks correct. Fixing this on about 30% of the questions should be noticeable by a user.

---

## 3. How many queries you need

The size of the gold set follows from three numbers: how large a difference you want to detect (Δ), how variable the per-query differences are (sd), and the usual choices of a 5% false-alarm rate and 80% power.

```
n = ((1.96 + 0.84) * sd / Δ)^2
```

Here sd is the standard deviation of the per-query differences between your two systems, which `results/results.json` holds for the shared practice queries.
Compute it from your stage 1 runs for the same two systems, or the nearest pair you have, and say which pair you used.
With only 20 practice queries the sd is itself noisy, so be generous and round up.

Some numbers to calibrate against.
At sd 0.3 and Δ 0.10 the formula gives about 71 queries, and with the t distribution's small-sample correction it is a few more, about 73.
At sd 0.3, a gold set of 30 queries can only detect a difference of about 0.15, which is why 30 queries cannot support a claim about a gap of 0.10.
The spreads you will measure on the shared practice queries are mostly larger than 0.3: from about 0.31 for `hybrid` against `bm25` to about 0.66 for `dense` against `bm25`.
For `rerank` against `hybrid` the sd is about 0.39, so a Δ of 0.10 needs about 120 queries, 0.15 about 55, and 0.20 about 31.
So the course's Δ of 0.15 means about 55 queries for that pair; at an sd of 0.66 it would mean about 150, so compare a pair whose spread you can afford.
Choose Δ and the size of your gold set together: the smallest effect that matters to a user, and a number of queries you can write and judge in the time you have.
If the two do not meet, say which one you gave ground on and why.

After you score the own corpus, the minimum detectable difference that `uv run p2 score` prints for your two systems is this same calculation run the other way.
It should come out at or below your Δ.
If it does not, your queries varied more than your stage 1 sd suggested, and you will say so in the outcome.

- My sd is 0.394 coming from rerank versus hybrid on MRR@10 on the 20 shared practice queries. n = ((1.96 + 0.84) × 0.394 / 0.15)² ≈ 54. Rounding up from this, I will write 60 queries.

---

## 4. The test, and what each result will mean

The test is the paired 95% interval of the mean difference between your two systems on your own gold set, from the `own-pairs` table that `uv run p2 score` writes in `EVAL.md`.
Write the rule now.
This is the default rule, and you can tighten it, but do not loosen it after you see your numbers.

| The interval is | I will say |
|---|---|
| entirely above zero in the direction I predicted | supported: the difference is distinguishable from zero |
| entirely on the other side of zero | contradicted: the opposite of my hypothesis holds on this gold set |
| around zero, with both ends inside plus or minus Δ | well-powered null: a difference as large as Δ is ruled out |
| around zero, with an end beyond plus or minus Δ | inconclusive: the gold set could not settle it, and I say so |

- I confirm the default rule. The two systems are rerank and hybrid using the metric MRR@10, and positive means rerank outperforms hybrid.

---

## 5. Outcome (write this after the fact)

What was the interval?
Which row of the table in section 4 is it?
Did your gold set reach the size section 3 asked for, and what was the minimum detectable difference that `uv run p2 score` printed?
What would you do next, and what would you want a reader to take from this?

- The paired bootstrap interval, using rerank minus hybrid on MRR@10, has a 95% interval of [+0.011, +0.251] and a mean difference of +0.123. With this interval, the true gain could be well below or well above the delta of 0.15. The interval falls into row 1 in section 4 which is entirely above zero in the direction I predicted. 
- Section 3 asked for 60 queries which the amendment in section 6 lowers to 30 and the gold set reached the size of 30. The MDD for MRR@10 is 0.177, above the delta of 0.15 due to the amended 30 queries instead of the 60 intended. 
- Next, I would add more queries to bring the MDD down to delta which was the section 3 target before the amendment. The reader should notice that on this gold set, rerank's MRR@10 is reliably higher than hybrid's since the interval excludes 0, and the gain is concentrated since only 6 of 30 queries changed with 5 up and 1 down, meaning rerank fixes some paraphrase queries that hybrid ranks too low instead of rerank being better everywhere.

---

## 6. Amendments

Dated entries only, one per change, each saying what changed and why.
Leave this section as it is if nothing changed.

- Date: 2026-10-24. Changed gold set target from 60 queries to 30, 12 by hand and 18 from Claude, with 10 per class. This was done as 60 queries would entail around 15 hours of reading documents for qrels.txt against the project deadline and no own-corpus run or score existed yet. The minimum detectable difference rises from 0.14 to about 0.20, or 0.21 with the t correction. A true gain of 0.15 is now less likely to be detected. Δ = 0.15, the hypothesis in section 1 and the decision rule in section 4 are unchanged.
