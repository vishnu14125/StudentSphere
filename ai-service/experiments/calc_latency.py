import os
import sys
import json
import time
import math
import csv
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.rag_pipeline import get_rag_pipeline
from app.config import settings

rag = get_rag_pipeline()

file_path = os.path.join(os.path.dirname(__file__), 'results/evaluation_queries_v3_enriched.json')
with open(file_path, 'r', encoding='utf-8') as f:
    queries = json.load(f)

latency_results = []
metrics = {
    'emb': [],
    'vec': [],
    'retrieval': [],
    'llm': [],
    'total': []
}

for i, q in enumerate(queries):
    q_text = q['query']
    print(f"[{i+1}/{len(queries)}] Processing query: {q_text}")
    
    t_start = time.time()
    
    # 1. Query Embedding
    t0 = time.time()
    query_emb = rag.embedding_service.generate_embedding(q_text)
    t_emb = time.time() - t0
    
    # 2. Vector Search
    t0 = time.time()
    results = rag.vector_store.search(query_emb, n_results=settings.rag_top_k, where=None)
    
    contexts = []
    if results.get('ids') and results['ids'][0]:
        for idx, result_id in enumerate(results['ids'][0]):
            score = results['distances'][0][idx] if results.get('distances') else 0
            if score >= settings.rag_similarity_threshold:
                contexts.append({
                    'id': result_id, 
                    'text': results['documents'][0][idx], 
                    'metadata': results['metadatas'][0][idx] if results.get('metadatas') else {}, 
                    'score': score
                })
    t_vec = time.time() - t0
    
    # Total Retrieval
    t_retrieval = t_emb + t_vec
    
    # Formatting for LLM (as in pipeline)
    snippets_for_llm = []
    for context in contexts:
        text = context['text'].strip()
        meta = context.get('metadata', {})
        company = meta.get('companyName', 'Unknown company')
        role = meta.get('role', 'Unknown role')
        snippets_for_llm.append(f"Source: {company} - {role}\nContent: {text}")
        
    # 4. LLM Generation
    t0 = time.time()
    llm_response = rag.llm_service.generate_answer(q_text, snippets_for_llm)
    t_llm = time.time() - t0
    
    # End-to-end
    t_total = time.time() - t_start
    
    res = {
        'query_id': q['query_id'],
        'query': q_text,
        'embedding_ms': t_emb * 1000,
        'vector_ms': t_vec * 1000,
        'retrieval_ms': t_retrieval * 1000,
        'llm_ms': t_llm * 1000,
        'total_ms': t_total * 1000,
        'success': llm_response['success']
    }
    latency_results.append(res)
    
    metrics['emb'].append(res['embedding_ms'])
    metrics['vec'].append(res['vector_ms'])
    metrics['retrieval'].append(res['retrieval_ms'])
    metrics['llm'].append(res['llm_ms'])
    metrics['total'].append(res['total_ms'])
    
    time.sleep(2.0) # avoid Gemini rate limits

# Calculate Stats
stats = {}
for key, values in metrics.items():
    stats[key] = {
        'mean': np.mean(values),
        'median': np.median(values),
        'min': np.min(values),
        'max': np.max(values),
        'std': np.std(values)
    }

out_dir = os.path.join(os.path.dirname(__file__), 'results')

with open(os.path.join(out_dir, 'latency_evaluation_v3.json'), 'w', encoding='utf-8') as f:
    json.dump({'statistics': stats, 'raw': latency_results}, f, indent=2)

with open(os.path.join(out_dir, 'latency_evaluation_v3.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['query_id', 'embedding_ms', 'vector_ms', 'retrieval_ms', 'llm_ms', 'total_ms'])
    for res in latency_results:
        writer.writerow([res['query_id'], res['embedding_ms'], res['vector_ms'], res['retrieval_ms'], res['llm_ms'], res['total_ms']])

# Visualization
labels = ['Embedding', 'Vector Search', 'Total Retrieval', 'LLM Gen', 'End-to-End Total']
keys = ['emb', 'vec', 'retrieval', 'llm', 'total']
means = [stats[k]['mean'] for k in keys]
stds = [stats[k]['std'] for k in keys]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(labels, means, yerr=stds, capsize=5, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
ax.set_ylabel('Latency (ms)')
ax.set_title('End-to-End RAG Latency Evaluation')
for i, v in enumerate(means):
    ax.text(i, v + stds[i] + (max(means)*0.02), f'{v:.1f} ms', ha='center')

plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, 'figures', 'fig_latency_evaluation_v3.png'))

print("Latency Evaluation Results (ms)")
print("| Component | Mean | Median | Min | Max | Std Dev |")
print("|---|---:|---:|---:|---:|---:|")
for k, l in zip(keys, labels):
    print(f"| {l} | {stats[k]['mean']:.2f} | {stats[k]['median']:.2f} | {stats[k]['min']:.2f} | {stats[k]['max']:.2f} | {stats[k]['std']:.2f} |")
