from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
from app.core.ml import ml_service

class PasswordCheckRequest(BaseModel):
    password: str

class RiskCheckRequest(BaseModel):
    clicks: int
    weak_passwords: int
    training_completed: bool

@router.post("/password-strength")
def check_password_strength(request: PasswordCheckRequest):
    return ml_service.predict_password_strength(request.password)

@router.post("/user-risk")
def check_user_risk(request: RiskCheckRequest):
    return ml_service.predict_user_risk(request.clicks, request.weak_passwords, request.training_completed)

