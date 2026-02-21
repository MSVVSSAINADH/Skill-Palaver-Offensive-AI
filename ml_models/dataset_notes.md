# Skill-Palaver-Offensive-AI Dataset Transparency Notes

## Overview
This platform uses synthetic datasets to train its offline Machine Learning models (`RandomForest`, `LogisticRegression`, `GradientBoosting`, etc.). This document outlines the rationale, generation logic, class balances, and features for each model.

## 1. Password Strength Model
- **File**: `ml_models/password_model.pkl`
- **Features**: Password Length, Number of Digits, Number of Uppercase Letters, Number of Special Characters.
- **Target**: `strength` (0 = Weak, 1 = Medium, 2 = Strong)
- **Class Balance**: Evenly distributed (500 samples each) across the 3 classes.
- **Generation Logic**: 
  - Weak: Short strings of strictly lowercase letters or digits.
  - Medium: Alphanumeric strings of moderate length.
  - Strong: Long strings incorporating punctuation, mixed cases, and digits.

## 2. Risk Classification Model
- **File**: `ml_models/risk_model.pkl`
- **Features**: `phishing_clicks`, `weak_passwords_count`, `simulations_run`
- **Target**: `risk_score` (0 = Low Risk, 1 = High Risk)
- **Class Balance**: Determined dynamically via mathematical logic during generation.
- **Generation Logic**: High Risk is automatically assigned if the user's click rate ratio `(clicks / simulations) >= 0.3` or if they have logged `weak_passwords >= 2`.

## 3. Phishing Susceptibility Model
- **File**: `ml_models/phishing_susceptibility_model.pkl`
- **Features**: `past_click_rate`, `training_completion_rate`, `urgency_response_time` (minutes), `weak_password_count`, `security_score`
- **Target**: `clicked` (0 = Safe, 1 = Susceptible to Phishing)
- **Class Balance**: Dependent on weighted random heuristics.
- **Generation Logic**: Susceptibility probability is heavily weighted towards high past click rates (40% weight), low training completion (30%), and fast urgency response times (impulsive clicks, 20%). A threshold of `0.5` translates probability into a binary label.

## 4. Crack Time Predictor (ML Factor)
- **File**: `ml_models/crack_time_model.pkl`
- **Features**: `password_length`, `charset_size`, `entropy_estimate`, `pattern_score`
- **Target**: `adjustment_factor` (Continuous multiplier value, e.g., 0.1 to 1.0)
- **Generation Logic**: Generates an ML adjustment factor multiplier used in the Hybrid Crack Time Estimation engine. High human predictability patterns (high pattern scores) linearly reduce the adjustment factor (e.g., 0.1 drops estimated math crack time by 10x).

## Limitations and Assumptions
- Because the datasets are strictly synthetic, model decisions represent logical generalizations rather than real-world corporate data anomalies.
- NLP Models (TF-IDF) do not process a predefined synthetic dataset but rely on predefined logic mapping intent keywords to labels.
