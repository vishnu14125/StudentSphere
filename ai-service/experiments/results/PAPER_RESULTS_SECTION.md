# Results and Discussion

### 1. Evaluation Setup
To objectively assess the retrieval effectiveness of the StudentSphere system, we conducted a rigorous fair pooled evaluation. The evaluation corpus consisted of 200 documents representing normalized software engineering interview questions and answers. We formulated 15 information-seeking evaluation queries spanning various technical topics. A pooled evaluation methodology was employed, merging the Top-10 retrieval results from both the proposed semantic retrieval model and a lexical baseline. Human annotators assigned graded relevance judgments (0 = not relevant, 1 = partially relevant, 2 = directly relevant) to the entire candidate pool, ensuring a comprehensive ground truth consisting of 225 verified candidate-query pairs without relying on automated or LLM-inferred labels.

### 2. Lexical Baseline
We established a standard Term Frequency-Inverse Document Frequency (TF-IDF) model as the lexical baseline. TF-IDF models compute document relevance based on exact keyword matching and term frequency distributions across the corpus. In our evaluation, the TF-IDF baseline achieved a Mean Reciprocal Rank (MRR) of 0.813, a Precision@5 of 0.627, and a normalized Discounted Cumulative Gain (nDCG@10) of 0.760. These baseline metrics indicate that while keyword matching can identify relevant material, it struggles to surface contextually related evidence when exact vocabulary overlaps are absent.

### 3. Semantic Retrieval Results
The proposed StudentSphere retrieval architecture utilizes a dense vector representation approach powered by the `sentence-transformers/all-MiniLM-L6-v2` embedding model. Semantic retrieval achieved an MRR of 1.000, a Precision@5 of 0.800, and an nDCG@10 of 0.958. We performed a paired Student's t-test comparing the semantic model and the TF-IDF baseline. The null hypothesis—that there is no difference in means between the two systems—was rejected for nDCG@10 (p = 0.0037) and MRR (p = 0.0448). The semantic retrieval approach achieved higher scores than TF-IDF across all evaluated retrieval metrics.

### 4. Precision and Recall Behavior
Semantic retrieval consistently outperformed the lexical TF-IDF baseline in returning a greater proportion of judged relevant documents within the evaluated top-$k$ rankings. At a strict cutoff of $k=3$, semantic retrieval yielded a Precision@3 of 0.889 compared to the baseline's 0.689, demonstrating higher initial density of relevant evidence. 

Regarding Recall, the semantic model significantly improved the retrieval of the total available relevant pool. Most notably, semantic Recall@10 reached 0.964 versus the baseline's 0.746. This substantially higher R@10 value suggests that semantic representation successfully bridges the vocabulary gap, retrieving almost all available relevant interview evidence that the lexical baseline missed entirely.

### 5. Ranking Quality (MRR)
Mean Reciprocal Rank evaluates the ability of a system to surface at least one relevant document as early as possible in the ranking order. In our evaluation, the semantic retrieval system achieved a perfect MRR of 1.000, meaning that for every single one of the 15 evaluation queries, the system returned a relevant document at the absolute first rank ($k=1$). By contrast, the TF-IDF baseline achieved an MRR of 0.813, indicating that for certain queries, users would be forced to scan further down the results to find initial relevant evidence.

### 6. Graded Ranking Quality (nDCG)
While binary metrics treat partial and direct relevance identically, normalized Discounted Cumulative Gain (nDCG) accounts for graded relevance (0, 1, 2) and heavily penalizes systems that place lower-quality documents above highly relevant ones. Semantic retrieval achieved an nDCG@5 of 0.927 and an nDCG@10 of 0.958, outperforming the baseline (0.737 and 0.760, respectively). This confirms that the semantic representations not only surface more relevant candidates but successfully prioritize directly relevant evidence over partially relevant context at the top of the search results.

### 7. Overall Interpretation
The empirical results demonstrate that replacing lexical keyword matching with dense semantic embeddings yields a statistically significant improvement in retrieval quality for the tested technical interview corpus. The semantic architecture successfully bridges vocabulary mismatches, guaranteeing high-quality initial evidence (MRR = 1.000) while maximizing total evidence yield (Recall@10 = 0.964). 

### 8. Limitations
While these results are highly encouraging, the evaluation is subject to several boundaries. First, the evaluation scale is bounded to 15 queries and a specific pooled judgment scope. Second, the current corpus consists of cleanly formatted technical interview questions and answers, rather than a massive collection of noisy, unstructured candidate interview narratives (such as raw Reddit posts or Glassdoor reviews). Consequently, this evaluation validates retrieval effectiveness on the available structured software-engineering corpus; the broader capability to aggregate and parse raw, real-world candidate narratives remains a necessary area for future evaluation. Finally, this experiment strictly measures the intermediate retrieval component, not the complete factual accuracy or quality of the final downstream LLM generation.

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
**Figure 1.** Comparison of retrieval effectiveness between the TF-IDF baseline and Semantic Retrieval across Precision, Recall, MRR, and nDCG metrics. The semantic approach consistently demonstrates higher retrieval scores across all measured depths.
