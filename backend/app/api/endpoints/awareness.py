from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ReportRequest(BaseModel):
    user_name: str
    simulations_run: int
    phishing_clicks: int
    weak_passwords_count: int

@router.post("/generate")
def generate_report(request: ReportRequest):
    recommendations = []
    
    # Phishing Feedback
    if request.phishing_clicks > 0:
        risk_level = "High" if request.phishing_clicks >= max(1, request.simulations_run * 0.5) else "Medium"
        advice = (
            f"You fell for {request.phishing_clicks} phishing attempts. "
            "Attackers often use urgency and spoofed domains. Always verify unexpected requests via a secondary channel (e.g., call the sender)."
        )
        recommendations.append({
            "topic": "Phishing Awareness",
            "risk": risk_level,
            "advice": advice
        })
    elif request.simulations_run > 0:
        recommendations.append({
            "topic": "Phishing Awareness",
            "risk": "Low",
            "advice": "Excellent work spotting phishing attempts! Continue to scrutinize senders and links before clicking."
        })

    # Password Feedback
    if request.weak_passwords_count > 0:
        risk_level = "High" if request.weak_passwords_count > 2 else "Medium"
        advice = (
            f"You used {request.weak_passwords_count} weak passwords that could be cracked quickly. "
            "Stop relying on patterns (like appending '123' or '!') and start using a Password Manager to generate long, random passphrases."
        )
        recommendations.append({
            "topic": "Password Security",
            "risk": risk_level,
            "advice": advice
        })
    elif request.simulations_run > 0:
         recommendations.append({
            "topic": "Password Security",
            "risk": "Low",
            "advice": "Your password choices are resilient. Keep using secure, unique passphrases for each service."
        })
    
    score = 100 - (request.phishing_clicks * 20) - (request.weak_passwords_count * 10)
    score = max(0, score)

    return {
        "user_name": request.user_name,
        "security_score": score,
        "recommendations": recommendations,
        "training_status": "Complete" if score >= 80 else "Needs Improvement"
    }

@router.get("/")
def read_awareness_root():
    return {"message": "Awareness Training Module Ready"}
