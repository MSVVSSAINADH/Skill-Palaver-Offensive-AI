import requests
import hashlib
import time

BASE_URL = "http://localhost:8000/api/password"

def test_dictionary_attack():
    target_pwd = "password"
    target_hash = hashlib.md5(target_pwd.encode()).hexdigest()
    
    payload = {
        "target_hash": target_hash,
        "hash_type": "md5",
        "attack_type": "dictionary",
        "hints": {}
    }
    
    try:
        response = requests.post(f"{BASE_URL}/attack", json=payload)
        response.raise_for_status()
        data = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Response: {data}")
        
        if data["cracked"] and data["password"] == target_pwd:
            print("✅ Dictionary Attack Test PASSED")
        else:
            print("❌ Dictionary Attack Test FAILED")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Waiting for backend to be ready...")
    time.sleep(2)
    test_dictionary_attack()
