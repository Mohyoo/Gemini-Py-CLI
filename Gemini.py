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
from rich.console import Console
from rich.markdown import Markdown

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
        and paste it in this script at line (19). Remember, it's free, easy
        to get, and generous for the free tier.
       -You can change other settings (e.g: The used Gemini model at line
        (20)) if you wish.
    
    2) Usage:
       -Type 'quit' or 'exit' to quit.
       -Type 'clear' to clear the screen.
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
    
    print('\n' + '-' * 80)
    print(Color.BRIGHT_YELLOW + MESSAGE.lstrip('\n').rstrip() + Color.RESET)
    print('-' * 80 + '\n')

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
        "Chat complete. Have a productive day!",
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
        f"Okay okay, calm down, he only ended the chat...\nBUT AAAAARGHHH...!!!\n{Color.ERROR}System Rage Error Occured; {Color.RESET}Cya!",
        "Ladies & Gentlemen, we are closing.",
        "Pleasure: The End.",
        "Just a quick cleanup...\nOK, all done!",
        "Okay ladies, time to go home.",
        "Artryoos. Metryoos. Zeetoos!",
        "Remember, it's all about: Hakuna Matata!\n(No Worries :)",
        "Ma chère mademoiselle, it is with deepest pride and greatest pleasure\nthat we proudly present... The End.",
        
        # Enthusiastic
        "Keep coding and stay curious!\n(If you aren't a developer, ignore this, you owe me a coffee)",
        "May your logic be sound and your keys be clean.",
        "Go forth and query, friend.",
        "I'll be here. You know where to find me.",
        "Enjoy the silence. Goodbye.",
        "Until our paths cross again.",
        "Stay curious, stay connected.",
        "Farewell, may the consequences be ever in your favor.",
        "Ce sont été les mots que j'aime dans un chat! Au revoir!",
        "I will stay here... if you ever turn back.",
        "Sometimes it's too difficult, yet.. it's not impossible ;)",
        "Keep it up gentleman, the world needs your work.",
        "The waves are calling.. Captain.",
        
        # Serious
        "Remember to commit your changes!",
        "Don't forget to save your work!",
        "Bye Bye! Check your API key status if you run into trouble.",
    ]
    
    message = choice(FAREWELLS)
    print('\n' + '-' * 80)
    print(Color.GEMINI + message + Color.RESET)
    print('-' * 80)
    sys.exit(0)

def setup_chat():
    """Initializes the Gemini client and chat session."""
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        print('\n\n' + '-' * 80)
        print(f"{Color.ERROR}ERROR: Please replace 'YOUR_API_KEY_HERE' in the script with your actual key.")
        print(f"You'll find the key placeholder at line(19).")
        print(f"{Color.GEMINI}To get a new API key, visit: https://aistudio.google.com/app/api-keys\n")
        print(f"Showing the quick help menu...{Color.RESET}")
        print('-' * 80)
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
        print("-" * 80)
        print(f"{Color.GEMINI}Welcome to {gemini_logo_string}{Color.GEMINI} Py-CLI! (An API-based chat)")
        print(f"Chat Initialized (Type 'help' for a quick start.){Color.RESET}")
        print("-" * 80)
        return client, chat

    except APIError as error:
        print('\n' + '-' * 80)
        print(f"{Color.ERROR}API Error occurred:\n{error}.\n")
        print(f"Please check your API key validations or limits.")
        print(f"{Color.GEMINI}To get a new API key, visit: https://aistudio.google.com/app/api-keys")
        print(f"(Remember that it requires a google account)\n")
        print(f"Showing the quick help menu...{Color.RESET}")
        print('-' * 80)
        help()
        clean_output()
        sys.exit(1)

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
        
        # A quick cleanup
        lines_to_erase = len(user_input) - len(user_input.rstrip('\n'))
        clean_output(lines_to_erase)
        
        # Check if it's a command
        command = user_input.strip().lower()
        if command == 'quit' or command == 'exit':
            farewell()
        
        elif command == 'help':
            help()
            continue
            
        elif command == 'clear':
            os.system('cls')
            continue
            
        try:
            response = chat.send_message(user_input)
        
        except APIError as error:
            print('\n' + '-' * 80)
            print(f"{Color.ERROR}API Error occurred:\n{error}.\n")
            print(f"Please check your API key limits, or wait for sometime.{Color.RESET}")
            print('-' * 80 + '\n')
            
        except genai.errors.ServerError:
            print('\n' + '-' * 80)
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
                    
            print(f'{Color.RESET}' + '-' * 80 + '\n')
            if not response:
                continue
        
        except (httpx.HTTPError, httpx.ConnectError, httpx.RemoteProtocolError,
                httpcore.ConnectError, IOError):
            print('\n' + '-' * 80)
            print(f"{Color.ERROR}Failed to connect, check your network or firewall!{Color.RESET}")
            print('-' * 80 + '\n')
            continue
                    
        except KeyboardInterrupt:
            print('\n' + '-' * 80)
            print(f"{Color.GEMINI}Prompt cancelled, skipping...")
            print(f'Rest assured, Gemini has no idea about what you just sent.{Color.RESET}')
            print('' + '-' * 80 + '\n')
            continue
        
        except Exception as error:
            print('\n' + '-' * 80)
            print(f"{Color.ERROR}An error occured: {error}!{Color.RESET}")
            see_error = input("See the error? (y/n) ").strip().lower()
            
            if see_error == 'y':
                print(Color.ERROR)
                traceback.print_exc()
                print(Color.RESET)
                clean_output()
                print('-' * 80 + '\n')
                continue
            else:
                print(f"{Color.GEMINI}Ignoring the error...{Color.RESET}")
                print('' + '-' * 80 + '\n')
                continue
        
        try:
            print(f"{Color.GEMINI_BG + Color.GEMINI}\n Gemini: {Color.RESET}")
            console = Console(width=80)
            formatted_response = Markdown(response.text)
            console.print(formatted_response)
            print() 
            sys.stdout.flush()
        
        except KeyboardInterrupt:
            print('\n' + '-' * 80)
            print(f"{Color.GEMINI}Response blocked, skipping the rest of it...{Color.RESET}")
            print('-' * 80 + '\n')
            continue  # Go back to the start of the while loop

        except Exception as error:
            print('\n' + '-' * 80)
            print(f"{Color.ERROR}An error occured: {error}!{Color.RESET}")
            see_error = input("See the error? (y/n) ").strip().lower()
            
            if see_error == 'y':
                print(Color.ERROR)
                traceback.print_exc()
                print(Color.RESET)
                clean_output()
                print('-' * 80 + '\n')
                continue
            else:
                print(f"{Color.GEMINI}Ignoring the error...{Color.RESET}")
                print('' + '-' * 80 + '\n')
                continue

if __name__ == "__main__":
    try:
        client, chat_session = setup_chat()
        if chat_session:
            run_chat(chat_session)

    except KeyboardInterrupt:
        farewell()
    
    except SystemExit:
        pass

    except Exception as error:
        try:
            print('\n' + '-' * 80)
            print(f"{Color.GEMINI + Color.BOLD}Congratulations! You found it. It's a BUG!\n")
            print(f"{Color.ERROR}A fatal error occured: '{error}'! and the program has to QUIT.{Color.RESET}")
            see_error = input("See the error? (y/n) ").strip().lower()
            
            if see_error == 'y':
                print(Color.ERROR)
                traceback.print_exc()
                print(Color.RESET)
                clean_output()
                print('-' * 80)
            else:
                print('-' * 80)
                sys.exit(1)
                
        except KeyboardInterrupt:
            print('\n' + '-' * 80)
            sys.exit(1)
