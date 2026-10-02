import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.rag.rag_pipeline import get_rag_pipeline
from app.config import settings
import importlib
import app.services.llm_service

def run_error_tests():
    print("Testing Error Handling...")
    
    # 1. Missing Gemini Key
    settings.gemini_api_key = ""
    importlib.reload(app.services.llm_service)
    from app.services.llm_service import get_llm_service
    # Force re-init
    app.services.llm_service._llm_service = None
    rag = get_rag_pipeline()
    rag.llm_service = get_llm_service()
    
    print("Missing Key Query:")
    res = rag.answer_query("What topics commonly appear in software engineering interviews?")
    print(json.dumps(res, indent=2))
    
    # 2. Invalid Gemini Key
    settings.gemini_api_key = "INVALID_KEY_123"
    importlib.reload(app.services.llm_service)
    app.services.llm_service._llm_service = None
    rag.llm_service = get_llm_service()
    
    print("Invalid Key Query:")
    res = rag.answer_query("What topics commonly appear in software engineering interviews?")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    run_error_tests()
