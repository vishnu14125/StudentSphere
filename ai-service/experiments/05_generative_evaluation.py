import sys
import os
import json
import csv
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.rag_pipeline import get_rag_pipeline

def evaluate_generative():
    rag = get_rag_pipeline()
    
    # 5 specific test queries based on mock dataset
    test_queries = [
        "What questions are asked in Amazon SDE interviews?",
        "What topics commonly appear in software engineering interviews?",
        "What should I know for Stripe backend?",
        "Data science questions at Amazon",
        "Geospatial indexing at Uber"
    ]
    
    results = []
    print("Running Generative Evaluation (RAG vs Non-RAG)...")
    
    for q in test_queries:
        print(f"Query: {q}")
        
        # 1. Non-RAG Baseline (calling Gemini directly without context)
        t0 = time.time()
        ans_baseline = "Failed"
        try:
            res_base = rag.llm_service.generate_answer(q, ["(No specific interview experience context provided. Answer generally.)"])
            if res_base.get("success"):
                ans_baseline = res_base["answer"]
            else:
                ans_baseline = f"Failed: {res_base.get('error')}"
        except Exception as e:
            ans_baseline = f"Error: {str(e)}"
        
        # 2. RAG Generation
        ans_rag = "Failed"
        sources = []
        try:
            res_rag = rag.answer_query(q)
            if res_rag.get("success"):
                ans_rag = res_rag["answer"]
                sources = res_rag.get("sources", [])
            else:
                ans_rag = f"Failed: {res_rag.get('answer', 'Unknown error')}"
        except Exception as e:
            ans_rag = f"Error: {str(e)}"
            
        results.append({
            "query": q,
            "baseline_answer": ans_baseline,
            "rag_answer": ans_rag,
            "sources_used": len(sources)
        })
        time.sleep(2) # rate limit mitigation
        
    out_json = os.path.join(os.path.dirname(__file__), 'results', '05_generative_eval.json')
    with open(out_json, 'w') as f:
        json.dump(results, f, indent=2)

    out_csv = os.path.join(os.path.dirname(__file__), 'results', '05_generative_eval.csv')
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["query", "baseline_answer", "rag_answer", "sources_used"])
        writer.writeheader()
        writer.writerows(results)

    print("Generative evaluation completed. Note: LLM-as-a-judge scoring is omitted here to conserve quota. Manual/heuristic inspection of these results is recommended in EXPERIMENT_REPORT.md.")

if __name__ == "__main__":
    evaluate_generative()
