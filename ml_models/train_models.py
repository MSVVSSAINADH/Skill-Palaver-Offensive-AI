import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
import joblib
import os
import string

# Create directory if not exists
os.makedirs("ml_models", exist_ok=True)

# --- 1. Password Strength Model ---
print("Training Password Strength Model...")
# Synthetic dataset: password, strength (0=weak, 1=medium, 2=strong)
data = [
    ("password", 0), ("123456", 0), ("qwerty", 0),
    ("admin123", 1), ("pass1234", 1), ("Welcome1", 1),
    ("P@ssw0rd2024!", 2), ("Xy9#mK2$pL", 2), ("Correct-Horse-Battery-Staple", 2)
]
df_pwd = pd.DataFrame(data, columns=["password", "strength"])

def extract_features(password):
    return [
        len(password),
        sum(c.isdigit() for c in password),
        sum(c.isupper() for c in password),
        sum(c in string.punctuation for c in password)
    ]

X_pwd = np.array([extract_features(p) for p in df_pwd["password"]])
y_pwd = df_pwd["strength"]

clf_pwd = RandomForestClassifier(n_estimators=10, random_state=42)
clf_pwd.fit(X_pwd, y_pwd)
joblib.dump(clf_pwd, "ml_models/password_model.pkl")
print("Password Model Saved.")

# --- 2. Risk Classification Model ---
print("Training Risk Classification Model...")
# Features: [phishing_clicks, weak_passwords_count, training_completed]
# Target: 0=Low Risk, 1=High Risk
risk_data = [
    ([0, 0, 1], 0), ([1, 1, 1], 0), 
    ([5, 2, 0], 1), ([3, 5, 0], 1),
    ([0, 1, 0], 0), ([10, 0, 0], 1)
]
X_risk = np.array([x[0] for x in risk_data])
y_risk = np.array([x[1] for x in risk_data])

clf_risk = LogisticRegression()
clf_risk.fit(X_risk, y_risk)
joblib.dump(clf_risk, "ml_models/risk_model.pkl")
print("Risk Model Saved.")
