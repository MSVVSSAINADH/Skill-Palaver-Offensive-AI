from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import time
import hashlib
import bcrypt
import random
import string

router = APIRouter()

class PasswordAttackRequest(BaseModel):
    target_hash: str
    hash_type: str  # md5, sha256, bcrypt
    attack_type: str  # dictionary, bruteforce, ai_guided, mask
    max_length: Optional[int] = 5
    hints: Optional[dict] = None
    mask: Optional[str] = None
    use_rules: Optional[bool] = False

class PasswordAttackResponse(BaseModel):
    cracked: bool
    password: Optional[str]
    time_taken: float
    attempts: int
    method: str

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
    attacker = PasswordAttacker()
    
    if request.attack_type == "dictionary":
        wordlist = DICTIONARY + (list(request.hints.values()) if request.hints else [])
        # Flatten hints if they are a dict context (though request.hints values is cleaner)
        if request.hints:
             for k, v in request.hints.items():
                 if isinstance(v, str):
                     wordlist.append(v)

        cracked, pwd, attempts = attacker.dictionary_attack(request.target_hash, request.hash_type, wordlist, use_rules=request.use_rules)
        cracked_password = pwd
    
    elif request.attack_type == "mask":
        mask = request.mask if request.mask else "?l?l?l?l"
        cracked, pwd, attempts = attacker.mask_attack(request.target_hash, request.hash_type, mask, timeout=15)
        cracked_password = pwd

    elif request.attack_type == "bruteforce":
        # Use user-provided max length, default to 4 if not provided (safety cap at 6 for demo)
        max_len = request.max_length if request.max_length else 4
        if max_len > 6: max_len = 6 # Safety cap
        cracked, pwd, attempts = attacker.brute_force_attack(request.target_hash, request.hash_type, max_length=max_len, timeout=15)
        cracked_password = pwd
    
    else:
        # AI Guided
        hints = request.hints if request.hints else {}
        cracked, pwd, attempts = attacker.ai_guided_attack(request.target_hash, request.hash_type, hints)
        cracked_password = pwd

    from app.core.stats import stats_service
    stats_service.increment_simulations()
    if cracked:
        stats_service.increment_weak_passwords()

    return PasswordAttackResponse(
        cracked=cracked,
        password=cracked_password,
        time_taken=time.time() - start_time,
        attempts=attempts,
        method=request.attack_type
    )
