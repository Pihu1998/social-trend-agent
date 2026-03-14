import os
import json
import google.generativeai as genai

class TrendProcessor:
    def __init__(self, brand_guidelines):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is missing or invalid in .env file.")
        
        genai.configure(api_key=self.api_key)
        # Using gemini-2.5-flash for content generation
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.brand_guidelines = brand_guidelines

    def filter_and_analyze(self, videos_data):
        """
        Takes raw trending video data and asks Gemini to act as a Creative Director
        to filter the best ones and generate tailored scripts.
        """
        prompt = f"""
You are an expert Social Media Creative Director.

Here are our Brand Guidelines & Persona:
---
{self.brand_guidelines}
---

I am providing you with a list of {len(videos_data)} recently trending videos on TikTok in our niche.
Your job is to:
1. Filter out videos that are just generic dances, irrelevant, or clearly don't fit our brand guidelines.
2. Pick the TOP 3 most relevant and actionable trends for our brand.
3. For each of the top 3 trends, provide:
   - The core concept (Break down WHY it worked).
   - A bespoke hook and script for us to recreate it seamlessly in our own voice.
   - The original URL as reference.
4. Output everything in clearly formatted Markdown.

Here is the raw video data (in JSON format):
{json.dumps(videos_data, indent=2)}
"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error during AI processing: {str(e)}"
