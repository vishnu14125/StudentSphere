import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.rag.rag_pipeline import get_rag_pipeline

rag = get_rag_pipeline()
print("RAG pipeline initialized.")

# Index a document
doc = {
    "id": "doc1",
    "text": "In my Amazon SDE interview, I was asked to implement a LRU cache and explain Dijkstra algorithm. The interviewer was friendly.",
    "metadata": {"interviewId": "int1", "companyName": "Amazon", "role": "SDE", "year": 2024}
}
rag.ingest_document_with_chunks(doc["id"], doc["text"], doc["metadata"])
print("Document indexed.")

# Semantic Search
contexts = rag.search_relevant_context("Amazon SDE interview questions")
print("Search results:")
for c in contexts:
    print(c)

# Answer Query
ans = rag.answer_query("What questions were reported for Amazon SDE interviews?")
print("Answer query results:")
print(ans)

# No evidence query
ans_no_evidence = rag.answer_query("How to cook a turkey?", similarity_threshold=0.99)
print("No evidence query results:")
print(ans_no_evidence)
