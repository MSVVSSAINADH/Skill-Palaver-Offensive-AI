import joblib
import os
import string
import numpy as np

class MLService:
    def __init__(self):
        self.pwd_model = None
        self.risk_model = None
        self.models_loaded = False

    def load_models(self):
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) # Adjust path to root
        models_dir = os.path.join(base_path, "ml_models")
        
        pwd_path = os.path.join(models_dir, "password_model.pkl")
        risk_path = os.path.join(models_dir, "risk_model.pkl")

        if os.path.exists(pwd_path) and os.path.exists(risk_path):
            try:
                self.pwd_model = joblib.load(pwd_path)
                self.risk_model = joblib.load(risk_path)
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

    def predict_user_risk(self, clicks: int, weak_pwds: int, training_done: bool) -> dict:
        if not self.models_loaded:
            self.load_models()
            
        if not self.models_loaded:
             return {"error": "Model not loaded"}

        features = [clicks, weak_pwds, int(training_done)]
        prediction = self.risk_model.predict([features])[0]
        
        labels = ["Low Risk", "High Risk"]
        return {"risk_score": int(prediction), "label": labels[prediction]}

ml_service = MLService()
