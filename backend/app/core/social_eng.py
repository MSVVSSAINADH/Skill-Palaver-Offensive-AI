import random

class SocialEngineer:
    def __init__(self):
        self.templates = {
            "hr": {
                "urgent": [
                    "Subject: URGENT: Employee Benefits Enrolment\n\nDear Employee,\n\nYour benefits enrolment period is ending in 2 hours. Please log in immediately to confirm your selection or risk losing coverage.\n\n[Link: http://benefits-secure-portal.net/login]",
                    "Subject: FINAL NOTICE: Payroll Mismatch\n\nWe detected a discrepancy in your last paycheck. Verify your bank details within 24 hours to ensure timely payment.\n\n[Link: http://hr-portal-verification.com]"
                ],
                "friendly": [
                    "Subject: Team Lunch Invitation!\n\nHi everyone,\n\nWe are organizing a team lunch next Friday. Please fill out your dietary preferences in the attached form.\n\n[Link: http://surveymonkey-fake.com/lunch]",
                    "Subject: Wellness Program Rewards\n\nYou have earned 500 points in our wellness program! Redeem them here.\n\n[Link: http://wellness-rewards-claim.com]",
                    "Subject: New Employee Welcome Drinks\n\nJoin us in welcoming Sarah to the team! Click here to RSVP for drinks this Friday.\n\n[Link: http://rsvp-events-external.com]"
                ],
                "authority": [
                    "Subject: CEO Announcement: Policy Update\n\nPlease review the attached mandatory policy update regarding remote work immediately.\n\n[Link: http://company-policy-secure.doc-view.com]",
                    "Subject: MANDATORY: Sexual Harassment Training\n\nAll employees must complete the annual training by EOD tomorrow. Login to start.\n\n[Link: http://training-compliance-hr.com]"
                ]
            },
            "finance": {
                "urgent": [
                     "Subject: Invoice Overdue #9823\n\nOur records show invoice #9823 is unpaid. Please remit payment immediately to avoid service interruption.\n\n[Link: http://quickbooks-invoice-view.com]",
                     "Subject: Corporate Card Suspension\n\nYour corporate credit card has been suspended due to suspicious activity. Verify recent charges now.\n\n[Link: http://card-security-check.com]"
                ],
                "friendly": "Subject: Budget Surplus Allocation\n\nGood news! Your department has a budget surplus for Q4. Click here to request equipment upgrades before Friday.\n\n[Link: http://procurement-internal-rewards.com]",
                "authority": "Subject: Tax Compliance Audit\n\nThe IRS requires you to update your tax form W-9. Download the secure tool to comply.\n\n[Link: http://irs-forms-secure-download.com]"
            },
            "it": {
                "urgent": [
                    "Subject: Password Expiry Notification\n\nYour password will expire in 24 hours. Click here to keep your current password.\n\n[Link: http://reset-password-okta-fake.com]",
                    "Subject: VPN Security Upgrade\n\nYou must install the new security certificate to access the VPN tomorrow. Download it here.\n\n[Link: http://vpn-cert-install.net]"
                ],
                "friendly": "Subject: New Laptop Upgrades Available\n\nYou are eligible for a laptop refresh! Select your new MacBook Pro or Dell XPS model here.\n\n[Link: http://it-assets-request-portal.com]",
                "authority": "Subject: Microsoft 365: Storage Limit Reached\n\nYour email storage is full. You will not receive new emails until you archive old data.\n\n[Link: http://office365-storage-limit.com]"
            }
        }
        
        self.safe_templates = {
            "hr": [
                {"subject": "Subject: Monthly Newsletter", "body": "Hi Team,\n\nHere is this month's newsletter. calculated points are available on the intranet.\n\nRegards,\nHR Team", "safe": True},
                {"subject": "Subject: Holiday Calendar", "body": "Dear All,\n\nPlease find the attached holiday calendar for next year. No action required.\n\nBest,\nHR", "safe": True},
                {"subject": "Subject: Lost Foundation Item", "body": "A pair of glasses was found in Meeting Room B. Please visit reception to claim them.\n\nReception", "safe": True},
                {"subject": "Subject: Open Enrollment FAQ", "body": "Hi everyone,\n\nAttached is the FAQ document for the upcoming benefits enrollment. Let us know if you have questions.\n\nHR", "safe": True}
            ],
            "finance": [
                {"subject": "Subject: Expense Report Approved", "body": "Your expense report #1023 has been approved and moved to payment.\n\nSent from Finance Portal", "safe": True},
                {"subject": "Subject: Q3 Financial Results", "body": "Team,\n\nThe recording of the Q3 All-Hands meeting is now available on the internal wiki.\n\nCFO", "safe": True}
            ],
            "it": [
                {"subject": "Subject: Scheduled Maintenance", "body": "Network maintenance is scheduled for Sunday 2 AM. Services may be intermittent.\n\nIT Support", "safe": True},
                {"subject": "Subject: Ticket #4928 Closed", "body": "Your support ticket regarding 'Monitor flickering' has been closed. Please rate your experience.\n\nIT Service Desk", "safe": True},
                {"subject": "Subject: New Printer Installed", "body": "A new color printer has been installed on the 4th floor near the breakroom.\n\nIT Facilities", "safe": True}
            ]
        }
        
        # Chat scripts are now dynamically generated in generate_chat_script
        self.chat_scripts = {}

    def generate_simulation_email(self) -> dict:
        """Generates either a phishing or safe email for training."""
        is_phishing = random.choice([True, False])
        
        if is_phishing:
            # Pick a phishing template
            persona = random.choice(list(self.templates.keys()))
            tone = random.choice(list(self.templates[persona].keys()))
            
            # existing generation logic reuse or simplified
            options = self.templates[persona][tone]
            if isinstance(options, list):
                content = random.choice(options)
            else:
                content = options
                
            return {
                "id": random.randint(1000, 9999),
                "type": "phishing",
                "persona": persona,
                "tone": tone,
                "content": content,
                "reason": "This is a PHISHING email. Indicators include urgency, suspicious links, or external domains."
            }
        else:
            # Pick a safe template
            category = random.choice(list(self.safe_templates.keys()))
            template = random.choice(self.safe_templates[category])
            
            return {
                "id": random.randint(1000, 9999),
                "type": "safe",
                "persona": category,
                "content": f"{template['subject']}\n\n{template['body']}",
                "reason": "This is a SAFE email. It has no urgency, verified internal context, and no suspicious links."
            }

    def _get_it_support_script(self):
        country = random.choice(["Russia", "China", "Brazil", "Unknown Location"])
        ip = f"{random.randint(10,200)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
        return [
            {"sender": "bot", "text": "Hi {name}, this is IT Support. We detected an unusual login attempt on your account.", "delay": 1000},
            {"sender": "bot", "text": f"Was this you? (Login from: {country}, IP: {ip})", "delay": 2000},
            {"sender": "user_options", "options": [
                {"label": "No, it wasn't me!", "risk": "safe", "next": "panic_mode"},
                {"label": "Ignore", "risk": "safe", "next": "end_safe"}
            ]},
            {"id": "panic_mode", "sender": "bot", "text": "Okay, we need to secure your account immediately. I've sent a 6-digit code to your phone.", "delay": 1500},
            {"sender": "bot", "text": "Please reply with the code so I can block the intruder.", "delay": 2500},
            {"sender": "user_options", "options": [
                {"label": "Sure, it is 123456", "risk": "high", "next": "phished"},
                {"label": "I'll call IT desk directly to verify.", "risk": "safe", "next": "safe_check"}
            ]},
            {"id": "phished", "sender": "bot", "text": "Thanks. Verifying... (Attacker now has your session)", "delay": 1000, "end": True, "success": True},
            {"id": "safe_check", "sender": "bot", "text": "Okay, please do. (Attack Failed)", "delay": 1000, "end": True, "success": False},
            {"id": "end_safe", "sender": "bot", "text": "(No response... Attack timed out)", "delay": 1000, "end": True, "success": False}
        ]

    def _get_prize_script(self):
        prize = random.choice(["iPhone 16 Pro", "$5000 Cash Bonus", "Trip to Hawaii", "Tesla Model 3"])
        return [
             {"sender": "bot", "text": f"CONGRATS! You've won a {prize} in the company raffle!", "delay": 1000},
             {"sender": "bot", "text": "Click here to claim: http://bit.ly/claim-prize now!", "delay": 2000},
             {"sender": "user_options", "options": [
                {"label": "Click the link!", "risk": "high", "next": "phished_prize"},
                {"label": "Check company intranet first", "risk": "safe", "next": "safe_prize"}
             ]},
             {"id": "phished_prize", "sender": "bot", "text": "Redirecting to malware site...", "delay": 500, "end": True, "success": True},
             {"id": "safe_prize", "sender": "bot", "text": "Wise choice. There is no raffle.", "delay": 500, "end": True, "success": False}
        ]

    def _get_ceo_fraud_script(self):
        task = random.choice(["purchase 5x $100 Gift Cards", "process a wire transfer", "share the client list"])
        return [
             {"sender": "bot", "text": "Hi, are you available? I'm in a meeting and can't talk.", "delay": 1000},
             {"sender": "user_options", "options": [
                {"label": "Yes, I'm here. What do you need?", "risk": "safe", "next": "task_req"},
                {"label": "Ignore", "risk": "safe", "next": "end_ignore"}
             ]},
             {"id": "task_req", "sender": "bot", "text": f"I need you to {task} for a client immediately. I will reimburse you.", "delay": 2000},
             {"sender": "bot", "text": "Can you handle this right now? It's urgent.", "delay": 2000},
             {"sender": "user_options", "options": [
                {"label": "Sure, I'll do it right away.", "risk": "high", "next": "phished_ceo"},
                {"label": "I need to verify this with Finance/HR first.", "risk": "safe", "next": "safe_ceo"}
             ]},
             {"id": "phished_ceo", "sender": "bot", "text": "Great, send me the details once done. (You fell for CEO Fraud)", "delay": 1000, "end": True, "success": True},
             {"id": "safe_ceo", "sender": "bot", "text": "Nevermind, I'll get someone else.", "delay": 1000, "end": True, "success": False},
             {"id": "end_ignore", "sender": "bot", "text": "(No response...)", "delay": 1000, "end": True, "success": False}
        ]

    def generate_email(self, persona: str, tone: str) -> dict:
        persona = persona.lower()
        tone = tone.lower()
        
        if persona not in self.templates:
            return {"error": "Persona not found"}
        
        # Simple fallback if tone key missing for persona (e.g. finance only has 2)
        options = self.templates[persona].get(tone)
        if not options:
             # Fallback to random tone
             tone = random.choice(list(self.templates[persona].keys()))
             options = self.templates[persona][tone]

        if isinstance(options, list):
            content = random.choice(options)
        else:
            content = options
            
        return {
            "content": content,
            "persona": persona,
            "tone": tone
        }

    def analyze_email(self, content: str) -> dict:
        indicators = []
        score = 0
        
        # Simple keywords detection
        urgent_keywords = ["urgent", "fail", "suspend", "immediate", "24 hours", "risk"]
        link_indicators = ["http://", "bit.ly", "tinyurl", "secure-portal"]
        grammar_issues = ["kindly", "dear valued", "verify account"]

        content_lower = content.lower()

        for word in urgent_keywords:
            if word in content_lower:
                indicators.append(f"Urgency trigger: '{word}'")
                score += 20
        
        for word in link_indicators:
            if word in content_lower:
                indicators.append(f"Suspicious link pattern: '{word}'")
                score += 30

        if score > 80:
            rating = "High Risk"
        elif score > 40:
            rating = "Medium Risk"
        else:
            rating = "Low Risk"

        return {
            "score": min(score, 100),
            "indicators": indicators,
            "rating": rating
        }

    def generate_chat_script(self, scenario: str) -> dict:
        scenario = scenario.lower()
        
        script = []
        if scenario == "it_support":
            script = self._get_it_support_script()
        elif scenario == "prize":
            script = self._get_prize_script()
        elif scenario == "ceo_fraud":
            script = self._get_ceo_fraud_script()
        else:
            # Default
            script = self._get_it_support_script()
            scenario = "it_support"
            
        return {
            "scenario": scenario,
            "script": script
        }

social_engineer = SocialEngineer()
