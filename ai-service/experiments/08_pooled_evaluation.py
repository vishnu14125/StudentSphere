import os
import sys
import json
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.embeddings.embeddings import get_embedding_service
from app.config import settings

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)

def main():
    print("Loading data...")
    corpus_path = os.path.join(os.path.dirname(__file__), '../datasets/research_corpus.json')
    eval_path = os.path.join(os.path.dirname(__file__), 'results/evaluation_queries_v3_enriched.json')
    
    with open(corpus_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
        
    doc_map = {doc['id']: doc for doc in corpus}
        
    with open(eval_path, 'r', encoding='utf-8') as f:
        eval_queries = json.load(f)
        
    gt_map = {}
    for q in eval_queries:
        qid = q['query_id']
        for cand in q['candidates']:
            gt_map[(qid, cand['doc_id'])] = cand['relevance']
            
    print("Setting up TF-IDF Configuration...")
    # Map index to doc_id
    doc_ids = [doc['id'] for doc in corpus]
    texts = [doc['experienceText'] for doc in corpus]
    
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    print("Setting up Semantic Configuration...")
    emb_service = get_embedding_service()
    
    # We will use exactly what rag_pipeline.py uses: sentence-aware chunking
    chunk_embeddings = []
    for doc in corpus:
        chunks = emb_service.generate_chunks_embedding(
            doc['experienceText'], 
            chunk_max_words=settings.chunk_max_words, 
            chunk_overlap_words=settings.chunk_overlap_words
        )
        for chunk_text, emb in chunks:
            chunk_embeddings.append({
                'doc_id': doc['id'],
                'embedding': emb
            })
            
    results = []
    total_pooled = 0
    total_already_labeled = 0
    total_new = 0
    new_per_query = {}
    unique_new = set()

    for q in eval_queries:
        query_text = q['query']
        query_id = q['query_id']
        
        # --- SEMANTIC TOP 10 ---
        q_emb = emb_service.generate_embedding(query_text)
        scores_chunk = []
        for item in chunk_embeddings:
            score = cosine_similarity(q_emb, item['embedding'])
            scores_chunk.append((item['doc_id'], score))
        scores_chunk.sort(key=lambda x: x[1], reverse=True)
        
        semantic_top10 = []
        seen = set()
        for doc_id, score in scores_chunk:
            if doc_id not in seen:
                seen.add(doc_id)
                semantic_top10.append({'doc_id': doc_id, 'score': score})
            if len(semantic_top10) == 10:
                break
                
        # --- TF-IDF TOP 10 ---
        query_tfidf = vectorizer.transform([query_text])
        from sklearn.metrics.pairwise import cosine_similarity as sk_cosine
        tfidf_sims = sk_cosine(query_tfidf, tfidf_matrix)[0]
        sorted_indices = np.argsort(tfidf_sims)[::-1]
        
        tfidf_top10 = []
        for idx in sorted_indices[:10]:
            tfidf_top10.append({
                'doc_id': doc_ids[idx],
                'score': float(tfidf_sims[idx])
            })
            
        # --- POOLING ---
        pooled_map = {} # doc_id -> merged dict
        
        for rank, item in enumerate(semantic_top10, start=1):
            pooled_map[item['doc_id']] = {
                'doc_id': item['doc_id'],
                'semantic_rank': rank,
                'semantic_similarity': item['score']
            }
            
        for rank, item in enumerate(tfidf_top10, start=1):
            doc_id = item['doc_id']
            if doc_id not in pooled_map:
                pooled_map[doc_id] = {
                    'doc_id': doc_id,
                    'tfidf_rank': rank,
                    'tfidf_similarity': item['score']
                }
            else:
                pooled_map[doc_id]['tfidf_rank'] = rank
                pooled_map[doc_id]['tfidf_similarity'] = item['score']
                
        # --- FORMAT OUTPUT ---
        pooled_candidates = []
        query_new_count = 0
        
        for doc_id, data in pooled_map.items():
            doc_info = doc_map[doc_id]
            
            orig_text = doc_info['experienceText']
            q_part = orig_text.split('\nAnswer: ')[0].replace('Question: ', '')
            a_part = orig_text.split('\nAnswer: ')[1] if '\nAnswer: ' in orig_text else ''
            
            cand = {
                'doc_id': doc_id,
                'semantic_rank': data.get('semantic_rank'),
                'semantic_similarity': data.get('semantic_similarity'),
                'tfidf_rank': data.get('tfidf_rank'),
                'tfidf_similarity': data.get('tfidf_similarity'),
                'question': q_part,
                'answer': a_part,
                'category': doc_info.get('category'),
                'difficulty': doc_info.get('difficulty')
            }
            
            # Label lookup
            relevance = gt_map.get((query_id, doc_id))
            cand['relevance'] = relevance
            
            pooled_candidates.append(cand)
            
            total_pooled += 1
            if relevance is not None:
                total_already_labeled += 1
            else:
                total_new += 1
                query_new_count += 1
                unique_new.add(doc_id)
                
        new_per_query[query_id] = query_new_count
                
        # Sort by semantic rank first, then tfidf rank for consistent presentation
        pooled_candidates.sort(key=lambda x: (
            x['semantic_rank'] if x['semantic_rank'] is not None else 999,
            x['tfidf_rank'] if x['tfidf_rank'] is not None else 999
        ))
        
        results.append({
            'query_id': query_id,
            'query': query_text,
            'semantic_top10': [c['doc_id'] for c in semantic_top10],
            'tfidf_top10': [c['doc_id'] for c in tfidf_top10],
            'pooled_candidates': pooled_candidates
        })
        
    out_json = os.path.join(os.path.dirname(__file__), 'results/pooled_evaluation_v4.json')
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
        
    print(f"\n--- POOLED EVALUATION SUMMARY ---")
    print(f"Total pooled candidates: {total_pooled}")
    print(f"Already human-labeled candidates: {total_already_labeled}")
    print(f"New candidates requiring human judgment: {total_new}")
    print(f"Number of unique new candidates overall: {len(unique_new)}")
    print("\nNew candidates per query:")
    for qid, count in new_per_query.items():
        print(f"  {qid}: {count}")

if __name__ == '__main__':
    main()
