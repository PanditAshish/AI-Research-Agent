import os
import streamlit as st
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from google import genai

# Load API key
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# Gemini client
client = genai.Client(api_key=API_KEY)

# Page
st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🔎"
)

st.title("🔎 AI Research Agent")
st.write("Ask a question and the agent will research it on the web.")

question = st.text_input(
    "What do you want to research?"
)

if st.button("Research"):

    if not question:
        st.warning("Please enter a research question.")
        st.stop()

    # Web search
    with st.spinner("Searching the web..."):

        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                question,
                max_results=5
            )

            for result in search_results:
                results.append(
                    f"Title: {result['title']}\n"
                    f"URL: {result['href']}\n"
                    f"Summary: {result['body']}\n"
                )

    research_data = "\n\n".join(results)

    # Gemini analysis
    with st.spinner("Analyzing research..."):

        prompt = f"""
You are an AI research agent.

Research question:
{question}

Web search results:
{research_data}

Create a concise research report.

Use this structure:

# Research Summary

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Important Details
Explain the most important information.

## Conclusion
Give a short factual conclusion.

## Sources
List the source titles and URLs from the search results.

findstr /n "gemini" app.pyDo not invent information.
Use only the information available in the search results.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

    st.markdown(response.text)
