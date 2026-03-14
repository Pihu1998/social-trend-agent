import streamlit as st
import asyncio
from main import TikTokScraper
from processor import TrendProcessor

st.set_page_config(page_title="AI Social Trend Agent", page_icon="📈", layout="wide")

st.title("💡 Autonomous Social Trend Agent")
st.markdown("Discover and adapt trending content for your brand using open-source scraping and Gemini 2.5 Flash Multi-Agent Simulation.")

# Initialize session state for analysis results
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None

with st.sidebar:
    st.header("⚙️ Settings")
    
    hashtag = st.text_input("Hashtag to Monitor", value="gymtok")
    video_count = st.slider("Number of Raw Videos to Scrape", min_value=5, max_value=20, value=10)
    
    st.markdown("---")
    st.header("🧠 Multi-Agent Configuration")
    
    brand_persona = st.text_area(
        "[Agent 1] Brand Guidelines",
        value="BRAND NAME: EcoFit\nINDUSTRY: Sustainable Athletic Wear\nTONE: Energetic, Professional, Inspiring\n\nCONTENT PREFERENCES:\n- We LOVE 'Day in the life' (POV) videos.\n- We LOVE 'Educational' videos about sustainability or workout tips.\n- Skip purely generic trends without substance.",
        height=150
    )
    
    target_audience = st.text_area(
        "[Agent 2] Target Audience Persona",
        value="Millennials and Gen-Z who care about the environment but want stylish gym clothes. They value authenticity, fast tips, and hate being sold to directly.",
        height=100
    )
    
    simulation_scenario = st.text_input(
        "[Agent 2] Simulation Scenario",
        value="Scrolling TikTok at 11 PM on the couch, looking for quick motivation or entertainment before bed."
    )
    
    run_agent = st.button("🚀 Run Analysis & Simulation", use_container_width=True)

if run_agent:
    with st.spinner(f"Scraping #{hashtag} on TikTok..."):
        try:
            # Create a new event loop for asyncio within Streamlit
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            scraper = TikTokScraper()
            videos = loop.run_until_complete(scraper.fetch_trending_by_hashtag(hashtag, count=video_count))
            
            if not videos:
                st.error(f"No videos found for #{hashtag}. Check your TIKTOK_MS_TOKEN.")
            else:
                st.success(f"Successfully scraped {len(videos)} videos!")
                
                with st.status("🤖 Multi-Agent Simulation Running...", expanded=True) as status:
                    def status_update(msg):
                        st.write(msg)
                        
                    def feedback_update(iteration, score, critique):
                        st.markdown(f"**Target Audience Feedback - Draft #{iteration} (Score: {score}/10):**\n> {critique}")
                    
                    processor = TrendProcessor(
                        brand_guidelines=brand_persona,
                        target_audience=target_audience,
                        simulation_scenario=simulation_scenario
                    )
                    
                    result = processor.filter_and_analyze(
                        videos, 
                        status_callback=status_update,
                        feedback_callback=feedback_update
                    )
                    
                    status.update(label="Analysis and Validation Complete! ✅", state="complete", expanded=False)
                    
                    st.session_state.analysis_result = result
                    
        except Exception as e:
            st.error(f"Error during execution: {str(e)}")

# Display the results
if st.session_state.analysis_result:
    st.markdown("---")
    st.header("🎯 AI Generated Trend Actions")
    
    st.markdown(st.session_state.analysis_result)
