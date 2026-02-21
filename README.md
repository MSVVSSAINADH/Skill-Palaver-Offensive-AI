# Skill-Palaver-Offensive-AI

**Skill-Palaver-Offensive-AI** is an AI-driven, adaptive Cybersecurity simulator designed for Red-Team Awareness Training. It provides a safe, gamified environment to simulate real-world attacks such as password cracking and social engineering, empowering users to build practical defense skills and understand the mechanics of cyber threats.

> **⚠️ FOR EDUCATIONAL & SECURITY TRAINING PURPOSES ONLY**
> This platform is a dual-use red-team simulator intended strictly for controlled awareness training. It does not possess real-world exploit capabilities outside of its sandbox simulation environment.

## 🚀 Key Features

### 1. 🔐 Password Attack Simulation Engine
A realistic password attack simulator that demonstrates the vulnerabilities of weak passwords.
*   **Dictionary Attacks:** Highlights common password pitfalls.
*   **Brute-Force Simulations:** Visualizes hash cracking complexity and time estimation.
*   **AI-Guided Password Guessing:** Simulates intelligent, targeted guessing based on user patterns and hints.
*   Calculates Risk Severity Scores based on attack success.

### 2. 🤖 AI-Driven Behavior Learning Module
Integrates genuine Scikit-Learn Machine Learning models to predict and analyze user behavior.
*   **User Susceptibility Prediction:** Identifies high-risk users based on their interactions.
*   **Password Strength Classification:** ML-based evaluation of password robustness.
*   Adaptive engine that learns from simulated campaigns.

### 3. 🎣 Social Engineering Simulation
A structured phishing and messaging simulator.
*   **Email Phishing:** Analyzes text context to identify urgency, spoofing, and manipulative markers.
*   **Chat Phishing (Smishing/Vishing prototypes):** Interactively demonstrates manipulation tactics.
*   Outputs Phishing Risk Scores and specific Threat Indicators.

### 4. 📊 Evaluation & Metrics Dashboard
A centralized dashboard to measure training effectiveness.
*   Tracks Attack Success Rates and User Risk Trends.
*   Monitors Model Accuracy Metrics.
*   Delivers an intelligent Awareness Training Feedback Engine, providing personalized recommendations based on exact simulation failures.

---

## 🏗️ Architecture & Tech Stack

### Frontend
*   **React (TypeScript) + Vite**: Fast, robust UI development.
*   **Tailwind CSS**: Modern, responsive styling with a dark-mode, hacker aesthetic.
*   **Lucide React**: Clean iconography.

### Backend
*   **FastAPI (Python)**: High-performance, asynchronous backend engine.
*   **Scikit-Learn, Pandas, NumPy**: Powers the core AI/ML behavior learning and prediction models.
*   **Passlib, Hashlib, Bcrypt**: Secure cryptographic hashing simulations.
*   **Pydantic**: Strict data validation and sanitization.

---

## 📥 Installation & Setup

### Requirements
*   Node.js (v18+)
*   Python 3.10+

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/Skill-Palaver-Offensive-AI.git
cd Skill-Palaver-Offensive-AI
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run the backend Server
uvicorn app.main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Train AI Models (Optional/If missing)
To retrain the synthetic behavioral ML models:
```bash
python ml_models/train_models.py
```

---

## 🛡️ Educational Disclaimer
This project is designed specifically for **Red-Team Awareness Training**. All simulated attacks (password cracking, phishing) run against internal synthetic data and hashes. It strictly enforces ethical boundaries and cannot be repurposed for malicious external actions.
