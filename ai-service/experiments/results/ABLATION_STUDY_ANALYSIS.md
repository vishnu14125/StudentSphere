# Retrieval Pipeline Ablation Study Analysis

Based on an inspection of the current StudentSphere AI Service implementation, multiple components of the retrieval pipeline can be isolated and ablated without executing any LLM generation calls. The pipeline relies heavily on specific, decoupled retrieval mechanics that can be modified via configuration or minor parameter overrides.

Here is the analysis of valid, LLM-free ablation experiments:

## 1. Text Chunking Ablation

*   **Component:** Document Chunking Strategy
*   **What the full system does:** In `app/embeddings/embeddings.py`, the `generate_chunks_embedding` method splits raw interview experiences by sentence boundaries (`re.split(r'(?<=[.!?])\s+', ...)`) into chunks of max 150 words with a 30-word overlap.
*   **What would be removed/changed:** The chunking logic would be disabled, meaning each interview experience is embedded as a single, full-length document (Whole-Document Embedding).
*   **What experiment would be run:** Sentence-aware Chunking vs. Whole-Document Embedding. We would re-ingest the corpus without chunking, run the 15 queries, and compare the retrieval rankings.
*   **Which existing labels could be reused:** The existing human judgments in `evaluation_queries_v3_enriched.json` map queries directly to parent `doc_id`s, so they are perfectly valid for scoring document-level retrieval regardless of how the document was chunked internally.
*   **Which metrics could be calculated:** Precision@K, Recall@K, MRR, NDCG@10.
*   **Scientifically meaningful:** Yes. Interview experiences can be long and contain multiple topics. This ablation proves whether chunking actually reduces embedding noise and improves the surfacing of specific evidence.
*   **Can be performed without LLM:** Yes.

## 2. Similarity Threshold Ablation

*   **Component:** Dynamic Result Filtering
*   **What the full system does:** In `app/rag/rag_pipeline.py`, the `search_relevant_context` method enforces a hard cutoff: `if score >= threshold:` before adding a vector search result to the context.
*   **What would be removed/changed:** The threshold would be set to `0.0` or `-1.0` (or the condition removed), allowing the system to return exactly Top-K results regardless of how semantically distant they are.
*   **What experiment would be run:** Filtered Retrieval (Threshold > 0) vs. Unfiltered Naive Top-K.
*   **Which existing labels could be reused:** `evaluation_queries_v3_enriched.json`.
*   **Which metrics could be calculated:** Noise Ratio (percentage of irrelevant documents passed to the next stage), Precision@K.
*   **Scientifically meaningful:** Yes. It justifies the inclusion of the threshold step in the architecture diagram by proving that a naive Top-K approach introduces unacceptable levels of noise (irrelevant context).
*   **Can be performed without LLM:** Yes.

## 3. Embedding Model Ablation

*   **Component:** Dense Vector Representation
*   **What the full system does:** `app/config.py` defines `embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"`.
*   **What would be removed/changed:** Swap the lightweight MiniLM model for a higher-capacity embedding model (e.g., `BAAI/bge-small-en-v1.5` or `all-mpnet-base-v2`).
*   **What experiment would be run:** Lightweight Embedding (MiniLM) vs. State-of-the-Art Dense Embedding.
*   **Which existing labels could be reused:** `evaluation_queries_v3_enriched.json`.
*   **Which metrics could be calculated:** Precision@K, Recall@K, MRR, NDCG@10.
*   **Scientifically meaningful:** Yes. It demonstrates whether the current lightweight model is sufficient for the specific domain of software engineering interview questions, or if the system suffers a significant quality penalty compared to heavier models.
*   **Can be performed without LLM:** Yes.

---

### Recommendation

**An ablation experiment is highly justified and entirely feasible without touching the Gemini API.**

I recommend executing the **Text Chunking Ablation**. 

*Why?* The threshold and Top-K parameters are hyperparameters that we have already partially analyzed (in your previous Top-K and Threshold scripts). The embedding model swap is a standard benchmark. However, **chunking** is a core architectural decision. Proving that sentence-aware overlapping chunks significantly outperform whole-document embeddings for long-form interview text will strongly reinforce the scientific rigor of the StudentSphere paper's retrieval methodology.

This experiment can be executed instantly using the existing metrics calculation scripts and the pre-labeled dataset, requiring zero LLM quota.
