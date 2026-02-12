from backend.app.core.social_eng import social_engineer

print("Loaded social_engineer")
try:
    print(f"Templates keys: {list(social_engineer.templates.keys())}")
    print(f"Has chat_scripts? {hasattr(social_engineer, 'chat_scripts')}")
    if hasattr(social_engineer, 'chat_scripts'):
        print(f"Chat scripts keys: {list(social_engineer.chat_scripts.keys())}")
    
    # Test generation
    script = social_engineer.generate_chat_script("it_support")
    print("Script generated successfully")
    print(script.keys())
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
