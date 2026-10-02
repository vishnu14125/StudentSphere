import os
import json
import sys

# Ensure imports work from ai-service directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.rag_pipeline import get_rag_pipeline
from app.config import settings

rag = get_rag_pipeline()

# Re-index corpus if needed to ensure we have the latest fixed data
rag.vector_store.documents = []
rag.vector_store.metadatas = []
rag.vector_store.ids = []
rag.vector_store.embeddings = []
rag.vector_store.save()

corpus_path = os.path.join(os.path.dirname(__file__), '../datasets/research_corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

for doc in corpus:
    rag.ingest_document_with_chunks(doc['id'], doc['experienceText'], doc)

print(f"Indexed {len(rag.vector_store.ids)} chunks.")

# 15 realistic queries
queries = [
    "How does compilation differ from interpretation?",
    "What object-oriented concepts should I know for interviews?",
    "What should I understand about database normalization?",
    "How does caching improve system performance?",
    "What are common approaches to handling concurrent requests?",
    "What are the benefits of using a version control system?",
    "How do load balancers work in distributed systems?",
    "What is the difference between SQL and NoSQL databases?",
    "Explain the concept of microservices architecture.",
    "What are common software testing strategies?",
    "How is containerization used in DevOps?",
    "What are common XSS vulnerabilities and how to prevent them?",
    "What is RESTful API design?",
    "Explain the MVC design pattern.",
    "What is a race condition and how do you prevent it?"
]

results_dir = os.path.join(os.path.dirname(__file__), 'results')
os.makedirs(results_dir, exist_ok=True)

human_eval_candidates = []
evaluation_queries_v3 = []

for i, q in enumerate(queries):
    q_id = f"Q{i+1:02d}"
    
    q_emb = rag.embedding_service.generate_embedding(q)
    search_res = rag.vector_store.search(q_emb, n_results=30)
    
    metas = search_res.get('metadatas', [[]])[0]
    scores = search_res.get('distances', [[]])[0]
    
    # De-duplicate by parent doc ID
    unique_candidates = []
    seen_ids = set()
    
    for meta, score in zip(metas, scores):
        doc_id = meta.get('parent_doc_id', meta.get('id', ''))
        if doc_id not in seen_ids:
            seen_ids.add(doc_id)
            # Find original doc to get full text
            orig_doc = next((d for d in corpus if d['id'] == doc_id), None)
            if orig_doc:
                unique_candidates.append({
                    'doc_id': doc_id,
                    'score': float(score),
                    'question': orig_doc['experienceText'].split('\nAnswer: ')[0].replace('Question: ', ''),
                    'answer': orig_doc['experienceText'].split('\nAnswer: ')[1] if '\nAnswer: ' in orig_doc['experienceText'] else '',
                    'category': orig_doc['topics'][0] if orig_doc['topics'] else 'Unknown'
                })
        
        if len(unique_candidates) == 10:
            break
            
    human_eval_candidates.append({
        'query_id': q_id,
        'query': q,
        'candidates': unique_candidates
    })
    
    v3_candidates = []
    for rank, cand in enumerate(unique_candidates):
        v3_candidates.append({
            'doc_id': cand['doc_id'],
            'rank': rank + 1,
            'similarity': cand['score'],
            'relevance': None
        })
        
    evaluation_queries_v3.append({
        'query_id': q_id,
        'query': q,
        'candidates': v3_candidates
    })

with open(os.path.join(results_dir, 'human_eval_candidates.json'), 'w', encoding='utf-8') as f:
    json.dump(human_eval_candidates, f, indent=2)

with open(os.path.join(results_dir, 'evaluation_queries_v3.json'), 'w', encoding='utf-8') as f:
    json.dump(evaluation_queries_v3, f, indent=2)
    
print("Successfully generated human evaluation templates.")
