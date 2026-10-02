import os
import json
from scipy import stats

def main():
    json_path = os.path.join(os.path.dirname(__file__), 'results/final_fair_evaluation_v5.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    results = data['query_results']
    
    tf_mrr_arr = [r['tfidf']['MRR'] for r in results]
    se_mrr_arr = [r['semantic']['MRR'] for r in results]
    
    tf_ndcg10 = [r['tfidf']['nDCG@10'] for r in results]
    se_ndcg10 = [r['semantic']['nDCG@10'] for r in results]
    
    print("ROBUSTNESS CHECK: Wilcoxon signed-rank test")
    print(f"Number of paired observations: {len(results)}")
    print("Alternative hypothesis: two-sided\n")
    
    try:
        w_stat_mrr, p_val_mrr = stats.wilcoxon(se_mrr_arr, tf_mrr_arr, alternative='two-sided')
        print(f"MRR Wilcoxon Statistic: {w_stat_mrr}")
        print(f"MRR Wilcoxon p-value: {p_val_mrr}")
    except Exception as e:
        print(f"MRR Wilcoxon Error: {str(e)}")
        
    print()
    
    try:
        w_stat_ndcg, p_val_ndcg = stats.wilcoxon(se_ndcg10, tf_ndcg10, alternative='two-sided')
        print(f"nDCG@10 Wilcoxon Statistic: {w_stat_ndcg}")
        print(f"nDCG@10 Wilcoxon p-value: {p_val_ndcg}")
    except Exception as e:
        print(f"nDCG@10 Wilcoxon Error: {str(e)}")

if __name__ == '__main__':
    main()
