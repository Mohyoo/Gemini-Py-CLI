<div align="center">
  <h3 style="margin: 0; font-family: Arial, sans-serif; color: red">Palestine Children, Women and Men are dying...</h3>
  <img src="Palestine.jpg" alt="Palestine Flag" style="width: 475px; border-radius: 3%;">
</div>

<p align="center">
  <br><b>LIST OF CONTENT</b><br> •
  <a href="#gemini-py-cli">Introduction</a> •
  <a href="SCREENSHOTS.md">Screenshots</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#wiki">Wiki</a> •
  <a href="#limitations">Limitations</a> • <br>
</p>

## Gemini Py-CLI
A simple Gemini CLI program, written in Python. <br>
Used for simple conversations (and for fun too :) <br>
+ Tested using Command Prompt & ConEmu console, in Windows 8.1 64-bit. <br>
+ <span style="color:orange; font-weight:bold;">In development, help is highly appreciated!</span><br>
+ **Screenshots can be seen [here](SCREENSHOTS.md).**

---
<span style="color:cyan"><b><i>Reminder:</i></b><br>For people who don't know Python, it's just a small command-line program. After installing it, you only run 2 commands, one to install dependencies (which took me 10 min with my 80kb/s internet), then the main command which is instant.</span>

----

## Features
* Free program & API access. Built for the free-tier users, but also works for users with a billing account or paid subscription (not tested on paid accounts).
* Made primarily for low-spec or slow internet users; Worked even with a dead connection (< 15 kb/s); Yeah! but with only short messages (< 100 characters).
* Privacy respect, the program doesn't send, hold or manipulate any personal data or sent-messages; your ***API key*** is only yours; even with logs (which can be turned OFF), the program removes file paths and user prompts, keeping only what is absolutely needed.
* Content can be saved locally in many forms, even if the program crashes:
	+ Automatically, save chat history & prompt history to a structured text file.
	+ At request, save chat history, last AI response or saved info to a human readable text file.
* Colorful & vital console text.
* Word suggestion & completion:
	+ Suggest from a wordlist, a menu popup to choose a word from.
	+ Suggest from history, you get inline completion upon typing words from previous prompts.
* Customizable, you can edit many settings, like colors, delays, completion...
  (Not all areas are modifiable yet, but in progress).
* Common keyboard shortcuts + Vim/Emacs shortcuts (beta) + Mouse support (beta).
* Cross platform, binaries are not yet created, perhaps on request I'll do that (I'm too lazy).
* Stubborn error handling, yet still not perfect.

## Quick Start
#### 1) Python Setup:
1. Install [Python](https://www.python.org/downloads/) version suitable for your system.
2. Install required libraries, open terminal & type: `pip install httpx google-genai prompt_toolkit rich pyperclip questionary tksvg resvg_py`
3. Clone this repository; or download the [ZIP](https://github.com/Mohyoo/Gemini-Py-CLI/archive/refs/heads/main.zip) file, extract it, and enter the extracted folder.
4. Unleash Gemini Py-CLI! open CMD & type: `python gemini.py` <br> (Obviously, you'll get an API key error, just continue reading)

#### 2) First Launch:
1. Get an API key from [AI-Studio](https://aistudio.google.com/app/api-keys) ***(It's free and easy to get)***
2. Type: `python settings_editor.py` and enter your API key.
3. Run the script again: `python gemini.py`
* ***Optionally:*** You can change other settings if you wish (e.g: The Gemini model), using either the settings editor (which is limited but user friendly) or by freely editing `settings.py`.

#### 3) Usage:
1. Press `Ctrl-Space` to add a new line to your prompt.
2. Press `Ctrl-C` to clear/cancel a prompt, stop a response, or quit
the program.
3. Press `F3` to upload a file.
3. Type `help` for more details (No *bla bla bla...* just 1 min reading).

## Wiki
Visit the [Wiki](https://github.com/Mohyoo/Gemini-Py-CLI/wiki) for some valuable information.

Don't worry, there is no *bla bla bla...* everything is hardly summarized :)


## Limitations:
1. Tables with many columns will appear chaotic.
2. Special characters (like the asterisk '*' for bold or italic text)
will appear as a plain text.
3. Some other bugs I didn't discover yet :)

## To Do
1. Handle big markdown tables so that they appear readable.
2. Refactor the code and make it human readable (A total mess is here).
3. Enhance response speed (If already possible).
4. Handle more stupid errors.
5. Change the world...
6. And more... I'm suffering.

---
***Useless Notes:*** <br>
This script in under development, and I'm too lazy to keep working on it. <br>
If you want more features, or want binaries for Windows, etc. You can tell me (In the [Issues](https://github.com/Mohyoo/Gemini-Py-CLI/issues) section for example). <br>
Let's just hope google won't change its Gemini server protocols. <br>

There is also a serie of commented `raise` statements in the script, ignore them, they are just for testing.

---

## Disclaimer
This is not an official **Google** program!