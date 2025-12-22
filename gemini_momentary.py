# This is a quick (only one message at a time) version, where gemini won't
# remember any previous message you sent. Nothing will be saved.
# This is good for quick questioning or when you are bored.
# This code is simple & fast; but also fragile & less featured.

import os
from settings import GEMINI_API_KEY, GEMINI_MODEL
from google.genai import Client

# Initialize chat components & functions.
client = Client(api_key=GEMINI_API_KEY)
generate_content = client.models.generate_content
get_response =  lambda text: generate_content(model=GEMINI_MODEL, contents=text).text
size = os.get_terminal_size

# Preparation.
sep = '─' * (size().columns - 1)
prompt = 'None'
welcome = """
┌────────────────────────────────────────────┐
│   Momentary Chat (Press Ctrl-C to quit)    │
│                                            │
│ # Remember:                                │
│ - Nothing will be saved.                   │
│ - Already saved content won't be affected. │
│ - Gemini will forget each sent message     │
│   immediately.                             │
└────────────────────────────────────────────┘
"""

# Start the conversation.
def main(welcome=welcome):
    """Start the conversation; take user input & return AI response."""
    global sep, prompt
    print(welcome)
    
    while True:
        try:
            # Get input.
            prompt = input('You: ' if prompt.strip() else '.... ')
            if not prompt.strip(): continue
            
            # Get response.
            sep = '─' * (size().columns - 1)
            response = get_response(prompt)
            print(f'{sep}\nGemini:\n{response}\n{sep}')
        
        except KeyboardInterrupt:
            print(f'\n{sep}\nQuitting...')
            quit()
        
        except Exception as error:
            error_type = type(error).__name__
            try: msg = error.message     # Get 'message' attribute from 'genai' errors.
            except: msg = error.args[0]  # Built-in excepetions have 'args' tuple, 1st item is the message.
            print(f'{sep}\n{error_type}: {msg}.\n{sep}')

if __name__ == '__main__':
    main(welcome)
