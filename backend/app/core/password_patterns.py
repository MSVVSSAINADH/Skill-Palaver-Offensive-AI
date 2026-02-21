import re

class PasswordPatternAnalyzer:
    """
    Advanced pattern analyzer to detect human password habits beyond simple character sets.
    """
    def __init__(self):
        self.keyboard_walks = ["qwerty", "asdfgh", "zxcvbn", "123456", "987654"]
        self.common_substitutions = {
            'a': ['@', '4'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['$', '5'],
            't': ['7']
        }
        
        # A basic heuristic for name-like tokens: looking for common standalone English syllables or generic words
        # In a real enterprise system this would hook into a large name dataset or AD directory lookup.
        self.name_heuristics = ["admin", "root", "user", "test", "demo", "guest", "company"]

    def analyze(self, password: str) -> dict:
        patterns_detected = []
        score_penalty = 0  # Higher score = more predictable
        
        pwd_lower = password.lower()

        # 1. Keyboard Walks
        for walk in self.keyboard_walks:
            if walk in pwd_lower or walk[::-1] in pwd_lower:
                patterns_detected.append("keyboard_walk")
                score_penalty += 30
                break

        # 2. Leet Speak / Substitutions
        sub_count = 0
        normalized_pwd = pwd_lower
        for char, subs in self.common_substitutions.items():
            for sub in subs:
                if sub in password:
                    normalized_pwd = normalized_pwd.replace(sub, char)
                    sub_count += 1
        
        if sub_count > 0:
            patterns_detected.append("common_substitutions")
            # Substitutions are predictable, heavily penalize if there are multiple
            score_penalty += 15

        # 3. Repeating Sequences (e.g., "abcabc" or "1212")
        if re.search(r"(.+?)\1+", pwd_lower):
            # Check if it's more than just a simple double letter (e.g. 'book')
            match = re.search(r"(.{2,})\1+", pwd_lower)
            if match:
                patterns_detected.append("repeating_sequence")
                score_penalty += 20
        
        # Also check single character repeats (e.g. "aaaa")
        if re.search(r"(.)\1{2,}", pwd_lower):
            patterns_detected.append("repeating_character")
            score_penalty += 20

        # 4. Year Patterns (1900-2029)
        if re.search(r"(19[0-9]{2}|20[0-2][0-9])", password):
            patterns_detected.append("year_pattern")
            score_penalty += 25

        # 5. Name-like tokens
        for name in self.name_heuristics:
            if name in normalized_pwd:
                patterns_detected.append("name_like_token")
                score_penalty += 25
                break

        # Predictability score bounded between 0 and 100
        predictability_score = min(100, score_penalty)

        return {
            "patterns_detected": list(set(patterns_detected)),
            "human_predictability_score": predictability_score
        }

pattern_analyzer = PasswordPatternAnalyzer()
