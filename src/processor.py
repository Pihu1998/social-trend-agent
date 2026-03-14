import os
import json
import google.generativeai as genai

class TrendProcessor:
    def __init__(self, brand_guidelines, target_audience, simulation_scenario):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is missing or invalid in .env file.")
        
        genai.configure(api_key=self.api_key)
        # Using gemini-2.5-flash for content generation
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.brand_guidelines = brand_guidelines
        self.target_audience = target_audience
        self.simulation_scenario = simulation_scenario

    def filter_and_analyze(self, videos_data, status_callback=None, feedback_callback=None):
        """
        Takes raw trending video data and asks Gemini to act as a Creative Director.
        Then, a second 'Audience' persona critiques the output. If the score is low,
        the Creative Director is forced to rewrite it.
        """
        if status_callback: status_callback("🧑‍🎨 Agent 1 (Creative Director) is writing the initial draft...")
        
        # --- AGENT 1: THE CREATOR ---
        creative_prompt = f"""
You are an expert Social Media Creative Director.

Here are our Brand Guidelines:
---
{self.brand_guidelines}
---
The target audience we are trying to reach is:
---
{self.target_audience}
---

I am providing you with a list of {len(videos_data)} recently trending videos on TikTok in our niche.
Your job is to:
1. Filter out videos that are just generic dances, irrelevant, or clearly don't fit our brand guidelines.
2. Pick the TOP 1 most relevant and actionable trend to adapt. (Only pick 1 for deep analysis).
3. Provide:
   - The core concept (Break down WHY it worked).
   - A bespoke hook and script for us to recreate it seamlessly in our own voice.
   - The original URL as reference.
4. Output everything in clearly formatted Markdown.

Here is the raw video data (in JSON format):
{json.dumps(videos_data, indent=2)}
"""
        
        try:
            draft_response = self.model.generate_content(creative_prompt)
            current_draft = draft_response.text
            
            # --- THE VALIDATION LOOP ---
            max_iterations = 2
            
            for i in range(max_iterations):
                if status_callback: status_callback(f"👀 Agent 2 (Target Audience) is reviewing Draft #{i+1}...")
                
                # --- AGENT 2: THE CRITIC ---
                critic_prompt = f"""
You are the target audience member defined below:
---
Persona: {self.target_audience}
Current Scenario (What you are doing right now): {self.simulation_scenario}
---

You just scrolled past this TikTok script on your For You Page.
Read it carefully:
---
{current_draft}
---

Evaluate it strictly based on these 3 criteria:
1. The 3-Second Rule: Did the hook make you stop scrolling immediately based on your scenario?
2. Value/Relevance: Does it feel like a boring, skippable ad, or does it genuinely entertain/educate you?
3. Authenticity: Does the tone sound natural to the platform?

Provide a brutal, honest critique explicitly addressing those 3 points. Let us know WHY it works or doesn't work for YOU.
Then, on the VERY LAST LINE, output a final score out of 10 in this exact format:
SCORE: X
"""
                critique_response = self.model.generate_content(critic_prompt)
                critique = critique_response.text
                
                # Extract score from the last line (e.g. "SCORE: 7")
                score_str = critique.strip().split('\n')[-1].replace("SCORE:", "").strip()
                try:
                    score = float(score_str)
                except ValueError:
                    score = 7.0 # Default if it fails to parse
                
                # Report feedback to UI Live
                if feedback_callback: feedback_callback(i+1, score, critique)
                
                if score >= 8.5:
                    if status_callback: status_callback(f"✅ Audience highly approved! (Score: {score}/10)")
                    return f"### Audience Score: {score}/10 🌟\n\n#### Audience Feedback:\n{critique}\n\n---\n\n#### Final Scorer-Approved Script:\n{current_draft}"
                
                if status_callback: status_callback(f"❌ Audience rejected it (Score: {score}/10). Sending back to Creative Director for a rewrite...")
                
                # --- AGENT 1: REWRITE ---
                if i < max_iterations - 1:
                    rewrite_prompt = f"""
You are the Creative Director. Your previous script was ripped apart by the target audience.
Here was your script:
---
{current_draft}
---
Here is their brutal feedback:
---
{critique}
---
Rewrite the script to address all of their feedback perfectly.
Make it punchier, more authentic, and ensure the hook is undeniable.
Output the full revised script in Markdown.
"""
                    current_draft = self.model.generate_content(rewrite_prompt).text
                
            if status_callback: status_callback("⚠️ Reached max rewrites. Proceeding with best attempt.")
            return f"### Audience Validation Failed to reach 8.5/10 (Max Retries Reached) ⚠️\n\n#### Final Audience Feedback:\n{critique}\n\n---\n\n#### Final Script Attempt:\n{current_draft}"
            
        except Exception as e:
            return f"❌ Error during AI processing: {str(e)}"
