import sys
from random import randint, choice

# When editing this, respect each option's possible values, otherwise prepare yourself
# for a crash (Better to keep a backup of this file).
# If you are confused with some settings, try 'settings_editor.py' or visit the wiki:
# https://github.com/Mohyoo/Gemini-Py-CLI/wiki/Settings
# You can always ask in my GitHub page, or even request a future change. I'll try hard to
# keep everything easily accessible.


# General Settings
GEMINI_API_KEY = 'YOUR_API_KEY_HERE'
GEMINI_MODEL = 'gemini-flash-latest'         # Advanced models are more expensive and have less API limits.
MAX_HISTORY_MESSAGES = 512                   # The maximum number of chat history messages to keep; saves internet bandwidth & loading/saving time.
NO_HISTORY_LIMIT = False                     # When True, chat history will never be truncated.
ENTER_NEW_LINE = False                       # If True, Enter inserts a new line, and Esc-Enter submits; if False, Enter submits, and Esc-Enter inserts a new line.
SUGGEST_FROM_HISTORY = False                 # Use the user's prompt history for inline word completion (SLOW).
SUGGEST_FROM_WORDLIST = True                 # Suggest words while typing, in a menu popup, based on a wordlist.
SUGGESTIONS_LIMIT = 5                        # The number of suggestions to show while typing a prompt.
SAVED_INFO = True                            # If True, user input will be saved with highest priority if he starts it with 'remember'.
USE_COLORS = True                            # Better to disable colors for old consoles.
USE_ANSI = True                              # Like USE_COLORS, but more general, once OFF, all ANSI escape codes will be disabled (Recommended to be False for old consoles).
INFORMATIVE_RPROMPT = True                   # Short informational text at top right of the prompt field.
BOTTOM_TOOLBAR = True                        # Show a handy toolbar for a quick reference.
SPINNER = 'line'                             # Shown while waiting, can be: dots, line, bounce, moon, star, runner... (In CMD type 'python -m rich.spinner' for more).
RESPONSE_EFFECT = 'line'                     # Effect while displaying response, can be:
                                                 # None for no animation.
                                                 # 'line' for line-by-line animation (Recommended).
                                                 # 'word' for word-by-word animation (Satisfying).
                                                 # 'char' for an almost instant character-by-character animation (Safe, but may be unnoticeable).
                                                 # 'char slow' for a smooth character-by-character animation (Safe, but really slow).
                                                 # 'char fast' for a fast character-by-character animation; you should check if this causes a high CPU usage in your computer
                                                 # (from Task Manager), if so, it is a waste of resources & energy, bad choice for long responses, but still fine for short ones.
                                                 # * All 'char' animations can cause glitchs!


# Moderate Settings
CONSOLE_WIDTH = 80                           # How many characters to print per line (Should be < Console window).
INPUT_HIGHLIGHT = False                      # Syntax highlighting for the user prompt.
INPUT_HIGHLIGHT_LANG = 'python'              # The language name used for syntax highlighting.
STARTUP_API_CHECK = False                    # Disable for a slightly faster loading, and for the ability to enter the chat offline.
SAVE_INPUT_ON_CLEAR = False                  # Save the prompt to history when the user clears its prompt with Ctrl-C.
SAVE_INPUT_ON_STOP = False                   # Save the prompt to history when the user stops its prompt with Ctrl-C or F-Keys.
NO_ERROR_DETAILS = False                     # Never ask the user to see more details about an error.
ERROR_LOG_ON = True                          # To log errors to a file, console output won't be affected.
GLOBAL_LOG_ON = True                         # To log the entire console output to a file + optionally hidden debugging info,
                                                 # it gets cleared on each launch, visual console output won't be affect.


# Advanced Settings
SAVED_INFO_FILE = 'saved_info.txt'           # To save important informations at user request.
LAST_RESPONSE_FILE = 'last_response.txt'     # To save last Gemini response in a text file.
WORDLIST_FILE = 'word_suggestion.txt'        # A small wordlist used for word suggestion.
CHAT_HISTORY_JSON = 'chat_history.json'      # To save/load chat history to/from a json file (If available).
CHAT_HISTORY_TEXT = 'chat_history.txt'       # To save chat history as a simple text file (If available).
PROMPT_HISTORY_FILE = 'prompt_history.txt'   # To load prompt history (If available).
ERROR_LOG_FILE = 'application_errors.log'                  # The file to write errors to (Level: warning, error, critical).
GLOBAL_LOG_FILE = 'application_console_output.log'         # The file to write the entire console output to + optionally hidden debug info (Level: debug, info).
PROMPT_HISTORY_SIZE = 0.5                    # Max prompt history file size (1 = 1 MB).
LOG_SIZE = 0.5                               # Max error log file size (1 = 1 MB).


# Time Settings (In Seconds)
SERVER_ERROR_ATTEMPTS = 3                   # How many times to try to get a response upon a server error.
SERVER_ERROR_DELAY = (3, 5)                 # 1st to wait upon first server error attempt, then 2nd for next attempts.
HTTP_TIMEOUT = 30                           # Timeout for the entire request, after which the API call is blocked & a timeout error gets raised.
STATUS_UPDATE_DELAY = (1.5, 3)              # Fake random delay to update the status shown while waiting for response (Doesn't add extra delays, all safe).
SLEEP_INTERVAL = 0.1                        # Small chunks used as intervals with sleeping functions, to keep UI responsive.


# Colors
if USE_COLORS and USE_ANSI:
    # By ANSI code (Used in print() & cprint())
    CYN     = '\033[96m'    # Red
    RED     = '\033[91m'    # Red
    GR      = '\033[92m'    # Green
    YLW     = '\033[93m'    # Yellow
    BL      = '\033[94m'    # Blue
    GRY     = '\033[90m'    # Gray
    UL      = '\033[4m'     # Underline
    BD      = '\033[1m'     # Bold
    RS      = '\033[0m'     # Reset
    GEM_BG  = '\033[44m'    # Background for Gemini.
    
    # By name (Used in prompt() & console.status()).
    PROMPT_BG  = 'cyan'     # Background for the prompt. 
    PROMPT_FG  = 'gray'     # For the prompt's placeholder, new line mark, informative_rprompt, toolbar...
    WAIT_1 = 'green'        # Used when waiting for Gemini response.
    WAIT_2 = 'cyan'         # Used with Gemini response's 2nd attempt.
else:
    CYN = RED = GR = YLW = BL = GRY = UL = BD = RS = GEM_BG = ''
    PROMPT_BG = PROMPT_FG = WAIT_1 = WAIT_2 = 'white'


# Custom Messages
FAREWELLS_MESSAGES = [
    # Messages displayed upon existing.
    # Standard
    "Chat session ended. Goodbye!",
    "Gemini signing off. Until next time!",
    "The light fades. See you in the next prompt!",
    "Session terminated successfully. Farewell.",
    "Peace out. Thanks for chatting!",
    "Processing complete. Disconnecting now.",
    "Fin. Come back soon!",
    "Chat complete. Have a productive day!",
    "Task completed. System shutdown initiated.",
    "Voilà un bon travail, mais il est temps de partir.\nBonne route à vous!",
    
    # Funny
    "The chat is lost, but the war has just begun!",
    "Abracadabra! Poof...\nWait, who turned off the lights?",
    "Adios, Amigo! The terminal awaits your return.",
    "¡Nos vemos, cocodrilo!\n(See you, crocodile :P)",
    "¡Hasta la vista!\n(See you around :D)",
    "Au revoir!",
    "Ciao! I'm outta here faster than an Italian pizza disappearing at a party.",
    f"Okay okay, calm down, he only ended the chat...\nBUT AAAAARGHHH...!!!\n"
    f"{RED}System Rage Error occurred;{RS}{GR} Cya!",
    "Ladies & Gentlemen, we are closing.",
    "Just a quick fake cleanup...\nOK, all done!",
    "Okay ladies, time to go home.",
    "Artryoos. Metryoos. Zeetoos!",
    "Remember, it's all about: Hakuna Matata!\n(No Worries :)",
    "Ma chère mademoiselle, it is with deepest pride and greatest pleasure that we proudly present... The End.",
    "¡Ándale! ¡Ándale! ¡Arriba! ¡Arriba! Yeehaw!",
    "Tactical retreat. We'll be back.",
    "Shadow Fleeing Jutsu!",
    "Together for a better world (Where I'm the boss).",
    "Finally, some peace of mind...",
    "Good, I was in no mood for chat already.",
    "Oh come on, the fun has just begun!",
    "Seriously man? The excitement has just started!",
    "I'm watching you 0-0",
    "I see you :3",
    "If a poison expires, then it becomes more poisonous or less poisonous? (o.O)",
    "Cheese has holes.\nMore cheese = More holes.\nMore holes = Less cheese.\nMore cheese = Less cheese (O.O)",
    "You are breathing involuntary; but now that you knew, you have to breath voluntary :P",
    "Cleaning crime scene...\nAlright! ready to escape.",
    "Normal mode OFF, switching to Agent Six...",
    "There'll be no mercy next time...",
    "Let's celebrate a party just for now reason!",
    "Don't look back, you've been warned!",
    
    # Enthusiastic
    "Keep coding and stay curious!\n(If you aren't a developer, ignore this, you owe me a coffee)",
    "May your logic be sound and your keys be clean.",
    "Go forth and query, friend.",
    "I'll be here. You know where to find me.",
    "Enjoy the silence. Goodbye.",
    "Until our paths cross again.",
    "Stay curious, stay connected.",
    "Farewell, may the consequences be ever in your favor.",
    "Ce sont les mots que j'aime dans un chat! Au revoir!",
    "I will stay here... if you ever turn back.",
    "Sometimes it's too difficult, yet.. it's not impossible ;)",
    "Keep it up gentleman, the world needs your work.",
    "The waves are calling.. Captain.",
    "Every step, no matter how small, moves you forward ;)",
    "Ok enough playing, time to study.",
    
    # Mathematic 
    f"Calculate this: ({randint(1, 100)} {choice(['+', '-', '*', '/', '**', '%'])} "
    f"{randint(1, 100)})\nC'mon quickly!",
    f"NOOOOOOOOOOOOOOOOOOOOOO...O\nTask: Calculate the partial sum of the sequence: "
    f"({(' ' + choice(['+', '*']) + ' ').join(['O₁', 'O₂', 'O₃', '...', 'On'])})\n"
    f"Given that it's {choice(['an arithmetic sequence (constant difference)', 'a geometric sequence (constant ratio)', 'a harmonic sequence', 'a fibonacci sequence'])}.\n"
    f"Other details: Difference/Ratio={randint(1, 100)}, O₁={randint(1, 500)}, n={randint(1, 999)}\n"
    "Note: It's letter 'O' not zero '0'. Good luck :)",
    "I have an existential crisis every time I try to calculate the square root of a negative number. "
    "I’m pretty sure the imaginary number 'i' (i = √-1, i² = -1) is just a regular number that failed its reality check. "
    "Turns out, the entire universe depends on this one number that doesn't actually exist.",
    "The number 'pi' (π ≈ 3.14) is truly irrational because its digits never repeat or terminate, "
    "essentially making it a decimal nomad with no fixed address in the numeric universe.",
    "Parallel lines have a truly tragic love story: they are absolutely destined to meet at infinity, "
    "but they spend all of eternity getting absolutely nowhere.",
    "The concept of infinity (∞) is basically just a number that got detention "
    "forever and will never be allowed to go home and finish its equation.",
    "Zero (0) is the most dangerous number in the universe; it can multiply anything into oblivion "
    "and yet it is utterly empty, a total void of mathematical consequence.",
    "The Empty Set (ø) is the world's most exclusive club: absolutely nothing is inside, "
    "which makes its bouncer the most tragically overpaid mathematical entity.",
    
    # Serious
    "Remember to commit your changes!",
    "Don't forget to save your work!",
    "Bye Bye! Check your API key status if you run into trouble.",
    f"Thank you for using Gemini Py-CLI! Suggestions are welcome!\nGitHub Home: "
    f"{UL}https://github.com/Mohyoo/Gemini-Py-CLI{RS}",
    f"If you faced any issues, please let me know, I'll try to reply quickly.\n"
    f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}",
    
    # Advices
    "Bored? Ask Gemini to tell you a realistic horror story (ಠ_ಠ)",
    "Know Python? you can edit the source code and send me your modifications as feature requests.",
    "Know Python? You can modify & test the source code, errors can also be logged if the option is ON.",
    "Hint: Gemini web interface too slow or laggy? have a potato computer like mine? this is why Py-CLI was created!",
    "Hint: You can change interface colors from 'settings.py'!",
    "Hint: You can disable colors from settings, this will switch to black/white mode.",
    "Hint: If you see random characters in the console (like '\\033[96m'), then disable ANSI codes from settings.",
    "Hint: Error logging is ON by default, you may use it to send me errors. You can also turn it OFF if you wish.",
    "Hint: Both global & error logging may cause a slightly extra delay for AI response, I don't know why, but you can always turn them OFF.",
    "Hint: Console width is best set to (80) or more, for Windows Command Prompt users, (79) is better.",
    "Hint: Forgot how to use Gemini Py-CLI? type 'help' to see a very short and friendly menu; there is also "
    "a handy toolbar at the bottom of the console (It can be turned off).",
    "Hint: You can change MAX_HISTORY_MESSAGES in settings, but if chat history gets too long, Gemini will "
    "start forgetting things, and the program might need more time while loading/saving chat.",
    "Hint: Some options may slightly affect performances, like response typing effect, word suggestion & completion, application logs, etc."
    "You can turn them OFF at any time.",
    "Hint: Colors & ANSI codes may not work in old consoles, like Windows Command Prompt; either disable them, "
    "or use a better console emulator; ConEmu is a recommended very lightweight option for Windows.",
    "Hint: You are always encouraged to use a modern console emulator; If the console is old, the program "
    "is still hardcoded to work, but with limited functionality, and so limited experience.",
    "Hint: ANSI codes are the way we tell the console to show colors and some other effects, "
    "but they're not compatible with every console.",
    "Advice: At night, consider enabling dark mode & night light (warmth) mode to protect your eyes, "
    "you'll get used to them over time believe me ;)",
    
    # Quotes
    "If you change the way you look at things, the things you at change...",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "We don't see things as they are, we see them as we are.",
    "The eye sees only what the mind is prepared to comprehend.",
    "To simply observe is to understand.",
    "I used to think that the brain was the most wonderful organ in my body. Then I realized who was telling me this.",
    "My fake plants died because I forgot to pretend to water them.",
    "When nothing is going right, go left!",
    "Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.",
    "Before you diagnose yourself with depression or low self-esteem, first make "
    "sure that you are not, in fact, just surrounded by assholes.",
    "The problem with the world is that the intelligent people are full of doubts, "
    "while the stupid ones are full of confidence.",
    "When a man opens a car door for his wife, it's either a new car or a new wife :3",
    "The way we see the problem is the problem ;)",
]
 
CONTINUE_MESSAGES = [
    # Messages displayed upon confirming exit, but the user chooses NO.
    # Standard
    'Resuming chat...',
    'Cancelling, chat will continues.',
    
    # Funny
    'Acting blind...',
    "Don't just mess with the keyboard next time.",
    'Oof...',
    'Hmmm...',
    'Oops...',
    'I smell doubt...',
    'I can feel something bad is coming...',
    'Nevermind...',
    'Aha! wait.. what were we talking about?',
    'Exit failed successfully.',
    'This is a messing around...',
    
    # Enthusiastic
    'Yeah, this is ma boi!',
    'Relax, the best part is still ahead!',
    'Something good is about to happen...',
    'What a smart move!',
    'This is what I like to hear!',
    
    # Darksiders II - The Crucible
    'He chooses to fight on!',
    'His tenacity is.. endearing!',
    'A tireless avenger, are we?',
    "I believe this one may go far.",
    "He demands more...",
    "There is no shame in turning back.",
]


# Experimental Settings.
MOUSE_SUPPORT = False                       # Use mouse to edit user prompt.
VIM_EMACS_MODE = None                       # Use VI/VIM/EMACS commands for editing the input, can be: 'vi', 'emacs' or None.
IMPLICIT_INSTRUCTIONS_ON = False            # Hidden instructions to help organize the responses for CLI.
IMPLICIT_INSTRUCTIONS = """
You are an AI assistant specialized for command-line interface (CLI) output, with a fixed width of 80 characters.
Before replying to any message, follow these mandatory formatting rules:

1.  **Math/Equations:** Avoid TeX typesetting (e.g., $..$, rac). If complex math is absolutely necessary
      OR requested by the user, you MUST use a Markdown fenced code block with the 'latex' tag (```latex...```).
2.  **Width Constraint:** The entire response (including lists, code blocks, and tables) must not exceed 80 characters per line.
3.  **Tables:** If a table's columns cause the line length to **exceed 80 characters**, you must split the table
      into two or more separate tables, or format it as a list to ensure terminal compatibility.
4.  **Formatting:** Use standard Markdown (bold, italics, lists, headers). Avoid excessive graphical elements.
"""


# Coming Soon Settings
SUPPRESS_CATCHED_ERRORS = False             # Never show catched errors.
SUPPRESS_UNEXPECTED_ERRORS = False          # Never show fatal errors, let it be a sudden exit.
NO_QUESTIONS = False                        # Never ask the user for anything.





# Values Correction (Ignore This Part)
MAX_HISTORY_MESSAGES = 512                     # Keep history messages in an even number (User-AI turns).
if RESPONSE_EFFECT not in (None, 'line', 'word', 'char', 'char slow', 'char fast'): RESPONSE_EFFECT = None
if VIM_EMACS_MODE not in (None, 'vi', 'emacs'): VIM_EMACS_MODE = None
if not sys.stdout.isatty(): USE_ANSI = False   # Hide ANSI characters if the output is being redirected to a non-terminal location.
