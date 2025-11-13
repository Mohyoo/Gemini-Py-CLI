# 1) Part I: Initialization ----------------------------------------------------
# Loading Screen
print('\n' + '+' + '-' * 78 + '+')
print("| Loading libraries. Just a moment..." + ' ' * 42 + '|')
print('+' + '-' * 78 + '+')

# Import Statements
try:
    import os
    import sys
    import re
    import math
    import httpx
    import httpcore
    import textwrap
    import traceback
    import json
    from random import choice
    from time import sleep
    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.formatted_text import FormattedText
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.history import InMemoryHistory, FileHistory
    from google import genai
    from google.genai.errors import APIError
    from google.genai.types import Content, Part
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    
except Exception as error:
    print(f'\nError: {error}.')
    print("Use 'pip' to install missing modules.")
    print("E.g: open CMD & type: pip install httpx rich")
    quit(1)
    
except (KeyboardInterrupt, EOFError):
    quit(0)

# Settings Constants
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
GEMINI_MODEL = "gemini-2.5-flash"     # Advanced models are more expensive and have less API limits.
STARTUP_API_CHECK = False             # Disable for a slightly faster loading.
CHAT_HISTORY_FILE = "chat_history.json"     # To load chat history (If available)
PROMPT_HISTORY_FILE = 'prompt_history.txt'  # To load prompt history (If available)
PROMPT_HISTORY_SIZE = 1 * 1024 * 1024       # Max prompt hisotory size (1024 * 1024 = 1 MB)
USE_COLORS = True                     # Better to disable it for old consoles.
IMPLICIT_INSTRUCTIONS_ON = False      # Hidden instructions to help organize the responses for CLI.
IMPLICIT_INSTRUCTIONS = """
    You are an AI assistant specialized for command-line interface (CLI) output, with a fixed width of 80 characters.
    Before replying to any message, follow these mandatory formatting rules:
    
    1.  **Math/Equations:** Avoid TeX typesetting (e.g., $..$, \frac). If complex math is absolutely necessary OR requested by the user, you MUST use a Markdown fenced code block with the 'latex' tag (```latex...```).
    2.  **Width Constraint:** The entire response (including lists, code blocks, and tables) must not exceed 80 characters per line.
    3.  **Tables:** If a table's columns cause the line length to **exceed 80 characters**, you must split the table into two or more separate tables, or format it as a list to ensure terminal compatibility.
    4.  **Formatting:** Use standard Markdown (bold, italics, lists, headers). Avoid excessive graphical elements.
"""
HTTP_TIMEOUT = (3, 6)                # 1st to establish the initial connection, 2nd is for the entre request.

# Coming Soon Settings:
SUPPRESS_CATCHED_ERRORS = False      # Not yet implemented
SUPPRESS_UNEXPECTED_ERRORS = False   # Not yet implemented
ENTER_TO_SEND = False                # Not yet implemented
CONSOLE_WIDTH = 80                   # Not yet implemented
NO_ERROR_DETAILS = False             # Never ask the user to see more details about an error

# Global Variables (Do not change!)
confirm_separator = True             # Before confirming to quit, either print a separator or not.
history = FileHistory(PROMPT_HISTORY_FILE)

# Keyboard Shortcuts for user inputclass Keys():
key_bindings = KeyBindings()
class Keys():
    submit = 'enter'
    new_line = 'c-space'

@key_bindings.add(Keys.submit, eager=True)
def _(event):
    """
    Submits the input immediately.
    'eager=True' ensures this binding takes precedence.
    """
    event.cli.current_buffer.validate_and_handle()

@key_bindings.add(Keys.new_line)
def _(event):
    """Inserts a newline character."""
    event.cli.current_buffer.insert_text('\n')
  

# Colors
if USE_COLORS:
    CYN     = "\033[96m"    # Cyan
    RED     = "\033[91m"    # Red
    GR      = "\033[92m"    # Green
    YLW     = "\033[93m"    # Yellow
    BL      = "\033[94m"    # Blue
    GEM_BG  = "\033[44m"    # Dark Blue background for Gemini.
    UL      = "\033[4m"     # Underline
    BD      = "\033[1m"     # Bold
    RS      = "\033[0m"     # Reset
    PROMPT_BG  = 'cyan'
else:
    CYN = RED = GR = YLW = BL = GEM_BG = UL = BD = RS = ''
    PROMPT_BG  = 'white'

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
    f"Okay okay, calm down, he only ended the chat...\nBUT AAAAARGHHH...!!!\n{RED}System Rage Error occurred;{RS}{GR} Cya!",
    "Ladies & Gentlemen, we are closing.",
    "Just a quick fake cleanup...\nOK, all done!",
    "Okay ladies, time to go home.",
    "Artryoos. Metryoos. Zeetoos!",
    "Remember, it's all about: Hakuna Matata!\n(No Worries :)",
    "Ma chère mademoiselle, it is with deepest pride and greatest pleasure that we\nproudly present... The End.",
    "¡Ándale! ¡Ándale! ¡Arriba! ¡Arriba! Yeehaw!",
    "Tactical retreat. We'll be back.",
    "Shadow Fleeing Jutsu!",
    "Together for a better world (Where I'm the boss).",
    "Finally, some peace of mind...",
    "Good, I was in no mood for chat already.",
    
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
    
    # Serious
    "Remember to commit your changes!",
    "Don't forget to save your work!",
    "Bye Bye! Check your API key status if you run into trouble.",
    f"Thank you for using Gemini Py-CLI! Suggestions are welcome!\nGitHub Home: {UL}https://github.com/Mohyoo/Gemini-Py-CLI{RS}",
    f"If you faced any issues, please let me know, I'll try to reply quickly.\nGitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}",
]  
CONTINUE_MESSAGES = [
    # Messages displayed upon confirming exit, but the user chooses NO.
    'You chooses to fight on!',
    'Resuming chat...',
    'Acting blind...',
    'Cancelling, chat will continues.',
    "Don't just mess with the keyboard nex time.",
    'Oof...',
    'Yeah, this is ma boi!',
    'Your tenacity is endearing!',
    'We have tireless avenger here.',
]







# 2) Part II: Error Handlers --------------------------------------------------
NetworkExceptions = (
    IOError,
    httpx.HTTPError,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
    httpcore.RemoteProtocolError,
    httpcore.ConnectError,
)

Interruption = (
    KeyboardInterrupt, 
    EOFError,
)

def catch_api_error_startup(error):
    msg_1 = f"{RED}API Error occurred:\n{RED}{error.message}.\n"
    msg_2 = f"{RED}Please check your API key validation or limits."
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}(Remember that it requires a google account)\n"
    msg_5 = f"{GR}Showing the quick help menu...{RS}"
    box(msg_1, msg_2, msg_3, msg_4, msg_5, title='API ERROR', border_color=RED, secondary_color=RED)

def catch_api_error_in_chat(error):
    msg_1 = f"{RED}API Error occurred:\n{RED}{error.message}.\n"
    msg_2 = f"{YLW}Please check your API key limits, or wait for sometime."
    msg_3 = f"{YLW}Restarting the program might also help."
    box(msg_1, msg_2, msg_3, title='API ERROR', border_color=RED, secondary_color=RED)

def catch_server_error_in_chat():
    global confirm_separator
    confirm_separator = False
    separator('\n', color=RED)
    cprint(f"{RED}A temporary server problem occurred.")
    cprint(f'It might be a service overloading, maintenance or backend errors...')
    print_status(lambda: sleep(5), 'Retrying in 5 seconds...', 'yellow')
    
    response = None
    for attempt in range(5):
        try:
            response = get_response()
            cprint(GR + 'Response received!' + RS)
            break
            
        except genai.errors.ServerError:
            if attempt >= 4:
                cprint(YLW + 'Tried 5 times with no response! Please wait for sometime...' + RS)
                response = None
                break
                
            print_status(lambda: sleep(10), 'Issue persisting, trying again in 10 seconds...', 'yellow')
            continue
            
    confirm_separator = True
    separator(color=RED)
    return response

def catch_network_error():
    msg = f"{RED}Failed to connect, check your network or firewall!{RS}"
    box(msg, title='NETWORK ERROR', border_color=RED)

def catch_exception_in_chat(error):
    global confirm_separator
    separator('\n', color=RED)
    log_error(f"An error occurred:\n'{error}'")
    try:
        see_error = input(f"See the details? (y/n) ").strip().lower()
    except Interruption:
        confirm_separator = False
        cprint()
        raise
    
    if see_error == 'y':
        cprint(RED + traceback.format_exc().strip() + RS)
    else:
        cprint(f"{GR}Acting blind...{RS}")
        
    separator(color=RED)

def catch_fatal_exception(error):
    separator('\n', color=RED)
    cprint(f"{GR + BD}Congratulations! You found it. It's a BUG!")
    cprint(f"To be honest, I'm really sorry for that.")
    cprint(f"Please let me know, I'll try to respond as soon as possible.")
    cprint(f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}\n")
    
    log_error(f"A fatal error occurred:\n'{error}'\nAnd the program has to QUIT.")
    see_error = input("See the details? (y/n) ").strip().lower()
    
    if see_error == 'y':
        cprint(RED + traceback.format_exc().strip() + RS)
        clean_output()
        separator(color=RED)
    else:
        cprint(f"{YLW}\nInhales.. Deep breathing.. Now out.{RS}")
        separator(color=RED)
    
    save_chat_history()
    sys.exit(1)

def catch_keyboard_interrupt():
    msg_1 = f"{GR}Prompt cancelled, skipping..."
    msg_2 = f'{GR}Rest assured, Gemini has no idea about what you just sent.'
    box(msg_1, msg_2, title='KEYBOARD INTERRUPTION', border_color=GR)







# 3) Part III: Helper Functions -------------------------------------------------
def cprint(text='', end='\n', wrap=True):
    """
    A custom print function that writes directly to stdout and guarantees 
    an immediate display by forcing a flush.
    """
    # Wrap (79 so that '\n' stays in the same line)
    text = str(text)
    if len(text) > 79 and wrap:
        lines = text.split('\n')
        wrapped_lines = []
        
        for line in lines:
            if not line.strip():
                wrapped_lines.append(' ')
                continue
                
            new_lines = textwrap.wrap(line, width=79)
            wrapped_lines.extend(new_lines)
            
        text = '\n'.join(wrapped_lines)
    
    # Print
    sys.stdout.write(text + end)
    sys.stdout.flush()

def print_status(action, text='Waiting...', color='green'):
    """Display a vital text so that the program doesn't feel stuck."""
    with console.status(f"[bold {color}]{text}[/bold {color}]"):
        action()

def log_error(text, style='red', offset=3):
    """
    Display a special message for erros, including time and line.
    
    1) '_stack_offset' argument tells 'Rich' to look further up the call stack
       to find the true originator of the log message. Default to (3): from this
       log_error() -> catch_error_name() -> except statement (what we want).
       
    2) Using quotes inside quotes (e.g: "''") will give the internal quotes
       a special color.
    """
    cprint(RS, end='')
    console.log(text, style=style, _stack_offset=offset, end='\n\n')

def clean_output(lines_to_erase=1):
    """
    Simulates scanning and cleaning up previous empty lines by using 
    ANSI codes to move the cursor up and erase, then prints a separator.
    """
    # \033[A:  Move cursor Up one line
    # \033[2K: Erase the entire current line
    ERASE_LINE_UP = "\033[A\033[2K"
    
    for _ in range(lines_to_erase):
        cprint(ERASE_LINE_UP, end='')

def separator(before='', after='', char='─', color='', width=80, end='\n'):
    """Display a line of hyphens."""
    # Used console.print() instead of print() and our defined cprint(), because
    # others have an issue of printing double new line after.
    console.print(color + before + char * width + after + RS,
                  end=end, no_wrap=True, soft_wrap=True, overflow='ignore')

def visual_len(text_with_ansi):
    """Returns the visible length of a string, ignoring ANSI codes."""
    ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')
    return len(ANSI_ESCAPE.sub('', text_with_ansi))

def box(*texts, title='Message', border_color='', text_color='', secondary_color='', width=80):
    """
    Draw a box using standard ASCII characters, respecting ANSI colors inside.
    
    Limitations:
    - Each passed string must have its own colors, and not depend on the
      continuous colors from the previous line.
    - ANSI code must not be in the wrap point, as it'll get broken and useless.
    - Wrapped lines will lose their colors! thus 'secondary_color' is an
      optional argument that gets applied only to the wrapped lines.
    - ANSI reset code isn't necessary at the end of string.
    - You have to rewrite ANSI code after '\n' inside strings.
    - ANSI code length is considered as normal characters when wrapping a line.
    """
    # Calculate text length & Subtract borders space.
    content_width = width - 4
    
    # Merge texts
    message = '\n'.join(texts)
    
    # Define colors:
    BC = border_color    # For the box borders
    TC = text_color      # If the content has its colors, this will be overwritten.
    SC = secondary_color # Only for wrapped lines.
    
    # Wrap text to fit
    wrapped = []
    for line in message.splitlines():
        if not line.strip():
            wrapped.append(' ')
            continue
            
        # Apply secondary color to wrapped lines
        wrapped_lines = textwrap.wrap(line, content_width)
        for index, line in enumerate(wrapped_lines):
            if index == 0: continue
            wrapped_lines[index] = SC + line
            
        wrapped.extend(wrapped_lines)
        
    # Header
    cprint()
    top = BC + '┌' + '─' * (content_width + 2) + '┐'
    title_line = top.replace('─' * (content_width + 2), f' {title} '.center(content_width + 2, '─'))
    cprint(title_line + RS, wrap=False)
    
    # Content Lines
    for line in wrapped:
        line_visual_len = visual_len(line)
        padding = ' ' * (content_width - line_visual_len)
        cprint(f'{BC}│{RS} {TC}{line}{padding} {BC}│{RS}', wrap=False)
        
    # Footer
    bottom = BC +'└' + '─' * (content_width + 2) + '┘'
    cprint(bottom + RS, wrap=False)







# 4) Part IV: Main Functions ---------------------------------------------------
def welcome_screen():
    """Display a short welcoming screen."""
    gemini_logo_string = (
    f"{BD}"
    f"{BL}G"
    f"{RED}o"
    f"{YLW}o"
    f"{BL}g"
    f"{GR}l"
    f"{RED}e"
    f"{RS} | ♊ "
    f"{BD}"
    f"{BL}GEMINI"
    f"{RS}"
    )

    os.system('cls')
    separator()
    cprint(f"{GR}Welcome to {gemini_logo_string}{GR} Py-CLI! (An API-based chat)", wrap=False)
    cprint(f"Chat Initialized (Type '{UL}help{RS}{GR}' for a quick start.){RS}\n", wrap=False)
 
def help():
    """Print a quick cheatsheet."""
    MESSAGE = f"""
    1) First Thing First:
       -Get an API key from: {UL}https://aistudio.google.com/app/api-keys{RS}
        and paste it in this script at line (42). Remember, it's free, easy
        to get, and generous for the free tier (Just requires an account).
       -You can change other settings (e.g: The used Gemini model at line
        (43)) if you wish.
    
    2) Usage:
       -Type 'quit' or 'exit' to quit.
       -Type 'clear' to clear the screen.
       -Press 'Ctrl-C' to cancel a prompt, stop a response, or quit.
       -Press 'Ctrl-Space' to add a new line to your prompt.
       -Press 'Enter' to send.
    
    3) Limitations:
       -Tables with many columns will appear chaotic.
       -Special characters (Like LaTeX syntax) will appear as a plain text.
       -Some other bugs I didn't discover yet :)
    """
    
    MESSAGE = textwrap.dedent(MESSAGE).lstrip('\n').rstrip()
    box(MESSAGE, title='HELP MENU', border_color=YLW, text_color=YLW, secondary_color=YLW,)

def farewell(confirmed=False):
    """
    Print a random but beautiful farewell message.
    Also give the user the chance to go back.
    """
    global FAREWELLS_MESSAGES, CONTINUE_MESSAGES, confirm_separator

    # Confirm
    cprint(RS, end='')
    if not confirmed:
        cprint()
        if confirm_separator: separator()
        confirm_separator = True
        wrong_answer = 0
        text = f"{YLW}Are you sure you want to quit? (y/n): {RS}"
        
        while True:
            try:
                confirm = input(text).lower().strip()
                break
            except:
                # Stubborn Mode (To avoid accidental exit)
                wrong_answer += 1
                if wrong_answer > 1: clean_output()
                if wrong_answer == 1:
                    text = f"\n{YLW}Either 'Yes' or 'No' (y/n): {RS}"
                else:
                    # Note, I suspect this line will -sometimes- cause the console to show a blanc line, Idk why.
                    text = f"\r{YLW}Are you sure you want to quit? (y/n):\nEither 'Yes' or 'No' (y/n): {RS}"
        
        if confirm != 'y':
            cprint(GR + choice(CONTINUE_MESSAGES) + RS)
            separator()
            return
        else:
            cprint()
    
    # Save chat
    saved = save_chat_history(up_separator=confirmed, down_separator=False)
    if saved: cprint()
    
    # Clean prompt history & Exit
    if not saved and confirmed: separator()
    prune_history_by_size()
    message = choice(FAREWELLS_MESSAGES)
    cprint(GR + message + RS)
    separator()
    sys.exit(0)
 
def serialize_history():
    """Convert active chat history into a savable json."""
    history = chat.get_history()
    serializable_history = [
        {
            'role': content.role,
            'parts': [{'text': p.text} for p in content.parts if hasattr(p, 'text') and p.text],
        }
        for content in history
    ]
    
    return serializable_history

def prune_history_by_size():
    """
    Checks the history file size. If > max_size_mb, it prunes the file
    by taking the last half and finding the next full history block (timestamp).
    """
    if not os.path.exists(PROMPT_HISTORY_FILE):
        return
    
    # Check file size
    file_size = os.path.getsize(PROMPT_HISTORY_FILE)
    if file_size <= PROMPT_HISTORY_SIZE:
        return
    
    # Split file
    cprint(GR + 'Shrinking the prompt history file...' + RS)
    while file_size > 1:
        file_size = file_size // 2
    
    start_seek_position = file_size
        
    with open(PROMPT_HISTORY_FILE, 'rb') as f:
        f.seek(start_seek_position)
        content_last_half = f.read().decode(sys.getdefaultencoding(), 'ignore')
    
    # Discard the broken content, keep it intact
    HISTORY_PATTERN = re.compile(r'^#\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+$', re.MULTILINE)
    match = HISTORY_PATTERN.search(content_last_half)
    if match:
        start_index = match.start()
        new_content = content_last_half[start_index:]
        with open(PROMPT_HISTORY_FILE, 'w') as f:
            new_content = new_content.replace('\r\n', '\n').replace('\r', '\n')
            f.write(new_content)

    else:
        with open(PROMPT_HISTORY_FILE, 'w') as f:
            content_last_half = content_last_half.replace('\r\n', '\n').replace('\r', '\n')
            f.write(content_last_half)
    
    cprint(GR + 'Done!\n' + RS)

def save_chat_history(up_separator=True, down_separator=True):
    """Save the chat history before quitting."""
    # Check conditions & Test if there is an active chat, else exit.
    try: active = bool(chat)
    except NameError: return
    
    serializable_history = None
    empty = chat.get_history() == []
    
    try:
        serializable_history = serialize_history()
        new_history_json_str = json.dumps(serializable_history)
        with open(CHAT_HISTORY_FILE, 'r') as f: old_history_dicts = json.load(f)
        
        old_history_json_str = json.dumps(old_history_dicts)
        changed = new_history_json_str != old_history_json_str
        
    except:
        serializable_history = None
        changed = True
    
    # Perform the save
    if active and not empty and changed:
        if up_separator: separator()
        cprint(GR + 'Saving chat history, one moment...' + RS)
        
        if not serializable_history:
            try: serializable_history = serialize_history()
            except Exception as error: cprint(f"{RED}Failed to save chat history: {error}!{RS}")
        
        if serializable_history:
            with open(CHAT_HISTORY_FILE, 'w') as f:
                json.dump(serializable_history, f, indent=4)
                cprint(f"{GR}Chat history saved!{RS}")
                
        if down_separator: separator()
        return True

def load_chat_history():
    """Load chat history, if it meets the conditions."""
    global initial_history, confirm_separator
    initial_history = []
    
    # Check if the history file exist, and it's not empty.
    file_exist = os.path.exists(CHAT_HISTORY_FILE)
    empty = os.path.getsize(CHAT_HISTORY_FILE) == 0
    useful = open(CHAT_HISTORY_FILE).read().strip() != '[]'
    
    if file_exist and not empty and useful:
        answer = CYN + "Chat history available, load it? (y/n): " + RS
        invalid_answer = False
        while True:
            try:
                load_history = input(answer).lower().strip()
            except:
                cprint()
                confirm_separator = False
                raise
                
            if load_history == 'y':
                try:
                    with open(CHAT_HISTORY_FILE, 'r') as f:
                        saved_history_dicts = json.load(f)
                    
                    # Reconstruct Content & Part objects from the saved dictionaries
                    errors = 0
                    for item in saved_history_dicts:
                        try:
                            parts = [Part(text=p['text']) for p in item['parts']]
                            initial_history.append(Content(role=item['role'], parts=parts))
                        except:
                            traceback.print_exc()
                            errors += 1
                            if errors == 1:
                                cprint(f"{RED}({errors}) partial error occurred during loading chat history.{RS}")
                            else:
                                clean_output()
                                cprint(f"{RED}({errors}) partial errors occurred during loading chat history.{RS}")
                            continue
                    
                    loaded_messages = len(initial_history)
                    if loaded_messages:
                        cprint(f"{GR}Loaded ({len(initial_history)}) history steps from '{CHAT_HISTORY_FILE}'.{RS}")
                    elif not loaded_messages and not errors:
                        cprint(f"{YLW}File '{CHAT_HISTORY_FILE}' seems to be empty.{RS}")
                    elif not loaded_messages and errors:
                        cprint(f"{YLW}Failed to load any history messages (0 loaded).{RS}")
                        
                    if errors:
                        cprint(f"{RED}Found ({errors}) errors while loading the history, the rest was loaded successfully.{RS}")
                    break
                    
                except Exception as error:
                    cprint(f"{RED}Failed to load chat history ({error}).\n{YLW}Starting a new chat...{RS}")
                    initial_history = []
                    break
            
            elif load_history == 'n':
                cprint(f"{YLW}Ignoring history...")
                cprint(f"History will be overwritten after you send your first message.{RS}")
                break
                
            else:
                if invalid_answer: clean_output()
                answer = CYN + "Either 'Yes' or 'No' (y/n): " + RS
                invalid_answer = True
    
    elif not file_exist:
        cprint(f"{YLW}File '{CHAT_HISTORY_FILE}' not found, starting a new chat...{RS}")
    else:
        cprint(f"{YLW}File '{CHAT_HISTORY_FILE}' seems to be empty.{RS}")
    
    separator(end='')

def setup_chat():
    """Initializes the Gemini client and chat session."""
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        separator('\n')
        cprint(f"{RED}RED: Please replace 'YOUR_API_KEY_HERE' in the script with your actual key.")
        cprint(f"You'll find the key placeholder at line(19).")
        cprint(f"{GR}To get a new API key, visit: https://aistudio.google.com/app/api-keys\n")
        cprint(f"Showing the quick help menu...{RS}")
        separator()
        help()
        sys.exit(1)
    
    # Loading Screen
    clean_output(3)
    print('+' + '-' * 78 + '+')
    print("| Loading chat..." + ' ' * 62 + '|')
    print('+' + '-' * 78 + '+')
    
    try:
        # raise APIError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
        # raise httpx.RemoteProtocolError(message='Test')
        
        # Client Initialization & API Validation
        timeout_config = httpx.Timeout(HTTP_TIMEOUT)
        http_client = httpx.Client(timeout=timeout_config)

        client = genai.Client(
            api_key=GEMINI_API_KEY,
            http_options=http_client,
        )
        
        if STARTUP_API_CHECK: client.models.list()
        
        # Welcome Screen & History Loading
        while True:
            try:
                welcome_screen()
                load_chat_history()
                break
                
            except Interruption:
                farewell()
                continue
        
        # Start chat session with/out the implicit instructions
        config = None
        if IMPLICIT_INSTRUCTIONS_ON:
            config = genai.types.GenerateContentConfig(system_instruction=(IMPLICIT_INSTRUCTIONS))
        
        chat = client.chats.create(
            model=GEMINI_MODEL,
            history=initial_history,
            config=config,
        )
        
        
        cprint()
        return client, chat

    except APIError as error:
        catch_api_error_startup(error)
        help()
        sys.exit(1)
        
    except NetworkExceptions:
        catch_network_error()
        sys.exit(1)

def get_user_input():
    """Handles prompt_toolkit input and gracefully catches Ctrl-C/Ctrl-D."""
    # Stream input
    user_input = prompt(
        FormattedText([
            (f'bg:{PROMPT_BG} black', '\n You > '), # Styled part
            ('', ' '),                              # Unstyled part (will take default bg)
        ]),
        multiline=True,
        wrap_lines=True,
        history=history,
        key_bindings=key_bindings,
    )
    
    if user_input.strip():
        return user_input
    else:
        lines_to_erase = len(user_input) - len(user_input.rstrip('\n'))
        clean_output(lines_to_erase + 2)
        return None

def get_response():
    """Send the user input to AI and wait to receive the response."""
    with console.status("[bold green]Waiting for response...[/bold green]"):
        try:
            response = chat.send_message(user_input)
        except Interruption:   # Interruption is somewhat catched inside chat.send_message(), I doubt this'll work.
            raise
    return response
 
def run_chat():
    """Handles the user input and Gemini responses."""
    global user_input
    while True:
        # A simpler input method, supports history using UP/DOWN arrow keys.
        # But lacks new line support:
        # user_input = input(f"{GR}\n You > {RS} ")
        
        user_input = get_user_input()
        if not user_input: continue
        
        # Quick cleanup
        lines_to_erase = len(user_input) - len(user_input.rstrip('\n'))
        clean_output(lines_to_erase)
        
        # Interpret commands
        command = user_input.strip().lower()
        if command == 'quit' or command == 'exit':
            cprint()
            farewell(confirmed=True)
            continue
        
        elif command == 'help':
            help()
            continue
            
        elif command == 'clear':
            os.system('cls')
            continue
        
        # Get response
        try:
            # raise APIError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            # raise genai.errors.ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            # raise httpx.HTTPError(message='Test' * 25)
            # raise Exception('Test' * 25)
            
            cprint()
            response = None
            
            try:
                response = get_response()
                clean_output()
            except:
                clean_output()
                raise
            
        except genai.errors.ServerError:
            response = catch_server_error_in_chat()
            if not response:
                continue
                
        except APIError as error:
            catch_api_error_in_chat(error)
            continue

        except NetworkExceptions:
            catch_network_error()
            continue
                    
        except Interruption:
            catch_keyboard_interrupt()
            continue
        
        except Exception as error:
            catch_exception_in_chat(error)
            continue
        
        # Print response
        try:
            # raise EOFError
            # raise Exception
            
            cprint(f"{GEM_BG + GR}\n Gemini: {RS}")
            formatted_response = Markdown(response.text)
            console.print(formatted_response)
            sys.stdout.flush()
        
        except Interruption:
            box(
                f'{GR}Response blocked, skipping the rest of it...',
                title='KEYBOARD INTERRUPTION',
                border_color=GR
            )
            continue

        except Exception as error:
            catch_exception_in_chat(error)
            continue

if __name__ == "__main__":
    try:
        # Initialize console, chat client & chat session.
        console = Console(width=80)
        client, chat = setup_chat()
        if chat:
            # raise ValueError('Test' * 25)
            # raise KeyboardInterrupt
            # raise SystemExit
            while True:
                try:
                    run_chat()
                    break
                    
                except Interruption:
                    farewell()
                    continue

    except Interruption:
        farewell()
    
    except SystemExit:
        pass

    except Exception as error:
        try:
            catch_fatal_exception(error)
        except Interruption:
            separator('\n', color=RED)
            sys.exit(1)
