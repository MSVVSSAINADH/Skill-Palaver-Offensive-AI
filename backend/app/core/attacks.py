import time
import hashlib
import bcrypt
import itertools
import string

class PasswordAttacker:
    def __init__(self):
        pass

    def hash_password(self, password: str, algorithm: str) -> str:
        if algorithm == "md5":
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()
        elif algorithm == "bcrypt":
            # bcrypt needs bytes
            pwd_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
        else:
            raise ValueError("Unsupported algorithm")

    def dictionary_attack(self, target_hash: str, algorithm: str, wordlist: list[str], use_rules: bool = False, mutation_intensity: str = "low") -> tuple[bool, str, int]:
        attempts = 0
        rules = []
        if use_rules:
            # mimic basic "best64" style rules
            rules = [
                lambda w: w,                             # No change
                lambda w: w.capitalize(),                # Capitalize
                lambda w: w.upper(),                     # Uppercase
                lambda w: w + "1",                       # Append 1
                lambda w: w + "123",                     # Append 123
                lambda w: w + "!",                       # Append !
                lambda w: w + "2023",                    # Append Year
                lambda w: w + "2024",                    # Append Year
                lambda w: w + "2025",                    # Append Year
                lambda w: w.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$') # Leet
            ]
            if mutation_intensity == "high":
                rules.extend([
                    lambda w: w + "1234",
                    lambda w: w + "!!!",
                    lambda w: w + "999",
                    lambda w: w.replace('a', '@').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '$').upper()
                ])
        else:
            rules = [lambda w: w]

        for word in wordlist:
            for rule in rules:
                try:
                    candidate = rule(word)
                except:
                    continue
                
                attempts += 1
                if self.hash_password(candidate, algorithm) == target_hash:
                    # Double check for bcrypt
                    if algorithm == "bcrypt":
                         if bcrypt.checkpw(candidate.encode(), target_hash.encode()):
                             return True, candidate, attempts
                    else:
                        return True, candidate, attempts
        
        return False, None, attempts

    def mask_attack(self, target_hash: str, algorithm: str, mask: str, timeout: int = 10) -> tuple[bool, str, int]:
        """
        Implements Hashcat-style mask attack.
        Masks:
        ?l = abcdefghijklmnopqrstuvwxyz
        ?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
        ?d = 0123456789
        ?s = !@#$%^&*
        ?a = ?l?u?d?s
        Example: ?u?l?l?l?d?d = Pass12
        """
        attempts = 0
        charsets = []
        
        i = 0
        while i < len(mask):
            if mask[i] == '?':
                if i + 1 < len(mask):
                    code = mask[i+1]
                    if code == 'l': charsets.append(string.ascii_lowercase)
                    elif code == 'u': charsets.append(string.ascii_uppercase)
                    elif code == 'd': charsets.append(string.digits)
                    elif code == 's': charsets.append("!@#$%^&*")
                    elif code == 'a': charsets.append(string.ascii_letters + string.digits + "!@#$%^&*")
                    else: charsets.append(code) # Literal if unknown
                    i += 2
                else:
                    break
            else:
                charsets.append(mask[i]) # Literal char
                i += 1
        
        start_time = time.time()
        # Product of all charsets
        for guess_tuple in itertools.product(*charsets):
            if attempts % 10000 == 0:
                if time.time() - start_time > timeout:
                    return False, "TIMEOUT", attempts

            guess = "".join(guess_tuple)
            attempts += 1
            
            if algorithm == "bcrypt":
                    if bcrypt.checkpw(guess.encode(), target_hash.encode()):
                        return True, guess, attempts
            else:
                # Optimized inline check
                if algorithm == "md5":
                    if hashlib.md5(guess.encode()).hexdigest() == target_hash: return True, guess, attempts
                elif algorithm == "sha256":
                    if hashlib.sha256(guess.encode()).hexdigest() == target_hash: return True, guess, attempts
                else: 
                     # Fallback
                     if self.hash_password(guess, algorithm) == target_hash: return True, guess, attempts
                    
        return False, None, attempts

    def brute_force_attack(self, target_hash: str, algorithm: str, max_length: int = 4, charset: str = string.ascii_letters + string.digits, timeout: int = 10) -> tuple[bool, str, int]:
        attempts = 0
        start_time = time.time()
        
        for length in range(1, max_length + 1):
            for guess_tuple in itertools.product(charset, repeat=length):
                if attempts % 10000 == 0:
                    if time.time() - start_time > timeout:
                        return False, "TIMEOUT", attempts
                        
                guess = "".join(guess_tuple)
                attempts += 1
                
                if algorithm == "bcrypt":
                     if bcrypt.checkpw(guess.encode(), target_hash.encode()):
                         return True, guess, attempts
                else:
                    # Optimized inline check
                    if algorithm == "md5":
                        if hashlib.md5(guess.encode()).hexdigest() == target_hash: return True, guess, attempts
                    elif algorithm == "sha256":
                        if hashlib.sha256(guess.encode()).hexdigest() == target_hash: return True, guess, attempts
                    else:
                        if self.hash_password(guess, algorithm) == target_hash: return True, guess, attempts
                        
        return False, None, attempts


    def ai_guided_attack(self, target_hash: str, algorithm: str, hints: dict, mutation_intensity: str = "low") -> tuple[bool, str, int]:
        attempts = 0
        guesses = set()

        if not hints:
            return False, None, attempts

        # Base words from hints
        raw_words = set()
        for key, value in hints.items():
            if value:
                val_str = str(value)
                raw_words.add(val_str)
                # If there are spaces, try splitting into individual words
                if ' ' in val_str:
                    for w in val_str.split():
                        raw_words.add(w)

        base_words = set()
        for w in raw_words:
            base_words.add(w)
            base_words.add(w.lower())
            base_words.add(w.upper())
            base_words.add(w.capitalize())
            base_words.add(w.title())

            # Add reverse strings for flavor 
            if len(w) > 3:
                base_words.add(w[::-1])
                base_words.add(w[::-1].lower())
                base_words.add(w[::-1].capitalize())

        # Common patterns to append/prepend
        appendages = ["123", "1", "!", "2023", "2024", "2025", "@123", "123!", "321", "01", "12", "69", "99", "?", ".", "$", "!!", "0", "007", "11", "22", "88", "999", "admin", "password", "qwe"]
        
        # Expand years dynamically (Huge expansion 1900-2030)
        years = [str(y) for y in range(1930, 2030)]
        appendages.extend(years)
        
        # Add year + punctuation combos
        for y in range(1980, 2025):
             appendages.append(f"{y}!")
             appendages.append(f"@{y}")
             appendages.append(f"!{y}")

        if mutation_intensity == "high":
            appendages.extend(["1234", "12345", "!!!", "111", "999", "0000", "123456", "??", "10", "11", "00", "123123", "000", "abc", "xyz"])
            # Expand month combinations
            for m in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
                for d in ["01", "15", "30", "31", "12", "07"]:
                    appendages.append(f"{m}{d}")
                    appendages.append(f"{d}{m}")
            
            # Massive loop of pure numbers if high intensity
            for i in range(100, 999):
                 appendages.append(str(i))
            
        import itertools

        def check_add(guess):
            nonlocal attempts
            if guess not in guesses:
                guesses.add(guess)
                attempts += 1
                if algorithm == "bcrypt":
                    if bcrypt.checkpw(guess.encode(), target_hash.encode()): return True
                else:
                    if algorithm == "md5":
                        if hashlib.md5(guess.encode()).hexdigest() == target_hash: return True
                    elif algorithm == "sha256":
                        if hashlib.sha256(guess.encode()).hexdigest() == target_hash: return True
                    else:
                        if self.hash_password(guess, algorithm) == target_hash: return True
            return False

        # 1. Try raw hints and casing
        for word in list(base_words):
            if check_add(word): return True, word, attempts

        # 2. Try hints + appendages (Suffix and Prefix)
        for word in list(base_words):
            for suffix in appendages:
                if check_add(word + suffix): return True, word + suffix, attempts
                if mutation_intensity == "high":
                    # Prepend suffixes and separate with underscores
                    if check_add(suffix + word): return True, suffix + word, attempts
                    if check_add(word + "_" + suffix): return True, word + "_" + suffix, attempts
                    if check_add(word + "-" + suffix): return True, word + "-" + suffix, attempts

        # 3. Try combining hints (e.g. Name + Year or Pet + City)
        hint_list = list(raw_words)
        combinators = ["", "-", "_", "."] if mutation_intensity == "high" else [""]
        for w1, w2 in itertools.permutations(hint_list, 2):
            for comb in combinators:
                guess1 = w1.lower() + comb + w2.lower()
                guess2 = w1.capitalize() + comb + w2.lower()
                guess3 = w1.capitalize() + comb + w2.capitalize()
                
                if check_add(guess1): return True, guess1, attempts
                if check_add(guess2): return True, guess2, attempts
                if check_add(guess3): return True, guess3, attempts
                
                # Combine combinations + basic subset of appendages
                subset_appendages = ["1", "!", "123", "2024", "2025"]
                for suffix in subset_appendages:
                    if check_add(guess1 + suffix): return True, guess1 + suffix, attempts
                    if check_add(guess3 + suffix): return True, guess3 + suffix, attempts

        # 4. Try Leet speak variations on hints
        leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$', 'l': '1', 't': '7'}
        leet_map_complex = {'a': '4', 'e': '3', 'i': '!', 'o': '0', 's': '5', 't': '+', 'b': '8', 'g': '9'}

        for word in list(raw_words):
            variants = [word.lower(), word.capitalize()]
            if mutation_intensity == "high":
                variants.append(word.upper())
                
            for var in variants:
                chars = list(var)
                # Full leet substitution (Standard)
                leet_word_std = "".join([leet_map.get(c.lower(), c) for c in chars])
                if check_add(leet_word_std): return True, leet_word_std, attempts
                
                # Full leet substitution (Complex)
                if mutation_intensity == "high":
                    leet_word_cx = "".join([leet_map_complex.get(c.lower(), c) for c in chars])
                    if check_add(leet_word_cx): return True, leet_word_cx, attempts

                # Leet + Appendages
                for suffix in appendages:
                    if check_add(leet_word_std + suffix): return True, leet_word_std + suffix, attempts
                    if mutation_intensity == "high":
                        if check_add(suffix + leet_word_std): return True, suffix + leet_word_std, attempts
                        if check_add(leet_word_cx + suffix): return True, leet_word_cx + suffix, attempts

        # 5. Vowel stripping (Deep AI Guessing Heuristic)
        if mutation_intensity == "high":
            vowels = "aeiouAEIOU"
            for word in list(raw_words):
                stripped = "".join([c for c in word if c not in vowels])
                if stripped and len(stripped) >= 3:
                     variants = [stripped.lower(), stripped.capitalize()]
                     for var in variants:
                         if check_add(var): return True, var, attempts
                         for suffix in appendages:
                             if check_add(var + suffix): return True, var + suffix, attempts

        return False, None, attempts

password_attacker = PasswordAttacker()
