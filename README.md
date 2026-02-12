# 🛡️ CyberAware - Gamified Cybersecurity Training Platform

**CyberAware** is an advanced, interactive training platform designed to bridge the gap between theoretical cybersecurity knowledge and practical defense. By simulating real-world attacks in a safe, gamified environment, it empowers users to build "muscle memory" against threats like phishing, social engineering, and weak password policies.

---

## 🚀 Problem Statement
**The Human Factor** is the weakest link in cybersecurity.
- **80%+ of breaches** start with human error (phishing, weak passwords).
- Traditional training (videos/quizzes) is **passive** and **forgettable**.
- Users adhere to policies (e.g., "Complex Passwords") without understanding **why** they matter, leading to predictable patterns (e.g., `Password123!`).

**The Solution:**
CyberAware moves from *telling* users about security to *showing* them.
*   "Don't click suspicious links" -> **Simulation:** "Here is a safe email vs. a phishing email. Can you spot the difference?"
*   "Use strong passwords" -> **Simulation:** "Watch this cracking tool break `Password123` in 0.002 seconds."

---

## 🛠️ Module Breakdown & Features

### 1. 🔐 Password Attack Simulator
*Demystifying how hackers break into accounts.*

This module simulates a real password cracking environment (similar to Hashcat or John the Ripper) to demonstrate the mathematical reality of password strength.

#### **Attack Vectors Supported:**
*   **Dictionary Attack:**
    *   Uses a curated list of 10,000+ common passwords.
    *   **Rule-Based Mutations:** Toggles intelligent rules (Append `1`, `!`, `2024`, Leet Speak `a->@`) to show how hackers guess variations.
*   **Mask Attack (New!):**
    *   Simulates targeting specific patterns.
    *   Example: A mask of `?u?l?l?l?d?d` instantly cracks `Pass12` by skipping all other combinations.
    *   **Educational Value:** Teaches that "Length + Complexity" policies are often predictable if the pattern is common.
*   **Brute Force Simulation:**
    *   Calculates the time-to-crack for truly random passwords.
    *   Visualizes the exponential growth of security with every added character.
*   **AI-Guided Guessing (Prototype):**
    *   Uses personal hints (Name, Company, Year) to generate targeted wordlists, simulating a targeted attack.

---

### 2. 🎣 Social Engineering Simulator
*Training resilience against psychological manipulation.*

#### **A. Phishing Email Training**
*   **Training Mode:**
    *   Directly challenges users to classify emails as **"Safe"** or **"Phishing"**.
    *   **Dynamic Content:** Generates infinite variations of emails (HR, IT, Finance contexts).
    *   **Immediate Feedback:** If a user gets it wrong, the system highlights the *exact* indicators (e.g., "Mismatched Sender Domain", "Urgency").
*   **Generator Mode:**
    *   Allows Red Teams/Admins to craft custom scenarios for testing.

#### **B. Chat Phishing (Smishing/Vishing)**
*   Simulates a live chat interface (Teams/Slack/WhatsApp) with an AI bot.
*   **Scenarios:**
    *   **CEO Fraud:** "I'm in a meeting, wire this money ASAP." (Authority/Urgency)
    *   **IT Support:** "We need your 2FA code to fix a virus." (Fear/Helpfulness)
    *   **Prize Scam:** "You won an iPhone! Click to claim." (Greed/Excitement)
*   **Dynamic Scripting:**
    *   Chats are not static text; they are generated dynamically with randomized IPs, names, and contexts to keep training fresh.

---

### 3. 📊 Risk Analytics & Reporting
*   **User Risk Score:**
    *   Calculates a "Cyber Hygiene" score (0-100) based on simulation performance.
    *   High Phishing Click Rate + Weak Password Usage = **High Risk**.
*   **Actionable Insights:**
    *   "User falls for Urgency tactics."
    *   "User relies on Pattern-based passwords."

---

## 💻 Tech Stack

### **Frontend**
*   **React (TypeScript):** For a robust, type-safe UI as complex as a desktop tool.
*   **Tailwind CSS:** For modern, "Dark Mode" hacker aesthetic styling.
*   **Lucide React:** Iconography for intuitive navigation.
*   **Axios:** efficient API communication.

### **Backend**
*   **FastAPI (Python):** High-performance, async API handling.
*   **Python Security Libraries:**
    *   `hashlib`, `bcrypt`: For real cryptographic operations.
    *   `itertools`: For generating attack combinations.
*   **Architecture:**
    *   RESTful API design.
    *   Modular `core/attacks.py` and `core/social_eng.py` logic for easy extensibility.

---

## 📥 Installation & Setup

1.  **Backend:**
    ```bash
    cd backend
    pip install -r requirements.txt
    python -m app.main
    ```

2.  **Frontend:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

3.  **Access:**
    *   Frontend: `http://localhost:5173`
    *   API Docs: `http://localhost:8000/docs`

---

## 🔮 Future Roadmap
*   **AI-Bot Integration:** Replace static chat scripts with a real LLM (Local/API) for dynamic conversations.
*   **Network Sniffer Module:** Visualize how unencrypted data travels (HTTP vs HTTPS).
*   **Leaderboard:** Gamify widely across an organization to encourage competitive security practices.
