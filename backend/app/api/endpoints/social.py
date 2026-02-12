from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
from typing import Optional
from app.core.social_eng import social_engineer

class PhishingRequest(BaseModel):
    persona: str
    tone: str

class AnalysisRequest(BaseModel):
    content: str

@router.post("/generate")
def generate_phishing_email(request: PhishingRequest):
    from app.core.stats import stats_service
    stats_service.increment_phishing()
    return social_engineer.generate_email(request.persona, request.tone)

@router.post("/analyze")
def analyze_phishing_email(request: AnalysisRequest):
    return social_engineer.analyze_email(request.content)

@router.get("/email/simulation")
def get_simulation_email():
    return social_engineer.generate_simulation_email()

class ChatRequest(BaseModel):
    scenario: str

@router.post("/chat/generate")
def generate_chat_script(request: ChatRequest):
    return social_engineer.generate_chat_script(request.scenario)

