import os
import sys
import json
import math
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import stats

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.embeddings.embeddings import get_embedding_service
from app.config import settings

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)

def compute_dcg(relevances, k):
    dcg = 0.0
    for i in range(min(k, len(relevances))):
        dcg += (2 ** relevances[i] - 1) / math.log2(i + 2)
    return dcg

def compute_ndcg(retrieved_rels, ideal_rels, k):
    dcg = compute_dcg(retrieved_rels, k)
    idcg = compute_dcg(sorted(ideal_rels, reverse=True), k)
    if idcg == 0: return 0.0
    return dcg / idcg

def calc_metrics(retrieved_docs, query_ground_truth):
    """
    retrieved_docs: list of retrieved doc_ids
    query_ground_truth: dict mapping doc_id -> relevance (0, 1, 2)
    """
    total_relevant = sum(1 for rel in query_ground_truth.values() if rel >= 1)
    
    bin_rels = [1 if query_ground_truth.get(doc, 0) >= 1 else 0 for doc in retrieved_docs]
    graded_rels = [query_ground_truth.get(doc, 0) for doc in retrieved_docs]
    ideal_rels = list(query_ground_truth.values())
    
    p3 = sum(bin_rels[:3]) / 3.0
    p5 = sum(bin_rels[:5]) / 5.0
    p10 = sum(bin_rels[:10]) / 10.0
    
    r3 = sum(bin_rels[:3]) / total_relevant if total_relevant > 0 else 0.0
    r5 = sum(bin_rels[:5]) / total_relevant if total_relevant > 0 else 0.0
    r10 = sum(bin_rels[:10]) / total_relevant if total_relevant > 0 else 0.0
    
    mrr = 0.0
    for i, rel in enumerate(bin_rels):
        if rel == 1:
            mrr = 1.0 / (i + 1)
            break
            
    ndcg5 = compute_ndcg(graded_rels, ideal_rels, k=5)
    ndcg10 = compute_ndcg(graded_rels, ideal_rels, k=10)
    
    unjudged = sum(1 for doc in retrieved_docs if doc not in query_ground_truth)
    
    return p3, r3, p5, r5, p10, r10, mrr, ndcg5, ndcg10, unjudged

def main():
    print("Loading data...")
    corpus_path = os.path.join(os.path.dirname(__file__), '../datasets/research_corpus.json')
    pooled_path = os.path.join(os.path.dirname(__file__), 'results/pooled_evaluation_v4.json')
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    valid_doc_ids = {doc['id'] for doc in corpus}
        
    with open(pooled_path, 'r', encoding='utf-8') as f:
        pooled_data = json.load(f)
        
    # Validation
    queries = []
    total_pooled = 0
    null_rels = 0
    invalid_rels = 0
    query_ids = set()
    
    ground_truth = {}
    
    for q in pooled_data:
        qid = q['query_id']
        query_ids.add(qid)
        queries.append((qid, q['query']))
        
        ground_truth[qid] = {}
        
        seen_docs = set()
        for cand in q['pooled_candidates']:
            doc_id = cand['doc_id']
            rel = cand['relevance']
            
            if doc_id in seen_docs:
                print(f"FAILED: Duplicate candidate {doc_id} in query {qid}")
                sys.exit(1)
            seen_docs.add(doc_id)
            
            total_pooled += 1
            if rel is None: null_rels += 1
            elif rel not in [0, 1, 2]: invalid_rels += 1
            
            if doc_id not in valid_doc_ids:
                print(f"FAILED: Invalid corpus document ID {doc_id}")
                sys.exit(1)
                
            ground_truth[qid][doc_id] = rel

    if len(query_ids) != 15:
        print(f"FAILED: Expected 15 queries, found {len(query_ids)}")
        sys.exit(1)
    if total_pooled != 225:
        print(f"FAILED: Expected 225 candidates, found {total_pooled}")
        sys.exit(1)
    if null_rels > 0:
        print(f"FAILED: Found {null_rels} null relevance values")
        sys.exit(1)
    if invalid_rels > 0:
        print(f"FAILED: Found {invalid_rels} invalid relevance values")
        sys.exit(1)
        
    print("Validation passed. Data integrity verified.")
    
    # TF-IDF Setup
    print("Running TF-IDF Retrieval...")
    doc_ids = [doc['id'] for doc in corpus]
    texts = [doc['experienceText'] for doc in corpus]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Semantic Setup
    print("Running Semantic Retrieval...")
    emb_service = get_embedding_service()
    chunk_embeddings = []
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
            
    # Evaluation Loop
    results = []
    total_unjudged = 0
    
    for qid, query_text in queries:
        gt = ground_truth[qid]
        
        # TF-IDF Retrieval
        query_tfidf = vectorizer.transform([query_text])
        from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
        tfidf_sims = sk_cosine(query_tfidf, tfidf_matrix)[0]
        sorted_indices = np.argsort(tfidf_sims)[::-1]
        retrieved_tfidf = [doc_ids[idx] for idx in sorted_indices[:10]]
        
        # Semantic Retrieval
        q_emb = emb_service.generate_embedding(query_text)
        scores_chunk = []
        for item in chunk_embeddings:
            score = cosine_similarity(q_emb, item['embedding'])
            scores_chunk.append((item['doc_id'], score))
        scores_chunk.sort(key=lambda x: x[1], reverse=True)
        
        retrieved_semantic = []
        seen = set()
        for doc_id, _ in scores_chunk:
            if doc_id not in seen:
                seen.add(doc_id)
                retrieved_semantic.append(doc_id)
            if len(retrieved_semantic) == 10:
                break
                
        # Metrics
        tf_p3, tf_r3, tf_p5, tf_r5, tf_p10, tf_r10, tf_mrr, tf_n5, tf_n10, tf_unj = calc_metrics(retrieved_tfidf, gt)
        se_p3, se_r3, se_p5, se_r5, se_p10, se_r10, se_mrr, se_n5, se_n10, se_unj = calc_metrics(retrieved_semantic, gt)
        
        total_unjudged += (tf_unj + se_unj)
        
        results.append({
            'query_id': qid,
            'query': query_text,
            'tfidf': {
                'P@3': tf_p3, 'R@3': tf_r3, 'P@5': tf_p5, 'R@5': tf_r5, 'P@10': tf_p10, 'R@10': tf_r10,
                'MRR': tf_mrr, 'nDCG@5': tf_n5, 'nDCG@10': tf_n10, 'unjudged': tf_unj
            },
            'semantic': {
                'P@3': se_p3, 'R@3': se_r3, 'P@5': se_p5, 'R@5': se_r5, 'P@10': se_p10, 'R@10': se_r10,
                'MRR': se_mrr, 'nDCG@5': se_n5, 'nDCG@10': se_n10, 'unjudged': se_unj
            }
        })
        
    # Aggregate
    agg = {'tfidf': {}, 'semantic': {}}
    metrics = ['P@3', 'R@3', 'P@5', 'R@5', 'P@10', 'R@10', 'MRR', 'nDCG@5', 'nDCG@10']
    
    for m in metrics:
        agg['tfidf'][m] = np.mean([r['tfidf'][m] for r in results])
        agg['semantic'][m] = np.mean([r['semantic'][m] for r in results])
        
    # Statistical paired t-test for nDCG@10
    tf_ndcg10 = [r['tfidf']['nDCG@10'] for r in results]
    se_ndcg10 = [r['semantic']['nDCG@10'] for r in results]
    t_stat, p_val = stats.ttest_rel(se_ndcg10, tf_ndcg10)
    
    tf_mrr_arr = [r['tfidf']['MRR'] for r in results]
    se_mrr_arr = [r['semantic']['MRR'] for r in results]
    mrr_t_stat, mrr_p_val = stats.ttest_rel(se_mrr_arr, tf_mrr_arr)
    
    out_json = {
        'metadata': {'queries': 15, 'pooled_candidates': 225},
        'aggregate': agg,
        'statistics': {
            'nDCG@10': {'p_value': p_val, 't_stat': t_stat},
            'MRR': {'p_value': mrr_p_val, 't_stat': mrr_t_stat}
        },
        'unjudged_total': total_unjudged,
        'query_results': results
    }
    
    json_path = os.path.join(os.path.dirname(__file__), 'results/final_fair_evaluation_v5.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(out_json, f, indent=2)
        
    # Generate Markdown Report
    md_path = os.path.join(os.path.dirname(__file__), 'results/FINAL_FAIR_EVALUATION_REPORT.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# FINAL FAIR RETRIEVAL EVALUATION REPORT\n\n")
        f.write("## 1. Overview\n")
        f.write("This report presents the final fair comparison between TF-IDF lexical retrieval and Semantic Retrieval (sentence-transformers/all-MiniLM-L6-v2).\n")
        f.write(f"- **Queries:** 15\n")
        f.write(f"- **Pooled candidates evaluated:** 225\n")
        f.write(f"- **Total unjudged candidates retrieved:** {total_unjudged}\n\n")
        
        f.write("## 2. Aggregate Results\n\n")
        f.write("| Metric | TF-IDF | Semantic | Absolute Difference | Relative Improvement % |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for m in metrics:
            tf_v = agg['tfidf'][m]
            se_v = agg['semantic'][m]
            diff = se_v - tf_v
            rel = (diff / tf_v * 100) if tf_v > 0 else 0
            rel_str = f"{rel:+.1f}%" if tf_v > 0 else "N/A"
            f.write(f"| {m} | {tf_v:.3f} | {se_v:.3f} | {diff:+.3f} | {rel_str} |\n")
            
        f.write("\n## 3. Statistical Analysis (Paired t-test)\n")
        f.write(f"- **nDCG@10:** p-value = {p_val:.4f}. Null hypothesis: No difference in means. Interpretation: {'Statistically significant (p < 0.05)' if p_val < 0.05 else 'Not statistically significant (p >= 0.05)'}.\n")
        f.write(f"- **MRR:** p-value = {mrr_p_val:.4f}. Null hypothesis: No difference in means. Interpretation: {'Statistically significant (p < 0.05)' if mrr_p_val < 0.05 else 'Not statistically significant (p >= 0.05)'}.\n\n")
        
        f.write("## 4. Query-Level Results\n\n")
        f.write("| Query ID | Query | TF-IDF P@5 | Sem P@5 | TF-IDF R@5 | Sem R@5 | TF-IDF MRR | Sem MRR | TF-IDF nDCG@5 | Sem nDCG@5 |\n")
        f.write("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|\n")
        for r in results:
            f.write(f"| {r['query_id']} | {r['query']} | {r['tfidf']['P@5']:.3f} | {r['semantic']['P@5']:.3f} | {r['tfidf']['R@5']:.3f} | {r['semantic']['R@5']:.3f} | {r['tfidf']['MRR']:.3f} | {r['semantic']['MRR']:.3f} | {r['tfidf']['nDCG@5']:.3f} | {r['semantic']['nDCG@5']:.3f} |\n")
            
    print("\nFINAL FAIR RETRIEVAL EVALUATION\n")
    print("Queries: 15")
    print("Pooled candidates: 225\n")
    
    print("TF-IDF:")
    for m in metrics:
        print(f"{m} = {agg['tfidf'][m]:.3f}")
        
    print("\nSemantic:")
    for m in metrics:
        print(f"{m} = {agg['semantic'][m]:.3f}")
        
    print("\nCOMPARISON:")
    for m in metrics:
        tf_v = agg['tfidf'][m]
        se_v = agg['semantic'][m]
        diff = se_v - tf_v
        rel_str = f"{(diff / tf_v * 100):+.1f}%" if tf_v > 0 else "N/A"
        print(f"{m}: Diff {diff:+.3f} | Rel {rel_str}")
        
    print(f"\nUnjudged retrieved candidates: {total_unjudged}")
    print("\nValidation status: PASSED")
    print(f"\nSaved JSON: {json_path}")
    print(f"Saved Markdown: {md_path}")

if __name__ == '__main__':
    main()
