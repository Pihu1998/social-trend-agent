import asyncio
import os
import json
from dotenv import load_dotenv

# Import the scraper and processor we built
from main import TikTokScraper
from processor import TrendProcessor

load_dotenv()

async def run_hackathon_demo():
    print("\n" + "="*70)
    print("🚀 STARTING: HACKATHON DEMO - AI SOCIAL TREND AGENT")
    print("="*70 + "\n")
    
    # ---------------------------------------------------------
    # STEP 1: DEFINE THE BRAND PERSONA (The "Smart Filter" Logic)
    # ---------------------------------------------------------
    # This is where the magic happens. Instead of hard-coding rules,
    # we give the AI a persona. It will judge the scraped videos
    # against these instructions.
    
    demo_brand_persona = """
    BRAND NAME: "EcoFit" 
    INDUSTRY: Sustainable Athletic Wear
    TARGET AUDIENCE: Millennials and Gen-Z who care about the environment but want stylish gym clothes.
    
    CONTENT PREFERENCES:
    - We LOVE 'Day in the life' (POV) videos.
    - We LOVE 'Educational' videos about sustainability or workout tips.
    - We DO NOT want generic dance trends unless they relate to working out.
    - TONE: Energetic, inspiring, and eco-conscious.
    
    GOAL: Pick the top 3 trends from the list provided that EcoFit can seamlessly adapt.
    """
    
    print("📋 [STEP 1] Loaded Brand Persona for 'EcoFit' (Sustainable Activewear)")
    print("   Looking for: POV, Educational, Eco-conscious. Rejecting: Generic dances.\n")
    
    # ---------------------------------------------------------
    # STEP 2: SCRAPE RAW TRENDS (The Niche Discovery)
    # ---------------------------------------------------------
    # We scrape TikTok for a specific hashtag relevant to our niche.
    
    niche_hashtag = "gymtok"
    print(f"🕵️‍♂️ [STEP 2] Scraping TikTok for raw trends in: #{niche_hashtag}")
    
    scraper = TikTokScraper()
    try:
        # We grab 10 videos as a sample size for the demo
        videos = await scraper.fetch_trending_by_hashtag(niche_hashtag, count=10)
        print(f"   ✅ Successfully pulled data for {len(videos)} top videos.")
        
        # Show a quick snippet of the raw data before AI filtering
        print("\n   [Sample of Raw Data Collected]:")
        for v in videos[:2]:
            print(f"   - Desc: {v['desc'][:60]}... | Views: {v['stats'].get('playCount', 0)}")
        print("   ...\n")
        
    except Exception as e:
        print(f"❌ Scraping Error: {str(e)}")
        print("💡 Ensure TIKTOK_MS_TOKEN is valid in .env")
        return

    # ---------------------------------------------------------
    # STEP 3: AI SMART FILTERING & IDEATION (The "Brain")
    # ---------------------------------------------------------
    # We pass the raw JSON data and the Brand Persona to Gemini.
    
    print(f"🧠 [STEP 3] Passing {len(videos)} raw videos to Gemini AI (gemini-2.5-flash)...")
    print("   Evaluating against EcoFit's Brand Persona and generating scripts...\n")
    
    try:
        processor = TrendProcessor(brand_guidelines=demo_brand_persona)
        analysis_result = processor.filter_and_analyze(videos)
        
        print("🎉 [RESULT] AI FILTERED TRENDS & BESPOKE CONTENT PLANS")
        print("="*70)
        print(analysis_result)
        
    except Exception as e:
        print(f"❌ AI Processing Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_hackathon_demo())
