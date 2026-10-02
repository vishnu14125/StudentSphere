import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.rag.rag_pipeline import get_rag_pipeline
from app.config import settings

def run_tests():
    print(f"Starting validation tests...")
    print(f"Embedding model: {settings.embedding_model}")
    print(f"OPENAI_MODEL: {settings.openai_model}")
    
    rag = get_rag_pipeline()
    
    print("\n--- 1. Indexing Data ---")
    docs = [
        {
            "id": "doc1",
            "text": "In my Amazon SDE interview, they asked me to implement LRU cache and explain Dijkstra algorithm. The interviewer was friendly.",
            "metadata": {"interviewId": "int1", "companyName": "Amazon", "role": "SDE", "year": 2024}
        },
        {
            "id": "doc2",
            "text": "Software engineering interviews usually cover Data Structures, Algorithms, and System Design. You should prepare well.",
            "metadata": {"interviewId": "int2", "companyName": "General", "role": "Software Engineer", "year": 2023}
        },
        {
            "id": "doc3",
            "text": "System design interviews focus on scalability, database sharding, caching, and load balancing.",
            "metadata": {"interviewId": "int3", "companyName": "General", "role": "Backend Developer", "year": 2023}
        }
    ]
    
    for doc in docs:
        rag.ingest_document_with_chunks(doc["id"], doc["text"], doc["metadata"])
    print("Indexed 3 documents successfully.")
    
    queries = [
        "What questions were asked in Amazon SDE interviews?",
        "What topics commonly appear in software engineering interviews?",
        "What should I prepare for technical interviews?",
        "What was reported about system design interviews?",
        "How do I cook a turkey?"
    ]
    
    print("\n--- 2. Executing Queries ---")
    for q in queries:
        print(f"\nQuery: {q}")
        res = rag.answer_query(q)
        print(json.dumps(res, indent=2))
        
    print("\n--- 3. Testing High Threshold (No Evidence) ---")
    res_no_ev = rag.answer_query("How do I cook a turkey?", similarity_threshold=0.99)
    print(json.dumps(res_no_ev, indent=2))
    
    print("\nValidation complete.")

if __name__ == "__main__":
    run_tests()
