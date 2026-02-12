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
        return {
            "simulations_run": self.simulations_run,
            "weak_passwords": self.weak_passwords_found,
            "phishing_campaigns": self.phishing_campaigns_generated,
            "threat_level": "Low"  # Static for now
        }

stats_service = StatsService()
