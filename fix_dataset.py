import pandas as pd
import json

df = pd.read_csv('ai-service/datasets/raw/Software Questions.csv', encoding='windows-1252')

print('--- RAW CSV INFO ---')
print('Columns:', list(df.columns))
print('Data types:', {k: str(v) for k, v in df.dtypes.to_dict().items()})
print('Number of columns:', len(df.columns))
print('Number of rows:', len(df))
print('\nFirst 10 rows:')
for i in range(min(10, len(df))):
    print(f'Row {i}:')
    for col in df.columns:
        print(f'  {col}: {df.iloc[i][col]}')

q_col = 'Question'
a_col = 'Answer'
c_col = 'Category'
d_col = 'Difficulty'

df_no_dupes = df.drop_duplicates()

corpus = []
for idx, row in df_no_dupes.iterrows():
    q = str(row[q_col]).strip()
    a = str(row[a_col]).strip()
    cat = str(row[c_col]).strip()
    diff = str(row[d_col]).strip()
    
    doc = {
        'id': f'DOC_{idx+1:03d}',
        'documentType': 'interview_question',
        'company': None,
        'role': None,
        'year': None,
        'experienceText': f'Question: {q}\nAnswer: {a}',
        'topics': [cat] if cat and cat.lower() != 'nan' else [],
        'difficulty': diff if diff and diff.lower() != 'nan' else None,
        'rounds': None,
        'source': 'Kaggle - Software Engineering Interview Questions Dataset',
        'sourceUrl': 'https://www.kaggle.com/datasets/syedmharis/software-engineering-interview-questions-dataset',
        'license': 'MIT'
    }
    corpus.append(doc)

with open('ai-service/datasets/research_corpus.json', 'w', encoding='utf-8') as f:
    json.dump(corpus, f, indent=2)

print('\n--- TASK 3: VALIDATE (First 10 normalized) ---')
for doc in corpus[:10]:
    print(f"ID: {doc['id']}")
    print(doc['experienceText'])
    print(f"Category: {doc['topics']}")
    print(f"Difficulty: {doc['difficulty']}\n")

total_records = len(corpus)
q_lengths = []
a_lengths = []
questions_seen = set()
duplicates = 0
missing_q = 0
missing_a = 0
categories = {}
difficulties = {}

for doc in corpus:
    text = doc['experienceText']
    q_part = text.split('\nAnswer: ')[0].replace('Question: ', '')
    a_part = text.split('\nAnswer: ')[1] if '\nAnswer: ' in text else ''
    
    if not q_part or q_part.lower() == 'nan': missing_q += 1
    if not a_part or a_part.lower() == 'nan': missing_a += 1
    
    q_lengths.append(len(q_part))
    a_lengths.append(len(a_part))
    
    if q_part in questions_seen: duplicates += 1
    questions_seen.add(q_part)
    
    cat = doc['topics'][0] if doc['topics'] else 'Unknown'
    diff = doc['difficulty'] if doc['difficulty'] else 'Unknown'
    categories[cat] = categories.get(cat, 0) + 1
    difficulties[diff] = difficulties.get(diff, 0) + 1

report = f'''# DATASET REPORT V2
- Total Records: {total_records}
- Duplicate Questions: {duplicates}
- Missing Questions: {missing_q}
- Missing Answers: {missing_a}
- Average Question Length: {sum(q_lengths)/len(q_lengths):.2f} chars
- Average Answer Length: {sum(a_lengths)/len(a_lengths):.2f} chars
- Category Distribution: {categories}
- Difficulty Distribution: {difficulties}
'''
with open('ai-service/datasets/DATASET_REPORT_V2.md', 'w') as f:
    f.write(report)
print('Generated DATASET_REPORT_V2.md')
