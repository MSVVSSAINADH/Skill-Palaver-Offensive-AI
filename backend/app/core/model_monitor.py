import logging
import time

# Configure lightweight custom logging for ML operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMonitor:
    """
    Lightweight MLOps visibility tracker.
    Non-blocking hooks to log predictions, confidence scores, and basic metrics.
    """
    def __init__(self):
        self.prediction_count = 0
        self.drift_warnings = 0

    def log_prediction(self, model_name: str, input_features: list, prediction: any, confidence: float = None):
        """
        Logs an executed ML prediction block. Can handle simple integer prediction outputs,
        as well as continuous vectors or text intents.
        """
        self.prediction_count += 1
        log_msg = f"[MLOps] Model: {model_name} | Input: {input_features} | Pred: {prediction}"
        
        if confidence is not None:
             log_msg += f" | Conf: {confidence:.2f}"
             
        logger.info(log_msg)
        
        # Schema for Data Drift Warning 
        self.check_data_drift(model_name, input_features)

    def check_data_drift(self, model_name: str, input_features: list):
        """
        Placeholder schema designed for detecting data drift over time.
        In a cloud production state, this would pipe out to an external validation distribution.
        """
        # Generic heuristic flag check logic goes here
        # Example: if len(input_features) causes an unexpected anomaly state
        pass

monitor = ModelMonitor()
