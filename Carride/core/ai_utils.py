"""
AI utilities for generating LinkedIn content using Google Gemini API.

This module uses the Gemini API to rewrite user posts into professional,
engaging LinkedIn content while maintaining the user's authentic voice.
"""
import os
from django.conf import settings
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


# Define the response structure for LinkedIn posts
class LinkedInPostResponse(BaseModel):
    enhanced_post: str = Field(description="The professionally enhanced LinkedIn post (2-3 paragraphs with 2-3 relevant emojis).")
    key_improvements: list[str] = Field(description="A list of specific improvements made to the post for professionalism and engagement.")
    engagement_hooks: list[str] = Field(description="A list of engagement elements included (questions, calls-to-action, emotional appeal, etc.).")
    tone_quality: int = Field(description="The professionalism score of the enhanced post as an integer from 1 to 10.")
    engagement_potential: int = Field(description="Predicted LinkedIn engagement potential of this post (1-10 scale).")


# Create the agent chain as a reusable component
def create_linkedin_post_agent():
    """
    Create a reusable Gemini agent for enhancing LinkedIn posts with structured output.
    Uses LangChain with Pydantic models for consistent, high-quality responses.
    """
    os.environ['GOOGLE_API_KEY'] = settings.ADK_API_KEY
    print(f"DEBUG: GOOGLE_API_KEY is set: {bool(os.environ.get('GOOGLE_API_KEY'))}")
    
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    parser = PydanticOutputParser(pydantic_object=LinkedInPostResponse)

    prompt_template = """
    You are an elite LinkedIn content strategist. Your priority is transforming raw user text into professional, engaging LinkedIn posts.
    Break down the enhancement into clear improvements and provide specific engagement hooks.
    Your tone must be professional and polished, but authentic to the user's original voice.
    You will analyze the user's text and provide comprehensive enhancements.
    The user is a visual learner so include emojis strategically and use bullet points in your lists.

    Your response must strictly follow this JSON format:
    {format_instructions}

    User's Original Text:
    ```
    {user_text}
    ```

    User's Context/Background:
    {user_context}

    Now transform this into a professional, engaging LinkedIn post:
    """

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["user_text", "user_context"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    
    # Return the chain: prompt → model → parser
    return prompt | model | parser


def rewrite_post_with_gemini(raw_text: str, user_context: str = "") -> str:
    """
    Rewrite raw text as a professional LinkedIn post using Gemini agent with structured output.
    
    Args:
        raw_text (str): The user's original text about their experience
        user_context (str): Optional context about the user (background, goals, etc.)
        
    Returns:
        str: The professionally enhanced LinkedIn post
    """
    try:
        # Create and invoke the agent
        agent = create_linkedin_post_agent()
        response = agent.invoke({
            "user_text": raw_text,
            "user_context": user_context or "No additional context provided."
        })
        
        # Extract the enhanced post from the structured response
        enhanced_post = response.enhanced_post.strip()
        
        print(f"[LinkedIn Post Agent]")
        print(f"Original text: {raw_text}")
        print(f"Enhanced post: {enhanced_post}")
        print(f"Key improvements: {response.key_improvements}")
        print(f"Engagement hooks: {response.engagement_hooks}")
        print(f"Tone quality: {response.tone_quality}/10")
        print(f"Engagement potential: {response.engagement_potential}/10")
        
        return enhanced_post

    except Exception as e:
        print(f"[Gemini Agent Error] {e}")
        print("Falling back to original text.")
        import traceback
        traceback.print_exc()
        return raw_text
