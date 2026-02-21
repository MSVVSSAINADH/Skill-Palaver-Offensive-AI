import sys
import os

# Ensure backend acts as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.core.chat_nlp import chat_nlp
from app.core.password_patterns import pattern_analyzer

print("--- Testing Chat NLP Classifier ---")
res1 = chat_nlp.analyze_chat("verify your login credentials immediately")
print(f"Test 1 (Obvious Phishing): {res1}")

res2 = chat_nlp.analyze_chat("Hi, did you watch the football game last night? It was crazy.")
print(f"Test 2 (Unrelated Chat): {res2}")

print("\n--- Testing Password Pattern Analyzer ---")
pwd_res = pattern_analyzer.analyze("qwerty2024!")
print(f"Pattern Analysis for 'qwerty2024!': {pwd_res}")

pwd_res2 = pattern_analyzer.analyze("admin123admin")
print(f"Pattern Analysis for 'admin123admin': {pwd_res2}")

print("\n--- Tests Complete ---")
