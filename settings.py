# When editing this, respect each option's possible values, otherwise prepare yourself for a crash).
# Coming Soon Settings
SUPPRESS_CATCHED_ERRORS = False             # Not yet implemented
SUPPRESS_UNEXPECTED_ERRORS = False          # Not yet implemented

# General Settings
GEMINI_API_KEY = 'YOUR_API_KEY_HERE'
GEMINI_MODEL = 'gemini-2.5-flash'           # Advanced models are more expensive and have less API limits.
ENTER_NEW_LINE = False                      # Enter inserts a new line, and Esc-Enter submits; if False,
                                                # Enter submits, and Esc-Enter insets a new line.
WORD_SUGGESTION = True                      # Suggest words while typing in a menu popup.
SUGGEST_FROM_HISTORY = False                # Use the user's prompt history for inline word completion (SLOW).
USE_COLORS = True                           # Better to disable it for old consoles.
NO_ERROR_DETAILS = False                    # Never ask the user to see more details about an error.
INFORMATIVE_RPROMPT = True                  # Short informational text at top right of the prompt field.
BOTTOM_TOOLBAR = True                       # Show a handy toolbar for a quick reference.
RESPONSE_EFFECT = 'line'                    # Effect while displaying response, can be:
                                                # None for no animation.
                                                # 'line' for line-by-line animation (Recommended).
                                                # 'word' for word-by-word animation (Satisfying).
                                                # 'char' for an almost instant character-by-character animation (Safe, but may be unnoticeable).
                                                # 'char slow' for a smooth character-by-character animation (Safe to use, but really slow).
                                                # 'char fast' for a fast character-by-character animation; you should check if this causes a high CPU usage in your computer
                                                # (from Task Manager), if so, it is a waste of resources & energy, bad choice for long responses, but still fine for short ones.

# Advanced Settings
CONSOLE_WIDTH = 80                          # How many characters to print per line (Should be >= Console window).
SUGGESTIONS_LIMIT = 5                       # The number of suggestions to show while typing a prompt.
SPINNER = 'dots'                            # Shown while waiting, can be: dots, line, bounce, moon, star, runner... (In CMD type 'python -m rich.spinner' for more).
VIM_EMACS_MODE = None                       # Use VI/VIM/EMACS commands for editing the input, can be: 'vi', 'emacs' or None.
STARTUP_API_CHECK = False                   # Disable for a slightly faster loading.
SAVE_INPUT_ON_CLEAR = False                 # Save the prompt to history when the user clears its prompt with Ctrl-C.
SAVE_INPUT_ON_QUIT = False                  # Save the prompt to history when the user stops its prompt with Ctrl-C.
WORDLIST_FILE = 'word_suggestion.txt'       # A small wordlist used for word suggestion.
CHAT_HISTORY_FILE = 'chat_history.json'     # To load chat history (If available).
PROMPT_HISTORY_FILE = 'prompt_history.txt'  # To load prompt history (If available).
PROMPT_HISTORY_SIZE = 0.5 * 1024 * 1024     # Max prompt hisotory size (1024 * 1024 = 1 MB)
SERVER_ERROR_ATTEMPTS = 3                   # How many times to try to get a response upon a server error.
SERVER_ERROR_DELAY = (3, 5)                 # 1st to wait upon first error, then 2nd for next errors.
HTTP_TIMEOUT = (2.5, 5)                     # 1st to establish the initial connection, 2nd is for the entire request.
STATUS_UPDATE_DELAY = (1, 3)                # (Integers only) Fake random delay to update the status shown while waiting for response (Doesn't add extra delays, all safe).
IMPLICIT_INSTRUCTIONS_ON = False            # Hidden instructions to help organize the responses for CLI.
IMPLICIT_INSTRUCTIONS = """
    You are an AI assistant specialized for command-line interface (CLI) output, with a fixed width of 80 characters.
    Before replying to any message, follow these mandatory formatting rules:
    
    1.  **Math/Equations:** Avoid TeX typesetting (e.g., $..$, \frac). If complex math is absolutely necessary OR requested by the user, you MUST use a Markdown fenced code block with the 'latex' tag (```latex...```).
    2.  **Width Constraint:** The entire response (including lists, code blocks, and tables) must not exceed 80 characters per line.
    3.  **Tables:** If a table's columns cause the line length to **exceed 80 characters**, you must split the table into two or more separate tables, or format it as a list to ensure terminal compatibility.
    4.  **Formatting:** Use standard Markdown (bold, italics, lists, headers). Avoid excessive graphical elements.
"""
SLEEP_INTERVAL = 0.1                        # Small chunks used as intervals with sleeping functions, to keep UI responsive.

# Colors
if USE_COLORS:
    # By ANSI code (Used in print() & cprint())
    CYN     = '\033[96m'    # Cyan
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
    CYN = RED = GR = YLW = BL = UL = BD = RS = GEM_BG = ''
    PROMPT_BG = PROMPT_FG = WAIT_1 = WAIT_2 = 'white'
