# Project Audit: StudentSphere Codebase

## Current Architecture
The current implementation follows a three-tier microservice-like architecture:
1. **Frontend**: React.js SPA handling UI and user interactions.
2. **Backend**: Node.js/Express REST API serving as the primary gateway, handling business logic, authentication, and MongoDB interactions.
3. **AI Service**: Python/FastAPI service dedicated to embeddings, vector storage, and AI tasks.

## Actual Technologies
- **Frontend**: React, Tailwind CSS, React Router, Axios.
- **Backend**: Node.js, Express, MongoDB (Mongoose), JWT.
- **AI Service**: Python, FastAPI, SentenceTransformers, ChromaDB, OpenAI SDK, httpx.

## Actual AI Models
- **Embeddings**: `sentence-transformers` (specifically configured for `all-MiniLM-L6-v2` in README) running locally.
- **Summarization**: OpenAI `gpt-3.5-turbo` is implemented for summarization, but it includes a rudimentary naive string-matching fallback if no API key is provided.
- **Generative QA (RAG)**: **No LLM is used.** The query generation is completely faked using naive string concatenation of retrieved snippets.

## Actual Data Flow
1. **Interview Submission**:
   - Client POSTs to Express backend (`/api/interviews`).
   - Backend saves to MongoDB, then asynchronously POSTs to FastAPI (`/api/ai/summarize`).
2. **AI Processing & Indexing**:
   - FastAPI calls OpenAI (or fallback) to extract a summary and topics.
   - FastAPI naive-chunks the full text (by word count) and generates embeddings.
   - Vectors are stored in ChromaDB.
   - FastAPI PUTs the generated summary back to Express (`/api/interviews/:id/ai-update`).
3. **AI Insights Query (RAG)**:
   - Client POSTs query.
   - FastAPI embeds the query and searches ChromaDB.
   - *Fake Generation*: Instead of sending retrieved context to an LLM, FastAPI simply extracts sentences and concatenates them with a hardcoded prefix: `"Based only on the retrieved interview experiences: "`.
4. **Analytics**:
   - Express runs real MongoDB aggregation pipelines to calculate topic frequencies, difficulties, and trends.
5. **Preparation Roadmap**:
   - Express fetches priority topics from Analytics.
   - It statically maps these topics into a fixed weekly template (e.g., "Week X preparation", "Learn concepts") rather than generating a truly personalized plan.

## Existing Features
- User Auth & Company CRUD.
- Interview Experience submission and storage.
- Real Analytics aggregation from MongoDB.
- Vector indexing of interview texts using ChromaDB.

## Broken / Faked / Misleading Components
- **RAG Generation**: The generative step is completely missing. It fakes AI generation by concatenating snippets from the vector database.
- **Chunking Strategy**: The `generate_chunks_embedding` function splits text naively by an exact word count (default 220), which splits sentences and degrades retrieval quality.
- **Summarization Fallback**: The fallback logic is extremely poor, extracting lines ending with `?` as questions and splitting the first 3 sentences as a summary.
- **Roadmap Generation**: It is not AI-generated; it is a static programmatic loop that drops database topics into a hardcoded boilerplate array.
- **Source Attribution in QA**: The attribution logic in RAG is flawed and bases its snippet extraction on naive string manipulation instead of LLM reasoning.

## Missing Research Components
To support an academic conference paper, the project lacks:
- **Advanced RAG Techniques**: E.g., Semantic chunking, re-ranking, query expansion, or hybrid search (BM25 + Dense).
- **True Generative LLM QA**: A real LLM call to synthesize the retrieved context with accurate citations.
- **Evaluation Metrics**: No implementation of RAG evaluation (like RAGAS metrics: faithfulness, answer relevance, context precision).
- **Graph/Ontology Mapping**: No advanced mapping of technical concepts beyond naive string matching.

## Recommended Implementation Changes
1. **Fix RAG Pipeline**: Integrate an actual LLM call in `rag_pipeline.py`'s `answer_query` method to synthesize the final answer based on ChromaDB context.
2. **Improve Chunking**: Replace the naive word-count chunker with a semantic text splitter (e.g., LangChain's RecursiveCharacterTextSplitter or NLTK sentence tokenizer).
3. **Enhance Roadmap Generation**: Move the roadmap generation logic to the Python AI service and use an LLM to generate a personalized, dynamic study plan rather than a static loop.
4. **Error Handling & Reliability**: Remove hardcoded fallbacks like `http://localhost:5000` in `ai_routes.py` and ensure the async updates are robust.

## Recommended Experiments (For Research Paper)
1. **Chunking Strategy Comparison**: Compare naive word-count chunking vs. semantic sentence chunking on retrieval accuracy.
2. **Retrieval Effectiveness**: Evaluate vector search (dense) vs. hybrid search (dense + sparse/BM25) for technical interview questions.
3. **Generation Quality**: Measure the hallucination rate and groundedness of the real LLM-synthesized answers versus the baseline faked snippet concatenation.
4. **Personalization Impact**: Measure user progress metrics using the static roadmap vs. a true LLM-generated dynamic roadmap.

Audit complete — waiting for implementation approval.
