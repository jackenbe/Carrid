"""
AI utilities for generating LinkedIn content using Gemini API
"""
from django.conf import settings
import google.generativeai as genai

# Configure the API with settings
genai.configure(api_key=settings.ADK_API_KEY)

def rewrite_post_with_gemini(raw_text):
    """
    Rewrite raw text as a professional LinkedIn post using Gemini API
    
    Args:
        raw_text (str): The raw text to rewrite
        
    Returns:
        str: The rewritten professional LinkedIn post
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""Rewrite the following as a professional, engaging LinkedIn post. 
Make it compelling, use relevant emojis, and keep it under 3 paragraphs:

{raw_text}"""
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Return the original text if API call fails
        print(f"Error with Gemini API: {e}")
        return raw_text
