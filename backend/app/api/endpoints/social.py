from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from app.core.social_eng import social_engineer

router = APIRouter()

class Persona(str, Enum):
    hr = "hr"
    finance = "finance"
    it = "it"

class Tone(str, Enum):
    urgent = "urgent"
    friendly = "friendly"
    authority = "authority"

class PhishingRequest(BaseModel):
    persona: Persona
    tone: Tone

class AnalysisRequest(BaseModel):
    content: str = Field(..., min_length=10, max_length=5000, description="The email text to analyze")

class Scenario(str, Enum):
    it_support = "it_support"
    prize = "prize"
    ceo_fraud = "ceo_fraud"

class ChatRequest(BaseModel):
    scenario: Scenario

class ChatAnalysisRequest(BaseModel):
    message: str = Field(..., min_length=2, max_length=2000, description="The free-form chat message to analyze")

@router.post("/generate")
def generate_phishing_email(request: PhishingRequest):
    from app.core.stats import stats_service
    from app.core.adaptive_engine import adaptive_engine
    
    stats_service.increment_phishing()
    current_stats = stats_service.get_stats()
    
    try:
        adaptive_params = adaptive_engine.get_phishing_parameters(
            current_stats.get("phishing_campaigns", 0),
            current_stats.get("weak_passwords", 0),
            current_stats.get("simulations_run", 0)
        )
        difficulty = adaptive_params["difficulty_level"]
    except Exception:
        difficulty = "basic"
        
    return social_engineer.generate_email(request.persona.value, request.tone.value, difficulty=difficulty)

@router.post("/analyze")
def analyze_phishing_email(request: AnalysisRequest):
    return social_engineer.analyze_email(request.content)

@router.get("/email/simulation")
def get_simulation_email():
    return social_engineer.generate_simulation_email()

@router.post("/chat/generate")
def generate_chat_script(request: ChatRequest):
    return social_engineer.generate_chat_script(request.scenario.value)

@router.post("/chat/analyze")
def analyze_chat(request: ChatAnalysisRequest):
    from app.core.chat_nlp import chat_nlp
    from app.core.model_monitor import monitor
    
    analysis = chat_nlp.analyze_chat(request.message)
    monitor.log_prediction("chat_nlp_model", [request.message], analysis["intent_label"], analysis.get("confidence_score"))
    return analysis
