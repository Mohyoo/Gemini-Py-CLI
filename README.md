## Gemini Py-CLI
A simple Gemini CLI program, written in Python. <br>
Used for simple conversations. <br>
🇵🇸

## Quick Start
#### 1) Python Setup:
1. Install [Python](https://www.python.org/downloads/) version suitable for your system.
2. Install required libraries, open CMD & type: `pip install google-genai prompt_toolkit`
3. Unleash the power of the script, open CMD & type: `python Gemini.py` <br> (Obviously, you'll get an API key error, just continue reading.)

#### 2) First Launch:
1. Get an API key from [AI-Studio](https://aistudio.google.com/app/api-keys)
and paste it in this script at line (19). <br> ***(It's free and easy to get)***
2. You can change other settings (e.g: The used Gemini model at line
(20)) if you wish.
3. Run the script again: `python Gemini.py`

#### 3) Usage:
1. Type 'quit' or 'exit' to quit.
2. Press 'Ctrl-C' to cancel a prompt, stop a response, or quit
the program.
3. Press 'Enter' to add a new line to your prompt.
4. Press 'ESC' then 'Enter' to send.

#### 4) Limitations:
1. Tables with many columns will appear chaotic.
2. Special characters (like the asterisk '*' for bold or italic text)
will appear as a plain text.
3. Some other bugs I didn't discover yet :)


## Note
I'm too lazy to keep working on this script. <br>
If you want more features, or want binaries for Windows, you can tell me (In the **Issues** section for example). <br>
Let's just hope google won't change its Gemini server protocols.


## To Do
1. Handle big markdown tables in Gemini responses so that they appear readable.
2. Handle special characters (like the asterisk *) in Gemini Responses, without affecting code blocks or math expressions.
3. Refactor the code and make it human readable (A total mess is here).
4. Save chat history locally, and pass it to Gemini at startup.
5. Enhance response speed (If already possible).
6. Handle more stupid errors.

