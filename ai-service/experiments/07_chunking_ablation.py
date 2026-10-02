import os
import sys
import json
import csv
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.embeddings.embeddings import get_embedding_service
from app.config import settings

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)

def compute_dcg(relevances, k=10):
    dcg = 0.0
    for i in range(min(k, len(relevances))):
        dcg += (2 ** relevances[i] - 1) / math.log2(i + 2)
    return dcg

def compute_ndcg(retrieved_rels, ideal_rels, k=10):
    dcg = compute_dcg(retrieved_rels, k)
    idcg = compute_dcg(sorted(ideal_rels, reverse=True), k)
    if idcg == 0: return 0.0
    return dcg / idcg

def calc_metrics(retrieved_docs, query_ground_truth):
    """
    retrieved_docs: list of doc_ids
    query_ground_truth: dict mapping doc_id to relevance score (0, 1, 2)
    Returns: P@3, P@5, P@10, R@3, R@5, R@10, MRR, NDCG@10
    """
    # Number of relevant documents in ground truth (relevance >= 1)
    total_relevant = sum(1 for rel in query_ground_truth.values() if rel >= 1)
    if total_relevant == 0:
        return 0, 0, 0, 0, 0, 0, 0, 0
    
    # Binary relevances for P/R/MRR
    bin_rels = [1 if query_ground_truth.get(doc, 0) >= 1 else 0 for doc in retrieved_docs]
    
    # Graded relevances for NDCG
    graded_rels = [query_ground_truth.get(doc, 0) for doc in retrieved_docs]
    ideal_rels = list(query_ground_truth.values())
    
    p3 = sum(bin_rels[:3]) / 3.0
    p5 = sum(bin_rels[:5]) / 5.0
    p10 = sum(bin_rels[:10]) / 10.0
    
    r3 = sum(bin_rels[:3]) / total_relevant
    r5 = sum(bin_rels[:5]) / total_relevant
    r10 = sum(bin_rels[:10]) / total_relevant
    
    mrr = 0.0
    for i, rel in enumerate(bin_rels):
        if rel == 1:
            mrr = 1.0 / (i + 1)
            break
            
    ndcg10 = compute_ndcg(graded_rels, ideal_rels, k=10)
    
    return p3, p5, p10, r3, r5, r10, mrr, ndcg10

def main():
    print("Loading data...")
    corpus_path = os.path.join(os.path.dirname(__file__), '../datasets/research_corpus.json')
    eval_path = os.path.join(os.path.dirname(__file__), 'results/evaluation_queries_v3_enriched.json')
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
        
    with open(eval_path, 'r', encoding='utf-8') as f:
        eval_queries = json.load(f)
        
    emb_service = get_embedding_service()
    
    print("Generating Whole Document Embeddings (Ablation)...")
    t0 = time.time()
    whole_doc_embeddings = []
    for doc in corpus:
        emb = emb_service.generate_embedding(doc['experienceText'])
        whole_doc_embeddings.append({
            'doc_id': doc['id'],
            'embedding': emb
        })
    time_whole = time.time() - t0
    
    print("Generating Sentence-Aware Chunk Embeddings (Proposed)...")
    t0 = time.time()
    chunk_embeddings = []
    total_chunks = 0
    for doc in corpus:
        chunks = emb_service.generate_chunks_embedding(
            doc['experienceText'], 
            chunk_max_words=150, 
            chunk_overlap_words=30
        )
        for chunk_text, emb in chunks:
            chunk_embeddings.append({
                'doc_id': doc['id'],
                'embedding': emb
            })
            total_chunks += 1
    time_chunk = time.time() - t0
    
    avg_chunks_per_doc = total_chunks / len(corpus)
    print(f"Total whole documents: {len(corpus)}")
    print(f"Total chunks generated: {total_chunks} (Avg {avg_chunks_per_doc:.2f} per doc)")
    
    results = []
    
    t0_retrieval_whole = 0
    t0_retrieval_chunk = 0
    
    for q in eval_queries:
        query_text = q['query']
        query_id = q['query_id']
        
        # Build ground truth dict
        # We only have ground truth for the 10 candidates already evaluated.
        # But this is a standard pooling evaluation setup (the pool is from earlier runs).
        gt = {cand['doc_id']: cand['relevance'] for cand in q['candidates']}
        
        # Embed query
        q_emb = emb_service.generate_embedding(query_text)
        
        # A. Whole Document Retrieval
        t_start = time.time()
        scores_whole = []
        for item in whole_doc_embeddings:
            score = cosine_similarity(q_emb, item['embedding'])
            scores_whole.append((item['doc_id'], score))
        scores_whole.sort(key=lambda x: x[1], reverse=True)
        retrieved_whole = [doc_id for doc_id, _ in scores_whole[:10]]
        t0_retrieval_whole += (time.time() - t_start)
        
        # B. Chunk Retrieval (Mapping to parent doc)
        t_start = time.time()
        scores_chunk = []
        for item in chunk_embeddings:
            score = cosine_similarity(q_emb, item['embedding'])
            scores_chunk.append((item['doc_id'], score))
        scores_chunk.sort(key=lambda x: x[1], reverse=True)
        
        # Unique parent doc retrieval
        retrieved_chunk = []
        seen = set()
        for doc_id, _ in scores_chunk:
            if doc_id not in seen:
                seen.add(doc_id)
                retrieved_chunk.append(doc_id)
            if len(retrieved_chunk) == 10:
                break
        t0_retrieval_chunk += (time.time() - t_start)
        
        # Calc metrics
        pw3, pw5, pw10, rw3, rw5, rw10, mrrw, ndcgw = calc_metrics(retrieved_whole, gt)
        pc3, pc5, pc10, rc3, rc5, rc10, mrrc, ndcgc = calc_metrics(retrieved_chunk, gt)
        
        results.append({
            'query_id': query_id,
            'query': query_text,
            'whole_p3': pw3, 'whole_p5': pw5, 'whole_p10': pw10,
            'whole_r3': rw3, 'whole_r5': rw5, 'whole_r10': rw10,
            'whole_mrr': mrrw, 'whole_ndcg10': ndcgw,
            'chunk_p3': pc3, 'chunk_p5': pc5, 'chunk_p10': pc10,
            'chunk_r3': rc3, 'chunk_r5': rc5, 'chunk_r10': rc10,
            'chunk_mrr': mrrc, 'chunk_ndcg10': ndcgc
        })
        
    # Aggregate
    agg = {}
    for k in ['p3', 'p5', 'p10', 'r3', 'r5', 'r10', 'mrr', 'ndcg10']:
        agg[f'whole_{k}'] = np.mean([r[f'whole_{k}'] for r in results])
        agg[f'chunk_{k}'] = np.mean([r[f'chunk_{k}'] for r in results])
        agg[f'diff_{k}'] = agg[f'chunk_{k}'] - agg[f'whole_{k}']
        
    # Better/Equal/Worse for P@5
    better_p5 = sum(1 for r in results if r['chunk_p5'] > r['whole_p5'])
    worse_p5 = sum(1 for r in results if r['chunk_p5'] < r['whole_p5'])
    equal_p5 = sum(1 for r in results if r['chunk_p5'] == r['whole_p5'])
    
    better_r5 = sum(1 for r in results if r['chunk_r5'] > r['whole_r5'])
    worse_r5 = sum(1 for r in results if r['chunk_r5'] < r['whole_r5'])
    equal_r5 = sum(1 for r in results if r['chunk_r5'] == r['whole_r5'])

    out_data = {
        'summary': agg,
        'statistics': {
            'whole_documents': len(corpus),
            'total_chunks': total_chunks,
            'avg_chunks_per_doc': avg_chunks_per_doc,
            'avg_latency_whole_ms': (t0_retrieval_whole / 15) * 1000,
            'avg_latency_chunk_ms': (t0_retrieval_chunk / 15) * 1000
        },
        'wins': {
            'p5': {'chunk_better': better_p5, 'chunk_worse': worse_p5, 'equal': equal_p5},
            'r5': {'chunk_better': better_r5, 'chunk_worse': worse_r5, 'equal': equal_r5}
        },
        'per_query': results
    }
    
    # Save JSON
    out_json = os.path.join(os.path.dirname(__file__), 'results/chunking_ablation_v3.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, indent=2)
        
    # Save CSV
    out_csv = os.path.join(os.path.dirname(__file__), 'results/chunking_ablation_v3.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    # Plot
    labels = ['P@3', 'P@5', 'P@10', 'Recall@5', 'MRR', 'NDCG@10']
    whole_vals = [agg['whole_p3'], agg['whole_p5'], agg['whole_p10'], agg['whole_r5'], agg['whole_mrr'], agg['whole_ndcg10']]
    chunk_vals = [agg['chunk_p3'], agg['chunk_p5'], agg['chunk_p10'], agg['chunk_r5'], agg['chunk_mrr'], agg['chunk_ndcg10']]
    
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, whole_vals, width, label='Whole Document')
    rects2 = ax.bar(x + width/2, chunk_vals, width, label='Sentence-Aware Chunking')
    
    ax.set_ylabel('Score')
    ax.set_title('Chunking Ablation: Whole-Doc vs Chunking')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)
                        
    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    out_png = os.path.join(os.path.dirname(__file__), 'results/figures/fig_chunking_ablation_v3.png')
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.savefig(out_png)
    
    print("\nOVERALL COMPARISON")
    print(f"| Representation | P@3 | P@5 | P@10 | R@3 | R@5 | R@10 | MRR | NDCG@10 |")
    print(f"|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    print(f"| Whole Document | {agg['whole_p3']:.3f} | {agg['whole_p5']:.3f} | {agg['whole_p10']:.3f} | {agg['whole_r3']:.3f} | {agg['whole_r5']:.3f} | {agg['whole_r10']:.3f} | {agg['whole_mrr']:.3f} | {agg['whole_ndcg10']:.3f} |")
    print(f"| Sentence-Aware Chunking | {agg['chunk_p3']:.3f} | {agg['chunk_p5']:.3f} | {agg['chunk_p10']:.3f} | {agg['chunk_r3']:.3f} | {agg['chunk_r5']:.3f} | {agg['chunk_r10']:.3f} | {agg['chunk_mrr']:.3f} | {agg['chunk_ndcg10']:.3f} |")
    
    print("\nABSOLUTE DIFFERENCE (Chunking - Whole)")
    print(f"P@3: {agg['diff_p3']:+.3f}")
    print(f"P@5: {agg['diff_p5']:+.3f}")
    print(f"P@10: {agg['diff_p10']:+.3f}")
    print(f"R@5: {agg['diff_r5']:+.3f}")
    print(f"MRR: {agg['diff_mrr']:+.3f}")
    print(f"NDCG@10: {agg['diff_ndcg10']:+.3f}")
    
    print("\nCHUNKING STATISTICS")
    print(f"Number of whole-document vectors: {len(corpus)}")
    print(f"Number of chunks generated: {total_chunks}")
    print(f"Average chunks per document: {avg_chunks_per_doc:.2f}")
    
    print("\nRETRIEVAL LATENCY COMPARISON")
    print(f"Whole Document Avg Latency: {(t0_retrieval_whole / 15) * 1000:.2f} ms")
    print(f"Sentence-Aware Chunking Avg Latency: {(t0_retrieval_chunk / 15) * 1000:.2f} ms")
    
    print(f"\nNumber of queries where Proposed is better for P@5: {better_p5}")
    print(f"Number of queries where Proposed is worse for P@5: {worse_p5}")
    print(f"Number of queries where equal for P@5: {equal_p5}")

if __name__ == '__main__':
    main()
