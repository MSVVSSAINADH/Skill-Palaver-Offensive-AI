import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
import joblib
import os
import string
import random

# Create directory if not exists
os.makedirs("ml_models", exist_ok=True)

# --- 1. Password Strength Model ---
print("Training Password Strength Model...")

def generate_passwords(n=1500):
    data = []
    # Weak: Only digits or only lowercase, short
    for _ in range(n // 3):
        pwd = ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 6)))
        if random.random() < 0.5:
            pwd = ''.join(random.choices(string.digits, k=random.randint(4, 6)))
        data.append((pwd, 0))
    # Medium: Alphanumeric, medium length
    for _ in range(n // 3):
        pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(6, 8)))
        data.append((pwd, 1))
    # Strong: Mixed case, digits, special chars, long
    chars = string.ascii_letters + string.digits + string.punctuation
    for _ in range(n - (2 * (n // 3))):
        pwd = ''.join(random.choices(chars, k=random.randint(10, 16)))
        pwd += random.choice(string.punctuation) + random.choice(string.ascii_uppercase) + random.choice(string.digits)
        data.append((pwd, 2))
    return data

df_pwd = pd.DataFrame(generate_passwords(1500), columns=["password", "strength"])

def extract_features(password):
    return [
        len(password),
        sum(c.isdigit() for c in password),
        sum(c.isupper() for c in password),
        sum(c in string.punctuation for c in password)
    ]

X_pwd = np.array([extract_features(p) for p in df_pwd["password"]])
y_pwd = df_pwd["strength"]

X_train, X_test, y_train, y_test = train_test_split(X_pwd, y_pwd, test_size=0.2, random_state=42)

clf_pwd = RandomForestClassifier(n_estimators=50, random_state=42)
clf_pwd.fit(X_train, y_train)

y_pred = clf_pwd.predict(X_test)
print("\nPassword Model Performance:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(clf_pwd, "ml_models/password_model.pkl")
print("Password Model Saved.\n")

# --- 2. Risk Classification Model ---
print("Training Risk Classification Model...")
# Features: [phishing_clicks, weak_passwords_count, simulations_run]
# Target: 0=Low Risk, 1=High Risk
def generate_risk_data(n=1500):
    data = []
    for _ in range(n):
        sims = random.randint(1, 20)
        clicks = random.randint(0, sims) 
        weak_pw = random.randint(0, 5)
        
        # Risk Logic
        risk = 0
        if (clicks / sims) >= 0.3 or weak_pw >= 2:
            risk = 1
        data.append(([clicks, weak_pw, sims], risk))
    return data

risk_data = generate_risk_data(1500)
X_risk = np.array([x[0] for x in risk_data])
y_risk = np.array([x[1] for x in risk_data])

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_risk, y_risk, test_size=0.2, random_state=42)

clf_risk = LogisticRegression()
clf_risk.fit(X_train_r, y_train_r)

y_pred_r = clf_risk.predict(X_test_r)
print("\nRisk Classification Model Performance:")
print("Accuracy:", accuracy_score(y_test_r, y_pred_r))
print(classification_report(y_test_r, y_pred_r))

joblib.dump(clf_risk, "ml_models/risk_model.pkl")
print("Risk Model Saved.")

# --- 3. Phishing Susceptibility Model ---
print("\nTraining Phishing Susceptibility Model...")
# Features: past_click_rate, training_completion_rate, urgency_response_time, weak_password_count, security_score
# Target: 0 = Safe, 1 = Clicked Phishing

def generate_susceptibility_data(n=1500):
    data = []
    for _ in range(n):
        click_rate = random.uniform(0.0, 1.0)
        training_rate = random.uniform(0.0, 1.0)
        urgency_response = random.uniform(1.0, 60.0) # minutes
        weak_pw_count = random.randint(0, 5)
        sec_score = random.randint(0, 100)
        
        # Logic for susceptibility target
        susceptibility_prob = click_rate * 0.4 + (1 - training_rate) * 0.3 + (1 / urgency_response) * 0.2 + (weak_pw_count / 5) * 0.1
        susceptibility_prob += random.uniform(-0.1, 0.1) # Noise
        
        clicked = 1 if susceptibility_prob > 0.5 else 0
        data.append(([click_rate, training_rate, urgency_response, weak_pw_count, sec_score], clicked))
    return data

suscep_data = generate_susceptibility_data(1500)
X_suscep = np.array([x[0] for x in suscep_data])
y_suscep = np.array([x[1] for x in suscep_data])

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_suscep, y_suscep, test_size=0.2, random_state=42)

clf_suscep = GradientBoostingClassifier(n_estimators=100, random_state=42)
clf_suscep.fit(X_train_s, y_train_s)

y_pred_s = clf_suscep.predict(X_test_s)
print("\nPhishing Susceptibility Model Performance:")
print("Accuracy:", accuracy_score(y_test_s, y_pred_s))
print(classification_report(y_test_s, y_pred_s))

joblib.dump(clf_suscep, "ml_models/phishing_susceptibility_model.pkl")
print("Phishing Susceptibility Model Saved.")

# --- 4. Estimated Crack Time Predictor (ML-based) ---
print("\nTraining Crack Time Predictor (Hybrid Factor) Model...")
# Features: password length, charset size, entropy estimate, pattern score (0-100)
# Target: ML adjustment factor (multiplier, e.g., 0.1 to 1.1)

def generate_crack_time_data(n=1500):
    data = []
    for _ in range(n):
        length = random.randint(4, 30)
        charset = random.choice([10, 26, 36, 52, 62, 94])
        entropy = length * np.log2(charset) if charset > 0 else 0
        pattern_score = random.randint(0, 100)
        
        # Baseline adjustment factor formula: high pattern predictability means smaller factor (faster crack)
        adjustment_factor = 1.0 - (pattern_score / 100.0) * 0.9 
        adjustment_factor += random.uniform(-0.05, 0.05)
        adjustment_factor = max(0.01, min(5.0, adjustment_factor)) 
        
        data.append(([length, charset, entropy, pattern_score], adjustment_factor))
    return data

crack_time_data = generate_crack_time_data(1500)
X_ct = np.array([x[0] for x in crack_time_data])
y_ct = np.array([x[1] for x in crack_time_data])

X_train_ct, X_test_ct, y_train_ct, y_test_ct = train_test_split(X_ct, y_ct, test_size=0.2, random_state=42)

reg_ct = RandomForestRegressor(n_estimators=50, random_state=42)
reg_ct.fit(X_train_ct, y_train_ct)

y_pred_ct = reg_ct.predict(X_test_ct)
print("\nCrack Time Estimator (Factor) Performance:")
print("MSE:", mean_squared_error(y_test_ct, y_pred_ct))
print("R2 Score:", r2_score(y_test_ct, y_pred_ct))

joblib.dump(reg_ct, "ml_models/crack_time_model.pkl")
print("Crack Time Predictor Model Saved.\n")
