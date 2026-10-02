# StudentSphere RAG Documentation

## Overview

StudentSphere implements a Retrieval-Augmented Generation (RAG) architecture to provide intelligent search and question-answering capabilities for interview experiences. The RAG system combines vector search with large language models to deliver relevant, context-aware responses.

## Architecture

```
┌─────────────────┐
│   User Query    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Query Encoder  │
│  (Embeddings)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Vector Search  │
│  (ChromaDB)     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Context        │
│  Retrieval      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  LLM Generation │
│  (OpenAI)       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Final Answer   │
│  + Citations    │
└─────────────────┘
```

## Components

### 1. Embedding Service

**Location:** `ai-service/app/embeddings/embeddings.py`

**Purpose:** Convert text into vector representations for semantic similarity search.

**Model:** `sentence-transformers/all-MiniLM-L6-v2`

**Features:**
- 384-dimensional embeddings
- Fast inference
- Good semantic understanding
- Multilingual support

**Key Functions:**

```python
class EmbeddingService:
    def generate_embedding(self, text: str) -> List[float]
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]
    def generate_chunks_embedding(self, text: str, chunk_size: int = 500) -> List[tuple]
```

**Usage Example:**
```python
from app.embeddings.embeddings import get_embedding_service

embedding_service = get_embedding_service()
embedding = embedding_service.generate_embedding("Amazon SDE interview")
# Returns: [0.123, -0.456, ...] (384 dimensions)
```

---

### 2. Vector Store

**Location:** `ai-service/app/rag/vector_store.py`

**Purpose:** Store and retrieve vector embeddings using ChromaDB.

**Database:** ChromaDB (Persistent)

**Collection:** `interview_experiences`

**Key Functions:**

```python
class VectorStore:
    def add_document(self, doc_id, text, embedding, metadata)
    def add_documents_batch(self, doc_ids, texts, embeddings, metadatas)
    def search(self, query_embedding, n_results=5, where=None)
    def delete_document(self, doc_id)
    def get_document(self, doc_id)
    def update_document(self, doc_id, text=None, embedding=None, metadata=None)
```

**Metadata Schema:**
```python
{
    "type": "interview_experience",
    "chunk_index": 0,
    "parent_doc_id": "interview_id",
    "company": "Amazon",  # Optional
    "role": "SDE",  # Optional
    "year": 2024  # Optional
}
```

**Usage Example:**
```python
from app.rag.vector_store import get_vector_store

vector_store = get_vector_store()

# Add document
vector_store.add_document(
    doc_id="interview_123",
    text="Interview experience text...",
    embedding=[0.123, -0.456, ...],
    metadata={"company": "Amazon", "role": "SDE"}
)

# Search
results = vector_store.search(
    query_embedding=[0.789, 0.321, ...],
    n_results=5
)
```

---

### 3. RAG Pipeline

**Location:** `ai-service/app/rag/rag_pipeline.py`

**Purpose:** Orchestrate the document ingestion and retrieval process.

**Key Functions:**

```python
class RAGPipeline:
    def ingest_document(self, doc_id, text, metadata)
    def ingest_document_with_chunks(self, doc_id, text, chunk_size=500, metadata)
    def search_relevant_context(self, query, n_results=5, filters=None)
    def delete_document(self, doc_id)
```

**Document Ingestion Flow:**

1. **Simple Ingestion:**
   - Generate embedding for entire document
   - Store in vector database
   - Return document ID

2. **Chunked Ingestion:**
   - Split document into chunks (default: 500 words)
   - Generate embeddings for each chunk
   - Store all chunks with metadata
   - Return document ID and chunk count

**Search Flow:**

1. Generate query embedding
2. Search vector database
3. Return top-k similar contexts with metadata
4. Optionally filter by metadata

**Usage Example:**
```python
from app.rag.rag_pipeline import get_rag_pipeline

rag_pipeline = get_rag_pipeline()

# Ingest document
result = rag_pipeline.ingest_document_with_chunks(
    doc_id="interview_123",
    text="Full interview experience...",
    chunk_size=500,
    metadata={"company": "Amazon", "role": "SDE"}
)

# Search
contexts = rag_pipeline.search_relevant_context(
    query="Amazon SDE interview questions about arrays",
    n_results=5,
    filters={"company": "Amazon"}
)
```

---

### 4. Summarization Service

**Location:** `ai-service/app/services/summarization_service.py`

**Purpose:** Generate AI summaries and extract key information from interview experiences.

**Model:** OpenAI GPT-3.5-turbo (with fallback)

**Key Functions:**

```python
class SummarizationService:
    def summarize_interview(self, text: str) -> Dict
```

**Output Format:**
```python
{
    "summary": "Concise summary of the interview",
    "topics": ["Arrays", "Trees", "Dynamic Programming"],
    "questions": ["LRU Cache", "Binary Tree Traversal"]
}
```

**Fallback Mechanism:**
- If OpenAI API is unavailable, uses rule-based extraction
- Extracts common technical topics
- Extracts questions (lines ending with '?')
- Creates simple summary from first few sentences

**Usage Example:**
```python
from app.services.summarization_service import get_summarization_service

summarization_service = get_summarization_service()
result = summarization_service.summarize_interview(interview_text)
```

---

## Integration with Backend

### Interview Submission Flow

1. **User submits interview experience**
   - Frontend → Backend API
   - Backend stores in MongoDB

2. **Backend triggers AI processing**
   - Backend → AI Service (async)
   - Endpoint: `POST /api/ai/summarize`

3. **AI Service processes**
   - Generates summary
   - Extracts topics/questions
   - Ingests into RAG system

4. **AI Service updates backend**
   - AI Service → Backend (internal endpoint)
   - Endpoint: `PUT /api/interviews/:id/ai-update`

5. **Frontend displays results**
   - Polls or waits for AI processing
   - Shows AI-generated insights

### API Integration

**Backend to AI Service:**
```javascript
// Backend (interviewController.js)
const processWithAI = async (interviewId, text) => {
  try {
    const aiServiceUrl = process.env.AI_SERVICE_URL || 'http://localhost:8000';
    
    await axios.post(`${aiServiceUrl}/api/ai/summarize`, {
      interviewId,
      text,
    });
  } catch (error) {
    console.error('AI Processing Error:', error.message);
  }
};
```

**AI Service to Backend:**
```python
# AI Service (ai_routes.py)
await client.put(
    f"{backend_url}/api/interviews/{request.interviewId}/ai-update",
    json=update_data
)
```

---

## Vector Database Schema

### Collection: `interview_experiences`

**Document Structure:**
```python
{
    "ids": ["interview_123_chunk_0", "interview_123_chunk_1", ...],
    "embeddings": [[0.123, ...], [0.456, ...], ...],
    "documents": ["Chunk 1 text...", "Chunk 2 text...", ...],
    "metadatas": [
        {
            "type": "interview_experience",
            "chunk_index": 0,
            "parent_doc_id": "interview_123",
            "company": "Amazon",
            "role": "SDE",
            "year": 2024
        },
        ...
    ]
}
```

### Indexing

ChromaDB automatically creates HNSW (Hierarchical Navigable Small World) indexes for efficient similarity search.

**Index Parameters:**
- Algorithm: HNSW
- Metric: Cosine similarity
- Efficiency: O(log n) search

---

## Query Processing

### Search Query Flow

1. **Query Preprocessing**
   - Clean and normalize query
   - Remove special characters
   - Lowercase text

2. **Embedding Generation**
   - Convert query to vector
   - Use same model as documents

3. **Vector Search**
   - Query ChromaDB
   - Apply filters if provided
   - Return top-k results

4. **Result Processing**
   - Format results
   - Include metadata
   - Calculate similarity scores

### Example Query

```python
# User query
query = "What are common questions in Amazon SDE interviews?"

# Process
contexts = rag_pipeline.search_relevant_context(
    query=query,
    n_results=5,
    filters={"company": "Amazon"}
)

# Result
[
    {
        "id": "interview_456_chunk_2",
        "text": "The interviewer asked about LRU Cache and binary trees...",
        "metadata": {
            "type": "interview_experience",
            "chunk_index": 2,
            "parent_doc_id": "interview_456",
            "company": "Amazon",
            "role": "SDE"
        },
        "distance": 0.234
    },
    ...
]
```

---

## Performance Optimization

### Chunking Strategy

**Default Chunk Size:** 500 words

**Rationale:**
- Large enough to capture context
- Small enough for precise matching
- Balances recall and precision

**Alternative Strategies:**
- Sentence-based chunking
- Semantic chunking (using embeddings)
- Overlapping chunks (with window)

### Embedding Caching

**Current:** No caching (each request generates new embedding)

**Future:** Implement caching for:
- Frequently asked queries
- Company profiles
- Role descriptions

### Batch Processing

**Current:** Sequential processing

**Future:** Implement batch processing for:
- Bulk document ingestion
- Multiple query processing
- Batch embedding generation

---

## Future Enhancements

### Phase 2: Advanced RAG Chatbot

**Features:**
- Conversational interface
- Context retention
- Multi-turn conversations
- Source citations

**Implementation:**
```python
class AdvancedRAGChatbot:
    def __init__(self):
        self.rag_pipeline = get_rag_pipeline()
        self.conversation_history = []
    
    def chat(self, query: str) -> str:
        # Add to conversation history
        self.conversation_history.append(query)
        
        # Search with context
        contexts = self.rag_pipeline.search_relevant_context(
            query=query,
            n_results=5
        )
        
        # Generate answer with citations
        answer = self.generate_answer_with_citations(
            query=query,
            contexts=contexts,
            history=self.conversation_history
        )
        
        return answer
```

### Phase 3: Hybrid Search

**Features:**
- Combine vector search with keyword search
- Re-ranking using cross-encoders
- Query expansion
- Spell correction

**Implementation:**
```python
class HybridSearch:
    def search(self, query: str):
        # Vector search
        vector_results = self.vector_search(query)
        
        # Keyword search
        keyword_results = self.keyword_search(query)
        
        # Combine and re-rank
        combined = self.combine_results(vector_results, keyword_results)
        ranked = self.rerank(combined, query)
        
        return ranked
```

### Phase 4: Multi-Modal RAG

**Features:**
- Process code snippets
- Handle technical diagrams
- Parse structured data
- Support multiple languages

---

## Monitoring and Logging

### Metrics to Track

1. **Search Performance**
   - Query latency
   - Index hit rate
   - Result relevance (feedback-based)

2. **Embedding Performance**
   - Generation time
   - Cache hit rate
   - Model accuracy

3. **System Health**
   - Vector database size
   - Memory usage
   - Query throughput

### Logging

**Current:** Console logging

**Future:** Structured logging with:
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Request/response logging
- Performance metrics
- Error tracking

---

## Troubleshooting

### Common Issues

#### Low Search Relevance

**Symptoms:** Search results not matching query intent

**Solutions:**
- Check embedding model compatibility
- Verify chunking strategy
- Review metadata filters
- Consider re-indexing

#### Slow Query Performance

**Symptoms:** Long response times

**Solutions:**
- Check vector database size
- Verify index status
- Optimize chunk size
- Implement caching

#### Memory Issues

**Symptoms:** Out of memory errors

**Solutions:**
- Reduce chunk size
- Implement streaming
- Increase available memory
- Use batch processing

---

## Evaluation

### Metrics

1. **Retrieval Metrics**
   - Precision@k
   - Recall@k
   - Mean Average Precision (MAP)
   - Normalized Discounted Cumulative Gain (NDCG)

2. **Generation Metrics**
   - ROUGE scores
   - BLEU scores
   - Human evaluation
   - User satisfaction

### Testing

**Test Dataset:**
- Sample interview experiences
- Varied query types
- Different domains
- Multiple difficulty levels

**Evaluation Process:**
1. Create test queries
2. Run RAG pipeline
3. Evaluate retrieval quality
4. Assess generated answers
5. Collect user feedback

---

## Security Considerations

### Data Privacy

- Ensure user consent for AI processing
- Anonymize sensitive information
- Secure API communication
- Regular security audits

### Access Control

- Implement rate limiting
- Add authentication for AI service
- Monitor for abuse
- Log all access

### Model Security

- Validate inputs
- Sanitize outputs
- Monitor for prompt injection
- Regular model updates

---

## References

### Technologies

- **Sentence Transformers:** https://www.sbert.net/
- **ChromaDB:** https://www.trychroma.com/
- **OpenAI API:** https://platform.openai.com/
- **FastAPI:** https://fastapi.tiangolo.com/

### Papers

- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- "Dense Passage Retrieval for Open-Domain Question Answering"
- "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks"

### Resources

- RAG documentation: https://www.pinecone.io/learn/retrieval-augmented-generation/
- Vector databases: https://www.pinecone.io/learn/vector-database/
- Embeddings: https://www.sbert.net/examples/applications/computing-embeddings.html
