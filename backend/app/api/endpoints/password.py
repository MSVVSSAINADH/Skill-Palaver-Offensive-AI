from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time
import hashlib
import bcrypt
import random
import string

router = APIRouter()

from enum import Enum
from pydantic import BaseModel, Field

class HashType(str, Enum):
    md5 = "md5"
    sha256 = "sha256"
    bcrypt = "bcrypt"

class AttackType(str, Enum):
    dictionary = "dictionary"
    bruteforce = "bruteforce"
    ai_guided = "ai_guided"
    mask = "mask"

class PasswordAttackRequest(BaseModel):
    target_hash: str = Field(..., min_length=1, description="The target hash string")
    hash_type: HashType
    attack_type: AttackType
    max_length: Optional[int] = Field(5, ge=1, le=10)
    hints: Optional[dict] = None
    mask: Optional[str] = None
    use_rules: Optional[bool] = False

class PasswordAttackResponse(BaseModel):
    cracked: bool
    password: Optional[str]
    time_taken: float
    attempts: int
    method: str
    risk_severity: str
    estimated_crack_time: Optional[str] = None
    patterns_detected: Optional[list] = []
    predictability_score: Optional[int] = 0

import os

# Load dictionary from file
def load_dictionary():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "../../core/common_passwords.txt")
        # Ensure file exists, if not create a dummy one
        if not os.path.exists(file_path):
             with open(file_path, "w") as f:
                 f.write("password\n123456\nadmin\nwelcome\nqwerty\n")
        
        with open(file_path, "r") as f:
            return [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"Error loading dictionary: {e}")
        return ["123456", "password", "admin", "welcome", "qwerty"]

DICTIONARY = load_dictionary()

@router.post("/attack", response_model=PasswordAttackResponse)
async def attack_password(request: PasswordAttackRequest):
    start_time = time.time()
    attempts = 0
    cracked_password = None
    from app.core.attacks import PasswordAttacker
    from app.core.stats import stats_service
    from app.core.adaptive_engine import adaptive_engine
    
    current_stats = stats_service.get_stats()
    user_clicks = current_stats.get("phishing_campaigns", 0)
    user_weak = current_stats.get("weak_passwords", 0)
    sims_run = current_stats.get("simulations_run", 0)
    
    adaptive_params = adaptive_engine.get_password_attack_parameters(user_clicks, user_weak, sims_run)
    dict_depth = adaptive_params["dictionary_depth"]
    mut_intensity = adaptive_params["mutation_intensity"]
    bf_max_ad = adaptive_params["brute_force_max_length"]

    attacker = PasswordAttacker()
    
    if request.attack_type == "dictionary":
        wordlist = DICTIONARY + (list(request.hints.values()) if request.hints else [])
        # Flatten hints if they are a dict context (though request.hints values is cleaner)
        if request.hints:
             for k, v in request.hints.items():
                 if isinstance(v, str):
                     wordlist.append(v)

        if dict_depth == "shallow":
             wordlist = wordlist[:1000] # Limit depth per adaptive strictness

        cracked, pwd, attempts = attacker.dictionary_attack(
            request.target_hash, request.hash_type, wordlist, 
            use_rules=request.use_rules, mutation_intensity=mut_intensity
        )
        cracked_password = pwd
    
    elif request.attack_type == "mask":
        mask = request.mask if request.mask else "?l?l?l?l"
        cracked, pwd, attempts = attacker.mask_attack(request.target_hash, request.hash_type, mask, timeout=15)
        cracked_password = pwd

    elif request.attack_type == "bruteforce":
        max_len = request.max_length if request.max_length else 4
        max_len = min(max_len, bf_max_ad) # Override with adaptive bounds
        cracked, pwd, attempts = attacker.brute_force_attack(request.target_hash, request.hash_type, max_length=max_len, timeout=15)
        cracked_password = pwd
    
    else:
        # AI Guided
        hints = request.hints if request.hints else {}
        cracked, pwd, attempts = attacker.ai_guided_attack(
            request.target_hash, request.hash_type, hints, mutation_intensity=mut_intensity
        )
        cracked_password = pwd

    from app.core.stats import stats_service
    stats_service.increment_simulations()
    if cracked:
        stats_service.increment_weak_passwords()

    time_elapsed = time.time() - start_time
    risk_severity = "Low"
    patterns_det = []
    pred_score = 0
    est_crack_time = "Unknown"
    
    if cracked:
        if time_elapsed < 1.0: risk_severity = "Critical"
        elif time_elapsed < 10.0: risk_severity = "High"
        elif time_elapsed < 60.0: risk_severity = "Medium"

        # Apply Advanced Pattern Analysis
        from app.core.password_patterns import pattern_analyzer
        pattern_res = pattern_analyzer.analyze(cracked_password)
        patterns_det = pattern_res["patterns_detected"]
        pred_score = pattern_res["human_predictability_score"]
        
        # Apply Hybrid Math/ML Crack Time Estimation
        from app.core.ml import ml_service
        charset_size = 62 
        length = len(cracked_password)
        entropy = length * 5.95 
        ml_factor = ml_service.predict_crack_time_factor(length, charset_size, entropy, pred_score)
        
        base_combinations = charset_size ** length
        hashes_per_sec = 1000000000 # Assume robust attacking rig
        math_seconds = base_combinations / hashes_per_sec
        final_seconds = math_seconds * ml_factor
        
        if final_seconds < 60: est_crack_time = "Instant (< 1 min)"
        elif final_seconds < 3600: est_crack_time = f"~{int(final_seconds/60)} minutes"
        elif final_seconds < 86400: est_crack_time = f"~{int(final_seconds/3600)} hours"
        else: est_crack_time = f"~{int(final_seconds/86400)} days"
            
        from app.core.model_monitor import monitor
        monitor.log_prediction("crack_time_model", [length, charset_size, entropy, pred_score], ml_factor)

    return PasswordAttackResponse(
        cracked=cracked,
        password=cracked_password,
        time_taken=time_elapsed,
        attempts=attempts,
        method=request.attack_type,
        risk_severity=risk_severity,
        estimated_crack_time=est_crack_time,
        patterns_detected=patterns_det,
        predictability_score=pred_score
    )
