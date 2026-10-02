# FINAL EXPERIMENT REPORT V2
## Dataset
The corpus consists of software engineering interview-question QA pairs and does not represent candidate-reported interview experiences.
## Evaluation Methodology
Relevance judgments were manually determined from document content, mapping queries to the semantic knowledge contained in the QA pair.
## Retrieval Evaluation
TF-IDF -> P@5: 0.250, R@5: 0.378, MRR: 0.633
Semantic -> P@5: 0.400, R@5: 0.568, MRR: 0.785
## Top-K
{3: {'precision': np.float64(0.5333333333333332), 'recall': np.float64(0.4758333333333333), 'mrr': np.float64(0.775)}, 5: {'precision': np.float64(0.39999999999999997), 'recall': np.float64(0.5675), 'mrr': np.float64(0.7849999999999999)}, 10: {'precision': np.float64(0.225), 'recall': np.float64(0.6174999999999999), 'mrr': np.float64(0.7849999999999999)}}
## Thresholds
{0.3: {'rel_retrieved_pct': np.float64(26.444444444444443), 'irrel_retrieved_pct': np.float64(73.55555555555556), 'no_evidence_rate': np.float64(0.0), 'avg_chunks': np.float64(7.85)}, 0.4: {'rel_retrieved_pct': np.float64(44.70238095238095), 'irrel_retrieved_pct': np.float64(35.297619047619044), 'no_evidence_rate': np.float64(20.0), 'avg_chunks': np.float64(4.35)}, 0.5: {'rel_retrieved_pct': np.float64(64.95833333333334), 'irrel_retrieved_pct': np.float64(15.04166666666667), 'no_evidence_rate': np.float64(20.0), 'avg_chunks': np.float64(2.4)}, 0.6: {'rel_retrieved_pct': np.float64(50.66666666666666), 'irrel_retrieved_pct': np.float64(19.333333333333336), 'no_evidence_rate': np.float64(30.0), 'avg_chunks': np.float64(1.8)}, 0.7: {'rel_retrieved_pct': np.float64(41.666666666666664), 'irrel_retrieved_pct': np.float64(8.333333333333334), 'no_evidence_rate': np.float64(50.0), 'avg_chunks': np.float64(0.95)}}
## Generative Methodology
5 representative queries manually evaluated. No automatic metrics used.
## Limitations
Does not contain real candidate interview experiences.
