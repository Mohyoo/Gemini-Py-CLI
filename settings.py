# When editing this, respect each option's possible values, otherwise prepare yourself
# for a crash (Better to keep a backup of this file).
# If you are confused with some settings, try 'settings_editor.py' or visit the wiki:
# https://github.com/Mohyoo/Gemini-Py-CLI/wiki/Settings
# You can always ask in my GitHub page, or even request a future change. I'll try hard to
# keep everything easily accessible.

import os
import sys

# General Settings
GEMINI_API_KEY = 'YOUR_API_KEY_HERE'
GEMINI_MODEL = 'gemini-flash-latest'         # Advanced models are more expensive and have less API limits.
MAX_HISTORY_MESSAGES = 512                   # The maximum number of chat history messages to keep; saves internet bandwidth & loading/saving time.
NO_HISTORY_LIMIT = False                     # When True, chat history will never be truncated.
ENTER_NEW_LINE = False                       # If True, Enter inserts a new line, and Esc-Enter submits; if False, Enter submits, and Esc-Enter inserts a new line.
SUGGEST_FROM_HISTORY = False                 # Use the user's prompt history for inline word completion (SLOW).
SUGGEST_FROM_WORDLIST = True                 # Suggest words while typing, in a menu popup, based on a wordlist.
SUGGEST_FROM_WORDLIST_FUZZY = False          # This completion mode is more forgiving, you get approximate suggestions instead of accurate ones.
SUGGESTIONS_LIMIT = 5                        # The number of suggestions to show while typing a prompt.
PROMPT_HISTORY_ON = True                     # Every user prompt is saved to a file and can be quickly reused in future chats.
PROMPT_HISTORY_MEMORY = False                # If True, prompt history will be saved in momory only, rather than in a file.
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
ALWAYS_LOAD_CHAT = True                      # If True, chat history will be always loaded without asking you.
STARTUP_API_CHECK = False                    # Disable for a slightly faster loading, and for the ability to enter the chat offline.
MAX_CONSOLE_WIDTH = 85                       # Max N° characters to print per line, only effective if the terminal size is bigger than this fixed value, should always be < terminal width.
DYNAMIC_CONSOLE_WIDTH = True                 # If True, console width will be automatically updated upon a terminal size change.
INPUT_HIGHLIGHT = 'special'                  # Syntax highlighting for the user prompt; 'special' is our built-in option, but 'python' may also be a good option.
SAVE_INPUT_ON_CLEAR = False                  # Save the prompt to history when the user clears its prompt with Ctrl-C.
SAVE_INPUT_ON_STOP = False                   # Save the prompt to history when the user stops its prompt with Ctrl-C or F-Keys.
EXTERNAL_EDITOR = True                       # Allow you to edit your prompt in an external editor by pressing CTRL-X-CTRL-E in a row.
FAVORITE_EDITOR = None                       # Full path for your favorite extrernal editor; if not set, fallback to default system editor.
                                                # E.g: 'notepad', 'vim' or 'C:\Program Files\Notepad++\notepad++.exe'.
NO_ERROR_DETAILS = False                     # Never ask the user to see more details about an error.
ERROR_LOG_ON = True                          # To log errors to a file, console output won't be affected.
GLOBAL_LOG_ON = True                         # To log the entire console output to a file + optionally hidden debugging info,
                                                 # it gets cleared on each launch; visual console output won't be affect.


# Advanced Settings
SAVED_INFO_FILE = 'saved_info.txt'           # To save important informations at user request.
LAST_RESPONSE_FILE = 'last_response.txt'     # To save last Gemini response in a text file.
WORDLIST_FILE = 'word_suggestion.txt'        # A small wordlist used for word suggestion.
CHAT_HISTORY_JSON = 'chat_history.json'      # To save/load chat history to/from a json file (If available).
CHAT_HISTORY_TEXT = 'chat_history.txt'       # To save chat history as a simple text file (If available).
ERROR_LOG_FILE = 'application_errors.log'                  # The file to write errors to (Level: warning, error, critical).
GLOBAL_LOG_FILE = 'application_console_output.log'         # The file to write the entire console output to + optionally hidden debug info (Level: debug, info).
PROMPT_HISTORY_FILE = 'prompt_history.txt'   # To load prompt history (If available).
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
    # By ANSI code (Used in print() & cprint()).
    CYN     = '\033[96m'    # Cyan
    RED     = '\033[91m'    # Red
    GR      = '\033[92m'    # Green
    YLW     = '\033[93m'    # Yellow
    YLW2    = '\033[33m'    # Gray Yellow
    BL      = '\033[94m'    # Blue
    GRY     = '\033[90m'    # Gray
    PURP    = '\033[35m'    # Purple
    BRW     = '\033[31m'    # Brown
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
    CYN = RED = GR = YLW = YLW2 = BL = GRY = PURP = BRW = UL = BD = RS = GEM_BG = ''
    PROMPT_BG = PROMPT_FG = WAIT_1 = WAIT_2 = 'white'


# Custom Messages
FAREWELLS_MESSAGES = [      # Messages displayed upon existing.
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
    "Bibbidi Bobbidi Boo!",
    "Artryoos. Metryoos. Zeetoos!",
    "¡Nos vemos, cocodrilo!\n(See you, crocodile :P)",
    "¡Hasta la vista!\n(See you around :D)",
    "Au revoir!",
    "Cya!",
    "Ciao! I'm outta here faster than an Italian pizza disappearing at a party.",
    f"Whoa there, easy! He just ended the chat, no need to panic...\nBUT WAIT... AAAAARGHHH...!!!\n"
    f"{RED}System Rage Error occurred!{RS}{GR} Catch you later!",
    "Ladies & Gentlemen, we are closing.",
    "Just a quick fake cleanup...\nOK, all done!",
    "Okay ladies, time to go home.",
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
    "Cleaning crime scene...\nAlright! ready to escape.",
    "Normal mode OFF, switching to Agent Six...",
    "There'll be no mercy next time, I promise...",
    "Let's celebrate a party just for no reason!",
    "Don't look back, you've been warned! >:)",
    "Goodbye! Don't forget to miss me a little.",
    "Goodbye! I’ll try not to miss you… too much ;-;",
    "Farewell! Remember, the door is always open - just don’t forget to close it behind you.",
    "Adios! May your life be as awesome as you pretend it is on social media.",
    "Farewell! May your future be as bright as your phone screen v.v",
    "Goodbye! Now you’re free to make all the bad decisions you’ve been planning >.>",
    "Good luck! If the new place doesn’t work out, you can always come back and pretend you never left ;)",
    "We have a winner! Ahuh.. I meant a dinner!",
    
    # Enthusiastic
    "Keep coding and stay curious!\n(If you aren't a developer, ignore this, you owe me a coffee)",
    "May your logic be sound and your keys be clean.",
    "Go forth and query, friend.",
    "I'll be here. You know where to find me.",
    "Enjoy the silence...",
    "Until our paths cross again.",
    "Stay curious, stay connected.",
    "Farewell, may the consequences be ever in your favor.",
    "Ce sont les mots que j'aime dans un chat! Au revoir!",
    "I will stay here... if you ever turn back.",
    "Sometimes it's too difficult, yet.. still feasible ;)",
    "Keep it up gentleman, the world needs your work.",
    "The waves are calling.. Captain.",
    "Every step, no matter how small, moves you forward ;)",
    "Ok enough playing, time to study.",
    
    # Serious
    "Remember to commit your changes!",
    "Don't forget to save your work!",
    "Bye Bye! Check your API key status if you run into trouble.",
    f"Thank you for using Gemini Py-CLI! Suggestions are welcome!\nGitHub Home: "
    f"{UL}https://github.com/Mohyoo/Gemini-Py-CLI{RS}",
    f"If you faced any issues, please let me know, I'll try to reply quickly.\n"
    f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}",
]
 
CONTINUE_MESSAGES = [       # Messages displayed upon confirming exit or editing sensitive stuff (saved-info...), but the user chooses NO.
    # Standard
    'Resuming chat...',
    'Cancelling, chat will continues.',
    
    # Funny
    'Acting blind...',
    "Don't just mess with the keyboard next time.",
    "Can you just stop doing that?",
    'Oof...',
    'Hmmm...',
    'Oops...',
    'Whoopsie!',
    'Interesting...',
    'I smell doubt...',
    'I can feel something bad is coming...',
    'Nevermind...',
    'Aha! wait.. what were we talking about?',
    'Exit failed successfully.',
    'This is a messing around...',
    'Back from the dead.',
    'Yowza! nice move.',
    
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


# Experimental Settings
MOUSE_SUPPORT = False                       # Use mouse to edit user prompt.
VIM_EMACS_MODE = None                       # Use VI/VIM/EMACS commands for editing the input, can be: 'vim', 'emacs' or None.
                                                # E.g.1: For VIM mode, ESC-I is for insert mode; beside navigation mode by pressing ESC + j or h, k, l.
                                                # E.g.2: For EMACS mode, Ctrl+A to go to line beginning, Ctrl+E to move to end.
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
NO_QUESTIONS = False                        # Never ask the user for anything, and use the default option.
SERIOUS_MODE = False                        # No jokes; everything becomes serious & boring. Good for old people.


# Hotkeys
    # Hard & Confusing; For now, I honestly don't know how to explain them.
    # The original format for combinations (i.e: pressed at once) is 'key1-key2', but since the library I use 'prompt_toolkit'
    # doen't provide so many keys & combinations, I had to use custom lists like (key1, key2) for combinations.
    # The problem is, the format (key1, key2) in my code can also represent (2) separated keys that can be pressed
    # individually to do the same job.
    # See (https://github.com/Mohyoo/Gemini-Py-CLI/wiki/Settings) to see all available hotkeys.
    
class Hotkeys():
    if ENTER_NEW_LINE:
        SUBMIT = ('escape', 'enter')                                # Press ESCAPE-ENTER at once.
        NEW_LINE = ('enter', 'c-space', 's-tab', 'c-j')             # Press either ENTER or CTRL-SPACE or SHIFT-TAB or CTRL-J.
    else:
        SUBMIT = ('enter',)                                         # Press ENTER alone, or ENTER-KEY2 if available.
        NEW_LINE = (('escape', 'enter'), 'c-space', 's-tab', 'c-j') # Press ESCAPE-ENTER or CTRL-SPACE or SHIFT-TAB or CTRL-J.
    
    CANCEL = 'escape'               # Press ESC.
    TAB = 'tab'                     # Press TAB.
    UNDO = 'c-z'                    # Press CTRL-Z at once.
    REDO = 'c-y'                    # Press CTRL-Y at once.
    COPY = 'c-a'                    # Press CTRL-A at once.
    INTERRUPT = ('c-c', 'c-d')      # Press CTRL-C or CTRL-D.
    # F_KEYS here is a dictionary of 'F' key to press & its fellow 'command' (commands are listed in the help menu).
    F_KEYS = {'f1': 'show', 'f2': 'copy', 'f3': 'restart', 'f4': 'quit', 'f5': 'discard', 'f6': 'kill', 'f7': 'help'}


# Values Correction (Ignore This Part)
MAX_HISTORY_MESSAGES = MAX_HISTORY_MESSAGES // 2        # Keep history messages an even number (User-AI turns).
console_width = min(MAX_CONSOLE_WIDTH, os.get_terminal_size().columns - 1)    # The current console width must always be <= MAX_CONSOLE_WIDTH < real terminal size.
if RESPONSE_EFFECT not in (None, 'line', 'word', 'char', 'char slow', 'char fast'): RESPONSE_EFFECT = None
if VIM_EMACS_MODE not in (None, 'vim', 'emacs'): VIM_EMACS_MODE = None
if INPUT_HIGHLIGHT == 'None': INPUT_HIGHLIGHT = None
if not USE_ANSI: USE_COLORS = False
if not USE_COLORS: INPUT_HIGHLIGHT = None
if not sys.stdout.isatty(): USE_ANSI = False            # Hide ANSI characters if the output is being redirected to a non-terminal location.
