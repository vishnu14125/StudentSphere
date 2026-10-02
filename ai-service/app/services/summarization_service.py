from openai import OpenAI
from typing import Dict, List
from app.config import settings


class SummarizationService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    def summarize_interview(self, text: str) -> Dict:
        """Generate summary and extract topics/questions from interview experience."""
        if not self.client:
            # Fallback to simple extraction if no API key
            return self._fallback_summarization(text)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an AI assistant that analyzes interview experiences. 
                        Your task is to:
                        1. Provide a concise summary of the interview experience
                        2. Extract key technical topics mentioned
                        3. Extract important questions asked
                        
                        Return your response in the following JSON format:
                        {
                            "summary": "Brief summary of the interview",
                            "topics": ["topic1", "topic2", ...],
                            "questions": ["question1", "question2", ...]
                        }"""
                    },
                    {
                        "role": "user",
                        "content": f"Analyze this interview experience:\n\n{text}"
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return {
                "summary": result.get("summary", ""),
                "topics": result.get("topics", []),
                "questions": result.get("questions", [])
            }
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_summarization(text)
    
    def _fallback_summarization(self, text: str) -> Dict:
        """Fallback summarization without AI API."""
        # Simple text-based extraction
        words = text.split()
        
        # Create a simple summary (first 3 sentences)
        sentences = text.split('. ')
        summary = '. '.join(sentences[:3]) if len(sentences) > 3 else text
        
        # Extract potential topics (common technical terms)
        common_topics = [
            "arrays", "linked lists", "trees", "graphs", "dynamic programming",
            "hashing", "sorting", "searching", "recursion", "backtracking",
            "database", "sql", "nosql", "api", "rest", "frontend", "backend",
            "javascript", "python", "java", "c++", "system design", "oop"
        ]
        
        text_lower = text.lower()
        topics = list(set([topic for topic in common_topics if topic in text_lower]))
        
        # Extract questions (lines ending with ?)
        questions = [line.strip() for line in text.split('\n') if '?' in line and len(line.strip()) > 10]
        
        return {
            "summary": summary[:500] + "..." if len(summary) > 500 else summary,
            "topics": topics[:10],
            "questions": questions[:5]
        }


# Global summarization service instance
_summarization_service = None


def get_summarization_service():
    global _summarization_service
    if _summarization_service is None:
        _summarization_service = SummarizationService()
    return _summarization_service
