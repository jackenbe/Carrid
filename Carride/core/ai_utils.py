# ai_utils.py
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

def rewrite_post_with_gemini(raw_text):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Rewrite the following as a professional LinkedIn post:\n\n{raw_text}
"""
    response = model.generate_content(prompt)
    return response.text
