# Hackathon Pitch Script: Autonomous Social Trend Agent

## Intro (The Hook)
**(10 Seconds - Look at the audience)**
"A quick show of hands: How many of you here have tried to create content for a business or a personal brand? ... Keep your hand up if you spend more time staring at a blank screen trying to figure out what to post than actually filming it."

*(Wait for agreement/hands)*

"Exactly. Staying relevant on social media is a full-time job. You have to scroll TikTok for hours to find a trend, figure out the psychology of *why* it worked, map it to your specific boring B2B or niche product, and then actually write a script that doesn’t sound like an ad. 

Today, we automated that entire job. Meet the **Autonomous Social Trend Agent**."

---

## Phase 1: The UI and Niche Discovery
**(Point to the screen - Show the Streamlit UI Sidebar)**
"We built an agent that doesn't just write generic ChatGPT scripts. It acts like a Senior Creative Director. Here on the left, we load in our brand's DNA. For this demo, we use 'EcoFit', an eco-conscious activewear brand aimed at Gen Z. We tell the agent exactly what formats we love—like educational POVs—and what we hate."

**(Click "Run Analysis" in the UI)**
"When I click this button, the agent uses an open-source, headless browser scraper to bypass TikTok's restrictions and secretly pull the top 20 trending videos in our hashtag, `#gymtok`, over the last 48 hours."

*Wait for the UI status to say 'Scraping TikTok...'*
"Right now, it's ingesting raw cultural data. But raw data is useless without context."

---

## Phase 2: The Multi-Agent Simulation
**(Point to the Live Status Updates in the UI)**
"Here is where the real magic happens. We didn't just build one agent. We built a Multi-Agent Simulation Loop powered by Gemini 2.5 Flash.

**Agent 1 is the Creative Director.** It reads the 20 raw trends, strips away the noise, picks the single best psychological hook, and writes a bespoke script for EcoFit. 

But it doesn't stop there. 

**Agent 2 is our Simulated Target Audience.** It acts as a Gen Z doom-scroller lying on their couch at 11 PM. Agent 2 reads Agent 1's script and explicitly grades it on the '3-Second Hook Rule', Relevance, and Authenticity. 

If Agent 2 scores it lower than an 8 out of 10... it brutally rejects it."

*(Point to the live feedback generated in the UI)*
"Notice what the Audience Agent outputs real-time on the screen. It explicitly tells us *why* it scored a draft a 7/10 or a 9/10, and exactly where the Creative Director lacked. 

It grades the draft against 3 strict metrics based on the data we fed it:
1. **The 3-Second Rule:** Is the hook strong enough to stop a Gen-Z doom-scroller?
2. **Value:** Does it provide actual value instead of feeling like a skippable ad?
3. **Authenticity:** Is the tone natural to TikTok?

If a draft scores lower than an 8 out of 10... it brutally rejects it and prints exactly what went wrong. The agents then loop. Agent 1 rewrites the script based on that exact harsh critique until the simulated audience finally approves it."

---

## The Reveal
**(Scroll down to the final Output in the UI)**
"And here is the final, audience-validated script. It tells us exactly why the trend works, gives us a perfectly tailored hook for our brand, and writes the entire script so that it sounds authentic to TikTok."

*(Optional: If video generation is added)*
"But what if we don't even want to film it? The final step pipes this validated script directly into a Video Synthesis API. From scraping a trend to generating a fully voiced, lip-synced video—zero human intervention required."

## Conclusion
"We've turned endless scrolling and writer's block into a predictable, automated content factory. Thank you."
