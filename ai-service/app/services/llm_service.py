import logging
from typing import Dict, List, Optional
from app.config import settings
import google.generativeai as genai
from openai import OpenAI

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.provider = settings.llm_provider.lower()
        self.openai_client = None
        self.gemini_model = None
        
        if self.provider == "gemini":
            if settings.gemini_api_key:
                genai.configure(api_key=settings.gemini_api_key)
                self.gemini_model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.openai_client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
            self.model = settings.openai_model
        
    def generate_answer(self, query: str, context_snippets: List[str]) -> Dict:
        if not context_snippets:
            return {
                "answer": "Insufficient retrieved evidence is available to answer this question. Try a broader question or add relevant interview experiences.",
                "success": True
            }
            
        if self.provider == "gemini" and not self.gemini_model:
            return {
                "answer": "Error: GEMINI_API_KEY is not configured.",
                "success": False
            }
        elif self.provider != "gemini" and not self.openai_client:
            return {
                "answer": "Error: OPENAI_API_KEY is not configured.",
                "success": False
            }
            
        context_text = "\n\n---\n\n".join(context_snippets)
        
        prompt = f"""You are an AI assistant helping students prepare for technical interviews based ONLY on the provided interview experiences.

Instructions:
- Answer the user's question using ONLY the provided interview experiences below.
- Do not invent facts, questions, or topics.
- If the answer cannot be found in the provided evidence, clearly state: "Insufficient retrieved evidence is available to answer this question."
- When citing specific questions or details, distinguish between different interview experiences if possible (e.g. "In an Amazon SDE interview...", "One candidate reported...").
- Be concise, structured, and helpful.

Retrieved Interview Experiences:
{context_text}

User Question: {query}"""

        try:
            if self.provider == "gemini":
                response = self.gemini_model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(temperature=0.1)
                )
                return {
                    "answer": response.text,
                    "success": True
                }
            else:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful and honest technical interview assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                )
                return {
                    "answer": response.choices[0].message.content,
                    "success": True
                }
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return {
                "answer": "An error occurred while generating the answer with the AI service.",
                "success": False,
                "error": str(e)
            }

_llm_service = None
def get_llm_service():
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
