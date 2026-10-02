# Results and Discussion

### 1. Evaluation Setup
To objectively assess the retrieval effectiveness of the StudentSphere system, we conducted a rigorous fair pooled evaluation. The evaluation corpus consisted of 200 documents representing normalized software engineering interview questions and answers. We formulated 15 information-seeking evaluation queries spanning various technical topics. A pooled evaluation methodology was employed, merging the Top-10 retrieval results from both the proposed semantic retrieval model and a lexical baseline. Human relevance judgments were assigned using graded relevance labels (0 = not relevant, 1 = partially relevant, 2 = directly relevant) to the entire candidate pool, ensuring a comprehensive ground truth consisting of 225 verified candidate-query pairs without relying on automated or LLM-inferred labels.

### 2. Lexical Baseline
We established a standard Term Frequency-Inverse Document Frequency (TF-IDF) model as the lexical baseline. TF-IDF models compute document relevance based on exact keyword matching and term frequency distributions across the corpus. In our evaluation, the TF-IDF baseline achieved a Mean Reciprocal Rank (MRR) of 0.813, a Precision@5 of 0.627, and a normalized Discounted Cumulative Gain (nDCG@10) of 0.760. These baseline metrics indicate that while keyword matching can identify relevant material, it struggles to surface contextually related evidence when exact vocabulary overlaps are absent.

### 3. Semantic Retrieval Results
The proposed StudentSphere retrieval architecture utilizes a dense vector representation approach powered by the `sentence-transformers/all-MiniLM-L6-v2` embedding model. Semantic retrieval achieved an MRR of 1.000, a Precision@5 of 0.800, and an nDCG@10 of 0.958. 

The empirical results demonstrate that replacing lexical keyword matching with dense semantic embeddings yielded higher scores across all evaluated retrieval metrics for the tested technical interview corpus. Both the paired Student's t-test (p = 0.0037) and Wilcoxon signed-rank test (p = 0.0019) indicated a statistically significant difference in nDCG@10. The paired Student's t-test indicated a statistically significant difference in MRR (p = 0.0448); however, the corresponding Wilcoxon signed-rank test did not reach the conventional significance threshold (p = 0.0679). The results are also consistent with the hypothesis that semantic embeddings capture contextual similarity beyond exact lexical overlap. The semantic approach achieved an MRR of 1.000 and a Recall@10 of 0.964 in this evaluation.

### 4. Precision and Recall Behavior
Semantic retrieval consistently outperformed the lexical TF-IDF baseline in returning a greater proportion of judged relevant documents within the evaluated top-$k$ rankings. At a strict cutoff of $k=3$, semantic retrieval yielded a Precision@3 of 0.889 compared to the baseline's 0.689, demonstrating higher initial density of relevant evidence. 

Regarding Recall, the semantic model improved the retrieval of the total available relevant pool, with Semantic Recall@10 reaching 0.964 versus the baseline's 0.746. This substantially higher R@10 value is consistent with the ability of semantic embeddings to capture similarity beyond exact lexical overlap. In this evaluation, semantic retrieval recovered a larger proportion of the judged relevant documents within the top-10 results than the lexical baseline.

### 5. Ranking Quality (MRR)
Mean Reciprocal Rank evaluates the ability of a system to surface at least one relevant document as early as possible in the ranking order. In our evaluation, the semantic retrieval system achieved an MRR of 1.000, meaning that for every single one of the 15 evaluation queries, the system returned a relevant document at the absolute first rank ($k=1$) under the experiment's relevance definition. By contrast, the TF-IDF baseline achieved an MRR of 0.813, indicating that the first relevant document occurred below rank 1 for some evaluation queries.

### 6. Graded Ranking Quality (nDCG)
While binary metrics treat partial and direct relevance identically, normalized Discounted Cumulative Gain (nDCG) accounts for graded relevance (0, 1, 2) and heavily penalizes systems that place lower-quality documents above highly relevant ones. Semantic retrieval achieved an nDCG@5 of 0.927 and an nDCG@10 of 0.958, outperforming the baseline (0.737 and 0.760, respectively). This indicates that, for the evaluated corpus, semantic retrieval placed more highly relevant evidence toward the top of the ranking.

### 7. Limitations
While these results validate the proposed retrieval design, the evaluation is subject to several boundaries. First, the evaluation scale is bounded to 15 queries and a specific pooled judgment scope. Second, the current evaluation uses a normalized software-engineering interview question/answer corpus. The broader capability to aggregate and parse raw, unstructured real-world candidate narratives (such as Reddit, Glassdoor, LeetCode Discuss, or GeeksforGeeks) remains a necessary area for future evaluation. Finally, this experiment strictly evaluates the intermediate retrieval component; it does not measure downstream LLM generation quality, factual correctness, hallucination reduction, or final user satisfaction.

---

**Table 1. Retrieval performance comparison between TF-IDF and semantic retrieval.**

| Metric | TF-IDF | Semantic Retrieval | Absolute Difference | Relative Improvement |
|---|---|---|---|---|
| P@3 | 0.689 | 0.889 | +0.200 | +29.0% |
| Recall@3 | 0.422 | 0.532 | +0.110 | +26.0% |
| P@5 | 0.627 | 0.800 | +0.173 | +27.7% |
| Recall@5 | 0.591 | 0.725 | +0.134 | +22.7% |
| P@10 | 0.427 | 0.573 | +0.147 | +34.4% |
| Recall@10 | 0.746 | 0.964 | +0.218 | +29.3% |
| MRR | 0.813 | 1.000 | +0.187 | +23.0% |
| nDCG@5 | 0.737 | 0.927 | +0.189 | +25.7% |
| nDCG@10 | 0.760 | 0.958 | +0.198 | +26.0% |

*(Note: Relative improvement calculated as (Semantic - TF-IDF) / TF-IDF * 100)*

![Retrieval Performance Comparison](file:///c:/Users/Vishnu/Web%20projects/MERN/StudentSphere/ai-service/experiments/results/final_retrieval_comparison.png)
**Figure 1.** Comparison of retrieval effectiveness between the TF-IDF baseline and Semantic Retrieval across Precision, Recall, MRR, and nDCG metrics. The semantic approach demonstrates higher retrieval scores across all measured depths.
