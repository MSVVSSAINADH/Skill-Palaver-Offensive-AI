import sys
import os
import hashlib
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.core.attacks import PasswordAttacker
from app.core.social_eng import social_engineer
from app.core.chat_nlp import chat_nlp
from app.core.ml import ml_service
from app.core.adaptive_engine import adaptive_engine

attacker = PasswordAttacker()

print("--- 🔐 SECTION A — Password Attack Engine ---")
# Test A1: Dictionary Attack
pwd = "admin123"
md5_hash = hashlib.md5(pwd.encode()).hexdigest()
base_words = ["password", "admin", "root"]

start = time.time()
cracked, guess, attempts = attacker.dictionary_attack(md5_hash, "md5", base_words, use_rules=True, mutation_intensity="high")
elapsed = time.time() - start
print(f"Test A1 - Dictionary (High Intensity): Cracked={cracked}, Guess={guess}, Attempts={attempts}, Time={elapsed:.4f}s")
if cracked and guess == "admin123":
    print("Test A1 Result: PASS\n")
else:
    print("Test A1 Result: FAIL\n")

# Test A2: Brute Force Bounds
pwd_bf = "a1!"
md5_bf = hashlib.md5(pwd_bf.encode()).hexdigest()
cracked_bf, guess_bf, attempts_bf = attacker.brute_force_attack(md5_bf, "md5", max_length=4, timeout=5)
print(f"Test A2 - Brute Force: Cracked={cracked_bf}, Guess={guess_bf}, Attempts={attempts_bf}")
if cracked_bf and guess_bf == "a1!":
    print("Test A2 Result: PASS\n")
else:
    print("Test A2 Result: FAIL\n")


print("--- 🎣 SECTION B — Social Engineering Engine ---")
# Test B1: Phishing Analysis
email_text = "URGENT: Verify your account immediately at http://fake-bank.com"
analysis = social_engineer.analyze_email(email_text)
print(f"Test B1 - Analysis: Score={analysis['score']}, Rating={analysis['rating']}, Indicators={analysis['indicators']}")
if analysis['score'] > 70 and "Urgency trigger: 'urgent'" in analysis['indicators'] and "Suspicious link pattern: 'http://'" in analysis['indicators']:
    print("Test B1 Result: PASS\n")
else:
    print("Test B1 Result: FAIL\n")

# Test B2: Adaptive Generation
low_risk_email = social_engineer.generate_email("hr", "urgent", difficulty="basic")
high_risk_email = social_engineer.generate_email("hr", "urgent", difficulty="advanced")
print(f"Test B2 - Basic: {repr(low_risk_email['content'][:50])}...")
print(f"Test B2 - Advanced: {repr(high_risk_email['content'][:100])}...")
if "(Note: Generated via Advanced Adaptive Simulation)" in high_risk_email['content']:
    print("Test B2 Result: PASS\n")
else:
    print("Test B2 Result: FAIL\n")


print("--- 💬 SECTION C — Chat NLP Analyzer ---")
# Test C1: Clear Phishing
c1_text = "Click this link immediately to avoid account suspension"
c1_res = chat_nlp.analyze_chat(c1_text)
print(f"Test C1 - Clear Phishing: Intent={c1_res['intent_label']}, Confidence={c1_res.get('confidence_score')}")
if c1_res['intent_label'] != "uncertain" and c1_res.get('confidence_score', 0) >= 0.6:
     print("Test C1 Result: PASS\n")
else:
     print("Test C1 Result: FAIL\n")

# Test C2: Ambiguous Message
c2_text = "Hey did you watch the football match yesterday?"
c2_res = chat_nlp.analyze_chat(c2_text)
print(f"Test C2 - Ambiguous: Intent={c2_res['intent_label']}, Confidence={c2_res.get('confidence_score')}")
if c2_res['intent_label'] == "uncertain" and c2_res.get('confidence_score', 1.0) < 0.6:
     print("Test C2 Result: PASS\n")
else:
     print("Test C2 Result: FAIL\n")


print("--- 🧠 SECTION D — ML Models ---")
ml_service.load_models()

# D1
risk = ml_service.predict_user_risk(clicks=3, weak_pwds=5, simulations_run=10)
print(f"Test D1 - Risk Model: {risk}")

# D2
strength_pred = ml_service.predict_password_strength("P@ssw0rd123!")
print(f"Test D2 - Password Strength: {strength_pred}")

# D3
suscep = ml_service.predict_phishing_susceptibility(past_clicks=0.8, training_rate=0.2, urgency_time=5.0, weak_pw=4, sec_score=20)
print(f"Test D3 - Susceptibility: {suscep}")

# D4
factor = ml_service.predict_crack_time_factor(length=8, charset=62, entropy=47.6, pattern_score=80)
print(f"Test D4 - Crack Time Factor: {factor}")


print("--- ⚙️ SECTION E — Adaptive Engine ---")
# Low Risk User
params_low = adaptive_engine.get_password_attack_parameters(user_clicks=0, user_weak_pwds=0, simulations_run=10)
print(f"Test E1 - Low Risk Params: {params_low}")
# High Risk User
params_high = adaptive_engine.get_password_attack_parameters(user_clicks=5, user_weak_pwds=5, simulations_run=10)
print(f"Test E1 - High Risk Params: {params_high}")

if params_low['mutation_intensity'] == 'low' and params_high['mutation_intensity'] == 'high':
    print("Test E1 Result: PASS\n")
else:
    print("Test E1 Result: FAIL\n")

print("--- 🛡️ SECTION G — Safety Mechanisms ---")
import tempfile
import shutil

# Temporarily rename models dir to test fallback
models_dir = os.path.join(os.path.dirname(__file__), 'ml_models')
backup_dir = os.path.join(os.path.dirname(__file__), 'ml_models_backup')
shutil.move(models_dir, backup_dir)
try:
    ml_service_fail = ml_service.__class__()
    risk_fail = ml_service_fail.predict_user_risk(5,5,5)
    print(f"Test G1 - Fallback Risk: {risk_fail}")
    if "Fallback" in risk_fail.get("label", ""):
        print("Test G1 Result: PASS\n")
    else:
        print("Test G1 Result: FAIL\n")
finally:
    shutil.move(backup_dir, models_dir)
