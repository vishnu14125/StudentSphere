import json
with open('ai-service/datasets/research_corpus.json', 'r', encoding='utf-8') as f: corpus = json.load(f)
doc_map = {d['id']: d['experienceText'].split('\nAnswer: ')[0].replace('Question: ', '') for d in corpus}
with open('ai-service/experiments/evaluation_queries_v2.json', 'r', encoding='utf-8') as f: queries = json.load(f)
for q in queries:
    print(f'QID: {q["query_id"]}')
    print(f'Query: {q["query"]}')
    for rid in q['relevant_document_ids']:
        print(f'  - {rid}: {doc_map.get(rid, "Unknown")}')
    print()
