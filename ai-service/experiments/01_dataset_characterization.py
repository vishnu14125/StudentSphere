import sys
import os
import json
import traceback

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def characterize_dataset():
    stats = {
        "total_experiences": 0,
        "companies": 0,
        "roles": 0,
        "years": 0,
        "rounds": 0,
        "questions": 0,
        "topics": 0,
        "chunks": 0,
        "data_source": "unknown"
    }
    
    # Check MongoDB first
    try:
        import pymongo
        client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
        db = client.studentsphere
        count = db.interviews.count_documents({})
        if count > 0:
            stats["data_source"] = "MongoDB (Actual Data)"
            stats["total_experiences"] = count
            stats["companies"] = len(db.interviews.distinct("company"))
            stats["roles"] = len(db.interviews.distinct("role"))
            stats["years"] = len(db.interviews.distinct("year"))
            # For simplicity, if we have real data, we'd aggregate rounds/questions
        else:
            stats["data_source"] = "vector_store.pkl (Mock Evaluation Dataset)"
    except Exception as e:
        stats["data_source"] = "vector_store.pkl (Mock Evaluation Dataset)"
        
    if stats["data_source"] == "vector_store.pkl (Mock Evaluation Dataset)":
        from app.rag.vector_store import get_vector_store
        vs = get_vector_store()
        stats["chunks"] = len(vs.ids)
        
        unique_interviews = set()
        unique_companies = set()
        unique_roles = set()
        unique_years = set()
        
        for meta in vs.metadatas:
            if meta:
                if 'interviewId' in meta: unique_interviews.add(meta['interviewId'])
                if 'company' in meta: unique_companies.add(meta['company'])
                if 'role' in meta: unique_roles.add(meta['role'])
                if 'year' in meta: unique_years.add(meta['year'])
        
        stats["total_experiences"] = len(unique_interviews)
        stats["companies"] = len(unique_companies)
        stats["roles"] = len(unique_roles)
        stats["years"] = len(unique_years)
        stats["rounds"] = "N/A (mock data limitation)"
        stats["questions"] = "N/A (mock data limitation)"
        stats["topics"] = "N/A (mock data limitation)"
        
    os.makedirs(os.path.join(os.path.dirname(__file__), 'results'), exist_ok=True)
    out_path = os.path.join(os.path.dirname(__file__), 'results', 'dataset_stats.json')
    with open(out_path, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Dataset characterization completed. Source: {stats['data_source']}")

if __name__ == "__main__":
    characterize_dataset()
