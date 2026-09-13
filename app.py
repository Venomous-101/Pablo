import sys
import os
import streamlit as st
import asyncio

# Cloud par writable directory set karna taake browser download ho sakay
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/tmp/ms-playwright"

@st.cache_resource
def setup_playwright():
    os.system("playwright install chromium")

try:
    setup_playwright()
except Exception:
    pass

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir in sys.path:
    sys.path.remove(current_dir)
    import site
    for path in site.getsitepackages():
        sys.path.append(path)
    sys.path.insert(0, current_dir)

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Browser, BrowserConfig

st.title("🌐 AI Browser Automation Agent")
st.write("Apna task likhein aur AI khud browser par perform karega!")

if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

task = st.text_input("Task likhein (maslan: Search for latest AI news on Google):")

if st.button("Run Agent"):
    if "GOOGLE_API_KEY" not in os.environ or not os.environ["GOOGLE_API_KEY"] or not task:
        st.error("Barah-e-karam Streamlit Secrets mein API Key set karein aur Task enter karein!")
    else:
        st.info("Agent kaam shuru kar raha hai, background mein browser download ho raha hai, intezaar karein...")
        
        async def main():
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
            object.__setattr__(llm, "provider", "google")
            
            # Explicit cloud browser configuration
            browser = Browser(
                config=BrowserConfig(
                    headless=True,
                    disable_security=True,
                )
            )
            
            agent = Agent(task=task, llm=llm, browser=browser)
            result = await agent.run()
            return result

        res = asyncio.run(main())
        st.success("Task successfully run ho gaya!")
        st.write(res)
