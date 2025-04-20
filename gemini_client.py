import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def ask_gemini(prompt: str, temperature: float = 0.7) -> str:
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro-latest",
        generation_config={
            "temperature": temperature,
            "max_output_tokens": 1024
        }
    )
    response = model.generate_content(prompt)
    return response.text
