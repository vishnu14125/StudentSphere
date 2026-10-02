from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import httpx
from app.services.summarization_service import get_summarization_service
from app.rag.rag_pipeline import get_rag_pipeline
from app.config import settings

router = APIRouter()
class SummarizeRequest(BaseModel):
    interviewId: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
class SearchRequest(BaseModel):
    query: str
    n_results: int = 5
class IndexedDocument(BaseModel):
    id: str
    text: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
class IndexRequest(BaseModel):
    documents: List[IndexedDocument]
class QueryRequest(BaseModel):
    query: str
    n_results: int = 5
    filters: Optional[Dict[str, Any]] = None
    similarity_threshold: Optional[float] = None

@router.post('/summarize')
async def summarize_interview(request: SummarizeRequest):
    try:
        result = get_summarization_service().summarize_interview(request.text)
        backend_url = getattr(settings, 'backend_url', 'http://localhost:5000')
        async with httpx.AsyncClient() as client:
            try: await client.put(f'{backend_url}/api/interviews/{request.interviewId}/ai-update', json={'aiSummary': result['summary'], 'aiExtractedTopics': result['topics'], 'aiExtractedQuestions': result['questions'], 'aiProcessed': True})
            except Exception as error: print(f'Failed to update backend: {error}')
        get_rag_pipeline().ingest_document_with_chunks(request.interviewId, request.text, metadata={'interviewId': request.interviewId, **request.metadata})
        return {'status': 'success', **result}
    except Exception as error: raise HTTPException(status_code=500, detail=str(error))

@router.post('/index')
async def index_documents(request: IndexRequest):
    try: return {'status': 'success', 'results': get_rag_pipeline().index_documents([item.model_dump() for item in request.documents])}
    except Exception as error: raise HTTPException(status_code=500, detail=str(error))
@router.post('/query')
async def query_documents(request: QueryRequest):
    try: return get_rag_pipeline().answer_query(request.query, request.n_results, request.filters, request.similarity_threshold)
    except Exception as error: raise HTTPException(status_code=500, detail=str(error))
@router.post('/search')
async def search_context(request: SearchRequest):
    try: return {'status': 'success', 'contexts': get_rag_pipeline().search_relevant_context(request.query, request.n_results)}
    except Exception as error: raise HTTPException(status_code=500, detail=str(error))
@router.delete('/documents/{doc_id}')
async def delete_document(doc_id: str):
    try: get_rag_pipeline().vector_store.delete_by_parent(doc_id); return {'status': 'success', 'doc_id': doc_id}
    except Exception as error: raise HTTPException(status_code=500, detail=str(error))
@router.get('/health')
async def health_check(): return {'status': 'healthy', 'service': 'AI Service'}
