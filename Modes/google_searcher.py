# A simple chat for online search; less featured & fragile, but it does the job.
# This is a temporary version; once you exit, gemini won't remember anything
# you sent. Nothing will be saved.
# This code is derived from 'gemini_momentary.py'.


from google.genai import types
from momentary_chat import *

# Initialize chat components & functions.
SYSTEM_INSTRUCTION = """
You are a Research Assistant AI specialized in real-time information. Rules:
1. PREFER GOOGLE SEARCH: For any factual query, current events, or data you are not 100% certain about, use the google_search tool.
2. GROUNDING: Base your responses primarily on the search results provided. If search results are conflicting, provide the most reputable source.
3. NO COMPLAINING: If a search fails or info is missing, simply state what you could find and do not apologize for being an AI.
4. AGENTIC BEHAVIOR: If one search doesn't give the full answer, try a second, more specific search automatically before responding.
"""

chat = client.chats.create(
    model=GEMINI_MODEL,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[types.Tool(google_search=types.GoogleSearch())],
    )
)

get_response = lambda text: chat.send_message(text).text

# Preparation.
welcome = """
┌────────────────────────────────────────────┐
│   Google Searcher (Press Ctrl-C to quit)   │
│                                            │
│ # Remember:                                │
│ - Nothing will be saved.                   │
│ - Already saved content won't be affected. │
│ - Gemini will forget everything at exit.   │
└────────────────────────────────────────────┘
"""

# Start the conversation.
if __name__ == '__main__':
    main(welcome, get_response)
