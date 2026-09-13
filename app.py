import streamlit as st
import asyncio
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

st.title("🌐 AI Browser Automation Agent")
st.write("Apna task likhein aur AI khud browser par perform karega!")

task = st.text_input("Task likhein (maslan: Search for latest AI news on Google):")
api_key = st.text_input("Apni Gemini API Key enter karein:", type="password")

if st.button("Run Agent"):
    if not api_key or not task:
        st.error("Barah-e-karam API Key aur Task dono enter karein!")
    else:
        os.environ["GOOGLE_API_KEY"] = api_key
        st.info("Agent kaam shuru kar raha hai, barah-e-karam intezaar karein...")
        
        async def main():
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
            agent = Agent(task=task, llm=llm)
            result = await agent.run()
            return result

        res = asyncio.run(main())
        st.success("Task successfully run ho gaya!")
        st.write(res)
