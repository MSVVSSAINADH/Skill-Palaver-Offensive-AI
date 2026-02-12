import requests
import json

try:
    response = requests.post("http://localhost:8000/api/social/chat/generate", json={"scenario": "it_support"})
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Script received:")
        print(len(data.get("script", [])))
        # Validate script structure
        script = data.get("script", [])
        for i, step in enumerate(script):
            if "sender" not in step:
                print(f"Error: Step {i} missing sender")
            if step["sender"] == "user_options" and "options" not in step:
                print(f"Error: Step {i} (options) missing options list")
        print("Structure looks valid.")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Connection failed: {e}")
