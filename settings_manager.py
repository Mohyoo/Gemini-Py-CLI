import os
import shutil
import ast
import questionary

# ==========================================
# 1. CONFIGURATION (EDIT THIS LIST!)
# ==========================================
# Define exactly what you want to be able to edit here.
# - 'key': The variable name in settings.py
# - 'desc': A friendly description to show in the menu
# - 'type': 'bool', 'select', or 'text'
# - 'options': A list of choices (only required if type is 'select')

MANAGED_SETTINGS = [
    {
        'key': 'GEMINI_MODEL',
        'desc': 'The AI Model to use',
        'type': 'select',
        'options': ['gemini-2.5-flash', 'gemini-pro', 'gemini-1.5-pro', 'gemini-ultra']
    },
    {
        'key': 'MAX_HISTORY_MESSAGES',
        'desc': 'Max number of messages in memory',
        'type': 'text'  # Treats input as text, but tries to convert to number
    },
    {
        'key': 'RESPONSE_EFFECT',
        'desc': 'Animation style for AI response',
        'type': 'select',
        'options': ['None', 'line', 'word', 'char', 'char slow', 'char fast']
    },
    {
        'key': 'USE_COLORS',
        'desc': 'Enable terminal colors',
        'type': 'bool'
    },
    {
        'key': 'USE_ANSI',
        'desc': 'Use ANSI escape codes (True for modern terminals)',
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
    {
        'key': 'GEMINI_API_KEY',
        'desc': 'Your Google API Key',
        'type': 'text'
    }
]

FILE_PATH = 'settings.py'
BACKUP_PATH = 'settings.py.bak'

# ==========================================
# 2. SIMPLE LOGIC
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
                comment = ' #' + parts[1] # Keep the comment
            else:
                comment = '\n' # Just a newline

            # 2. Reconstruct the line
            # "KEY = " + "NEW_VALUE" + " # Comment"
            new_lines.append(f"{key} = {formatted_value}{comment}")
            updated = True
        else:
            new_lines.append(line)

    if updated:
        shutil.copy(FILE_PATH, BACKUP_PATH) # Backup first
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        lines = read_file_lines()
        
        # 1. Prepare Menu Choices
        choices = []
        for item in MANAGED_SETTINGS:
            current_val = find_current_value(lines, item['key'])
            # Format: "VARIABLE (Current: value) - Description"
            choices.append(questionary.Choice(
                title=f"{item['key']:<25} [{str(current_val)}]  -- {item['desc']}",
                value=item['key']
            ))
            
        choices.append(questionary.Separator())
        choices.append(questionary.Choice("Exit", value="EXIT"))

        # 2. Show Menu
        print(f"--- Simple Editor for {FILE_PATH} ---")
        selected_key = questionary.select(
            "Select a setting to change:",
            choices=choices,
            use_shortcuts=False
        ).ask()

        if selected_key == "EXIT" or selected_key is None:
            print("Goodbye!")
            break

        # 3. Find the config for selected item
        config = next(c for c in MANAGED_SETTINGS if c['key'] == selected_key)
        current_val = find_current_value(lines, selected_key)
        
        print(f"\nEditing: {selected_key}")
        print(f"Description: {config['desc']}")
        print(f"Current Value: {current_val}")
        
        # 4. Get Input based on type
        new_val = None
        
        try:
            if config['type'] == 'bool':
                new_val = questionary.select(
                    f"Set {selected_key} to:",
                    choices=['True', 'False', '< Cancel >']
                ).ask()
                if new_val == '< Cancel >': continue
                new_val = (new_val == 'True')

            elif config['type'] == 'select':
                opts = config['options'] + ['< Cancel >']
                new_val = questionary.select(
                    f"Choose value:",
                    choices=opts
                ).ask()
                if new_val == '< Cancel >': continue
                if new_val == 'None': new_val = 'None' # Handle None string

            elif config['type'] == 'text':
                new_val = questionary.text(f"Enter value:", default=str(current_val)).ask()
                if new_val is None: continue
                # Try converting to number if it looks like one
                if new_val.isdigit(): new_val = int(new_val)
                elif new_val.replace('.','',1).isdigit(): new_val = float(new_val)
                
            # 5. Save
            if save_change(selected_key, new_val):
                print(f"\n[✓] Saved {selected_key} = {new_val}")
                input("Press Enter to continue...")
            else:
                print("\n[!] Could not find variable in file.")
                input("Press Enter...")

        except KeyboardInterrupt:
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")