import os
import io
import ast
import shutil
import tokenize
import traceback
import questionary
from settings import USER_DATA_DIR, TEMP_PROMPT_FILE


# ==========================================
# 1. STARTUP CHECK
# ==========================================
SETTINGS_FILE = 'settings.py'
BACKUP_FILE = SETTINGS_FILE + '.bak'
BACKUP_PATH = os.path.abspath(os.path.join(USER_DATA_DIR, BACKUP_FILE))

if not os.path.exists(SETTINGS_FILE):
    print(f"\n[!] File '{SETTINGS_FILE}' not found!\n[!] Quitting...")
    quit(1)


# ==========================================
# 2. CONFIGURATION
# ==========================================
# Adding/removing a list of options, means editing load_menu() function & ALL_SETTINGS variable.
# Define exactly what you want to be able to edit in each SETTINGS list.
# - 'key': The variable name in settings.py
# - 'desc': A friendly description to show in the menu
# - 'default': The default value for that option.
# - 'type': 'bool', 'select', 'text', 'integer' 'decimal'
# - 'options': A list of choices (only required if type is 'select')

SPACE = '\n' + ' ' * 13   # Used instead of tab inside settings descriptions.

PRIVACY_SETTINGS = [
    {
        'key': 'MAX_HISTORY_MESSAGES',
        'desc': 'Maximum N° of chat history turns to keep; set it low to save' + SPACE +
                'RPM/TPM limits, internet bandwidth & loading/saving time.' + SPACE +
                '* (1) turn = Your message + AI response.' + SPACE +
                '* RPM: Requests Per Minute.' + SPACE +
                '* TPM: Tokens Per Minute.' + SPACE +
                '* Set it to (0) if you want Gemini to forget every message' + SPACE +
                '  immediately.\n',
        'default': '48',
        'type': 'integer',
    },
    {
        'key': 'NO_HISTORY_LIMIT',
        'desc': 'When True, chat history will never be truncated.',
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'PROMPT_HISTORY_MODE',
        'desc': "Your prompts will be saved to history, allowing you to reuse'em" + SPACE +
                "quickly in future chat sessions (Use UP/DOWN keys); options:" + SPACE +
                "- permanent: it'll be saved to a file, auto-shrinked to a fixed" + SPACE +
                "  size at exit, and manually cleared using /del-prompt command." + SPACE +
                "- temporary: it'll be saved in momory only; so it gets cleared" + SPACE +
                "  on each exit." + SPACE +
                "- None: to not save it al all.\n",
                
        'default': 'permanent',
        'type': 'select',
        'options': ['None','temporary', 'permanent'],
    },
    {
        'key': 'SAVED_INFO',
        'desc': "If True, your prompt will be saved with highest priority" + SPACE +
                "if you start it with /remember (Use /forget to delete it).\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'LOAD_CHAT_MODE',
        'desc': "Whether to load or forget chat history at startup; options:" + SPACE +
                "- 'ask' to always ask you." + SPACE +
                "- 'load' to always load last chat without asking." + SPACE +
                "- 'forget' to always forget last chat without asking.\n",
        'default': 'load',
        'type': 'select',
        'options': ['ask', 'load', 'forget'],
    },
    {
        'key': 'ERROR_LOG_ON',
        'desc': "To log errors to a file; console output won't be affected." + SPACE +
                "* Not to brag, but this will make unexpected errors messages" + SPACE +
                "  more friendly." + SPACE +
                "* Personal files paths are not logged for privacy." + SPACE +
                "* Can be cleared with /del-log command.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'GLOBAL_LOG_ON',
        'desc': "To log the entire console output to a file + optionally hidden" + SPACE +
                "debugging info; it gets cleared on each launch; visual console" + SPACE +
                "output won't be affected." + SPACE +
                "* Your prompts won't be logged for privacy." + SPACE +
                "* Auto-cleared; or manually with /del-log command.\n",
        'default': 'False',
        'type': 'bool',
    },
]

GENERAL_SETTINGS = [
    {
        'key': 'GEMINI_API_KEY',
        'desc': 'Your Google API key; you can get it easily from:\n             '
                'https://aistudio.google.com/app/api-keys\n',
        'default': 'YOUR_API_KEY_HERE (Just a placeholder)',
        'type': 'text',
    },
    {
        'key': 'GEMINI_MODEL',
        'desc': "The AI model to use; advanced models are more expensive and" + SPACE +
                "have less API limits. For more specific models, see the WIKI." + SPACE +
                "* (flash-lite) versions are the most generous." + SPACE +
                "* Suffix (latest) is an alias to the newest version." + SPACE +
                "* Models other than (2.5-flash-lite or 2.5-flash) may require" + SPACE +
                "  linking a billing account even for the Free Tier! So fallback" + SPACE +
                "  to (gemini-2.5-flash-lite) if you face issues.\n",
        'default': 'gemini-2.5-flash-lite',
        'type': 'select',
        'options': ['gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-flash-latest', 'gemini-flash-lite-latest', 'gemini-pro-latest'],
    },  
    {
        'key': 'ENTER_NEW_LINE',
        'desc': 'If True, Enter inserts a new line, and Esc-Enter submits;' + SPACE +
                'if False, Enter submits, and Esc-Enter inserts a new line.\n',
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'INFORMATIVE_RPROMPT',
        'desc': "Short informational text at top right of the prompt field." + SPACE +
                "* Might cause glitches in terminals that resize dynamically.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'BOTTOM_TOOLBAR',
        'desc': "Show a handy bottom toolbar for a quick reference." + SPACE +
                "* Might cause glitches with CTRL-C.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'SUGGEST_FROM_HISTORY_MODE',
        'desc': "Use your prompt history for inline word completion; options:" + SPACE +
                "- normal: for normal completion; so if your text matches an old" + SPACE +
                "  prompt, you'll see the completion." + SPACE +
                "- flex: this mode is more forgiving & case-insensitive, using" + SPACE +
                "  past words instead of the whole prompts." + SPACE +
                "- None: to disable inline completion." + SPACE +
                "* Require (PROMPT_HISTORY_MODE) to be ON." + SPACE +
                "* Press RIGHT arrow (->) to confirm suggestions." + SPACE +
                "* If you encounter lag, disable it.\n",
        'default': 'None',
        'type': 'select',
        'options': ['None', 'normal', 'flex'],
    },
    {
        'key': 'SUGGEST_FROM_WORDLIST_MODE',
        'desc': "Suggest words while typing, in a menu popup, based on a wordlist" + SPACE +
                "file (Default file: word_suggestion.txt); options:" + SPACE +
                "- normal: accurate suggestions." + SPACE +
                "- fuzzy: more forgiving; you get approximate suggestions instead" + SPACE +
                "  of accurate ones." + SPACE +
                "- None: to disable wordlist suggestion." + SPACE +
                "* Press UP/DOWNB to choose a word, ESC to dismiss the menu." + SPACE +
                "* See (SUGGESTIONS_LIMIT) option.\n",
        'default': 'normal',
        'type': 'select',
        'options': ['None', 'normal', 'fuzzy'],
    },
    {
        'key': 'SUGGESTIONS_LIMIT',
        'desc': "The number of menu suggestions to show while typing a prompt.",
        'default': '5',
        'type': 'integer',
    },
    {
        'key': 'INPUT_HIGHLIGHT',
        'desc': 'Syntax highlighting language for your prompt.' + SPACE +
                'These are just the most common; for more, see' + SPACE +
                "the WIKI and look for your language alias.\n",
        'default': 'special',
        'type': 'select',
        'options': ['None', 'special', 'markdown', 'bash', 'diff', 'ini', 'python','c++',
                    'c#', 'java', 'yaml', 'sql', 'php', 'xml', 'html', 'javascript', 'css'],
    },
    {
        'key': 'RESPONSE_EFFECT',
        'desc': "Effect while displaying AI response; it can be:\n"
                "- None: for no animation.\n"
                "- line: for line-by-line animation (Recommended).\n"
                "- word: for word-by-word animation (Satisfying).\n"
                "- char: for an almost instant character-by-character animation.\n"
                "  (Safe, but may be unnoticeable)\n"
                "- char slow: for a smooth character-by-character animation.\n"
                "  (Safe, but really slow).\n"
                "- char fast: for a fast character-by-character animation; you should\n"
                "  check if this causes a high CPU usage in your computer (from Task\n" 
                "  Manager), if so, it is a waste of resources & energy, bad\n"
                "  choice for long responses, but still fine for short ones.\n"
                "* All 'char' animations can cause glitchs!'\n",
        'default': 'line',
        'type': 'select',
        'options': ['None', 'line', 'word', 'char', 'char slow', 'char fast'],
    },
    {
        'key': 'SPINNER',
        'desc': 'Shown while waiting for AI response; these are the simplest,' + SPACE +
                'for more, see the WIKI.\n',
        'default': 'line',
        'type': 'select',
        'options': ['line', 'dots', 'arc', 'point', 'circle', 'bounce', 'star'],
    },
    {
        'key': 'USE_COLORS',
        'desc': 'Enable terminal colors; better to disable this for old consoles.',
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'USE_ANSI',
        'desc': 'Once False, all ANSI escape codes (including colors) will be' + SPACE +
                'disabled (Recommended to be False for old consoles)\n',
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'ALWAYS_GUI_MODE',
        'desc': 'If True, GUI editor & markdown viewer will both be called' + SPACE +
                'automatically on each prompt/response.\n',
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'FUN_MODE',
        'desc': 'If True, you may see some clean jokes or funny statements while' + SPACE +
                'using the program. If False, everything becomes serious' + SPACE +
                "& professional, but boring (Good for adults) - and you'll lose" + SPACE +
                "access to some secrets (Use /secret command to find out)." + SPACE +
                '* Just for entertainment, no bad intentions.\n',
        'default': 'True',
        'type': 'bool',
    },
]

ADVANDED_SETTINGS = [
    {
        'key': 'DEV_MODE',
        'desc': "If True, you'll get access to the developper kit, like..." + SPACE +
                "(Shhh, it's secret); with also some bonuses, like an extended" + SPACE +
                "wordlist of suggestions & special hotkeys." + SPACE +
                '* Use /secret command while in chat to find out.\n',
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'STARTUP_API_CHECK',
        'desc': "Disable for a slightly faster loading, and for the ability to" + SPACE +
                "enter the chat offline.\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'FILE_COMPRESSION',
        'desc': "This will save tokens, but Gemini will pay less attention to" + SPACE +
                "details in your attached files.\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'TEXT_COMPRESSION',
        'desc': "Compress your prompt & save tokens by shortening it." + SPACE +
                "E.g: AI will understand 'Hi, prblm app...' instead of 'Hello" + SPACE +
                "there Gemini, I have this problem in my app...'" + SPACE +
                "* True = ON, False = OFF." + SPACE +
                "* This will remove stop words & replace long expressions with" + SPACE +
                "  shortcuts, causing a little bit of inaccuracy." + SPACE +
                "* If OFF, your text will never be compressed unless you use" + SPACE +
                "  /compress command" + SPACE +
                "* If ON, your text will always be compressed unless you use" + SPACE +
                "  /no-compress command (E.g: to keep important messages intact).\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'COMPRESSION_LANGUAGE',
        'desc': "Whether (TEXT_COMPRESSION) is ON or you use /compress command," + SPACE +
                "this will be the default language used to compress your prompt." + SPACE +
                "* Choose a language code (e.g: ar -> Arabic); if you ever write" + SPACE +
                "  a prompt in a different language, no error will occur, but" + SPACE +
                "  no compression either.\n",
        'default': 'en',
        'type': 'select',
        'options': ['ar', 'bg', 'ca', 'cz', 'da', 'nl', 'en', 'fi', 'fr', 'de', 'hi', 'hu', 'id', 
                    'it', 'nb', 'pl', 'pt', 'ro', 'ru', 'sk', 'es', 'sv', 'tr', 'uk', 'vi']
    },
    {
        'key': 'MAX_CONSOLE_WIDTH',
        'desc': "Max N° of characters to print per line; only effective if the" + SPACE +
                "terminal size is bigger than this fixed value, otherwise it'll" + SPACE +
                "be automatically reduced to fit the terminal size." + SPACE +
                "* Should always be smaller than default terminal width.\n",
        'default': '85',
        'type': 'integer',
    },
    {
        'key': 'DYNAMIC_CONSOLE_WIDTH',
        'desc': "If True, console text width will be automatically updated upon" + SPACE +
                "a terminal size change, to fit in it.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'CASE_SENSITIVITY',
        'desc': "If True, commands like /copy must be in lower case to be executed." + SPACE +
                "If False, commands become more forgiving, so you can type" + SPACE +
                "/COPY or /CoPy instead of /copy.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'FILE_GENERATOR_MODEL',
        'desc': "The AI model used for file/image generation; 'lite' models" + SPACE +
                "won't work since they are weak.\n",
        'default': 'gemini-2.5-flash',
        'type': 'text',
    },
    {
        'key': 'VALIDATE_INPUT',
        'desc': "Check your prompt while typing & show warnings about its length." + SPACE +
                "* Should be False if it's slow or causes gliches.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'HIDE_LONG_INPUT',
        'desc': "If you submit a long prompt, its last half will be hidden to" + SPACE +
                "beautify & clean the CLI.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'SAVE_INPUT_ON_CLEAR',
        'desc': "Save your prompt to history when you clear it with Ctrl-C" + SPACE +
                "(If prompt-history is ON).\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'SAVE_INPUT_ON_STOP',
        'desc': "Save your prompt to history when you stop it with Ctrl-C" + SPACE +
                "or F-Keys (If prompt-history is ON).\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'EXTERNAL_EDITOR',
        'desc': "Allow you to edit your prompt in an external editor by pressing" + SPACE +
                "CTRL-X-CTRL-E in a row; or by using /external command." + SPACE +
                "* In case of any issue, your prompt is always saved to:" + SPACE +
               f"  '{TEMP_PROMPT_FILE}' in Gemini Py-CLI's directory." + SPACE +
                "* See (FAVORITE_EDITOR) option.\n",
        'default': 'True',
        'type': 'bool',
    },
    {
        'key': 'FAVORITE_EDITOR',
        'desc': "Full path for your favorite external editor used with" + SPACE +
                "CTRL-X-CTRL-E (For some editors, you don't need the full path);" + SPACE +
                "if not set, we'll fallback to default system editor (if any)." + SPACE +
                "* E.g: notepad, vim, nano, or:" + SPACE +
                "  'C:\\Program Files\\Notepad++\\notepad++.exe'." + SPACE +
                "* The editor must be closed for your prompt to be submitted." + SPACE +
                "  Also, you should avoid multi-tab editors.\n",
        'default': 'None',
        'type': 'text',
    }, 
    {
        'key': 'NO_ERROR_DETAILS',
        'desc': "If True, never ask you to see more details about an error." + SPACE +
                "* Error details will be skipped.\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'NO_QUESTIONS',
        'desc': "If True, never ask you about usual questions, and use a default." + SPACE +
                "option; e.g:" + SPACE +
                "- Pressing CTRL-C on an empty prompt will directly exit without" + SPACE +
                "  confirming." + SPACE +
                "- If an unhandled error occurs; we directly show details unless" + SPACE +
                "  you set (NO_ERROR_DETAILS) or (SUPPRESS_ERRORS) to True." + SPACE +
                "* That's the idea; save yourself a few clicks when possible.\n",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'SUPPRESS_ERRORS',
        'desc': "If True, never show sudden errors; but critical errors" + SPACE +
                "(that leads to exit) & normal errors (like disconnection)" + SPACE +
                "will still appear.\n",
        'default': 'False',
        'type': 'bool',
    },    
]

EXPERIMENT_SETTINGS = [
    {
        'key': 'MOUSE_SUPPORT',
        'desc': "Use the mouse to edit your prompt.",
        'default': 'False',
        'type': 'bool',
    },
    {
        'key': 'VIM_EMACS_MODE',
        'desc': "Use VI/VIM/EMACS commands for editing your prompt." + SPACE +
                "* E.g.1: For VIM mode, ESC-I is for insert mode; besides" + SPACE +
                "  navigation mode by pressing ESC + j or h, k, l." + SPACE +
                "* E.g.2: For EMACS mode, CTRL-A to go to line beginning," + SPACE +
                "  CTRL-E to move to end.\n",
        'default': 'None',
        'type': 'select',
        'options': ['vim', 'emacs', 'None'],
    },
    {
        'key': 'IMPLICIT_INSTRUCTIONS_ON',
        'desc': "If True, hidden instructions will be sent to AI to help in" + SPACE +
                "organizing its responses for CLI." + SPACE +
               f"* Instructions content is inside '{SETTINGS_FILE}'.\n",
        'default': 'False',
        'type': 'bool',
    },
]

ALL_SETTINGS = PRIVACY_SETTINGS + GENERAL_SETTINGS + ADVANDED_SETTINGS + EXPERIMENT_SETTINGS

DEFAULT_SETTINGS = {d['key']: d['default'] for d in ALL_SETTINGS}

separator_1 = """
   ┌────────────────────┐
   │ Privacy Settings   │
   └────────────────────┘
"""

separator_2 = """
   ┌────────────────────┐
   │ General Settings   │
   └────────────────────┘
"""

separator_3 = """
   ┌────────────────────┐
   │ Advanced Settings  │
   └────────────────────┘
"""

separator_4 = """
   ┌────────────────────┐
   │    Experimental    │
   └────────────────────┘
"""


# ==========================================
# 3. RUNTIME LOGIC
# ==========================================
def clear():
    """Just clear the screen."""
    # Use 'try' because this code is a bit slower.
    try: os.system('cls' if os.name == 'nt' else 'clear')
    except KeyboardInterrupt: pass

def restore_default():
    """Nuclear reset for user settings."""
    new_lines = file_lines.copy()
    
    for key, value in DEFAULT_SETTINGS.items():
        updated = False
        for i, line in enumerate(file_lines):
            clean_line = line.replace(' ', '').strip()
            if clean_line.startswith(f'{key}='):
                # Prepare the default value.
                try: value = ast.literal_eval(value)
                except: pass
                if str(value).lower() == 'none': default_value = None # Special case.
                else: default_value = repr(value)   # Required for strings, so 'hi' -> "'hi'".
                key_value = f'{key} = {default_value}'
                comment = organize_comment(line, key_value)

                # 2. Reconstruct the line.
                # "KEY = NEW_VALUE # Comment".
                new_lines[i] = f"{key_value}{comment}"
                break
    
    # Save.
    if new_lines != file_lines:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def check_default():
    """Return True if all of the variables in 'settings.py' are in their default state."""
    for name, default_value in DEFAULT_SETTINGS.items():
        # Get the current value of the variable in 'settings.py'.
        current_value = find_current_value(name)
        if current_value != default_value:
            return False
            
    return True

def save_change(key: str, new_value: any):
    """Finds the line with the key and replaces the value, keeping comments."""
    # Format the new value for Python (adds quotes to strings, etc).
    # repr() is perfect for this: True -> True, "hi" -> 'hi', 1 -> 1.
    if str(new_value).lower() == 'none': formatted_value = None # Special case.
    else: formatted_value = repr(new_value)
    
    # Start changing 'settings.py' content.
    new_lines = file_lines.copy()
    updated = False
    
    for i, line in enumerate(file_lines):
        clean_line = line.replace(' ', '').strip()
        if clean_line.startswith(f'{key}='):
            # We found the line.
            key_value = f'{key} = {formatted_value}'
            comment = organize_comment(line, key_value)

            # 2. Reconstruct the line.
            # "KEY = NEW_VALUE # Comment".
            new_lines[i] = f"{key_value}{comment}"
            updated = True
            break
    
    # Save.
    if updated:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def read_file_lines():
    """Read the file and return a list of lines."""
    if not os.path.exists(SETTINGS_FILE):
        print(f"[!] File '{SETTINGS_FILE}' not found!\n[!] Quitting...")
        quit(1)
    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
        return f.readlines()

def find_current_value(wanted_key: str):
    """
    Find the current value of a variable in the file lines.
    We only take the first definition to skip values correction inside 'settings.py'.
    """
    for line in file_lines:
        # Look for line starting with "KEY =".
        line = line.strip()
        if line.startswith(wanted_key):
            # We use 'try' in case of mal-syntax inside 'settings.py'.
            try:
                # Extract key-value parts.
                parts = line.split('=', 1)
                key_part = parts[0].strip()
                val_part = parts[1].strip()
                # If there is a comment, 'ast' will ignore it.
            except:
                continue
        
        else:
            continue
            
        if key_part == wanted_key:
            # Use ast to safely evaluate python literal (True, 123, 'string').
            try:
                value = ast.literal_eval(val_part)
                return str(value)
            except:
                return val_part

def organize_comment(code: str, key_value: str):
    """
    A simple function to separate comments from key-value pairs.
    Especially if the value is a string containing '#'.
    """
    # Find the comment.
    tokens = tokenize.generate_tokens(io.StringIO(code).readline)

    comment = next(
        (tok.string for tok in tokens if tok.type == tokenize.COMMENT),
        None
    )
    
    # Keep comment, but beautify the code with a fixed distance.
    if comment:
        space = 45 - len(key_value)
        if space < 4: space = 60 - len(key_value)
        if space < 4: space = 75 - len(key_value)
        comment = ' ' * space + comment + '\n'  # Keep the comment.
    else:
        comment = '\n' # Just a newline.

    return comment

def list_settings(main_list: list, settings_list: list, separator: str):
    """
    Take a list of settings, organize them as questionary choices, and add
    them to the main list.
    * main_list will be passed a reference & edited directly.
    """
    main_list.append(questionary.Separator(separator.strip()))
    for item in settings_list:
        key = item['key']
        current_val = find_current_value(key)
        # Format: "VARIABLE_NAME  [Current Value]".
        main_list.append(questionary.Choice(
            title=f"{key:<26} [{current_val}]",
            value=key,
        ))

def load_menu():
    """Prepare the menu of options to show.""" 
    choices = []
    
    # Editor options.
    choices.append(questionary.Choice('< README >', value='README'))
    if check_default(): choices.append(questionary.Choice('RESET DEFAULT SETTINGS', value='DEFAULT', disabled='Already in default'))
    else: choices.append(questionary.Choice('< RESET DEFAULT SETTINGS >', value='DEFAULT'))
    choices.append(questionary.Choice('< EXIT >', value='EXIT'))
    
    # Main settings.
    list_settings(choices, PRIVACY_SETTINGS, separator_1)
    list_settings(choices, GENERAL_SETTINGS, separator_2)
    list_settings(choices, ADVANDED_SETTINGS, separator_3)
    list_settings(choices, EXPERIMENT_SETTINGS, separator_4)
    
    # End.
    choices.append(questionary.Separator('─' * 22))
    choices.append(questionary.Choice('END OF SETTINGS', value='END', disabled=True))
    choices.append(questionary.Choice('< EXIT >', value='EXIT'))
    return choices

def main():
    """You know... main."""
    # Backup first.
    global file_lines
    shutil.copy(SETTINGS_FILE, BACKUP_PATH)
    
    # Style.
    style = questionary.Style([
        ('qmark', 'fg:#00FFFF bold'),       # Question mark color/style.
        ('question', 'cyan bold'),          # Question text color/style.
        ('selected', 'fg:black bg:yellow bold'), # Selected item in lists.
        ('disabled', 'fg:#666666 italic'),  # For disabled choices.
        ('pointer', 'fg:cyan bold'),        # Selection pointer (e.g., the '>' symbol).
        ('instruction', 'fg:#999999'),      # Instructions text.
    ])
    
    last_selected_key = None
    while True:
        # 1. Main screen.
        clear()
        print('┌' + '─' * 58 + '┐')
        print(f"│{' ' * 13} Simple Editor for '{SETTINGS_FILE}'{' ' * 13}│")
        print('└' + '─' * 58 + '┘\n')
        
        # 2. Load settings & Show menu.
        file_lines = read_file_lines()
        choices = load_menu()
    
        selected_key = questionary.select(
            message='Select a setting to change:',
            choices=choices,
            default=last_selected_key,
            style=style,
            qmark='⚙️',
            pointer='>',
            use_arrow_keys=True,
            use_emacs_keys=True,
            mouse_support=True,
            use_search_filter=True,
            show_selected=True,
            use_shortcuts=False,
            use_indicator=False,
            show_description=False,
            use_jk_keys=False,
        ).ask()
        
        last_selected_key = selected_key
        
        # 3. Handle special options.
        if selected_key == 'README':
            print("\n♦ You can always press (CTRL-C) to cancel anything.\n")
            print("♦ Remember, this editor lacks some options.")
            print("  For some settings, choices are limited to the most common.")
            print(f"  For more control, edit '{SETTINGS_FILE}' directly.\n")
            print(f"♦ Remember that you always have a backup in:")
            print(f"  {BACKUP_PATH}")
            print("  You only need to remove the '.bak' suffix from its name.\n")
            print('♦ For a quick reference about verbose settings, visit the WIKI:')
            print('  https://github.com/Mohyoo/Gemini-Py-CLI/wiki/Settings\n')
            try: input("  Press Enter to continue...")
            finally: continue
        
        if selected_key == 'DEFAULT':
            clear()
            reminder = f"\n♦ You'll always have '{BACKUP_FILE}' in case of any issue, but...\n"
            print(reminder)
            choices = ["Yes, I'm sorry to mess with the settings...", "No, just checking the buttons...", "I don't know..."]
            answer = questionary.select(
                'Are you sure you want to reset all settings to default?',
                choices=choices,
                qmark='⚙️',
                pointer='>',
                style=style,
                default=choices[1],
            ).ask()
            
            if answer == choices[0]:
                clear()
                print(reminder)
                choices = ["Yes, certainly!", "No, just checking the buttons again...", "I still don't know..."]
                answer = questionary.select(
                    'Double check, still sure?',
                    choices=choices,
                    qmark='⚙️',
                    pointer='>',
                    style=style,
                    default=choices[1],
                ).ask()
                
                if answer == choices[0]:
                    if restore_default():
                        print(f"\n[✓] All settings have been reset to default.")
                        last_selected_key = None    # Because reset option is now locked.
                    else:
                        print(f"\n[✗] Could not reset settings!")
                        
                    try: input("    Press Enter to continue...")
                    finally: pass
                    
            continue
        
        if selected_key in ['EXIT', None]:  # None in case of CTRL-C.
            if selected_key == 'EXIT': print()
            print(f"♦ Remember that you always have a backup in:")
            print(f"  {BACKUP_PATH}")
            print("  You only need to remove the '.bak' suffix from its name.\n")
            print("♦ Goodbye!")
            exit()

        # 4. Find the config for selected item.
        config = next(c for c in ALL_SETTINGS if c['key'] == selected_key)
        current_val = find_current_value(selected_key)
        
        print(f"\nEditing: {selected_key}")
        print(f"Description: {config['desc']}")
        print(f"Default Value: {config['default']}")
        print(f"Current Value: {current_val}")
        
        # 5. Get Input based on type.
        new_val = None
        print()
        
        try:
            if config['type'] == 'bool':
                choices = ['True', 'False', '< Cancel >']
                default = current_val if current_val in choices else None
                new_val = questionary.select(
                    f"Set [{selected_key}] to:",
                    choices=choices,
                    pointer='>',
                    qmark='◊',
                    style=style,
                    default=default,
                ).ask()
                
                if new_val in['< Cancel >', None]: continue
                new_val = (new_val == 'True')

            elif config['type'] == 'select':
                choices = config['options'] + ['< Cancel >']
                default = current_val if current_val in choices else None
                new_val = questionary.select(
                    f"Choose an option:",
                    pointer='>',
                    qmark='◊',
                    choices=choices,
                    style=style,
                    default=default,
                ).ask()
                
                if new_val in['< Cancel >', None]: continue

            elif config['type'] in ['text', 'integer', 'decimal']:
                new_val = questionary.text(
                    f"Enter value:",
                    default=current_val,
                    qmark='>',
                    style=style
                ).ask()
                
                if new_val is None or not new_val.strip(): continue
                new_val = new_val.strip()
                
                if config['type'] in ['integer', 'decimal']:
                    # Remove chars & extra dots.
                    new_val = ''.join([c for c in new_val if c.isdigit() or c == '.'])
                    dot = new_val.find('.')
                    if dot != -1: new_val = new_val[:dot + 1] + new_val[dot + 1:].replace('.', '')
                    if not new_val.strip(): continue
                    
                    # Convert to a number.
                    new_val = float(new_val)
                    if new_val == int(new_val) or config['type'] == 'integer':
                        new_val = int(new_val)
                
            # 6. Save.
            if str(new_val) == current_val:
                print(f"\n[!] Same value, no need to save.")
            elif save_change(selected_key, new_val):
                print(f"\n[✓] Saved: {selected_key} = {new_val}")
            else:
                print(f"\n[✗] Could not find variable in '{SETTINGS_FILE}' file!")
                
            try: input("    Press Enter to continue...")
            finally: continue

        except KeyboardInterrupt:
            continue
        
        except Exception:
            print('\n' + '─' * 60)
            traceback.print_exc()
            print('─' * 60)
            try: input("Press Enter to continue...")
            finally: continue
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("\nExiting Settings Editor...")