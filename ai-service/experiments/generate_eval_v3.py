import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.rag.rag_pipeline import get_rag_pipeline
from app.config import settings

rag = get_rag_pipeline()

file_path = os.path.join(os.path.dirname(__file__), 'results/evaluation_queries_v3_enriched.json')
with open(file_path, 'r', encoding='utf-8') as f:
    all_queries = json.load(f)

target_qids = ['Q02', 'Q04', 'Q08', 'Q11', 'Q12']
eval_queries = [q for q in all_queries if q['query_id'] in target_qids]

out_dir = os.path.join(os.path.dirname(__file__), 'results')
raw_out_file = os.path.join(out_dir, 'generation_raw_outputs_v3.json')
eval_out_file = os.path.join(out_dir, 'generation_human_evaluation_v3.json')

raw_outputs = []
human_eval_data = []

corpus_path = os.path.join(os.path.dirname(__file__), '../datasets/research_corpus.json')
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus = json.load(f)
corpus_map = {d['id']: d['experienceText'] for d in corpus}

def generate_with_retry(model, prompt, retries=15):
    for attempt in range(retries):
        try:
            print(f"[DEBUG] Attempt {attempt+1} to generate...", flush=True)
            response = model.generate_content(prompt)
            print(f"[DEBUG] Success!", flush=True)
            return response.text
        except Exception as e:
            err_str = str(e)
            print(f"[DEBUG] Error on attempt {attempt+1}: {err_str}", flush=True)
            if "429" in err_str or "quota" in err_str.lower():
                print("[DEBUG] Sleeping 65s due to rate limit...", flush=True)
                time.sleep(65) # Wait for rate limit window to clear
            else:
                time.sleep(10)
    return f"Failed to generate after {retries} retries."

for i, q in enumerate(eval_queries):
    q_id = q['query_id']
    q_text = q['query']
        
    print(f"[DEBUG] Processing [{i+1}/5] {q_id}: {q_text}", flush=True)
    
    # BASELINE (Bypassing llm_service because it rejects empty context)
    t0 = time.time()
    baseline_prompt = f"Please answer this technical interview question clearly and factually:\n{q_text}"
    print(f"[DEBUG] Running baseline generation...", flush=True)
    baseline_answer_text = generate_with_retry(rag.llm_service.gemini_model, baseline_prompt)
    t_baseline_llm = time.time() - t0
    
    # RAG
    t0 = time.time()
    query_emb = rag.embedding_service.generate_embedding(q_text)
    t_emb = time.time() - t0
    
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
                    'score': float(score)
                })
    t_vec = time.time() - t0
    t_retrieval = t_emb + t_vec
    
    snippets_for_llm = []
    rag_evidence = []
    for context in contexts:
        text = context['text'].strip()
        doc_id = context['id']
        meta = context.get('metadata', {})
        score = context['score']
        
        orig_text = corpus_map.get(doc_id, text)
        q_part = orig_text.split('\nAnswer: ')[0].replace('Question: ', '')
        a_part = orig_text.split('\nAnswer: ')[1] if '\nAnswer: ' in orig_text else ''
        
        rag_evidence.append({
            'doc_id': doc_id,
            'question': q_part,
            'answer': a_part,
            'similarity': score
        })
        
        company = meta.get('companyName', 'Unknown company')
        role = meta.get('role', 'Unknown role')
        snippets_for_llm.append(f"Source: {company} - {role}\nContent: {text}")
        
    t0 = time.time()
    context_text = "\n\n---\n\n".join(snippets_for_llm)
    rag_prompt = f"""You are an AI assistant helping students prepare for technical interviews based ONLY on the provided interview experiences.

Instructions:
- Answer the user's question using ONLY the provided interview experiences below.
- Do not invent facts, questions, or topics.
- If the answer cannot be found in the provided evidence, clearly state: "Insufficient retrieved evidence is available to answer this question."
- When citing specific questions or details, distinguish between different interview experiences if possible (e.g. "In an Amazon SDE interview...", "One candidate reported...").
- Be concise, structured, and helpful.

Retrieved Interview Experiences:
{context_text}

User Question: {q_text}"""

    print(f"[DEBUG] Running RAG generation...", flush=True)
    rag_answer_text = generate_with_retry(rag.llm_service.gemini_model, rag_prompt)
    t_rag_llm = time.time() - t0
    t_rag_total = t_retrieval + t_rag_llm
    
    model_name = getattr(rag.llm_service, 'model_name', 'gemini-1.5-pro')
    
    raw_record = {
        'query_id': q_id,
        'query': q_text,
        'timestamp': time.time(),
        'baseline': {
            'prompt': baseline_prompt,
            'answer': baseline_answer_text,
            'model': model_name,
            'latency_ms': t_baseline_llm * 1000
        },
        'rag': {
            'prompt_context': snippets_for_llm,
            'retrieved_evidence': rag_evidence,
            'answer': rag_answer_text,
            'model': model_name,
            'retrieval_latency_ms': t_retrieval * 1000,
            'generation_latency_ms': t_rag_llm * 1000,
            'total_latency_ms': t_rag_total * 1000
        }
    }
    raw_outputs.append(raw_record)
    
    eval_record = {
        'query_id': q_id,
        'query': q_text,
        'retrieved_evidence': rag_evidence,
        'baseline_answer': baseline_answer_text,
        'rag_answer': rag_answer_text,
        'human_evaluation': {
            'baseline': {
                'relevance': None,
                'correctness': None,
                'evidence_support': None,
                'hallucination': None,
                'overall_quality': None
            },
            'rag': {
                'relevance': None,
                'correctness': None,
                'evidence_support': None,
                'hallucination': None,
                'overall_quality': None
            }
        }
    }
    human_eval_data.append(eval_record)
    
    with open(raw_out_file, 'w', encoding='utf-8') as f:
        json.dump(raw_outputs, f, indent=2)
    with open(eval_out_file, 'w', encoding='utf-8') as f:
        json.dump(human_eval_data, f, indent=2)
        
    print(f"[DEBUG] Saved {q_id}.", flush=True)

print("Generated evaluation files successfully.", flush=True)
