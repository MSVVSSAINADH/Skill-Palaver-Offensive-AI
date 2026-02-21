from app.core.ml import ml_service

class AdaptiveEngine:
    """
    Dynamically scales attack sophistication based on ML risk predictions.
    Uses composition to query the MLService, ensuring loose coupling and isolated testing.
    """
    def __init__(self):
        # Using composition: engine inherently relies on querying the ml_service without inheriting it.
        pass

    def get_password_attack_parameters(self, user_clicks: int, user_weak_pwds: int, simulations_run: int) -> dict:
        """
        Returns dynamic dictionary depth, mutation intensity, and brute-force bounds
        based on the user's ML risk trajectory.
        """
        risk_prediction = ml_service.predict_user_risk(user_clicks, user_weak_pwds, simulations_run)
        risk_score = risk_prediction.get("risk_score", 0) # 0 = Low Risk, 1 = High Risk

        if risk_score == 1:
            return {
                "dictionary_depth": "deep",      # Use larger wordlists
                "mutation_intensity": "high",    # Heavy leet speak, capitalization manipulation
                "brute_force_max_length": 8      # Longer mathematical bounds checking
            }
        else:
            return {
                "dictionary_depth": "shallow",   # Top 1000 commonly used words only
                "mutation_intensity": "low",     # Basic append mutations
                "brute_force_max_length": 4      # Short bounds for rapid failure simulation
            }

    def get_phishing_parameters(self, user_clicks: int, user_weak_pwds: int, simulations_run: int) -> dict:
        """
        Returns the difficulty level for the next generative phishing template.
        """
        risk_prediction = ml_service.predict_user_risk(user_clicks, user_weak_pwds, simulations_run)
        risk_score = risk_prediction.get("risk_score", 0)
        
        if risk_score == 1:
            return {
                "difficulty_level": "advanced", # No obvious spelling or grammatical errors, highly targeted
                "urgency_payload": "high"       # Aggressive urgency phrasing in templates
            }
        else:
            return {
                "difficulty_level": "basic",    # Standard phishing logic with obvious red flags
                "urgency_payload": "low"        # Minimal urgency
            }

adaptive_engine = AdaptiveEngine()
