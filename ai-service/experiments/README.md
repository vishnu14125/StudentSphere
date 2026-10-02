# StudentSphere Experimental Framework

This directory contains the automated evaluation framework for the RAG pipeline.

### Execution Order
1. `python setup_mock_data.py` (Provisions the test dataset)
2. `python 01_dataset_characterization.py`
3. `python 02_retrieval_evaluation.py` (Tests TF-IDF against Semantic search using Ground Truth labels)
4. `python 03_threshold_topk.py`
5. `python 04_latency.py`
6. `python 05_generative_evaluation.py` (Limited queries for quota protection)
7. `python 06_generate_report.py` (Aggregates CSV/JSONs into the final EXPERIMENT_REPORT.md and Matplotlib PNGs)

### Ground Truth Methodology
The retrieval ground truth (`data/retrieval_ground_truth.json`) was manually labeled (21 queries mapped to explicit `interviewId` constraints). Gemini was explicitly excluded from generating retrieval Ground Truth labels to ensure research integrity.
