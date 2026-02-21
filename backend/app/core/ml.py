import joblib
import os
import string
import numpy as np

class MLService:
    def __init__(self):
        self.pwd_model = None
        self.risk_model = None
        self.suscep_model = None
        self.crack_time_model = None
        self.models_loaded = False

    def load_models(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # Adjust path to root
        models_dir = os.path.join(base_path, "ml_models")
        
        pwd_path = os.path.join(models_dir, "password_model.pkl")
        risk_path = os.path.join(models_dir, "risk_model.pkl")
        suscep_path = os.path.join(models_dir, "phishing_susceptibility_model.pkl")
        crack_path = os.path.join(models_dir, "crack_time_model.pkl")

        if os.path.exists(pwd_path) and os.path.exists(risk_path) and os.path.exists(suscep_path) and os.path.exists(crack_path):
            try:
                self.pwd_model = joblib.load(pwd_path)
                self.risk_model = joblib.load(risk_path)
                self.suscep_model = joblib.load(suscep_path)
                self.crack_time_model = joblib.load(crack_path)
                self.models_loaded = True
                print("ML Models loaded successfully.")
            except Exception as e:
                print(f"Error loading models: {e}")
        else:
            print("Models not found. Run training script first.")

    def predict_password_strength(self, password: str) -> dict:
        if not self.models_loaded:
            self.load_models()
        
        if not self.models_loaded:
            return {"error": "Model not loaded"}
        
        # Feature extraction must match training
        features = [
            len(password),
            sum(c.isdigit() for c in password),
            sum(c.isupper() for c in password),
            sum(c in string.punctuation for c in password)
        ]
        
        prediction = self.pwd_model.predict([features])[0]
        # 0=Low, 1=Medium, 2=Strong
        labels = ["Low", "Medium", "High"]
        return {"strength_score": int(prediction), "label": labels[prediction]}

    def predict_user_risk(self, clicks: int, weak_pwds: int, simulations_run: int) -> dict:
        if not self.models_loaded:
            self.load_models()
            
        if not self.models_loaded:
             return {"error": "Model not loaded, using fallback", "risk_score": 0, "label": "Low Risk (Fallback)"}

        features = [clicks, weak_pwds, simulations_run]
        prediction = self.risk_model.predict([features])[0]
        
        labels = ["Low Risk", "High Risk"]
        return {"risk_score": int(prediction), "label": labels[prediction]}

    def predict_phishing_susceptibility(self, past_clicks: float, training_rate: float, urgency_time: float, weak_pw: int, sec_score: int) -> dict:
        if not self.models_loaded:
            self.load_models()
            
        if not self.models_loaded:
             return {"error": "Model not loaded, using fallback", "susceptibility": 0.5, "label": "Safe (Fallback)"}

        features = [past_clicks, training_rate, urgency_time, weak_pw, sec_score]
        prediction = self.suscep_model.predict([features])[0]
        
        labels = ["Safe", "High Risk of Clicking"]
        return {"susceptibility": int(prediction), "label": labels[prediction]}

    def predict_crack_time_factor(self, length: int, charset: int, entropy: float, pattern_score: int) -> float:
        if not self.models_loaded:
            self.load_models()
            
        if not self.models_loaded:
             return 1.0

        features = [length, charset, entropy, pattern_score]
        try:
            factor = self.crack_time_model.predict([features])[0]
            return float(factor)
        except Exception:
            return 1.0

ml_service = MLService()
