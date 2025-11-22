<div style="text-align: center; padding: 20px;">
  <h3 style="margin: 0; font-family: Arial, sans-serif; color: red">Palestine Children, Women and Men are dying...</h3>
  <img src="Palestine.jpg" alt="Palestine Flag" style="width: 475px; border-radius: 3%;">
</div>

## Gemini Py-CLI
A simple Gemini CLI program, written in Python. <br>
Used for simple conversations. <br>
+ Tested using Windows Command Prompt & ConEmu console, in Windows 8.1 64-bit. <br>
+ <span style="color:orange; font-weight:bold;">In development, help is highly appreciated!</span><br>

---
<span style="color:cyan">For people who don't know Python, it's just a small command-line program. After installing it, you only run 2 commands, one to install dependencies (which took me 3 min with my 80kb/s internet), then the main command which is instant.</span>

----

## Features
* Made primarily for low-spec or slow internet users, including myself (Not yet perfect, but in progress).
* Worked even with a dead connection (< 15 kb/s); Yeah! but with only short messages (< 100 characters).
* I respect privacy (because I'm a user like you too), thus I don't hold or manipulate any personal data, even with error log (which can be turned OFF), the program removes file paths and user prompts, keeping only what is absolutely needed.
* History can be saved locally in many forms, even if the program crashes:
	+ Automatically, save chat history to a json file.
	+ Automatically, save prompt history to a text file.
	+ At request, save chat history to a human readable text file.
    + At request, save the last Gemini response to a simple text file.
* Colorful & vital console text.
* Customizable, you can edit many settings, like colors, delays, completion...
  (Not all areas are modifiable yet, but in progress).
* Word suggestion & completion:
	+ Suggest from a wordlist, a menu popup to choose a word from.
	+ Suggest from history, you get inline completion upon typing words from previous prompts.
* Cross platform, binaries are not yet created, perhaps on request I'll do that (I'm too lazy).
* Common keyboard shortcuts + Vim/Emacs shortcuts (beta) + Mouse support (beta).
* Stubborn error handling, yet still not perfect.

## Quick Start
#### 1) Python Setup:
1. Install [Python](https://www.python.org/downloads/) version suitable for your system.
2. Install required libraries, open terminal & type: `pip install httpx google-genai prompt_toolkit rich pyperclip questionary`
3. Clone this repository, or download the [ZIP](https://github.com/Mohyoo/Gemini-Py-CLI/archive/refs/heads/main.zip) file.
4. Unleash Gemini Py-CLI, open CMD in the cloned repository folder & type: `python gemini.py` <br> (Obviously, you'll get an API key error, just continue reading.)

#### 2) First Launch:
1. Get an API key from [AI-Studio](https://aistudio.google.com/app/api-keys)
and paste it in **settings.py** (First few lines). <br> ***(It's free and easy to get)***
2. You can change other settings beside the API key if you wish (e.g: The used Gemini model).
3. Run the script again: `python gemini.py`

#### 3) Usage:
1. Press 'Ctrl-Space' to add a new line to your prompt.
2. Press 'Ctrl-C' to clear/cancel a prompt, stop a response, or quit
the program.
3. Type 'help' for more details (It's not too long, just 1 min reading).

#### 4) Limitations:
1. Tables with many columns will appear chaotic.
2. Special characters (like the asterisk '*' for bold or italic text)
will appear as a plain text.
3. Some other bugs I didn't discover yet :)

---

## Notes
This script in under development, and I'm too lazy to keep working on it. <br>
If you want more features, or want binaries for Windows, etc. You can tell me (In the [Issues](https://github.com/Mohyoo/Gemini-Py-CLI/issues) section for example). <br>
Let's just hope google won't change its Gemini server protocols. <br>

By the way, there is a serie of commented `raise` statements in the script, ignore them, they are just for testing.

---

## Advices
1. If you cancel a sent prompt earlier, Google will not receive it at all.
2. If you have a very slow internet that even browsers don't respond with:
    + Break your prompt into parts (< 100 characters).
    + Make sure the AI response will be short or broken into parts.
    + Periodically, restart both your network adapter & chat session.
    + And **BANG!** you are a network hacker!
3. The lower you set options (e.g: small history file size, faster typing effect), the better performance & network latency you get.
4. For old consoles (e.g: Windows CMD), some features must be OFF for the program to function correctly (e.g: colors, ANSI codes, console width).


## Privacy Summary
* If you want to help future visitors about privacy concerns, please help fulfill this page: [Gemini Terms](https://tosdr.org/en/service/7887).

* From this program's side, there is no data collection, or any anti-privacy matter (malware, adware, spyware...), but from Google's side:

* Google AI Data Collection:
    + Default Use (Free Tier): Google can use your prompts & AI responses to develop, improve, and train its models and services.
    + Your Data is Not Private by Default: If you are using the free Google AI Studio key, you have no guarantee that your data won't be used for training.
    + Data Ownership: You retain ownership of the content you create, but you grant Google a license to use it to operate the service.
    + No Code Opt-Out: You cannot configure Google API python library to stop data collection or training usage for standard API keys.

* Privacy Solution:
    + Vertex AI: The only guaranteed way to ensure your data is not used is to switch to Google Cloud Vertex AI. This is a feature of their enterprise/paid service tier.
    + Data Retention: Data is generally retained for a limited period for safety monitoring and debugging, regardless of the training policy.

## To Do
1. Handle big markdown tables so that they appear readable.
2. Add the ability to upload files.
3. Refactor the code and make it human readable (A total mess is here).
5. Enhance response speed (If already possible).
6. Handle more stupid errors.
7. And more... I'm suffering.

## Disclaimer
This is not an official **Google** program!