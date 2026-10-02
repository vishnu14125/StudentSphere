import json
import os
import math
import csv

file_path = 'ai-service/experiments/results/evaluation_queries_v3_enriched.json'

with open(file_path, 'r', encoding='utf-8') as f:
    queries = json.load(f)

# VALIDATION
total_queries = len(queries)
total_candidates = sum(len(q['candidates']) for q in queries)
null_count = 0
valid_values = True
for q in queries:
    for cand in q['candidates']:
        val = cand.get('relevance')
        if val is None:
            null_count += 1
        elif val not in [0, 1, 2]:
            valid_values = False

assert total_queries == 15, 'Total queries must be 15'
assert all(len(q['candidates']) == 10 for q in queries), 'Each query must have 10 candidates'
assert total_candidates == 150, 'Total candidates must be 150'
assert null_count == 0, 'No relevance value can be null'
assert valid_values, 'Every relevance value must be 0, 1, or 2'

# METRIC CALCULATION
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

results = []
macro = {'P@3': 0, 'P@5': 0, 'P@10': 0, 'R@3': 0, 'R@5': 0, 'R@10': 0, 'MRR': 0, 'NDCG@10': 0}

for q in queries:
    qid = q['query_id']
    rels_graded = [c['relevance'] for c in sorted(q['candidates'], key=lambda x: x['rank'])]
    rels_binary = [1 if r >= 1 else 0 for r in rels_graded]
    
    total_relevant_in_pool = sum(rels_binary)
    
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
    
    res = {
        'query_id': qid,
        'P@3': p3,
        'P@5': p5,
        'P@10': p10,
        'R@3': r3,
        'R@5': r5,
        'R@10': r10,
        'MRR': mrr,
        'NDCG@10': ndcg10
    }
    results.append(res)
    
    for k in macro:
        macro[k] += res[k]
        
for k in macro:
    macro[k] /= total_queries

out_dir = 'ai-service/experiments/results'
with open(os.path.join(out_dir, 'retrieval_evaluation_human_v3.json'), 'w', encoding='utf-8') as f:
    json.dump({'macro_averages': macro, 'per_query': results}, f, indent=2)

with open(os.path.join(out_dir, 'retrieval_evaluation_human_v3.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['query_id', 'P@3', 'P@5', 'P@10', 'R@3', 'R@5', 'R@10', 'MRR', 'NDCG@10'])
    writer.writeheader()
    for res in results:
        writer.writerow(res)

print('\nB. Overall results table\n')
print('| Metric | Score |')
print('|---|---:|')
print(f'| Precision@3 | {macro["P@3"]:.4f} |')
print(f'| Precision@5 | {macro["P@5"]:.4f} |')
print(f'| Precision@10 | {macro["P@10"]:.4f} |')
print(f'| Recall@3 | {macro["R@3"]:.4f} |')
print(f'| Recall@5 | {macro["R@5"]:.4f} |')
print(f'| Recall@10 | {macro["R@10"]:.4f} |')
print(f'| MRR | {macro["MRR"]:.4f} |')
print(f'| NDCG@10 | {macro["NDCG@10"]:.4f} |')

print('\nC. Per-query results\n')
print('| Query | P@3 | P@5 | P@10 | Recall@3 | Recall@5 | Recall@10 | RR | NDCG@10 |')
print('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in results:
    print(f'| {r["query_id"]} | {r["P@3"]:.4f} | {r["P@5"]:.4f} | {r["P@10"]:.4f} | {r["R@3"]:.4f} | {r["R@5"]:.4f} | {r["R@10"]:.4f} | {r["MRR"]:.4f} | {r["NDCG@10"]:.4f} |')
