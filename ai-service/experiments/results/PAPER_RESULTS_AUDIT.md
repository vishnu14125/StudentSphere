# Research Integrity Audit: PAPER_RESULTS_SECTION.md

**A. Numerical consistency: PASS**
Every metric, absolute difference, and relative improvement reported in the document precisely matches the exact values produced in `final_fair_evaluation_v5.json`. No rounding inconsistencies were found.

**B. Statistical-test verification: VERIFIED WITH CAVEATS**
- **Test used:** Paired Student's t-test (`scipy.stats.ttest_rel`).
- **Data compared:** Per-query MRR and nDCG@10 scores for Semantic vs. TF-IDF.
- **Number of paired observations:** 15.
- **Tailedness:** Two-sided (SciPy default).
- **p-value for MRR:** 0.0448.
- **p-value for nDCG@10:** 0.0037.
- **Other metrics:** No statistical significance tests were calculated for the Precision or Recall metrics.

**C. Unsupported claims found: FAIL**
1. **Section 4 (Precision and Recall Behavior):** The text states "semantic representation successfully bridges the vocabulary gap". This is a causal statement not directly proven by the numerical outcome. It should be softened to a hypothesis/interpretation.
2. **Section 7 (Overall Interpretation):** The text states "yields a statistically significant improvement in retrieval quality for the tested technical interview corpus." Because significance tests were only run on MRR and nDCG@10, a blanket claim of statistical significance for overall "retrieval quality" is an overclaim and violates the strict constraint against applying significance to untested metrics.

**D. Dataset-description issues: PASS**
The document accurately describes the corpus as "normalized software engineering interview questions and answers." It makes no false claims about real-world Reddit or Glassdoor narratives.

**E. RAG/generation claims requiring correction: PASS**
The text accurately restricts its conclusions to retrieval and explicitly explicitly states in Section 8 that it does not evaluate downstream LLM generation quality.

**F. MRR interpretation check: PASS**
The document correctly interprets MRR = 1.000 by explaining that "for every single one of the 15 evaluation queries, the system returned a relevant document at the absolute first rank (k=1)." This is validated by the query-level JSON output.

**G. nDCG interpretation check: PASS**
The text explicitly defines graded relevance (0, 1, 2) and explains how nDCG accounts for prioritization of directly relevant evidence over partially relevant evidence.

**H. Limitations check: PASS**
The limitations section robustly covers: the 15-query boundary, the structured/normalized QA nature of the corpus vs real-world narratives, the pooled judgment scope, and the restriction to retrieval-only evaluation. 

**I. Exact recommended corrections:**

**Correction 1:** In Section 4, revise paragraph 2:
*Current:*
> This substantially higher R@10 value suggests that semantic representation successfully bridges the vocabulary gap, retrieving almost all available relevant interview evidence that the lexical baseline missed entirely.

*Revised:*
> This substantially higher R@10 value is consistent with the ability of semantic embeddings to capture similarity beyond exact lexical overlap, retrieving almost all available relevant interview evidence that the lexical baseline missed entirely.

**Correction 2:** In Section 7, revise paragraph 1:
*Current:*
> The empirical results demonstrate that replacing lexical keyword matching with dense semantic embeddings yields a statistically significant improvement in retrieval quality for the tested technical interview corpus. The semantic architecture successfully bridges vocabulary mismatches, guaranteeing high-quality initial evidence (MRR = 1.000) while maximizing total evidence yield (Recall@10 = 0.964). 

*Revised:*
> The empirical results demonstrate that replacing lexical keyword matching with dense semantic embeddings yielded higher scores across all evaluated retrieval metrics for the tested technical interview corpus. Paired Student's t-tests indicated statistically significant differences for MRR (p = 0.0448) and nDCG@10 (p = 0.0037) on the evaluated queries. Furthermore, the results are consistent with the hypothesis that the semantic architecture captures contextual meaning, guaranteeing high-quality initial evidence (MRR = 1.000) while maximizing total evidence yield (Recall@10 = 0.964).

**Correction 3:** As an additional robustness analysis due to the small sample size (n=15), we recommend eventually performing a paired non-parametric test (e.g., Wilcoxon signed-rank test), though this is not strictly required unless assumptions of normality are fundamentally questioned.

**J. Final verdict: NEEDS REVISION**
