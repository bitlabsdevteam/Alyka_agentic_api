# test_api_keys.py

import os
from dotenv import load_dotenv
import openai
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")

print("Testing API Keys...\n")

# Test OpenAI API key
print("Testing OpenAI API key...")
try:
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}],
        max_tokens=10
    )
    print(f"OpenAI API Response: {response.choices[0].message.content}")
    print("OpenAI API key is working!\n")
except Exception as e:
    print(f"Error with OpenAI API key: {str(e)}\n")

# Test Google Gemini API key
print("Testing Google Gemini API key...")
try:
    genai.configure(api_key=gemini_api_key)
    
    # List available models
    print("Available Gemini models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
    
    # Try with gemini-1.5-pro-latest instead
    model = GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content("Say hello")
    print(f"Gemini API Response: {response.text}")
    print("Google Gemini API key is working!\n")
except Exception as e:
    print(f"Error with Google Gemini API key: {str(e)}\n")

print("API key testing completed.")