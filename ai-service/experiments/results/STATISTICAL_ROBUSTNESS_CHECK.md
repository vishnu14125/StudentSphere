# Statistical Robustness Check: Wilcoxon Signed-Rank Test

Because the final evaluation dataset comprised only 15 queries, an additional non-parametric paired robustness analysis was conducted using the Wilcoxon signed-rank test (`scipy.stats.wilcoxon`). The test compared the per-query differences between Semantic Retrieval and the TF-IDF Baseline.

**Test Details:**
- **Number of paired observations:** 15
- **Test used:** Wilcoxon signed-rank test
- **Alternative hypothesis:** two-sided

**Results:**

**1. MRR**
- Wilcoxon Statistic: 0.0
- Wilcoxon p-value: 0.06788915486182899
- Interpretation: The non-parametric test did not reach the conventional significance threshold (p < 0.05) for MRR.

**2. nDCG@10**
- Wilcoxon Statistic: 1.0
- Wilcoxon p-value: 0.0018714329102470324
- Interpretation: The non-parametric test reached statistical significance (p < 0.05) for nDCG@10, consistent with the parametric Student's t-test findings.
