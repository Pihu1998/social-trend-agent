import asyncio
import os
from TikTokApi import TikTokApi
from dotenv import load_dotenv
import json
from processor import TrendProcessor

load_dotenv()

class TikTokScraper:
    def __init__(self):
        self.ms_token = os.getenv("TIKTOK_MS_TOKEN")

    async def fetch_trending_by_hashtag(self, hashtag, count=10):
        """
        Fetches trending videos for a specific hashtag.
        """
        videos_data = []
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[self.ms_token], num_sessions=1, sleep_after=3)
            tag = api.hashtag(name=hashtag)
            
            async for video in tag.videos(count=count):
                v_dict = video.as_dict
                videos_data.append({
                    "id": v_dict.get('id', 'N/A'),
                    "desc": v_dict.get('desc', 'No description'),
                    "author": v_dict.get('author', {}).get('uniqueId', 'unknown'),
                    "stats": v_dict.get('stats', {}),
                    "url": f"https://www.tiktok.com/@{v_dict.get('author', {}).get('uniqueId', 'unknown')}/video/{v_dict.get('id', '')}"
                })
        return videos_data

async def main():
    print("🚀 Social Media Trend Agent Initialized.")
    scraper = TikTokScraper()
    
    # Example Niche: Marketing Tips
    niche_hashtag = "marketingtips"
    print(f"🔍 Searching for trending reels in: #{niche_hashtag}")
    
    try:
        # Fetching a larger batch to give Gemini choices to filter
        videos = await scraper.fetch_trending_by_hashtag(niche_hashtag, count=15)
        print(f"✅ Found {len(videos)} videos. Passing to Gemini for Smart Filtering...\n")
        
        # Define Brand Guidelines
        brand_persona = """
        We are a B2B Software Brand helping marketing teams save time with AI.
        Our tone is professional but witty. 
        We are looking for 'Educational', 'POV', 'Talking-head', or 'Listicle' formats.
        Skip purely generic trending dances unless they can be directly tied to B2B struggles.
        """
        
        processor = TrendProcessor(brand_guidelines=brand_persona)
        analysis_result = processor.filter_and_analyze(videos)
        
        print("="*60)
        print("🎯 AI FILTERED TRENDS & BESPOKE IDEAS")
        print("="*60)
        print(analysis_result)
        
    except Exception as e:
        print(f"❌ Error during scraping or AI processing: {str(e)}")
        print("💡 Tip: Double check your TIKTOK_MS_TOKEN and GEMINI_API_KEY in the .env file.")

if __name__ == "__main__":
    asyncio.run(main())
