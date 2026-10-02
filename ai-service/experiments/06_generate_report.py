import os
import json
import csv
import matplotlib.pyplot as plt

def generate_report():
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    os.makedirs(results_dir, exist_ok=True)
    
    # Load dataset stats
    stats_file = os.path.join(results_dir, 'dataset_stats.json')
    if os.path.exists(stats_file):
        with open(stats_file, 'r') as f:
            stats = json.load(f)
    else:
        stats = {}

    # Load retrieval summary
    retrieval_file = os.path.join(results_dir, '02_retrieval_summary.json')
    if os.path.exists(retrieval_file):
        with open(retrieval_file, 'r') as f:
            retrieval_summary = json.load(f)
    else:
        retrieval_summary = {}

    # Load Top K
    topk_file = os.path.join(results_dir, '03_topk_results.csv')
    topk_data = []
    if os.path.exists(topk_file):
        with open(topk_file, 'r') as f:
            topk_data = list(csv.DictReader(f))
            
    # Load Threshold
    thresh_file = os.path.join(results_dir, '03_threshold_results.csv')
    thresh_data = []
    if os.path.exists(thresh_file):
        with open(thresh_file, 'r') as f:
            thresh_data = list(csv.DictReader(f))

    # Load Latency
    latency_file = os.path.join(results_dir, '04_latency_stats.json')
    if os.path.exists(latency_file):
        with open(latency_file, 'r') as f:
            latency = json.load(f)
    else:
        latency = {}
        
    # Load Generative Eval
    gen_file = os.path.join(results_dir, '05_generative_eval.json')
    gen_data = []
    if os.path.exists(gen_file):
        with open(gen_file, 'r') as f:
            gen_data = json.load(f)
            
    # ---------------------------------------------
    # Generate Plots
    # ---------------------------------------------
    # 1. Retrieval Comparison
    if retrieval_summary:
        metrics = ['Precision@5', 'Recall@5', 'MRR']
        tfidf = [retrieval_summary.get('mean_tfidf_precision_5', 0), 
                 retrieval_summary.get('mean_tfidf_recall_5', 0), 
                 retrieval_summary.get('mean_tfidf_mrr', 0)]
        semantic = [retrieval_summary.get('mean_semantic_precision_5', 0), 
                    retrieval_summary.get('mean_semantic_recall_5', 0), 
                    retrieval_summary.get('mean_semantic_mrr', 0)]
                    
        x = range(len(metrics))
        width = 0.35
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar([i - width/2 for i in x], tfidf, width, label='TF-IDF')
        ax.bar([i + width/2 for i in x], semantic, width, label='Semantic (all-MiniLM-L6-v2)')
        ax.set_ylabel('Score')
        ax.set_title('Lexical vs Semantic Retrieval Performance')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, 'fig1_retrieval_comparison.png'))
        plt.close()
        
    # 2. Top-K Performance
    if topk_data:
        ks = [int(r['k']) for r in topk_data]
        prec = [float(r['precision']) for r in topk_data]
        rec = [float(r['recall']) for r in topk_data]
        mrr = [float(r['mrr']) for r in topk_data]
        
        plt.figure(figsize=(8, 5))
        plt.plot(ks, prec, marker='o', label='Precision')
        plt.plot(ks, rec, marker='s', label='Recall')
        plt.plot(ks, mrr, marker='^', label='MRR')
        plt.xlabel('K (Top-K)')
        plt.ylabel('Score')
        plt.title('Performance across Top-K Variations')
        plt.xticks(ks)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, 'fig2_topk_performance.png'))
        plt.close()
        
    # 3. Threshold Coverage
    if thresh_data:
        ts = [float(r['threshold']) for r in thresh_data]
        rel_rate = [float(r['relevant_retrieval_rate']) for r in thresh_data]
        no_ev = [float(r['no_evidence_rate']) for r in thresh_data]
        
        fig, ax1 = plt.subplots(figsize=(8, 5))
        ax1.plot(ts, rel_rate, 'g-o', label='Relevant Retrieval Rate')
        ax1.set_xlabel('Similarity Threshold')
        ax1.set_ylabel('Rate', color='g')
        ax1.tick_params(axis='y', labelcolor='g')
        
        ax2 = ax1.twinx()
        ax2.plot(ts, no_ev, 'r-s', label='No Evidence Rate')
        ax2.set_ylabel('No Evidence Rate (Short-circuit)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        plt.title('Threshold Impact on Retrieval Coverage')
        fig.tight_layout()
        plt.savefig(os.path.join(results_dir, 'fig3_threshold_coverage.png'))
        plt.close()
        
    # 4. Latency Breakdown
    if latency:
        comps = ['Embedding', 'Vector Search', 'LLM Gen']
        means = [
            latency.get('embedding', {}).get('mean', 0),
            latency.get('vector_search', {}).get('mean', 0),
            latency.get('llm_generation', {}).get('mean', 0)
        ]
        
        plt.figure(figsize=(8, 5))
        plt.bar(comps, means, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        plt.ylabel('Latency (seconds)')
        plt.title('Pipeline Latency Breakdown')
        for i, v in enumerate(means):
            plt.text(i, v + 0.05, f"{v:.3f}s", ha='center')
        plt.tight_layout()
        plt.savefig(os.path.join(results_dir, 'fig4_latency_breakdown.png'))
        plt.close()
        
    # ---------------------------------------------
    # Write EXPERIMENT_REPORT.md
    # ---------------------------------------------
    report_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'EXPERIMENT_REPORT.md'))
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# StudentSphere RAG Experimental Evaluation Report\n\n")
        
        f.write("## 1. Dataset Characterization\n")
        f.write(f"**Data Source:** {stats.get('data_source')}\n\n")
        f.write("| Metric | Value |\n|---|---|\n")
        f.write(f"| Total Experiences | {stats.get('total_experiences', 'N/A')} |\n")
        f.write(f"| Companies | {stats.get('companies', 'N/A')} |\n")
        f.write(f"| Roles | {stats.get('roles', 'N/A')} |\n")
        f.write(f"| Years | {stats.get('years', 'N/A')} |\n")
        f.write(f"| Chunks Indexed | {stats.get('chunks', 'N/A')} |\n\n")
        
        f.write("## 2. Retrieval Baseline Comparison\n")
        f.write("Comparing standard TF-IDF (lexical) against the `sentence-transformers` vector search.\n\n")
        f.write("| Metric | TF-IDF | Semantic (RAG) |\n|---|---|---|\n")
        f.write(f"| Precision@5 | {retrieval_summary.get('mean_tfidf_precision_5', 0):.3f} | {retrieval_summary.get('mean_semantic_precision_5', 0):.3f} |\n")
        f.write(f"| Recall@5 | {retrieval_summary.get('mean_tfidf_recall_5', 0):.3f} | {retrieval_summary.get('mean_semantic_recall_5', 0):.3f} |\n")
        f.write(f"| MRR | {retrieval_summary.get('mean_tfidf_mrr', 0):.3f} | {retrieval_summary.get('mean_semantic_mrr', 0):.3f} |\n\n")
        f.write("![Retrieval Comparison](ai-service/experiments/results/fig1_retrieval_comparison.png)\n\n")
        
        f.write("## 3. Top-K Evaluation\n")
        f.write("| K | Precision@K | Recall@K | MRR | Avg Latency (s) | Avg Retrieved Chunks |\n|---|---|---|---|---|---|\n")
        for row in topk_data:
            f.write(f"| {row['k']} | {float(row['precision']):.3f} | {float(row['recall']):.3f} | {float(row['mrr']):.3f} | {float(row['avg_latency']):.3f} | {float(row['avg_retrieved']):.1f} |\n")
        f.write("\n![Top K Performance](ai-service/experiments/results/fig2_topk_performance.png)\n\n")
        
        f.write("## 4. Similarity Threshold Impact\n")
        f.write("| Threshold | Relevant Retrieval Rate | Irrelevant Retrieval Rate | No-Evidence Rate | Avg Chunks |\n|---|---|---|---|---|\n")
        for row in thresh_data:
            f.write(f"| {row['threshold']} | {float(row['relevant_retrieval_rate']):.3f} | {float(row['irrelevant_retrieval_rate']):.3f} | {float(row['no_evidence_rate']):.3f} | {float(row['avg_chunks']):.1f} |\n")
        f.write("\n![Threshold Coverage](ai-service/experiments/results/fig3_threshold_coverage.png)\n\n")
        
        f.write("## 5. Latency Analysis\n")
        f.write("| Component | Mean (s) | Median (s) | Std Dev (s) | Min (s) | Max (s) |\n|---|---|---|---|---|---|\n")
        if latency:
            for comp, vals in latency.items():
                f.write(f"| {comp} | {vals['mean']:.3f} | {vals['median']:.3f} | {vals['std']:.3f} | {vals['min']:.3f} | {vals['max']:.3f} |\n")
        f.write("\n![Latency Breakdown](ai-service/experiments/results/fig4_latency_breakdown.png)\n\n")
        
        f.write("## 6. Generative Accuracy: RAG vs Non-RAG\n")
        f.write("Generative evaluation utilizing `gemini-3.6-flash`. The LLM-as-a-judge was omitted to conserve API quota. Below is a manual side-by-side comparison of generated output context.\n\n")
        if gen_data:
            for row in gen_data:
                f.write(f"### Query: {row['query']}\n")
                f.write(f"**Sources Used (RAG):** {row['sources_used']}\n\n")
                f.write(f"**Baseline Answer (No Context):**\n> {row['baseline_answer']}\n\n")
                f.write(f"**RAG Answer:**\n> {row['rag_answer']}\n\n---\n")

        f.write("## 7. Known Limitations\n")
        f.write("- **Dataset:** MongoDB was empty locally, so the experiment was evaluated on 20 explicitly designated mock interview profiles within the vector store.\n")
        f.write("- **Gemini Quota:** Generative LLM evaluation was limited to 5 targeted queries to prevent HTTP 429 quota exhaustion. Statistical LLM-as-a-judge was explicitly disabled.\n")

    # Write README.md
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# StudentSphere Experimental Framework\n\n")
        f.write("This directory contains the automated evaluation framework for the RAG pipeline.\n\n")
        f.write("### Execution Order\n")
        f.write("1. `python setup_mock_data.py` (Provisions the test dataset)\n")
        f.write("2. `python 01_dataset_characterization.py`\n")
        f.write("3. `python 02_retrieval_evaluation.py` (Tests TF-IDF against Semantic search using Ground Truth labels)\n")
        f.write("4. `python 03_threshold_topk.py`\n")
        f.write("5. `python 04_latency.py`\n")
        f.write("6. `python 05_generative_evaluation.py` (Limited queries for quota protection)\n")
        f.write("7. `python 06_generate_report.py` (Aggregates CSV/JSONs into the final EXPERIMENT_REPORT.md and Matplotlib PNGs)\n\n")
        f.write("### Ground Truth Methodology\n")
        f.write("The retrieval ground truth (`data/retrieval_ground_truth.json`) was manually labeled (21 queries mapped to explicit `interviewId` constraints). Gemini was explicitly excluded from generating retrieval Ground Truth labels to ensure research integrity.\n")

    print(f"Report generation complete. Written to: {report_path}")

if __name__ == "__main__":
    generate_report()
