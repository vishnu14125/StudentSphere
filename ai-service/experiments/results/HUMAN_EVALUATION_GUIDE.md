# Human Evaluation Guide

For every candidate document, compare the QUERY with the actual QUESTION + ANSWER in `human_eval_candidates.json`.

Assign the relevance value in `evaluation_queries_v3.json` using this exact scale:
- 2 — Highly relevant: directly answers the query
- 1 — Partially relevant: useful but only partially answers it
- 0 — Not relevant: does not answer the query

**Important Rules for Judges:**
- Do not judge based only on category.
- Do not judge based only on similarity score.
- Judge the actual information contained in the answer.
