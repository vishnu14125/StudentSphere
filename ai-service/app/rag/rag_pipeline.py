import time
import logging
from typing import List, Dict, Optional
from app.embeddings.embeddings import get_embedding_service
from app.rag.vector_store import get_vector_store
from app.services.llm_service import get_llm_service
from app.config import settings

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        self.embedding_service = get_embedding_service()
        self.vector_store = get_vector_store()
        self.llm_service = get_llm_service()

    def ingest_document_with_chunks(self, doc_id: str, text: str, metadata: Optional[Dict] = None):
        self.vector_store.delete_by_parent(str(doc_id))
        
        chunks_with_embeddings = self.embedding_service.generate_chunks_embedding(
            text, 
            chunk_max_words=settings.chunk_max_words, 
            chunk_overlap_words=settings.chunk_overlap_words
        )
        
        if not chunks_with_embeddings:
            return {'status': 'success', 'doc_id': doc_id, 'chunks_created': 0}
            
        chunk_ids = [f'{doc_id}_chunk_{i}' for i in range(len(chunks_with_embeddings))]
        chunk_texts = [chunk for chunk, _ in chunks_with_embeddings]
        chunk_embeddings = [embedding for _, embedding in chunks_with_embeddings]
        chunk_metadatas = [{**(metadata or {}), 'chunk_index': i, 'parent_doc_id': str(doc_id)} for i in range(len(chunks_with_embeddings))]
        
        self.vector_store.add_documents_batch(chunk_ids, chunk_texts, chunk_embeddings, chunk_metadatas)
        return {'status': 'success', 'doc_id': doc_id, 'chunks_created': len(chunk_ids)}

    def index_documents(self, documents: List[Dict]):
        return [self.ingest_document_with_chunks(item['id'], item['text'], metadata=item.get('metadata', {})) 
                for item in documents if item.get('id') and item.get('text')]

    def search_relevant_context(self, query: str, n_results: int = 5, filters: Optional[Dict] = None, threshold: float = 0.5) -> List[Dict]:
        query_emb = self.embedding_service.generate_embedding(query)
        results = self.vector_store.search(query_emb, n_results=n_results, where=filters)
        
        contexts = []
        if results.get('ids') and results['ids'][0]:
            for i, result_id in enumerate(results['ids'][0]):
                score = results['distances'][0][i] if results.get('distances') else 0
                if score >= threshold:
                    contexts.append({
                        'id': result_id, 
                        'text': results['documents'][0][i], 
                        'metadata': results['metadatas'][0][i] if results.get('metadatas') else {}, 
                        'score': score
                    })
        return contexts

    def answer_query(self, query: str, n_results: Optional[int] = None, filters: Optional[Dict] = None, similarity_threshold: Optional[float] = None):
        t0 = time.time()
        
        # Use config defaults if not provided
        top_k = n_results if n_results is not None else settings.rag_top_k
        threshold = similarity_threshold if similarity_threshold is not None else settings.rag_similarity_threshold
        
        # 1. Retrieval Phase
        t_retrieval_start = time.time()
        contexts = self.search_relevant_context(query, n_results=top_k, filters=filters, threshold=threshold)
        retrieval_latency = time.time() - t_retrieval_start
        
        logger.info(f"Query: '{query}'. Retrieved {len(contexts)} chunks passing threshold {threshold}.")
        
        sources = []
        snippets_for_llm = []
        topics = []
        
        for context in contexts:
            text = context['text'].strip()
            score = context['score']
            meta = context.get('metadata', {})
            source_key = meta.get('interviewId') or context['id']
            
            # Format context for LLM
            company = meta.get('companyName', 'Unknown company')
            role = meta.get('role', 'Unknown role')
            snippets_for_llm.append(f"Source: {company} - {role}\nContent: {text}")
            
            # Collect unique source metadata for frontend
            if source_key not in {item['interviewId'] for item in sources}:
                sources.append({
                    'interviewId': meta.get('interviewId'), 
                    'title': meta.get('title', 'Interview experience'), 
                    'company': company, 
                    'role': role, 
                    'year': meta.get('year', ''), 
                    'source': meta.get('source', 'StudentSphere submission'), 
                    'score': float(score),
                    'excerpt': text[:280].strip()
                })
                
            for word in (role or '').split():
                if word and word.lower() not in [topic.lower() for topic in topics]: 
                    topics.append(word)
        
        # 2. Generation Phase
        t_llm_start = time.time()
        llm_response = self.llm_service.generate_answer(query, snippets_for_llm)
        llm_latency = time.time() - t_llm_start
        
        total_latency = time.time() - t0
        
        logger.info(f"Total latency: {total_latency:.2f}s | Retrieval: {retrieval_latency:.2f}s | LLM: {llm_latency:.2f}s")
        
        return {
            'answer': llm_response['answer'], 
            'insights': topics[:6], 
            'sources': sources, 
            'grounded': True,
            'success': llm_response['success'],
            'metrics': {
                'retrieval_latency_sec': round(retrieval_latency, 3),
                'llm_latency_sec': round(llm_latency, 3),
                'total_latency_sec': round(total_latency, 3),
                'chunks_retrieved': len(contexts)
            }
        }

_rag_pipeline = None
def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None: _rag_pipeline = RAGPipeline()
    return _rag_pipeline
