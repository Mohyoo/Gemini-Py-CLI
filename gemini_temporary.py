# This is a temporary version; once you exit, gemini won't remember anything
# you sent. Nothing will be saved.
# This is good for side missions.
# This code is derived from 'gemini_momentary.py'.

from gemini_momentary import *

# Initialize chat components & functions.
chat = client.chats.create(model=GEMINI_MODEL)
get_response =  lambda text: chat.send_message(text).text

# Preparation.
welcome = """
┌────────────────────────────────────────────┐
│   Temporary Chat (Press Ctrl-C to quit)    │
│                                            │
│ # Remember:                                │
│ - Nothing will be saved.                   │
│ - Already saved content won't be affected. │
│ - Gemini will forget everything at exit.   │
└────────────────────────────────────────────┘
"""

# Start the conversation.
if __name__ == '__main__':
    main(welcome)
