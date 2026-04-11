This is a short description of the libraries/modules that need to be installed for the program to work. <br>
If some of them are missing, you won't necessarily get an error unless you try to use a feature that requires that library. <br><br>
Reminder: <br>
A library is just a piece of code; so instead of manually writing your needed code, I just use a ready template; I tried my best to use less dependencies.

### Required
> Installation command: `pip install httpx google-genai prompt_toolkit rich`
1. `httpx & google-genai`: These two libraries are ***required*** to establish the connection between the client (you) and Google; basically to send messages/files and receive responses.
2. `prompt_toolkit`: ***Required*** to handle user input (yours); it adds features like custom hotkeys, bottom toolbar, prompt history, syntax highlighting, word suggestion, etc.
3. `rich`: ***Required*** to handle rich text, mainly Gemini responses which are markdown-based; it adds colors, lines/tables, formatting, etc.

### Optional
> Installation command: `pip install pyperclip stop_words questionary tksvg resvg_py markdown tkinterweb json_repair html2text beautifulsoup4`
1. `pyperclip`: Needed to handle clipboard copy/paste; you won't be able to use CTRL-P, ALT-X or any clipboard feature in the program; CTRL-C, CTRL-X & CTRL-V will still work.
2. `stop_words`: Used -at request- to compress user prompt (yours) by removing unnecessary stop words.
3. `questionary`: Used to show & handle the options menu in `settings_editor.py`; only ***optional*** if you don't use `settings_editor.py`; thus, you'll have to edit `settings.py` manually.
4. `tksvg & resvg_py`: These two libraries are used for image generation mode; if you don't use it, this is ***optional***.
5. `markdown & tkinterweb`: These two libraries are used by the quick markdown viewer (`/viewer` command); if you don't use it, this is ***optional***.
6. `json_repair`: Only needed if the program JSON files (like `chat_history.json & config.json`) get corrupted; this will try to repair them automatically.
7. `html2text`: Only needed when you try to convert the last Gemini response or the whole chat to a simplified text file (without markup code).
8. `beautifulsoup4`: Only needed when you try to convert the last Gemini response or the whole chat to an HTML web page.