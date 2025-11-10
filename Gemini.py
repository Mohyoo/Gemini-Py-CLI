import os
import sys
import re
import httpx
import httpcore
import textwrap
import traceback
from random import choice
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.history import InMemoryHistory
from google import genai
from google.genai.errors import APIError
from time import sleep

# Settings
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
GEMINI_MODEL = "gemini-2.5-flash"    # Advaced models are more expensive and have less API limits.
STARTUP_API_CHECK = False            # Disable for a slightly faster loading.

# Coming Soon Settings:
SUPPRESS_CATCHED_ERRORS = False      # Not yet implemented
SUPPRESS_UNEXPECTED_ERRORS = False   # Not yet implemented
HISTORY_FILE = "chat_history.json"   # Not yet implemented

class Color:
    USER = "\033[94m" 
    GEMINI = "\033[92m"
    GEMINI_BG = "\033[44m"
    ERROR = "\033[91m"
    LOW_COLOR = "\033[2m\033[37m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    UNDERLINE = "\033[4m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def help():
    """Print a quick cheatsheet."""
    MESSAGE = f"""
    1) First Thing First:
       -Get an API key from: {Color.UNDERLINE}https://aistudio.google.com/app/api-keys{Color.RESET + Color.BRIGHT_YELLOW}
        and paste it in this script at line (19).
       -You can change other settings (e.g: The used Gemini model at line
        (20)) if you wish.
    
    2) Usage:
       -Type 'quit' or 'exit' to quit.
       -Press 'Ctrl-C' to cancel a prompt, stop a response, or quit
        the program.
       -Press 'Enter' to add a new line to your prompt.
       -Press 'ESC' then 'Enter' to send.
    
    3) Limitations:
       -Tables with many columns will appear chaotic.
       -Special characters (like the asterisk '*' for bold or italic text)
        will appear as a plain text.
       -Chat history will not be saved.
       -Some other bugs I didn't discover yet :)
    """
    
    print('\n' + '-' * 79)
    print(Color.BRIGHT_YELLOW + MESSAGE.lstrip('\n').rstrip() + Color.RESET)
    print('-' * 79 + '\n')

def farewell():
    """print a random but beautiful farewell message"""
    FAREWELLS = [
        # Standard
        "Chat session ended. Goodbye!",
        "Gemini signing off. Until next time!",
        "The light fades. See you in the next prompt!",
        "Session terminated successfully. Farewell.",
        "Peace out. Thanks for chatting!",
        "Processing complete. Disconnecting now.",
        "Fin. Come back soon!",
        "Task completed. System shutdown initiated.",
        "Voilà un bon travail, mais il est temps de partir.\nBonne route à vous!",
        
        # Funny
        "The chat is lost, but the war has just begun!",
        "Abracadabra! Poof...\nWait, who turned off the lights?",
        "Adios, amigo. The terminal awaits your return.",
        "¡Nos vemos, cocodrilo!\n(See you, crocodile :P)",
        "¡Hasta la vista!\n(See you around :)",
        "Au revoir!",
        "Ciao! I'm outta here faster than an Italian pizzadisappearing at a party.",
        f"Okay okay, calm down, he only ended the chat...\nBUT AAAAARGHHH...!!!\n{Color.ERROR}System rage error occured; {Color.RESET}Cya!",
        
        # Enthusiastic
        "Keep coding and stay curious!\n(If you aren't a developer, ignore this, you owe me a coffee)",
        "May your logic be sound and your keys be clean.",
        "Go forth and query, friend.",
        "I'll be here. You know where to find me.",
        "Enjoy the silence. Goodbye.",
        "Until our paths cross again.",
        "Stay curious, stay connected.",
        "Farewell, may the consequences be ever in your favor.",
        "Chat complete. Have a productive day!",
        "Ce sont les mots que j'aime dans un chat! Au revoir!",
        
        # Serious
        "Remember to commit your changes!",
        "Don't forget to save your work!",
        "Bye Bye! Check your API key status if you run into trouble.",
    ]
    
    message = choice(FAREWELLS)
    print('\n' + '-' * 79)
    print(Color.GEMINI + message + Color.RESET)
    print('-' * 79)
    sys.exit(0)

def setup_chat():
    """Initializes the Gemini client and chat session."""
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print('\n\n' + '-' * 79)
        print(f"{Color.ERROR}ERROR: Please replace 'GEMINI_API_KEY' in the script with your actual key.")
        print(f"You'll find the 'GEMINI_API_KEY' at line(19).")
        print(f"{Color.GEMINI}To get a new API key, visit: https://aistudio.google.com/app/api-keys\n")
        print(f"Showing the quick help menu...{Color.RESET}")
        print('-' * 79)
        help()
        clean_output()
        sys.exit(1)
        
    try:
        # Client initialization using the defined API key
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        if STARTUP_API_CHECK:
            client.models.list()
        
        # Start a new chat session using the fast model
        chat = client.chats.create(model=GEMINI_MODEL)
        gemini_logo_string = (
            # Google Logo Colors:
            f"{Color.BOLD}"
            f"{Color.BRIGHT_BLUE}G"
            f"{Color.BRIGHT_RED}o"
            f"{Color.BRIGHT_YELLOW}o"
            f"{Color.BRIGHT_BLUE}g"
            f"{Color.BRIGHT_GREEN}l"
            f"{Color.BRIGHT_RED}e"
            f"{Color.RESET} | ♊ "
            f"{Color.BOLD}"
            f"{Color.BRIGHT_BLUE}GEMINI"
            f"{Color.RESET}"
        )
        
        os.system('cls')
        print("-" * 79)
        print(f"{Color.GEMINI}Welcome to {gemini_logo_string}{Color.GEMINI} API!")
        print(f"Chat Initialized (Type 'help' for a quick start.){Color.RESET}")
        print("-" * 79)
        return client, chat

    except APIError as error:
        print('\n' + '-' * 79)
        print(f"{Color.ERROR}API Error occurred:\n{error}.\n")
        print(f"Please check your API key validations or limits.")
        print(f"{Color.GEMINI}To get a new API key, visit: https://aistudio.google.com/app/api-keys")
        print(f"(Remember that it requires a google account)\n")
        print(f"Showing the quick help menu...{Color.RESET}")
        print('-' * 79)
        help()
        clean_output()
        sys.exit(1)

def smart_format_response(text, width=79):
    """
    Cleans, wraps, and aligns the Gemini text smartly, preserving
    list alignment and treating code blocks/headers as separate blocks.
    """
    # 2. WRAPPING & ALIGNMENT STEP:
    lines = text.split('\n')
    formatted_output = []
    in_code_block = False
    
    # Pattern to detect list items: (optional spaces) + (marker: -, *, +, or 1. 2.) + (space)
    list_marker_pattern = re.compile(r'^(\s*[-*+]|\s*\d+\.)\s+')
    
    for line in lines:
        if not line.strip():
            # Preserve empty lines as separators
            formatted_output.append('\n')
            continue
            
        # NEW SEPARATOR & CODE BLOCK HANDLER
        # 1. Check for triple backticks (```) to toggle code block state
        if line.strip().startswith('```') or line.strip().endswith('```'):
            # If the line starts a block, toggle the state.
            in_code_block = not in_code_block
        
        if line.strip() == '---':
            if in_code_block:
                # If inside a code block, preserve the '---' line as is
                formatted_output.append(line + '\n')
            else:
                # If NOT inside a code block, convert it to the continuous line.
                styled_line = f"{Color.LOW_COLOR}{'─' * width}{Color.RESET}\n"
                formatted_output.append(styled_line)
            continue # Skip the rest of the loop for this line

        # 2. We must also bypass table/list logic if we're in a triple-backtick block.
        if in_code_block:
            # If we are inside a code block, append the line as is to preserve formatting
            formatted_output.append(line + '\n')
            continue
        
        # NEW TABLE HANDLER: Prevent wrapping for table content lines
        line_stripped = line.strip()
        
        # Rule 1: Lines containing at least two pipe characters (clear indicator of column data).
        is_data_line = line_stripped.count('|') >= 2
        
        # Rule 2: Lines that are almost entirely structural characters (borders/dividers).
        structural_chars = set(['|', '+', '-', '_', ':', ' ', '\t'])
        # Check if 90% or more of the non-whitespace characters are structural (for flexibility)
        is_structural_border = len(line_stripped) > 5 and \
                               sum(c in structural_chars for c in line_stripped if not c.isspace()) >= 0.9 * len(line_stripped.replace(' ', ''))
        
        if is_data_line or is_structural_border:
            # Append the special marker to signal INSTANT printing in run_chat, 
            # mitigating the chaotic console wrap.
            formatted_output.append(line + '\n')
            continue # Skip normal wrapping and list check
        
        match = list_marker_pattern.match(line)
        if match:
            # It's a list item.
            marker_full = match.group(0) # e.g., '1. ' or '* '
            
            # The length of the marker + subsequent spaces
            marker_len = len(marker_full) 
            
            # Text content starts after the marker
            content_text = line[marker_len:]
            
            # Use textwrap.fill to wrap the content and apply subsequent indentation
            wrapped_content = textwrap.fill(
                content_text,
                width=width,
                initial_indent=marker_full,
                subsequent_indent=' ' * marker_len # Indent subsequent lines under the marker
            )
            formatted_output.append(wrapped_content + '\n')
            
        else:
            # It's a standard paragraph or header (wrapped normally)
            wrapped_paragraph = textwrap.fill(
                line.strip(),
                width=width
            )
            formatted_output.append(wrapped_paragraph + '\n')

    return ''.join(formatted_output).strip()

def clean_output(max_lines_to_erase=1):
    """
    Simulates scanning and cleaning up previous empty lines by using 
    ANSI codes to move the cursor up and erase, then prints a separator.
    """
    
    # ANSI escape sequence for moving the cursor up and erasing the line:
    # \033[A: Move cursor Up one line
    # \033[2K: Erase the entire current line
    ERASE_LINE_UP = "\033[A\033[2K"
    
    # 1. Clean up the previous lines (overwriting empty space)
    for _ in range(max_lines_to_erase):
        print(ERASE_LINE_UP, end="")

def get_user_input():
    """Handles prompt_toolkit input and gracefully catches Ctrl-C/Ctrl-D."""
    try:
        history=InMemoryHistory()
        user_input = prompt(
            FormattedText([
                ('bg:cyan black', ' You > '), # Styled part
                ('', ' '),                               # Unstyled space (will take default bg)
            ]),
            multiline=True,   # Allows input to span multiple lines
            wrap_lines=True,  # Fixes the word-breaking issue (live word wrapping)
            history=history,
        )
        
    except EOFError:
        # Handles Ctrl-D (Termination signal in Linux/Mac)
        return None
    
    if user_input.strip():
        return user_input
    else:
        lines_to_erase = len(user_input) - len(user_input.rstrip('\n'))
        clean_output(lines_to_erase + 1)
        return None

def run_chat(chat):
    """Handles the user input and Gemini responses."""
    while True:
        # A simpler input method, supports history using UP/DOWN arrow keys.
        # But lacks new line support.
        # user_input = input(f"{Color.USER} You > {Color.RESET} ")
        user_input = get_user_input()
        
        if not user_input:
            continue
        
        command = user_input.strip().lower()
        if command == 'quit' or command == 'exit':
            farewell()
        
        elif command == 'help':
            help()
            continue
        
        # A quick cleanup
        lines_to_erase = len(user_input) - len(user_input.rstrip('\n'))
        clean_output(lines_to_erase)
        
        try:
            response = chat.send_message(user_input)
        
        except APIError as error:
            print('\n' + '-' * 79)
            print(f"{Color.ERROR}API Error occurred:\n{error}.\n")
            print(f"Please check your API key limits.")
            print(f"{Color.GEMINI}To get a new API key, visit: https://aistudio.google.com/app/api-keys{Color.RESET}")
            print('-' * 79)
            sys.exit(1)
            
        except genai.errors.ServerError:
            print('\n' + '-' * 79)
            print(f"{Color.ERROR}A temporary server problem occured.")
            print(f'It might be a service overloading, maintenance or backend errors...')
            print(f'Retrying in 5 seconds...')
            sleep(5)
            
            response = None
            for attempt in range(5):
                try:
                    response = chat.send_message(user_input)
                    print(Color.GEMINI + 'Response received!')
                    break
                    
                except genai.errors.ServerError:
                    if attempt >= 4:
                        print(f'Tried 5 times with no response, please wait for sometime...')
                        response = None
                        break
                    print('Issue persisting, trying again in 10 seconds...')
                    sleep(10)
                    continue
                    
            print(f'{Color.RESET}' + '-' * 79 + '\n')
            if not response:
                continue
        
        except KeyboardInterrupt:
            print('\n' + '-' * 79)
            print(f"{Color.GEMINI}Prompt cancelled, skipping...")
            print(f'Rest assured, Gemini has no idea about what you just sent.{Color.RESET}')
            print('' + '-' * 79 + '\n')
            continue
        
        except Exception as error:
            print('\n' + '-' * 79)
            print(f"{Color.ERROR}An error occured: {error}!{Color.RESET}")
            see_error = input("See the error? (y/n) ").strip().lower()
            
            if see_error == 'y':
                print(Color.ERROR)
                traceback.print_exc()
                print(Color.RESET)
                clean_output()
                print('-' * 79 + '\n')
                continue
            else:
                print(f"{Color.GEMINI}Ignoring the error...{Color.RESET}")
                print('' + '-' * 79 + '\n')
                continue
        
        try:
            print(f"{Color.GEMINI_BG + Color.GEMINI}\n Gemini: {Color.RESET}")
            # 1. Get the full text, clean it, and split into lines/paragraphs
            reponse_lines = smart_format_response(response.text).split('\n')

            for line in reponse_lines:
                print(line)
                sleep(0.07)
            
            print('')
        
        except KeyboardInterrupt:
            print('\n' + '-' * 79)
            print(f"{Color.GEMINI}Response blocked, skipping the rest of it...{Color.RESET}")
            print('-' * 79 + '\n')
            continue  # Go back to the start of the while loop

        except Exception as error:
            print('\n' + '-' * 79)
            print(f"{Color.ERROR}An error occured: {error}!{Color.RESET}")
            see_error = input("See the error? (y/n) ").strip().lower()
            
            if see_error == 'y':
                print(Color.ERROR)
                traceback.print_exc()
                print(Color.RESET)
                clean_output()
                print('-' * 79 + '\n')
                continue
            else:
                print(f"{Color.GEMINI}Ignoring the error...{Color.RESET}")
                print('' + '-' * 79 + '\n')
                continue

if __name__ == "__main__":
    try:
        client, chat_session = setup_chat()
        if chat_session:
            while True:
                try: 
                    run_chat(chat_session)

                except (httpx.HTTPError, httpx.ConnectError, httpx.RemoteProtocolError,
                        httpcore.ConnectError, IOError):
                    print('\n' + '-' * 79)
                    print(f"{Color.ERROR}Failed to connect, check your network or firewall!{Color.RESET}")
                    print('-' * 79 + '\n')
                    continue

    except KeyboardInterrupt:
        farewell()
    
    except SystemExit:
        pass

    except Exception as error:
        try:
            print('\n' + '-' * 79)
            print(f"{Color.ERROR}A fatal error occured: '{error}'! and the program has to quit.{Color.RESET}")
            see_error = input("See the error? (y/n) ").strip().lower()
            
            if see_error == 'y':
                print(Color.ERROR)
                traceback.print_exc()
                print(Color.RESET)
                clean_output()
                print('-' * 79)
            else:
                print('-' * 79)
                sys.exit(1)
                
        except KeyboardInterrupt:
            print('\n' + '-' * 79)
            sys.exit(1)
