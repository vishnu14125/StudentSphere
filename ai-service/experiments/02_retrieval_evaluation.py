import sys
import os
import json
import csv
import numpy as np
from typing import List, Dict, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.vector_store import get_vector_store
from app.embeddings.embeddings import EmbeddingService

def calc_metrics(retrieved_ids: List[str], ground_truth_ids: Set[str], k: int = 5):
    retrieved_k = retrieved_ids[:k]
    
    # Precision@K
    relevant_retrieved = sum(1 for doc_id in retrieved_k if doc_id in ground_truth_ids)
    precision = relevant_retrieved / k if k > 0 else 0.0
    
    # Recall@K
    recall = relevant_retrieved / len(ground_truth_ids) if ground_truth_ids else 0.0
    
    # MRR
    mrr = 0.0
    for i, doc_id in enumerate(retrieved_ids):
        if doc_id in ground_truth_ids:
            mrr = 1.0 / (i + 1)
            break
            
    return precision, recall, mrr

def evaluate_retrieval():
    print("Loading Ground Truth...")
    gt_path = os.path.join(os.path.dirname(__file__), 'data', 'retrieval_ground_truth.json')
    with open(gt_path, 'r') as f:
        ground_truth = json.load(f)
        
    vs = get_vector_store()
    
    # Map documents for TF-IDF
    # We will build TF-IDF on the chunk level, and aggregate to document level like RAG does
    texts = vs.documents
    doc_ids = vs.ids
    metadatas = vs.metadatas
    
    # Map chunk id to interview id
    chunk_to_interview = {doc_id: meta.get('interviewId') for doc_id, meta in zip(doc_ids, metadatas)}
    
    print("Building TF-IDF Baseline...")
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    from app.rag.rag_pipeline import get_rag_pipeline
    rag = get_rag_pipeline()
    embedding_service = rag.embedding_service
    
    results = []
    
    for item in ground_truth:
        query = item['query']
        gt_ids = set(item['relevant_interview_ids'])
        
        # 1. TF-IDF Retrieval
        query_tfidf = vectorizer.transform([query])
        tfidf_sims = cosine_similarity(query_tfidf, tfidf_matrix)[0]
        
        # Sort and aggregate to interview level
        sorted_indices = np.argsort(tfidf_sims)[::-1]
        tfidf_retrieved_interviews = []
        for idx in sorted_indices:
            interview_id = chunk_to_interview[doc_ids[idx]]
            if interview_id and interview_id not in tfidf_retrieved_interviews:
                tfidf_retrieved_interviews.append(interview_id)
                
        tf_p, tf_r, tf_mrr = calc_metrics(tfidf_retrieved_interviews, gt_ids, k=5)
        
        # 2. Semantic Retrieval
        query_emb = embedding_service.generate_embedding(query)
        res = vs.search(query_emb, n_results=50) # Get many to aggregate
        
        semantic_retrieved_interviews = []
        if res['metadatas'] and res['metadatas'][0]:
            for meta in res['metadatas'][0]:
                int_id = meta.get('interviewId')
                if int_id and int_id not in semantic_retrieved_interviews:
                    semantic_retrieved_interviews.append(int_id)
                    
        sem_p, sem_r, sem_mrr = calc_metrics(semantic_retrieved_interviews, gt_ids, k=5)
        
        results.append({
            "query_id": item['query_id'],
            "query": query,
            "category": item['category'],
            "tfidf_precision_5": tf_p,
            "tfidf_recall_5": tf_r,
            "tfidf_mrr": tf_mrr,
            "semantic_precision_5": sem_p,
            "semantic_recall_5": sem_r,
            "semantic_mrr": sem_mrr
        })
        
    # Aggregate and Save
    out_csv = os.path.join(os.path.dirname(__file__), 'results', '02_retrieval_eval.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    summary = {
        "mean_tfidf_precision_5": np.mean([r['tfidf_precision_5'] for r in results]),
        "mean_tfidf_recall_5": np.mean([r['tfidf_recall_5'] for r in results]),
        "mean_tfidf_mrr": np.mean([r['tfidf_mrr'] for r in results]),
        "mean_semantic_precision_5": np.mean([r['semantic_precision_5'] for r in results]),
        "mean_semantic_recall_5": np.mean([r['semantic_recall_5'] for r in results]),
        "mean_semantic_mrr": np.mean([r['semantic_mrr'] for r in results])
    }
    
    out_json = os.path.join(os.path.dirname(__file__), 'results', '02_retrieval_summary.json')
    with open(out_json, 'w') as f:
        json.dump(summary, f, indent=2)
        
    print(f"Retrieval evaluation completed.")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    evaluate_retrieval()
