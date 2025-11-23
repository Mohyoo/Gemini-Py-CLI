import os
import ast
import shutil
import questionary

# ==========================================
# 1. CONFIGURATION
# ==========================================
# Define exactly what you want to be able to edit here.
# - 'key': The variable name in settings.py
# - 'desc': A friendly description to show in the menu
# - 'type': 'bool', 'select', 'text' or 'digit'.
# - 'options': A list of choices (only required if type is 'select')

MANAGED_SETTINGS = [
    {
        'key': 'GEMINI_API_KEY',
        'desc': 'Your Google API key; you can get it easily from:\n             https://aistudio.google.com/app/api-keys\n',
        'type': 'text'
    },
    {
        'key': 'GEMINI_MODEL',
        'desc': 'The AI model to use; advanced models are more expensive and have less API limits.',
        'type': 'select',
        'options': ['gemini-2.5-flash', 'gemini-pro', 'gemini-1.5-pro', 'gemini-ultra']
    },
    {
        'key': 'MAX_HISTORY_MESSAGES',
        'desc': 'Maximum number of chat history messages to keep; keep it low to save internet bandwidth & loading/saving time.',
        'type': 'digit'
    },    
    {
        'key': 'ENTER_NEW_LINE',
        'desc': 'If True, Enter inserts a new line, and Esc-Enter submits;\n             '
                'if False, Enter submits, and Esc-Enter inserts a new line.\n',
        'type': 'bool'
    },
    {
        'key': 'RESPONSE_EFFECT',
        'desc': "Effect while displaying AI response; it can be:\n"
                "\t- 'None' for no animation.\n"
                "\t- 'line' for line-by-line animation (Recommended).\n"
                "\t- 'word' for word-by-word animation (Satisfying).\n"
                "\t- 'char' for an almost instant character-by-character animation.\n\t"
                "  (Safe, but may be unnoticeable)\n"
                "\t- 'char slow' for a smooth character-by-character animation\n\t"
                "  (Safe, but really slow)."
                "\n\t- 'char fast' for a fast character-by-character animation; you should\n\t"
                "  check if this causes a high CPU usage in your computer (from Task\n\t" 
                "  Manager), if so, it is a waste of resources & energy, bad\n\t"
                "  choice for long responses, but still fine for short ones.\n"
                "\t* All 'char' animations can cause glitchs!'\n",
        'type': 'select',
        'options': ['None', 'line', 'word', 'char', 'char slow', 'char fast']
    },
    {
        'key': 'USE_COLORS',
        'desc': 'Enable terminal colors; better to disable this for old consoles.',
        'type': 'bool'
    },
    {
        'key': 'USE_ANSI',
        'desc': 'Once False, all ANSI escape codes (including colors) will be\n             '
                'disabled (Recommended to be False for old consoles)\n',
        'type': 'bool'
    },
    {
        'key': 'INPUT_HIGHLIGHT_LANG',
        'desc': 'Syntax highlighting language for input',
        'type': 'select',
        'options': ['python', 'javascript', 'html', 'markdown', 'text']
    },
    {
        'key': 'SPINNER',
        'desc': 'Loading animation style',
        'type': 'select',
        'options': ['line', 'dots', 'bounce', 'moon', 'star', 'monkey']
    },
]

FILE_PATH = 'settings.py'
BACKUP_PATH = 'settings.py.bak'
if not os.path.exists(FILE_PATH):
    print(f"\n[!] File '{FILE_PATH}' not found!\n[!] Quitting...")
    quit()

# ==========================================
# 2. RUNTIME LOGIC
# ==========================================

def read_file_lines():
    """Reads the file and returns a list of lines."""
    if not os.path.exists(FILE_PATH):
        print(f"Error: {FILE_PATH} not found!")
        exit()
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        return f.readlines()

def find_current_value(lines, key):
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

def save_change(key, new_value):
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
            # 1. Split into [Variable=Value, Comment]
            if '#' in line:
                parts = line.split('#', 1)
                space = 45 - len(f'{key} = {formatted_value}')
                if space < 4: space = len(f'{key} = {formatted_value}') + 15
                comment = ' ' * space + '#' + parts[1] # Keep the comment
            else:
                comment = '\n' # Just a newline

            # 2. Reconstruct the line
            # "KEY = " + "NEW_VALUE" + " # Comment"
            new_lines.append(f"{key} = {formatted_value}{comment}")
            updated = True
        else:
            new_lines.append(line)

    if updated:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    # Backup first.
    shutil.copy(FILE_PATH, BACKUP_PATH)
    
    # Style.
    style = questionary.Style([
        ('qmark', 'fg:#00FFFF bold'),     # Question mark color/style
        ('question', 'bold'),             # Question text color/style
        ('selected', 'fg:#673AB7'),       # Selected item in lists
        ('pointer', 'fg:cyan bold'),      # Selection pointer (e.g., the '>' symbol)
        ('instruction', 'fg:#999999'),    # Instructions text
    ])
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        lines = read_file_lines()
        
        # 1. Prepare Menu Choices
        choices = []
        for item in MANAGED_SETTINGS:
            current_val = find_current_value(lines, item['key'])
            # Format: "VARIABLE (Current: value) - Description"
            choices.append(questionary.Choice(
                title=f"{item['key']:<25} [{str(current_val)}]",
                value=item['key']
            ))
            
        choices.append(questionary.Separator())
        choices.append(questionary.Choice("< Exit >", value="EXIT"))

        # 2. Show Menu
        print(f"{'-' * 24} Simple Editor for {FILE_PATH} {'-' * 24}")
        print('♦ You can always press CTRL-C to cancel anything.\n')
        
        selected_key = questionary.select(
            "Select a setting to change:",
            choices=choices,
            use_shortcuts=False,
            qmark="⚙️",
            style=style,
        ).ask()

        if selected_key == "EXIT" or selected_key is None:
            if selected_key == "EXIT": print()
            print(f"♦ Remember that you have '{BACKUP_PATH}' as a backup.")
            print("♦ You only need to remove the '.bak' suffix from its name.")
            print("♦ Goodbye!")
            break

        # 3. Find the config for selected item
        config = next(c for c in MANAGED_SETTINGS if c['key'] == selected_key)
        current_val = find_current_value(lines, selected_key)
        
        print(f"\nEditing: {selected_key}")
        print(f"Description: {config['desc']}")
        print(f"Current Value: {current_val}")
        
        # 4. Get Input based on type
        new_val = None
        print()
        
        try:
            if config['type'] == 'bool':
                new_val = questionary.select(
                    f"Set {selected_key} to:",
                    choices=['True', 'False', '< Cancel >'],
                    qmark='◊',
                    style=style,
                ).ask()
                if new_val == '< Cancel >': continue
                new_val = (new_val == 'True')

            elif config['type'] == 'select':
                opts = config['options'] + ['< Cancel >']
                new_val = questionary.select(
                    f"Choose a value:",
                    qmark='◊',
                    choices=opts,
                    style=style,
                ).ask()
                if new_val == '< Cancel >': continue

            elif config['type'] in ['text', 'digit']:
                new_val = questionary.text(
                    f"Enter value:",
                    default=str(current_val),
                    qmark='>',
                    style=style
                ).ask()
                
                if new_val is None: continue
                if config['type'] == 'digit':
                    new_val = ''.join([c for c in new_val if c.isdigit()])
                    new_val = float(new_val)
                    if new_val == int(new_val): new_val = int(new_val)
                    if new_val is None: continue
                
            # 5. Save
            if save_change(selected_key, new_val):
                print(f"\n[✓] Saved: {selected_key} = {new_val}")
            else:
                print("\n[!] Could not find variable in file.")
                
            try: input("    Press Enter to continue...")
            except: pass

        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")