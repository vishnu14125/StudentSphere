import sys
import os
import json
import csv
import time
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.rag_pipeline import get_rag_pipeline

def evaluate_threshold_topk():
    print("Loading Ground Truth...")
    gt_path = os.path.join(os.path.dirname(__file__), 'data', 'retrieval_ground_truth.json')
    with open(gt_path, 'r') as f:
        ground_truth = json.load(f)
        
    rag = get_rag_pipeline()
    
    # K sweeps
    k_values = [3, 5, 10]
    k_results = []
    
    print("Running Top-K Experiment...")
    for k in k_values:
        total_p = 0
        total_r = 0
        total_mrr = 0
        total_lat = 0
        total_retrieved = 0
        
        for item in ground_truth:
            query = item['query']
            gt_ids = set(item['relevant_interview_ids'])
            
            t0 = time.time()
            # Call semantic search directly to avoid LLM calls
            emb = rag.embedding_service.generate_embedding(query)
            res = rag.vector_store.search(emb, n_results=k)
            t1 = time.time()
            
            lat = t1 - t0
            
            sem_ids = []
            if res['metadatas'] and res['metadatas'][0]:
                for meta in res['metadatas'][0]:
                    int_id = meta.get('interviewId')
                    if int_id and int_id not in sem_ids:
                        sem_ids.append(int_id)
            
            total_retrieved += len(sem_ids)
            total_lat += lat
            
            rel = sum(1 for d in sem_ids if d in gt_ids)
            p = rel / k
            r = rel / len(gt_ids) if gt_ids else 0.0
            
            mrr = 0
            for i, d in enumerate(sem_ids):
                if d in gt_ids:
                    mrr = 1.0 / (i + 1)
                    break
                    
            total_p += p
            total_r += r
            total_mrr += mrr
            
        n = len(ground_truth)
        k_results.append({
            "k": k,
            "precision": total_p / n,
            "recall": total_r / n,
            "mrr": total_mrr / n,
            "avg_latency": total_lat / n,
            "avg_retrieved": total_retrieved / n
        })
        
    out_k = os.path.join(os.path.dirname(__file__), 'results', '03_topk_results.csv')
    with open(out_k, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=k_results[0].keys())
        writer.writeheader()
        writer.writerows(k_results)
        
    # Threshold sweeps
    print("Running Threshold Experiment...")
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    t_results = []
    
    for t in thresholds:
        relevant_retrieved = 0
        irrelevant_retrieved = 0
        no_evidence_count = 0
        total_chunks = 0
        
        for item in ground_truth:
            query = item['query']
            gt_ids = set(item['relevant_interview_ids'])
            
            emb = rag.embedding_service.generate_embedding(query)
            # Fetch plenty to filter by threshold
            res = rag.vector_store.search(emb, n_results=20) 
            
            passed_chunks = 0
            passed_rel = 0
            passed_irrel = 0
            
            if res['distances'] and res['distances'][0]:
                for i, score in enumerate(res['distances'][0]):
                    if score >= t:
                        passed_chunks += 1
                        meta = res['metadatas'][0][i]
                        if meta and meta.get('interviewId') in gt_ids:
                            passed_rel += 1
                        else:
                            passed_irrel += 1
                            
            total_chunks += passed_chunks
            relevant_retrieved += passed_rel
            irrelevant_retrieved += passed_irrel
            
            if passed_chunks == 0:
                no_evidence_count += 1
                
        n = len(ground_truth)
        total_items = relevant_retrieved + irrelevant_retrieved
        t_results.append({
            "threshold": t,
            "relevant_retrieval_rate": relevant_retrieved / total_items if total_items > 0 else 0,
            "irrelevant_retrieval_rate": irrelevant_retrieved / total_items if total_items > 0 else 0,
            "no_evidence_rate": no_evidence_count / n,
            "avg_chunks": total_chunks / n
        })
        
    out_t = os.path.join(os.path.dirname(__file__), 'results', '03_threshold_results.csv')
    with open(out_t, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=t_results[0].keys())
        writer.writeheader()
        writer.writerows(t_results)

    print("Top-K and Threshold experiments completed.")
    
if __name__ == "__main__":
    evaluate_threshold_topk()
