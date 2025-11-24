import os
import ast
import shutil
import questionary
from typing import Any

# ==========================================
# 2. STARTUP CHECK
# ==========================================

FILE_PATH = 'settings.py'
BACKUP_PATH = 'settings.py.bak'

if not os.path.exists(FILE_PATH):
    print(f"\n[!] File '{FILE_PATH}' not found!\n[!] Quitting...")
    quit()


# ==========================================
# 2. CONFIGURATION
# ==========================================
# Define exactly what you want to be able to edit here.
# - 'key': The variable name in settings.py
# - 'desc': A friendly description to show in the menu
# - 'type': 'bool', 'select', 'text' or 'digit'
# - 'options': A list of choices (only required if type is 'select')

SPACE = ' ' * 13        # Used instead of tab inside settings descriptions.

GENERAL_SETTINGS = [
    {
        'key': 'GEMINI_API_KEY',
        'desc': 'Your Google API key; you can get it easily from:\n             '
                'https://aistudio.google.com/app/api-keys\n',
        'type': 'text'
    },
    {
        'key': 'GEMINI_MODEL',
        'desc': 'The AI model to use; advanced models are more expensive and\n' + SPACE +
                'have less API limits. These are aliases to the latest versions\n' + SPACE +
                'For more specific models, see the WIKI.\n',
        'type': 'select',
        'options': ['gemini-flash-latest', 'gemini-flash-lite-latest', 'gemini-pro-latest']
    },
    {
        'key': 'MAX_HISTORY_MESSAGES',
        'desc': 'Maximum N° of chat history messages to keep; set it low\n' + SPACE +
                'to save internet bandwidth & loading/saving time.\n',
        'type': 'digit'
    },
    {
        'key': 'NO_HISTORY_LIMIT',
        'desc': 'When True, chat history will never be truncated.',
        'type': 'bool'
    },     
    {
        'key': 'ENTER_NEW_LINE',
        'desc': 'If True, Enter inserts a new line, and Esc-Enter submits;\n' + SPACE +
                'if False, Enter submits, and Esc-Enter inserts a new line.\n',
        'type': 'bool'
    },
    {
        'key': 'SAVED_INFO',
        'desc': "If True, your prompt will be saved with highest priority\n" + SPACE +
                "if you start it with 'remember'.\n",
        'type': 'bool',
    },
    {
        'key': 'INFORMATIVE_RPROMPT',
        'desc': "Short informational text at top right of the prompt field.",
        'type': 'bool',
    },
    {
        'key': 'BOTTOM_TOOLBAR',
        'desc': "Show a handy bottom toolbar for a quick reference.",
        'type': 'bool',
    },
    {
        'key': 'SUGGEST_FROM_HISTORY',
        'desc': "Use your prompt history for inline word completion (SLOW).",
        'type': 'bool'
    },
    {
        'key': 'SUGGEST_FROM_WORDLIST',
        'desc': "Suggest words while typing, in a menu popup, based on a wordlist\n" + SPACE +
                "file (Default file: word_suggestion.txt).\n",
        'type': 'bool'
    },
    {
        'key': 'SUGGESTIONS_LIMIT',
        'desc': "The number of menu suggestions to show while typing a prompt.",
        'type': 'digit'
    },
    {
        'key': 'INPUT_HIGHLIGHT',
        'desc': 'Syntax color highlighting for your prompt.',
        'type': 'bool',
    },
    {
        'key': 'INPUT_HIGHLIGHT_LANG',
        'desc': 'Syntax highlighting language for your prompt.\n' + SPACE +
                'These are just the most common, for more, see\n' + SPACE +
                "the WIKI and look for your language alias.\n",
        'type': 'select',
        'options': ['markdown', 'bash', 'diff', 'ini', 'python', 'c++', 'c#', 'java', 'yaml', 'sql', 'php', 'xml', 'html', 'javascript', 'css']
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
        'type': 'select',
        'options': ['None', 'line', 'word', 'char', 'char slow', 'char fast']
    },
    {
        'key': 'SPINNER',
        'desc': 'Shown while waiting for AI response; these are the simplest,\n' + SPACE +
                'for more, see the WIKI.\n',
        'type': 'select',
        'options': ['line', 'dots', 'arc', 'point', 'circle', 'bounce', 'star']
    },
    {
        'key': 'USE_COLORS',
        'desc': 'Enable terminal colors; better to disable this for old consoles.',
        'type': 'bool'
    },
    {
        'key': 'USE_ANSI',
        'desc': 'Once False, all ANSI escape codes (including colors) will be\n' + SPACE +
                'disabled (Recommended to be False for old consoles)\n',
        'type': 'bool'
    },
]

ADVANDED_SETTINGS = [
    {
        'key': 'STARTUP_API_CHECK',
        'desc': "Disable for a slightly faster loading, and for the ability to\n" + SPACE +
                "enter the chat offline.\n",
        'type': 'bool'
    },
    {
        'key': 'CONSOLE_WIDTH',
        'desc': "N° of characters to print per line (Should be < Console window).\n" + SPACE +
                "(79) may be the best for old consoles.\n",
        'type': 'digit'
    },
    {
        'key': 'NO_ERROR_DETAILS',
        'desc': "True = Never ask you to see more details about an error.",
        'type': 'bool'
    },
    {
        'key': 'ERROR_LOG_ON',
        'desc': "To log errors to a file, console output won't be affected.",
        'type': 'bool'
    },
    {
        'key': 'GLOBAL_LOG_ON',
        'desc': "To log the entire console output to a file + optionally hidden\n" + SPACE +
                "debugging info, it gets cleared on each launch; visual console\n" + SPACE +
                "output won't be affect.\n",
        'type': 'bool'
    },
    {
        'key': 'SAVE_INPUT_ON_CLEAR',
        'desc': "Save your prompt to history when you clear it with Ctrl-C.",
        'type': 'bool'
    },
    {
        'key': 'SAVE_INPUT_ON_STOP',
        'desc': "Save your prompt to history when you stop it with Ctrl-C\n" + SPACE +
                "or F-Keys.\n",
        'type': 'bool'
    },
]

separator_1 = """
   +--------------------+
   | General Settings   |
   +--------------------+
"""

separator_2 = """
   +--------------------+
   | Advanced Settings  |
   +--------------------+
"""

# ==========================================
# 3. RUNTIME LOGIC
# ==========================================

def read_file_lines():
    """Reads the file and returns a list of lines."""
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found!")
        exit()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return f.readlines()

def find_current_value(lines: list, key: str):
    """Finds the current value of a variable in the file lines."""
    for line in lines:
        # Look for line starting with "KEY =" or "KEY="
        clean_line = line.strip()
        if clean_line.startswith(f"{key}=") or clean_line.startswith(f"{key} ="):
            # Extract value part (everything after the first =)
            parts = clean_line.split('=', 1)
            val_part = parts[1].strip()
            
            # Remove inline comments if they exist
            if '#' in val_part:
                val_part = val_part.split('#')[0].strip()
                
            # Use ast to safely evaluate python literal (True, 123, 'string')
            try:
                return ast.literal_eval(val_part)
            except:
                return val_part
    return "Not Found"

def save_change(key: str, new_value: Any):
    """Finds the line with the key and replaces the value, keeping comments."""
    lines = read_file_lines()
    new_lines = []
    updated = False

    # Format the new value for Python (adds quotes to strings, etc.)
    # repr() is perfect for this: True -> True, "hi" -> 'hi', 1 -> 1
    formatted_value = repr(new_value)
    if new_value == 'None': formatted_value = 'None' # Special case

    for line in lines:
        clean_line = line.strip()
        if clean_line.startswith(f"{key}=") or clean_line.startswith(f"{key} ="):
            # We found the line.
            key_value = f'{key} = {formatted_value}'
            # 1. Split into [Variable=Value, Comment]
            if '#' in line:
                parts = line.split('#', 1)
                space = 45 - len(key_value)
                if space < 4: space = 60 - len(key_value)
                if space < 4: space = 75 - len(key_value)
                comment = ' ' * space + '#' + parts[1] # Keep the comment
            else:
                comment = '\n' # Just a newline

            # 2. Reconstruct the line
            # "KEY = " + "NEW_VALUE" + " # Comment"
            new_lines.append(f"{key_value}{comment}")
            updated = True
        else:
            new_lines.append(line)

    if updated:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def load_menu(lines: list):
    """Prepare the menu of options to show."""    
    # Readme option.
    choices = []
    choices.append(questionary.Choice(
        title='< README >',
        value='README',
        # disabled=True
    ))
    choices.append(questionary.Separator(separator_1.strip()))
    
    # General settings.
    for item in GENERAL_SETTINGS:
        current_val = find_current_value(lines, item['key'])
        # Format: "VARIABLE - Current Value"
        choices.append(questionary.Choice(
            title=f"{item['key']:<26} [{str(current_val)}]",
            value=item['key']
        ))
        
    choices.append(questionary.Separator(separator_2.strip()))
    
    # Advanced settings.
    for item in ADVANDED_SETTINGS:
        current_val = find_current_value(lines, item['key'])
        # Format: "VARIABLE - Current Value"
        choices.append(questionary.Choice(
            title=f"{item['key']:<26} [{str(current_val)}]",
            value=item['key']
        ))
    
    # Exit option.
    choices.append(questionary.Separator('=' * 22))
    choices.append(questionary.Choice("< EXIT >", value="EXIT"))
    
    return choices

def main():
    # Backup first.
    shutil.copy(FILE_PATH, BACKUP_PATH)
    
    # Style.
    style = questionary.Style([
        ('qmark', 'fg:#00FFFF bold'),       # Question mark color/style
        ('question', 'cyan bold'),          # Question text color/style
        ('selected', 'fg:black bg:yellow bold'), # Selected item in lists
        ('pointer', 'fg:cyan bold'),        # Selection pointer (e.g., the '>' symbol)
        ('instruction', 'fg:#999999'),      # Instructions text
    ])
    
    last_selected_key = None
    while True:
        # 1. Main screen.
        os.system('cls' if os.name == 'nt' else 'clear')
        print('=' * 79)
        print(f"{' ' * 23} Simple Editor for '{FILE_PATH}'")
        print('=' * 79 + '\n')

        # 2. Show Menu
        lines = read_file_lines()
        choices = load_menu(lines)
        
        selected_key = questionary.select(
            "Select a setting to change:",
            choices=choices,
            use_shortcuts=True,
            qmark="⚙️",
            style=style,
            default=last_selected_key,
        ).ask()
        
        # 3. Handle special options.
        if selected_key == 'README':
            print()
            print("♦ You can always press (CTRL-C) to cancel anything.\n")
            print("♦ Remember, this editor is for general options.")
            print("  For some settings, choices are limited to the most common.")
            print("  For more control, edit 'settings.py' directly.\n")
            print('♦ For a quick reference about verbose settings, visit the WIKI:')
            print('  https://github.com/Mohyoo/Gemini-Py-CLI/wiki/Settings\n')
            try: input("  Press Enter to continue...")
            finally: continue
            
        if selected_key == "EXIT" or selected_key is None:
            if selected_key == "EXIT": print()
            print(f"♦ Remember that you have '{BACKUP_PATH}' as a backup.")
            print("♦ You only need to remove the '.bak' suffix from its name.")
            print("♦ Goodbye!")
            break

        # 4. Find the config for selected item
        config = next(c for c in GENERAL_SETTINGS + ADVANDED_SETTINGS if c['key'] == selected_key)
        current_val = find_current_value(lines, selected_key)
        
        print(f"\nEditing: {selected_key}")
        print(f"Description: {config['desc']}")
        print(f"Current Value: {current_val}")
        
        # 5. Get Input based on type
        new_val = None
        print()
        
        try:
            if config['type'] == 'bool':
                last_selected_key = selected_key
                choices = ['True', 'False', '< Cancel >']
                default = str(current_val) if str(current_val) in choices else None
                new_val = questionary.select(
                    f"Set {selected_key} to:",
                    choices=choices,
                    qmark='◊',
                    style=style,
                    default=default,
                ).ask()
                
                if new_val in['< Cancel >', None]: continue
                new_val = (new_val == 'True')

            elif config['type'] == 'select':
                last_selected_key = selected_key
                choices = config['options'] + ['< Cancel >']
                default = str(current_val) if str(current_val) in choices else None
                new_val = questionary.select(
                    f"Choose a value:",
                    qmark='◊',
                    choices=choices,
                    style=style,
                    default=default,
                ).ask()
                
                if new_val in['< Cancel >', None]: continue

            elif config['type'] in ['text', 'digit']:
                last_selected_key = selected_key
                new_val = questionary.text(
                    f"Enter value:",
                    default=str(current_val),
                    qmark='>',
                    style=style
                ).ask()
                
                if new_val is None or not str(new_val).strip(): continue
                if config['type'] == 'digit':
                    new_val = ''.join([c for c in new_val if c.isdigit()])
                    new_val = float(new_val)
                    if new_val == int(new_val): new_val = int(new_val)
                    if new_val is None: continue
                
            # 6. Save
            if save_change(selected_key, new_val):
                print(f"\n[✓] Saved: {selected_key} = {new_val}")
            else:
                print(f"\n[!] Could not find variable in '{FILE_PATH}' file.")
                
            try: input("    Press Enter to continue...")
            finally: continue

        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\nExiting Settings Editor...")