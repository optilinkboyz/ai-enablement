"""
Lists all Gemini models available for your API key.
Run this to find the correct model name.
"""
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("\n=== Available Gemini Models for your API key ===\n")
for model in client.models.list():
    if "generateContent" in model.supported_actions:
        print(f"✅ {model.name}")

print("\n=== Copy one of the ✅ names above (without 'models/') ===")
