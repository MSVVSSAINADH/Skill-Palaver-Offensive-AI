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

    def dictionary_attack(self, target_hash: str, algorithm: str, wordlist: list[str], use_rules: bool = False) -> tuple[bool, str, int]:
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


    def ai_guided_attack(self, target_hash: str, algorithm: str, hints: dict) -> tuple[bool, str, int]:
        attempts = 0
        guesses = set()

        # Base words from hints
        base_words = []
        if hints:
            for key, value in hints.items():
                if value:
                    base_words.append(str(value))
                    base_words.append(str(value).lower())
                    base_words.append(str(value).upper())
                    base_words.append(str(value).title())

        # Common patterns to append
        appendages = ["123", "1", "!", "2023", "2024", "2025", "@123", "123!", "321"]
        
        # 1. Try raw hints
        for word in base_words:
            if word not in guesses:
                guesses.add(word)
                attempts += 1
                if self.hash_password(word, algorithm) == target_hash: return True, word, attempts

        # 2. Try hints + appendages
        for word in base_words:
            for suffix in appendages:
                 guess = word + suffix
                 if guess not in guesses:
                     guesses.add(guess)
                     attempts += 1
                     if self.hash_password(guess, algorithm) == target_hash: return True, guess, attempts

        # 2. Try hints + appendages
        for word in base_words:
            for suffix in appendages:
                 guess = word + suffix
                 if guess not in guesses:
                     guesses.add(guess)
                     attempts += 1
                     if self.hash_password(guess, algorithm) == target_hash: return True, guess, attempts

        # 2.5 Try combining hints (e.g. Name + Year)
        import itertools
        for w1, w2 in itertools.permutations(base_words, 2):
            guess = w1 + w2
            if guess not in guesses:
                guesses.add(guess)
                attempts += 1
                if self.hash_password(guess, algorithm) == target_hash: return True, guess, attempts

        # 3. Try Leet speak variations on hints
        leet_map = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
        for word in base_words:
            chars = list(word)
            # Simple full leet
            leet_word = "".join([leet_map.get(c.lower(), c) for c in chars])
            if leet_word not in guesses:
                 guesses.add(leet_word)
                 attempts += 1
                 if self.hash_password(leet_word, algorithm) == target_hash: return True, leet_word, attempts
            
            # Leet + appendages
            for suffix in appendages:
                 guess = leet_word + suffix
                 if guess not in guesses:
                     guesses.add(guess)
                     attempts += 1
                     if self.hash_password(guess, algorithm) == target_hash: return True, guess, attempts

        return False, None, attempts

password_attacker = PasswordAttacker()
