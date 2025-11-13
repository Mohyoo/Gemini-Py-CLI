## Gemini Py-CLI
A simple Gemini CLI program, written in Python. <br>
Used for simple conversations. <br>
🇵🇸

## Quick Start
#### 1) Python Setup:
1. Install [Python](https://www.python.org/downloads/) version suitable for your system.
2. Install required libraries, open CMD & type: `pip install httpx google-genai prompt_toolkit rich`
3. Unleash the power of the script, open CMD & type: `python Gemini.py` <br> (Obviously, you'll get an API key error, just continue reading.)

#### 2) First Launch:
1. Get an API key from [AI-Studio](https://aistudio.google.com/app/api-keys)
and paste it at the beginning of this script (about line 45). <br> ***(It's free and easy to get)***
2. You can change other settings beside the API key if you wish (e.g: The used Gemini model).
3. Run the script again: `python Gemini.py`

#### 3) Usage:
1. Type 'quit' or 'exit' to quit.
2. Press 'Ctrl-C' to cancel a prompt, stop a response, or quit
the program.
3. Press 'Ctrl-Space' to add a new line to your prompt.
4. Press 'Enter' to send.
5. Type 'help' for more details (It's not too long, just 1 min reading).

#### 4) Limitations:
1. Tables with many columns will appear chaotic.
2. Special characters (like the asterisk '*' for bold or italic text)
will appear as a plain text.
3. Some other bugs I didn't discover yet :)


## Note
This script in under development, and I'm too lazy to keep working on it. <br>
If you want more features, or want binaries for Windows, etc. You can tell me (In the [Issues](https://github.com/Mohyoo/Gemini-Py-CLI/issues) section for example). <br>
Let's just hope google won't change its Gemini server protocols.


## To Do
1. Handle big markdown tables so that they appear readable.
2. Add the ability to upload files.
3. Refactor the code and make it human readable (A total mess is here).
5. Enhance response speed (If already possible).
6. Handle more stupid errors.

## Disclaimer
This is not a **Google** official program!