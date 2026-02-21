from datetime import datetime

class StatsService:
    def __init__(self):
        self.simulations_run = 0
        self.weak_passwords_found = 0
        self.phishing_campaigns_generated = 0
        self.start_time = datetime.now()

    def increment_simulations(self):
        self.simulations_run += 1

    def increment_weak_passwords(self):
        self.weak_passwords_found += 1

    def increment_phishing(self):
        self.phishing_campaigns_generated += 1
        self.simulations_run += 1

    def get_stats(self):
        from app.core.ml import ml_service
        
        # Calculate dynamic susceptibility for the admin dashboard based on whole-platform metrics
        click_rate = self.weak_passwords_found / max(1, self.simulations_run)
        training_rate = 0.5 # assumed baseline for this demo view
        urgency = 10.0 # avg response minutes
        sec_score = 100 - (click_rate * 100)
        
        suscept_pred = ml_service.predict_phishing_susceptibility(click_rate, training_rate, urgency, self.weak_passwords_found, sec_score)
        
        return {
            "simulations_run": self.simulations_run,
            "weak_passwords": self.weak_passwords_found,
            "phishing_campaigns": self.phishing_campaigns_generated,
            "susceptibility_label": suscept_pred.get("label", "Safe"),
            "threat_level": "High" if click_rate > 0.3 else "Low"
        }

stats_service = StatsService()
