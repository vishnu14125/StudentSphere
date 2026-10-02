import json
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

file_path = 'ai-service/experiments/results/evaluation_queries_v3_enriched.json'

with open(file_path, 'r', encoding='utf-8') as f:
    queries = json.load(f)

thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]

results = {t: {
    'rel_count': 0,
    'irrel_count': 0,
    'no_evidence': 0,
    'avg_retrieved': 0,
    'precision': 0,
    'recall': 0
} for t in thresholds}

total_queries = len(queries)

for t in thresholds:
    t_precisions = []
    t_recalls = []
    t_retrieved = []
    no_ev = 0
    
    total_rel_global = 0
    total_irrel_global = 0
    
    for q in queries:
        cands = q['candidates']
        # Original relevant count for recall denominator
        total_relevant_in_pool = sum(1 for c in cands if c['relevance'] >= 1)
        
        # Filter by threshold
        passed = [c for c in cands if c['similarity'] >= t]
        
        t_retrieved.append(len(passed))
        if len(passed) == 0:
            no_ev += 1
            t_precisions.append(0.0)
            t_recalls.append(0.0)
            continue
            
        passed_rel = sum(1 for c in passed if c['relevance'] >= 1)
        passed_irrel = len(passed) - passed_rel
        
        total_rel_global += passed_rel
        total_irrel_global += passed_irrel
        
        p = passed_rel / len(passed)
        r = passed_rel / total_relevant_in_pool if total_relevant_in_pool > 0 else 0.0
        
        t_precisions.append(p)
        t_recalls.append(r)
        
    results[t]['avg_retrieved'] = sum(t_retrieved) / total_queries
    results[t]['no_evidence'] = no_ev
    results[t]['precision'] = sum(t_precisions) / total_queries
    results[t]['recall'] = sum(t_recalls) / total_queries
    
    total_passed = total_rel_global + total_irrel_global
    if total_passed > 0:
        results[t]['rel_pct'] = (total_rel_global / total_passed) * 100
        results[t]['irrel_pct'] = (total_irrel_global / total_passed) * 100
    else:
        results[t]['rel_pct'] = 0.0
        results[t]['irrel_pct'] = 0.0

out_dir = 'ai-service/experiments/results'
with open(os.path.join(out_dir, 'threshold_analysis_v3.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

with open(os.path.join(out_dir, 'threshold_analysis_v3.csv'), 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Threshold', 'Relevant %', 'Irrelevant %', 'No-Evidence Queries', 'Avg. Retrieved', 'Precision', 'Recall'])
    for t in thresholds:
        writer.writerow([t, f"{results[t]['rel_pct']:.2f}%", f"{results[t]['irrel_pct']:.2f}%", results[t]['no_evidence'], f"{results[t]['avg_retrieved']:.2f}", f"{results[t]['precision']:.4f}", f"{results[t]['recall']:.4f}"])

# Plot
fig, ax1 = plt.subplots(figsize=(8, 6))

color = 'tab:red'
ax1.set_xlabel('Similarity Threshold')
ax1.set_ylabel('Avg. Retrieved', color=color)
avg_r = [results[t]['avg_retrieved'] for t in thresholds]
ax1.plot(thresholds, avg_r, color=color, marker='o', label='Avg Retrieved')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color2 = 'tab:blue'
color3 = 'tab:green'
ax2.set_ylabel('Score')
prec_vals = [results[t]['precision'] for t in thresholds]
rec_vals = [results[t]['recall'] for t in thresholds]
ax2.plot(thresholds, prec_vals, color=color2, marker='s', label='Precision')
ax2.plot(thresholds, rec_vals, color=color3, marker='^', label='Recall')
ax2.tick_params(axis='y')

fig.tight_layout()
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
plt.title('Threshold vs Precision, Recall, and Avg Retrieved')
plt.savefig(os.path.join(out_dir, 'figures', 'fig_threshold_analysis_v3.png'))

print('| Threshold | Relevant % | Irrelevant % | No-Evidence Queries | Avg. Retrieved | Precision | Recall |')
print('|---|---:|---:|---:|---:|---:|---:|')
for t in thresholds:
    print(f"| {t} | {results[t]['rel_pct']:.2f}% | {results[t]['irrel_pct']:.2f}% | {results[t]['no_evidence']} | {results[t]['avg_retrieved']:.2f} | {results[t]['precision']:.4f} | {results[t]['recall']:.4f} |")

print('\nInterpretation:')
print('As the similarity threshold increases from 0.3 to 0.7, the system becomes strictly more conservative. The average number of retrieved documents passed to the LLM drops sharply, directly causing Recall to fall (as more relevant documents are erroneously discarded). However, this strictness successfully filters out noise, increasing the proportion of relevant documents (Precision) in the remaining pool. At the highest thresholds (e.g., 0.7), the system is too strict, resulting in a large number of "No-Evidence" queries where 0 documents are retrieved.')
