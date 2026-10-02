# RAG Implementation Details

## Architecture
The RAG pipeline is implemented entirely within the Python `ai-service`. It replaces the original simulated generation with an authentic end-to-end LLM-based Retrieval-Augmented Generation pipeline.

## Embedding Model
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Why**: It is the existing project standard, runs locally, provides excellent semantic density for English text, and is very fast for real-time embedding generation.

## Vector Storage & Persistence Mechanism
- **Implementation**: `PersistentNumpyVectorStore`
- **Persistence Mechanism**: Standard library `pickle` serializing the Numpy arrays (`embeddings`), documents, and metadata to `./vector_db/vector_store.pkl`.
- **Why**: Fulfils the requirement for a persistent local index without introducing the heavy `chromadb` dependency footprint. It automatically loads on startup and gracefully recovers if the file is corrupted.

## Chunking Algorithm
- **Algorithm**: Sentence-Aware Sliding Window Chunking.
- **Parameters**: 
  - `chunk_max_words`: 150
  - `chunk_overlap_words`: 30
- **Why**: Instead of splitting blindly at exactly 220 words (which often bifurcates critical sentences), this uses RegEx sentence boundary detection (`(?<=[.!?])\s+`). It aggregates sentences until the maximum word count is reached, retaining overlap to preserve context across boundaries. Each chunk inherits the full original `metadata` linked to the source interview.

## Retrieval Algorithm
- **Similarity Metric**: Cosine Similarity via `sklearn.metrics.pairwise.cosine_similarity`.
- **Top-K (`rag_top_k`)**: 5 (configurable).
- **Similarity Threshold (`rag_similarity_threshold`)**: 0.5 (configurable).
- **Filtering**: Filtering happens *before* LLM generation. Chunks that do not meet the similarity threshold are excluded from the context context pool.

## LLM Model & Generation
- **Model**: `gpt-4o-mini` (Configurable via `OPENAI_MODEL` in `.env`).
- **Prompt Structure**:
  - The system prompt enforces strict constraints: "You are an AI assistant helping students prepare for technical interviews based ONLY on the provided interview experiences... Do not invent facts..."
  - Context is injected dynamically and formatted cleanly.
- **No-Evidence Handling**: If the retrieved chunks list is empty (after similarity thresholding), the pipeline gracefully short-circuits *before* calling the OpenAI API, returning the structured message: `"Insufficient retrieved evidence is available to answer this question..."`.

## Source Attribution
Every retrieved chunk passed to the LLM contributes to the `sources` array in the API response. The response maps the source chunks to metadata objects containing:
- `interviewId`
- `company`
- `role`
- `year`
- `source`
- `score` (Cosine similarity score)
- `excerpt` (first 280 characters of the chunk)

## Error Handling
- **Missing API Keys**: If `OPENAI_API_KEY` is not present, `LLMService` returns a structured error: `{"answer": "Error: OPENAI_API_KEY is not configured.", "success": False}` rather than faking an answer.
- **OpenAI API Failures**: Caught and logged gracefully, returning `success: False` with the stringified error message.

## Observability (Latency Measurements)
Latency is measured explicitly in `rag_pipeline.py` and returned in the API payload under `metrics`:
- `retrieval_latency_sec`: Time for embedding the query and cosine search.
- `llm_latency_sec`: Time for OpenAI generation.
- `total_latency_sec`: Overall request time.
- `chunks_retrieved`: Final count of chunks passing threshold.
Logs also emit this information at `INFO` level.
