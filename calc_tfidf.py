import json
import os
import math
import csv
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as sklearn_cosine

file_path = 'ai-service/experiments/results/evaluation_queries_v3_enriched.json'
corpus_path = 'ai-service/datasets/research_corpus.json'

with open(file_path, 'r', encoding='utf-8') as f:
    queries = json.load(f)

with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)

doc_texts = [d['experienceText'] for d in corpus]
doc_ids = [d['id'] for d in corpus]
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(doc_texts)

def dcg_at_k(r, k):
    r = r[:k]
    return sum((rel / math.log2(idx + 2)) for idx, rel in enumerate(r))

def ndcg_at_k(r, k):
    dcg = dcg_at_k(r, k)
    ideal_r = sorted(r, reverse=True)
    idcg = dcg_at_k(ideal_r, k)
    if idcg == 0:
        return 0.0
    return dcg / idcg

def calc_metrics(rels_graded, total_relevant_in_pool):
    rels_binary = [1 if r >= 1 else 0 for r in rels_graded]
    
    p3 = sum(rels_binary[:3]) / 3
    p5 = sum(rels_binary[:5]) / 5
    p10 = sum(rels_binary[:10]) / 10
    
    r3 = sum(rels_binary[:3]) / total_relevant_in_pool if total_relevant_in_pool > 0 else 0
    r5 = sum(rels_binary[:5]) / total_relevant_in_pool if total_relevant_in_pool > 0 else 0
    r10 = sum(rels_binary[:10]) / total_relevant_in_pool if total_relevant_in_pool > 0 else 0
    
    mrr = 0
    for rank, rel in enumerate(rels_binary):
        if rel == 1:
            mrr = 1.0 / (rank + 1)
            break
            
    ndcg10 = ndcg_at_k(rels_graded, 10)
    
    return {'P@3': p3, 'P@5': p5, 'P@10': p10, 'R@3': r3, 'R@5': r5, 'R@10': r10, 'MRR': mrr, 'NDCG@10': ndcg10}

results = []
macro_sem = {'P@3': 0, 'P@5': 0, 'P@10': 0, 'R@3': 0, 'R@5': 0, 'R@10': 0, 'MRR': 0, 'NDCG@10': 0}
macro_tfidf = {'P@3': 0, 'P@5': 0, 'P@10': 0, 'R@3': 0, 'R@5': 0, 'R@10': 0, 'MRR': 0, 'NDCG@10': 0}

for q in queries:
    qid = q['query_id']
    q_text = q['query']
    
    sem_cands = sorted(q['candidates'], key=lambda x: x['rank'])
    sem_rels_graded = [c['relevance'] for c in sem_cands]
    
    rel_map = {c['doc_id']: c['relevance'] for c in sem_cands}
    total_relevant = sum(1 for r in sem_rels_graded if r >= 1)
    
    sem_metrics = calc_metrics(sem_rels_graded, total_relevant)
    
    q_vec = vectorizer.transform([q_text])
    sims = sklearn_cosine(q_vec, tfidf_matrix).flatten()
    top_indices = sims.argsort()[::-1][:10]
    tfidf_retrieved = [doc_ids[i] for i in top_indices]
    
    tfidf_rels_graded = [rel_map.get(doc_id, 0) for doc_id in tfidf_retrieved]
    tfidf_metrics = calc_metrics(tfidf_rels_graded, total_relevant)
    
    res = {
        'query_id': qid,
        'semantic': sem_metrics,
        'tfidf': tfidf_metrics
    }
    results.append(res)
    
    for k in macro_sem:
        macro_sem[k] += sem_metrics[k]
        macro_tfidf[k] += tfidf_metrics[k]

total_queries = len(queries)
for k in macro_sem:
    macro_sem[k] /= total_queries
    macro_tfidf[k] /= total_queries

counts = {k: {'better': 0, 'equal': 0, 'worse': 0} for k in ['P@5', 'R@5', 'MRR', 'NDCG@10']}
for res in results:
    for k in counts.keys():
        s = res['semantic'][k]
        t = res['tfidf'][k]
        if s > t: counts[k]['better'] += 1
        elif s < t: counts[k]['worse'] += 1
        else: counts[k]['equal'] += 1

out_dir = 'ai-service/experiments/results'
with open(os.path.join(out_dir, 'tfidf_vs_semantic_v3.json'), 'w', encoding='utf-8') as f:
    json.dump({'macro_semantic': macro_sem, 'macro_tfidf': macro_tfidf, 'per_query': results}, f, indent=2)

with open(os.path.join(out_dir, 'tfidf_vs_semantic_v3.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['query_id', 'Method', 'P@3', 'P@5', 'P@10', 'R@3', 'R@5', 'R@10', 'MRR', 'NDCG@10'])
    for res in results:
        writer.writerow([res['query_id'], 'Semantic', res['semantic']['P@3'], res['semantic']['P@5'], res['semantic']['P@10'], res['semantic']['R@3'], res['semantic']['R@5'], res['semantic']['R@10'], res['semantic']['MRR'], res['semantic']['NDCG@10']])
        writer.writerow([res['query_id'], 'TF-IDF', res['tfidf']['P@3'], res['tfidf']['P@5'], res['tfidf']['P@10'], res['tfidf']['R@3'], res['tfidf']['R@5'], res['tfidf']['R@10'], res['tfidf']['MRR'], res['tfidf']['NDCG@10']])

metrics_to_plot = ['P@5', 'R@5', 'MRR', 'NDCG@10']
sem_vals = [macro_sem[m] for m in metrics_to_plot]
tfidf_vals = [macro_tfidf[m] for m in metrics_to_plot]

x = np.arange(len(metrics_to_plot))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, tfidf_vals, width, label='TF-IDF')
rects2 = ax.bar(x + width/2, sem_vals, width, label='Semantic')

ax.set_ylabel('Scores')
ax.set_title('Semantic Retrieval vs TF-IDF Baseline')
ax.set_xticks(x)
ax.set_xticklabels(metrics_to_plot)
ax.legend()
plt.savefig(os.path.join(out_dir, 'figures', 'fig_tfidf_vs_semantic_v3.png'))

print('1. Overall comparison table')
print('| Method | P@3 | P@5 | P@10 | R@3 | R@5 | R@10 | MRR | NDCG@10 |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
print(f'| TF-IDF | {macro_tfidf["P@3"]:.4f} | {macro_tfidf["P@5"]:.4f} | {macro_tfidf["P@10"]:.4f} | {macro_tfidf["R@3"]:.4f} | {macro_tfidf["R@5"]:.4f} | {macro_tfidf["R@10"]:.4f} | {macro_tfidf["MRR"]:.4f} | {macro_tfidf["NDCG@10"]:.4f} |')
print(f'| Semantic Retrieval | {macro_sem["P@3"]:.4f} | {macro_sem["P@5"]:.4f} | {macro_sem["P@10"]:.4f} | {macro_sem["R@3"]:.4f} | {macro_sem["R@5"]:.4f} | {macro_sem["R@10"]:.4f} | {macro_sem["MRR"]:.4f} | {macro_sem["NDCG@10"]:.4f} |')

print('\n2. Absolute improvement (Semantic - TF-IDF)')
for k in macro_sem:
    diff = macro_sem[k] - macro_tfidf[k]
    print(f'- {k}: {diff:+.4f}')
    
print('\n3. Per-query comparison summary (Semantic Better / Equal / Worse)')
for k in counts:
    print(f'- {k}: {counts[k]["better"]} Better / {counts[k]["equal"]} Equal / {counts[k]["worse"]} Worse')
