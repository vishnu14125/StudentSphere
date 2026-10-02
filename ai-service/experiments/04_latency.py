import sys
import os
import time
import json
import csv
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.rag_pipeline import get_rag_pipeline

def evaluate_latency():
    rag = get_rag_pipeline()
    queries = [
        "What questions are asked in Amazon SDE interviews?",
        "What are common system design topics?",
        "How many rounds are there for Microsoft SWE?",
        "What data structures and algorithms should I prepare?",
        "What was asked in the Google Frontend interview?",
        "What do Meta Data Engineers get asked?",
        "Are there iOS specific questions for Apple?",
        "What should I know for Stripe backend?",
        "What are Netflix system design interviews like?",
        "Data science questions at Amazon"
    ]
    
    embedding_lats = []
    vector_lats = []
    
    print("Measuring Embedding and Vector Search Latency (10 runs)...")
    for q in queries:
        t0 = time.time()
        emb = rag.embedding_service.generate_embedding(q)
        t1 = time.time()
        embedding_lats.append(t1 - t0)
        
        t2 = time.time()
        res = rag.vector_store.search(emb, n_results=5)
        t3 = time.time()
        vector_lats.append(t3 - t2)
        
    print("Measuring LLM Generation Latency (3 runs)...")
    llm_lats = []
    for q in queries[:3]:
        # get context
        emb = rag.embedding_service.generate_embedding(q)
        res = rag.vector_store.search(emb, n_results=5)
        context = []
        if res['documents'] and res['documents'][0]:
            context = res['documents'][0]
            
        t0 = time.time()
        try:
            # Bypass RAG wrapper and call LLM directly to just measure generation
            ans = rag.llm_service.generate_answer(q, context)
            if ans.get("success"):
                t1 = time.time()
                llm_lats.append(t1 - t0)
            else:
                print(f"Skipped LLM latency for query due to failure: {ans.get('error')}")
        except Exception as e:
            print(f"LLM call failed: {e}")
            
    stats = {
        "embedding": {
            "mean": np.mean(embedding_lats),
            "median": np.median(embedding_lats),
            "std": np.std(embedding_lats),
            "min": np.min(embedding_lats),
            "max": np.max(embedding_lats)
        },
        "vector_search": {
            "mean": np.mean(vector_lats),
            "median": np.median(vector_lats),
            "std": np.std(vector_lats),
            "min": np.min(vector_lats),
            "max": np.max(vector_lats)
        },
        "retrieval_total": {
            "mean": np.mean(embedding_lats) + np.mean(vector_lats),
            "median": np.median(embedding_lats) + np.median(vector_lats),
            "std": np.sqrt(np.std(embedding_lats)**2 + np.std(vector_lats)**2), # approx assuming independence
            "min": np.min(embedding_lats) + np.min(vector_lats),
            "max": np.max(embedding_lats) + np.max(vector_lats)
        }
    }
    
    if llm_lats:
        stats["llm_generation"] = {
            "mean": np.mean(llm_lats),
            "median": np.median(llm_lats),
            "std": np.std(llm_lats),
            "min": np.min(llm_lats),
            "max": np.max(llm_lats)
        }
        stats["end_to_end"] = {
            "mean": stats["retrieval_total"]["mean"] + stats["llm_generation"]["mean"],
            "median": stats["retrieval_total"]["median"] + stats["llm_generation"]["median"],
            "std": np.sqrt(stats["retrieval_total"]["std"]**2 + stats["llm_generation"]["std"]**2),
            "min": stats["retrieval_total"]["min"] + stats["llm_generation"]["min"],
            "max": stats["retrieval_total"]["max"] + stats["llm_generation"]["max"]
        }
    else:
        print("No valid LLM latency captured (API failures).")
        stats["llm_generation"] = {"mean": 0, "median": 0, "std": 0, "min": 0, "max": 0}
        stats["end_to_end"] = stats["retrieval_total"]

    out_json = os.path.join(os.path.dirname(__file__), 'results', '04_latency_stats.json')
    with open(out_json, 'w') as f:
        json.dump(stats, f, indent=2)

    # Flatten for CSV
    flattened = []
    for k, v in stats.items():
        row = {"component": k}
        row.update(v)
        flattened.append(row)
        
    out_csv = os.path.join(os.path.dirname(__file__), 'results', '04_latency_results.csv')
    with open(out_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["component", "mean", "median", "std", "min", "max"])
        writer.writeheader()
        writer.writerows(flattened)
        
    print("Latency experiment completed.")
    print(json.dumps(stats, indent=2))

if __name__ == "__main__":
    evaluate_latency()
