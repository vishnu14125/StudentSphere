import os
import json
import matplotlib.pyplot as plt
import numpy as np

def main():
    json_path = os.path.join(os.path.dirname(__file__), 'results/final_fair_evaluation_v5.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    agg = data['aggregate']
    metrics = ['P@3', 'P@5', 'P@10', 'R@3', 'R@5', 'R@10', 'MRR', 'nDCG@5', 'nDCG@10']
    
    tf_vals = [agg['tfidf'][m] for m in metrics]
    sem_vals = [agg['semantic'][m] for m in metrics]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, tf_vals, width, label='TF-IDF Baseline', color='#4a90e2')
    rects2 = ax.bar(x + width/2, sem_vals, width, label='Semantic Retrieval', color='#50e3c2')
    
    ax.set_ylabel('Score')
    ax.set_title('Retrieval Performance: TF-IDF vs Semantic Retrieval')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.set_ylim(0, 1.1)
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.3f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), 
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
                        
    autolabel(rects1)
    autolabel(rects2)
    
    fig.tight_layout()
    out_png = os.path.join(os.path.dirname(__file__), 'results/final_retrieval_comparison.png')
    plt.savefig(out_png, dpi=300)
    print(f"Figure saved to {out_png}")

if __name__ == '__main__':
    main()
