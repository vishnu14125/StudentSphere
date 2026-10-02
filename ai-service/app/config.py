try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    backend_url: str = "http://localhost:5000"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    llm_provider: str = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.6-flash"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chroma_persist_directory: str = "./vector_db"
    rag_top_k: int = 5
    rag_similarity_threshold: float = 0.25
    chunk_max_words: int = 150
    chunk_overlap_words: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
