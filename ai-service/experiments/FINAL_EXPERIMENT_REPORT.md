# FINAL EXPERIMENT REPORT
## Dataset
200 Software Engineering Interview Questions from Kaggle.
## Retrieval Evaluation
TF-IDF -> P@5: 0.18, R@5: 0.29, MRR: 0.88
Semantic -> P@5: 0.05, R@5: 0.08, MRR: 0.15
## Top-K
{3: {'precision': np.float64(0.04), 'recall': np.float64(0.04), 'mrr': np.float64(0.12)}, 5: {'precision': np.float64(0.04800000000000001), 'recall': np.float64(0.08), 'mrr': np.float64(0.14800000000000002)}, 10: {'precision': np.float64(0.032), 'recall': np.float64(0.10666666666666666), 'mrr': np.float64(0.152)}}
## Thresholds
{0.3: {'rel_retrieved_pct': np.float64(4.0), 'irrel_retrieved_pct': np.float64(12.0), 'no_evidence_rate': np.float64(84.0), 'avg_chunks': np.float64(0.16)}, 0.4: {'rel_retrieved_pct': np.float64(0.0), 'irrel_retrieved_pct': np.float64(0.0), 'no_evidence_rate': np.float64(100.0), 'avg_chunks': np.float64(0.0)}, 0.5: {'rel_retrieved_pct': np.float64(0.0), 'irrel_retrieved_pct': np.float64(0.0), 'no_evidence_rate': np.float64(100.0), 'avg_chunks': np.float64(0.0)}, 0.6: {'rel_retrieved_pct': np.float64(0.0), 'irrel_retrieved_pct': np.float64(0.0), 'no_evidence_rate': np.float64(100.0), 'avg_chunks': np.float64(0.0)}, 0.7: {'rel_retrieved_pct': np.float64(0.0), 'irrel_retrieved_pct': np.float64(0.0), 'no_evidence_rate': np.float64(100.0), 'avg_chunks': np.float64(0.0)}}
## Latency
{'embedding': {'mean': np.float64(0.019490270614624022), 'min': np.float64(0.01452183723449707), 'max': np.float64(0.028865337371826172)}, 'search': {'mean': np.float64(0.008701839447021485), 'min': np.float64(0.006993532180786133), 'max': np.float64(0.010004758834838867)}, 'total_retrieval': {'mean': np.float64(0.028192110061645508), 'min': np.float64(0.02353072166442871), 'max': np.float64(0.03838777542114258)}, 'gemini_base': {'mean': np.float64(0.0)}, 'gemini_rag': {'mean': np.float64(1.4088171005249024)}}
