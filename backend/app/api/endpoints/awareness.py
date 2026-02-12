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
    # Logic to generate recommendations
    recommendations = []
    
    if request.phishing_clicks > 0:
        recommendations.append({
            "topic": "Phishing Awareness",
            "risk": "High",
            "advice": "Review the 'Social Engineering' module. Always check sender email and unexpected links."
        })
    else:
        recommendations.append({
            "topic": "Phishing Awareness",
            "risk": "Low",
            "advice": "Good job spotting phishing attempts! Stay vigilant."
        })

    if request.weak_passwords_count > 0:
        recommendations.append({
            "topic": "Password Security",
            "risk": "Medium",
            "advice": "Use a password manager and enable MFA. Avoid simple dictionary words."
        })

    score = 100 - (request.phishing_clicks * 20) - (request.weak_passwords_count * 10)
    score = max(0, score)

    return {
        "user_name": request.user_name,
        "security_score": score,
        "recommendations": recommendations,
        "training_status": "Complete" if score > 80 else "Needs Improvement"
    }

@router.get("/")
def read_awareness_root():
    return {"message": "Awareness Training Module Ready"}
