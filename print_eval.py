import json

with open('ai-service/experiments/results/generation_human_evaluation_v3.json', 'r', encoding='utf-8') as f:
    eval_data = json.load(f)

for i, record in enumerate(eval_data):
    print('========================================')
    print(f"QUERY {i+1}/5: [{record['query_id']}] {record['query']}")
    print('========================================')
    print('--- BASELINE ANSWER ---')
    print(record['baseline_answer'])
    print('\n--- RAG ANSWER ---')
    print(record['rag_answer'])
    print('\n--- RAG RETRIEVED EVIDENCE ---')
    for doc in record['retrieved_evidence']:
        print(f"- {doc['doc_id']} (Sim: {doc['similarity']:.3f}): {doc['question']}")
    print('\n')
