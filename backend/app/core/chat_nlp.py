from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

class ChatNLPAnalyzer:
    """
    Lightweight, offline NLP pipeline for free-form chat phishing analysis.
    Uses TF-IDF + rules/classifier to detect intent and apply a strict confidence threshold.
    """
    def __init__(self):
        # Synthetic minimal corpus for basic intent detection mapped strictly to problem statement domains
        corpus = [
            # credential harvesting
            "please enter your password here",
            "verify your login credentials immediately",
            "we need your pin code to proceed",
            "update your account details using your current password",
            
            # link bait
            "click here to claim your prize",
            "check out this amazing link",
            "you just won tap this link",
            "download the secure attachment below",
            
            # urgency
            "your account will be suspended in 24 hours",
            "act fast before time runs out",
            "immediate action required",
            "urgent notice regarding your payment",
            
            # authority impersonation
            "this is the ceo speaking transfer the funds now",
            "hr department needs you to sign this mandate",
            "it support here please run this diagnostic tool",
            "i am your manager, do this confidentially"
        ]
        
        labels = [
            "credential_harvesting", "credential_harvesting", "credential_harvesting", "credential_harvesting",
            "link_bait", "link_bait", "link_bait", "link_bait",
            "urgency", "urgency", "urgency", "urgency",
            "authority", "authority", "authority", "authority"
        ]
        
        self.vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
        X = self.vectorizer.fit_transform(corpus)
        
        self.classifier = MultinomialNB()
        self.classifier.fit(X, labels)

    def analyze_chat(self, text: str) -> dict:
        """
        Analyzes free-form user string input and buckets intent.
        Returns the labeled result or 'uncertain' if confidence < 0.6.
        """
        # Transform input
        X_input = self.vectorizer.transform([text])
        
        # Predict probability
        probs = self.classifier.predict_proba(X_input)[0]
        max_prob_index = np.argmax(probs)
        confidence = probs[max_prob_index]
        
        label = self.classifier.classes_[max_prob_index]
        
        # Apply strict confidence threshold as per requirements
        if confidence < 0.6:
            label = "uncertain"
            
        return {
            "intent_label": label,
            "confidence_score": round(float(confidence), 3),
            "requires_human_review": label == "uncertain"
        }

chat_nlp = ChatNLPAnalyzer()
