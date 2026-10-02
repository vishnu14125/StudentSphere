# FINAL FAIR RETRIEVAL EVALUATION REPORT

## 1. Overview
This report presents the final fair comparison between TF-IDF lexical retrieval and Semantic Retrieval (sentence-transformers/all-MiniLM-L6-v2).
- **Queries:** 15
- **Pooled candidates evaluated:** 225
- **Total unjudged candidates retrieved:** 0

## 2. Aggregate Results

| Metric | TF-IDF | Semantic | Absolute Difference | Relative Improvement % |
|---|---:|---:|---:|---:|
| P@3 | 0.689 | 0.889 | +0.200 | +29.0% |
| R@3 | 0.422 | 0.532 | +0.110 | +26.0% |
| P@5 | 0.627 | 0.800 | +0.173 | +27.7% |
| R@5 | 0.591 | 0.725 | +0.134 | +22.7% |
| P@10 | 0.427 | 0.573 | +0.147 | +34.4% |
| R@10 | 0.746 | 0.964 | +0.218 | +29.3% |
| MRR | 0.813 | 1.000 | +0.187 | +23.0% |
| nDCG@5 | 0.737 | 0.927 | +0.189 | +25.7% |
| nDCG@10 | 0.760 | 0.958 | +0.198 | +26.0% |

## 3. Statistical Analysis (Paired t-test)
- **nDCG@10:** p-value = 0.0037. Null hypothesis: No difference in means. Interpretation: Statistically significant (p < 0.05).
- **MRR:** p-value = 0.0448. Null hypothesis: No difference in means. Interpretation: Statistically significant (p < 0.05).

## 4. Query-Level Results

| Query ID | Query | TF-IDF P@5 | Sem P@5 | TF-IDF R@5 | Sem R@5 | TF-IDF MRR | Sem MRR | TF-IDF nDCG@5 | Sem nDCG@5 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Q01 | How does compilation differ from interpretation? | 0.200 | 0.200 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q02 | What object-oriented concepts should I know for interviews? | 0.400 | 0.800 | 0.333 | 0.667 | 1.000 | 1.000 | 0.401 | 0.844 |
| Q03 | What should I understand about database normalization? | 0.800 | 0.600 | 0.571 | 0.429 | 1.000 | 1.000 | 0.899 | 0.821 |
| Q04 | How does caching improve system performance? | 0.400 | 1.000 | 0.250 | 0.625 | 0.333 | 1.000 | 0.311 | 1.000 |
| Q05 | What are common approaches to handling concurrent requests? | 0.000 | 1.000 | 0.000 | 0.714 | 0.167 | 1.000 | 0.000 | 0.797 |
| Q06 | What are the benefits of using a version control system? | 0.600 | 0.600 | 1.000 | 1.000 | 0.500 | 1.000 | 0.683 | 0.951 |
| Q07 | How do load balancers work in distributed systems? | 0.200 | 0.800 | 0.167 | 0.667 | 0.200 | 1.000 | 0.161 | 0.946 |
| Q08 | What is the difference between SQL and NoSQL databases? | 1.000 | 1.000 | 0.714 | 0.714 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q09 | Explain the concept of microservices architecture. | 1.000 | 1.000 | 0.714 | 0.714 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q10 | What are common software testing strategies? | 0.800 | 1.000 | 0.400 | 0.500 | 1.000 | 1.000 | 0.891 | 0.825 |
| Q11 | How is containerization used in DevOps? | 1.000 | 1.000 | 0.625 | 0.625 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q12 | What are common XSS vulnerabilities and how to prevent them? | 0.800 | 0.600 | 0.800 | 0.600 | 1.000 | 1.000 | 0.913 | 0.821 |
| Q13 | What is RESTful API design? | 1.000 | 1.000 | 0.625 | 0.625 | 1.000 | 1.000 | 0.893 | 0.893 |
| Q14 | Explain the MVC design pattern. | 0.800 | 0.800 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Q15 | What is a race condition and how do you prevent it? | 0.400 | 0.600 | 0.667 | 1.000 | 1.000 | 1.000 | 0.907 | 1.000 |
