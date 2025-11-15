# 1) Part I: Initialization ----------------------------------------------------
# Loading
print('\n' + '+' + '-' * 78 + '+')
print("| Loading libraries. Just a moment..." + ' ' * 42 + '|')
print('+' + '-' * 78 + '+')

# Import Custom Modules
try:
    from settings import *

except Exception as error:
    print(f'\nError: {error}.')
    print('Reinstall the program to restore the missing file.')
    quit(1)
    
except (KeyboardInterrupt, EOFError):
    quit(0)

# Import Libraries
try:
    import re
    import io
    import os
    import sys
    import math
    import json
    import httpx
    import httpcore
    import textwrap
    import traceback
    import threading
    import contextlib
    from datetime import datetime
    from random import randint, choice
    from time import sleep, perf_counter
    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.completion import WordCompleter
    from prompt_toolkit.formatted_text import FormattedText
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from google import genai
    from google.genai.types import Content, Part
    from google.genai.errors import ClientError, ServerError
    from rich.text import Text 
    from rich.panel import Panel
    from rich.console import Console
    from rich.segment import Segment
    from rich.markdown import Markdown
    from rich.console import RenderResult
    
except Exception as error:
    print(f'\nError: {error}.')
    print("Use 'pip' to install missing modules.")
    print("E.g: open CMD & type: pip install httpx rich")
    quit(1)
    
except (KeyboardInterrupt, EOFError):
    quit(0)

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
    "Ma chère mademoiselle, it is with deepest pride and greatest pleasure that\n"
    "we proudly present... The End.",
    "¡Ándale! ¡Ándale! ¡Arriba! ¡Arriba! Yeehaw!",
    "Tactical retreat. We'll be back.",
    "Shadow Fleeing Jutsu!",
    "Together for a better world (Where I'm the boss).",
    "Finally, some peace of mind...",
    "Good, I was in no mood for chat already.",
    "Oh come on, the fun has just begun!",
    "Seriously man? The excitement has just started!",
    f"NOOOOOOOOOOOOOOOOOOOOOO...O\nTask: Calculate the partial sum of the sequence: "
    f"({(' ' + choice(['+', '*']) + ' ').join(['O1', 'O2', 'O3', '...', 'On'])})\n"
    f"Given that it's {choice(['an arithmetic sequence (constant difference)', 'a geometric sequence (constant ratio)', 'a harmonic sequence', 'a fibonacci sequence'])}.\n"
    f"Other details: Difference/Ratio={randint(1, 100)}, O1={randint(1, 500)}, n={randint(1, 999)}.\n"
    "Note: It's letter 'O', not zero '0'. Good luck :)", 
    
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
    f"Calculate this: ({randint(1, 100)} {choice(['+', '-', '*', '/', '**', '%'])} "
    f"{randint(1, 100)}); C'mon quicly!",
    
    # Serious
    "Remember to commit your changes!",
    "Don't forget to save your work!",
    "Bye Bye! Check your API key status if you run into trouble.",
    f"Thank you for using Gemini Py-CLI! Suggestions are welcome!\nGitHub Home: "
    f"{UL}https://github.com/Mohyoo/Gemini-Py-CLI{RS}",
    f"If you faced any issues, please let me know, I'll try to reply quickly.\n"
    f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}",
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
    'Your tenacity is.. endearing!',
    'We have tireless avenger here!',
    'Relax, the best part is still ahead!',
]







# 2) Part II: Classes ----------------------------------------------------------
class Keys():
    # Define constants at the class level.
    if ENTER_NEW_LINE:
        SUBMIT = ('escape', 'enter')
        NEW_LINE = ('enter', 'c-space', 's-tab', 'c-j')
    else:
        SUBMIT = ('enter',)
        NEW_LINE = (('escape', 'enter'), 'c-space', 's-tab', 'c-j')

    TAB = 'tab'
    INTERRUPT = ('c-c', 'c-d')
    UNDO = 'c-z'
    REDO = 'c-y'

    # Define variables.
    redo_fallback_stack = []
    
    def get_key_bindings(self):
        """Creates and returns the KeyBindings object with all custom bindings."""
        key_bindings = KeyBindings()
        
        @key_bindings.add(*self.SUBMIT, eager=True)
        def _(event):
            """
            - Copy the original non-stripped input.
            - Pass the stripped input to buffer for a cleaner output.
            - Save prompt to history.
            - Submits the original input.
            * 'eager=True' ensures this binding takes precedence.
            """
            original_text = event.cli.current_buffer.text
            self.trim_input_buffer(event)
            self.save_history(original_text)
            event.cli.exit(result=original_text)
      
        @key_bindings.add(self.TAB)
        def _(event):
            """Inserts a tab (4 spaces)."""
            event.cli.current_buffer.insert_text('    ')        
        
        @key_bindings.add(self.UNDO)
        def _(event):
            """
            Undo the last change.
            Only pushes a state to the Redo stack if the text actually changes.
            """
            buffer = event.cli.current_buffer
            before_undo = buffer.text
            buffer.undo()
            after_undo = buffer.text
            if before_undo != after_undo:
                self.redo_fallback_stack.append(before_undo)
            
        @key_bindings.add(self.REDO)
        def _(event):
            """
            Redo the last undone change.
            Use a manual method if the original one fails.
            """
            buffer = event.cli.current_buffer
            before_redo = buffer.text
            event.cli.current_buffer.redo()
            
            # If it doesn't work, try the secondary method (Less reliable but fine).
            after_redo = buffer.text
            if (before_redo == after_redo) and (self.redo_fallback_stack):
                restored_text = self.redo_fallback_stack.pop()
                buffer.text = restored_text
                buffer.cursor_position = self.first_diff_index(before_redo, restored_text) + 1
        
        for key in self.NEW_LINE:
            if not isinstance(key, tuple): key = (key,)
            @key_bindings.add(*key)
            def _(event):
                """Inserts a newline character."""
                event.cli.current_buffer.insert_text('\n')
                
        for key in self.INTERRUPT:
            @key_bindings.add(key)
            def _(event):
                """Handle interruption/termination signal, by either: clear or quit."""
                buffer = event.cli.current_buffer
                original_text = buffer.text
                if original_text:
                    if SAVE_INPUT_ON_CLEAR: self.save_history(original_text)
                    buffer.text = ""
                    buffer.cursor_position = 0
                    buffer.save_to_undo_stack()
                else:
                    self.trim_input_buffer(event)
                    if SAVE_INPUT_ON_QUIT: self.save_history(original_text)
                    event.cli.exit(exception=KeyboardInterrupt())

        return key_bindings
    
    def trim_input_buffer(self, event):
        """Strips leading and trailing whitespaces."""
        global NON_STRIPPED_INPUT
        # Get the input text & trim it.
        buffer = event.cli.current_buffer
        current_text = buffer.text
        stripped_text = current_text.strip() 
        
        # Replace the entire text content.
        if current_text != stripped_text:
            buffer.text = stripped_text
    
    def save_history(self, prompt):
        """Save the current prompt to history, if conditions meet."""
        if not prompt.strip(): return
        history_lines = list(history.get_strings())
        if not history_lines:
            history.append_string(prompt)
        else:
            last_saved_prompt = history_lines[-1]
            if prompt.strip() != last_saved_prompt.strip():
                history.append_string(prompt)
    
    def first_diff_index(self, s1, s2):
        """Return the exact point that two strings differ at."""
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]: return i
        
        return min_len

class LimitedWordCompleter(WordCompleter):
    """Overrides WordCompleter to enforce a limit on the number of returned completions."""
    def get_completions(self, document, complete_event):
        # Call the base class's method to get all completions
        all_completions = super().get_completions(document, complete_event)
        
        # Do not complete after whitespaces
        if document.text.endswith('\n') or document.text.endswith('\t') or document.text.endswith(' '):
            return
            
        # Iterate over the generator and only yield the first limited set of completions.
        for i, completion in enumerate(all_completions):
            if i >= SUGGESTIONS_LIMIT:
                break
            yield completion

class GeminiWorker(threading.Thread):
    """A worker thread to run the asynchronous (unblockable) API call."""
    def __init__(self, chat_session, user_input, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True      # Treat it as a service, so receiving a KeyboardInterrupt will kill it; although the Exception itself should kill it.
        self.chat = chat_session
        self.user_input = user_input
        self.response = None
        self.exception = None

    def run(self):
        """The main execution of the thread."""
        try:
            self.response = self.chat.send_message(self.user_input)
        except Exception as error:
            self.exception = error







# 3) Part III: Error Handlers --------------------------------------------------
NetworkExceptions = (
    ConnectionError,
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

def catch_no_api_key():
    msg_1 = "Please replace 'YOUR_API_KEY_HERE' in 'settings.py' with your actual key."
    msg_2 = "You'll find the key placeholder at the first few lines.\n"
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}Showing the quick help menu..."
    box(msg_1, msg_2, msg_3, msg_4, title='NO API KEY PROVIDED', border_color=RED, text_color=RED)

def catch_client_error_startup(error):
    msg_1 = f"{RED}Client side error occurred:\n{RED}{error.message}.\n"
    msg_2 = f"{RED}Check your settings, especially the API key validation or limits."
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}(Remember that it requires a google account)\n"
    msg_5 = f"{GR}Showing the quick help menu...{RS}"
    box(msg_1, msg_2, msg_3, msg_4, msg_5, title='CLIENT SIDE ERROR', border_color=RED, secondary_color=RED)

def catch_client_error_in_chat(error):
    msg_1 = f"{RED}Client side error occurred:\n{RED}{error.message}.\n"
    msg_2 = f"{YLW}Check your settings, especially the API key validation or limits."
    msg_3 = f"{YLW}Restarting the program might also help."
    box(msg_1, msg_2, msg_3, title='CLIENT SIDE ERROR', border_color=RED, secondary_color=RED)

def catch_server_error_startup(error_occurred, attempts):
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = SERVER_ERROR_ATTEMPTS, *SERVER_ERROR_DELAY
    if not error_occurred:
        separator('\n', color=RED)
        cprint(f"{RED}A temporary server problem occurred.")
        cprint(f'It might be a service overloading, maintenance or backend errors...')
    
    if attempts < SERVER_ERROR_ATTEMPTS:
        try:
            if not error_occurred: print_status(lambda: quick_sleep(DELAY_1), f'Retrying in {DELAY_1} seconds...', 'yellow')
            else: print_status(lambda: quick_sleep(DELAY_2), f'Issue persisting, retrying in {DELAY_2} seconds...', 'yellow')
        except Interruption:
            cprint(f'{GR}Quitting...{RS}')
            separator(color=RED)
            sys_exit(1)
        
    else:
        cprint(f'{YLW}Tried {MAX_ATTEMPTS} times with no response! Please wait for sometime...{RS}')
        separator(color=RED)
        sys_exit(1)
    
def catch_server_error_in_chat():
    global confirm_separator
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = SERVER_ERROR_ATTEMPTS, *SERVER_ERROR_DELAY
    
    confirm_separator = False
    separator('\n', color=RED)
    cprint(f"{RED}A temporary server problem occurred.")
    cprint(f'It might be a service overloading, maintenance or backend errors...')
    print_status(lambda: quick_sleep(DELAY_1), f'Retrying in {DELAY_1} seconds...', 'yellow')
    
    response = None
    for attempt in range(SERVER_ERROR_ATTEMPTS):
        try:
            worker = GeminiWorker(chat, user_input)
            worker.start()

            # Loop while the worker thread is still running & Update the status at random intervals.
            with console.status(status=f'[bold {WAIT_1}]Waiting for response...[/bold {WAIT_1}]',
                                spinner=SPINNER):
                while worker.is_alive(): worker.join(SLEEP_INTERVAL)
            
            if worker.exception: raise worker.exception            
            cprint(GR + 'Response received!' + RS)
            response = worker.response
            break
                    
        except ServerError:
            if attempt >= MAX_ATTEMPTS - 1:
                cprint(f'{YLW}Tried {MAX_ATTEMPTS} times with no response! Please wait for sometime...{RS}')
                response = None
                break
                
            print_status(lambda: quick_sleep(DELAY_2), f'Issue persisting, retrying in {DELAY_2} seconds...', 'yellow')
            continue
        
        except ClientError as error:
            separator(color=RED)
            catch_client_error_in_chat(error)
            return None
            
    confirm_separator = True
    separator(color=RED, end='\n')
    return response

def catch_network_error():
    msg = f"{RED}Failed to connect, check your network or firewall!{RS}"
    box(msg, title='NETWORK ERROR', border_color=RED)

def catch_exception(error):
    global confirm_separator
    separator('\n', color=RED)
    log_error(f'An error occurred:\n"{error}"')
    if not NO_ERROR_DETAILS:
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
    
    else:
        clear_lines()
        
    separator(color=RED, end='\n\n')

def catch_fatal_exception(error):
    separator('\n', color=RED)
    cprint(f"{GR + BD}Congratulations! You found it. It's a BUG!")
    cprint(f"To be honest, I'm really sorry for that.")
    cprint(f"Please let me know, I'll try to respond as soon as possible.")
    cprint(f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}\n")
    
    log_error(f'A fatal error occurred:\n"{error}"\nAnd the program has to QUIT.')
    
    if not NO_ERROR_DETAILS:
        see_error = input("See the details? (y/n) ").strip().lower()
        if see_error == 'y':
            cprint(RED + traceback.format_exc().strip() + RS)
        else:
            cprint(f"{YLW}\nInhales.. Deep breathing.. Now out.{RS}")
    
    else:
        clear_lines()
        
    separator(color=RED)
    save_chat_history(up_separator=False)
    sys_exit(1)

def catch_keyboard_interrupt():
    msg_1 = f"{GR}Prompt cancelled, skipping..."
    msg_2 = f'{GR}Rest assured, Google has no idea about what you just sent.'
    box(msg_1, msg_2, title='KEYBOARD INTERRUPTION', border_color=GR)








# 4) Part IV: Helper Functions -------------------------------------------------

# Place this code immediately after 'import sys' and other initial imports:
def cprint(text='', end='\n', wrap=True, flush=True):
    """
    A custom print function that writes directly to stdout and guarantees 
    an immediate display by forcing a flush.
    """
    # Wrap ('CONSOLE_WIDTH - 1' so that '\n' stays in the same line)
    text = str(text)
    if wrap and (len(text) > CONSOLE_WIDTH - 1):
        lines = text.split('\n')
        wrapped_lines = []
        
        for line in lines:
            if not line.strip():
                wrapped_lines.append(' ')
                continue
                
            new_lines = textwrap.wrap(line, width=CONSOLE_WIDTH - 1)
            wrapped_lines.extend(new_lines)
            
        text = '\n'.join(wrapped_lines)
    
    # Print
    stdout_write(text + end)
    if flush: stdout_flush()

def print_status(action, text='Waiting...', color='green'):
    """Display a vital text so that the program doesn't feel stuck."""
    with console.status(status=f"[bold {color}]{text}[/bold {color}]",
                        spinner=SPINNER):
        action()

def log_error(text, style='red', offset=3):
    """
    Display a special message for erros, including time and line.
    
    1) '_stack_offset' argument tells 'Rich' to look further up the call stack
       to find the true originator of the log message. Default to (3): from this
       log_error() -> catch_error_name() -> except statement (what we want).
       
    2) Using quotes inside quotes (e.g: '""') will give the internal quotes
       a special color.
    """
    cprint(RS, end='')
    console.log(text, style=style, _stack_offset=offset, end='\n\n')

def get_styled_lines(text: str) -> list[Text]:
    """
    Takes raw Markdown text, renders it into rich segments, flattens the result,
    assembles it into a single styled Text object, and returns it split into 
    a list of styled lines. This is the shared core logic for all typewriter effects.
    If you didn't understand this, fine, nor did I.
    """
    formatted_response = Markdown(text)

    # 1. Render the Markdown object to internal segments.
    segments: RenderResult = list(console.render(
        formatted_response,
        console.options
    ))
    
    all_segments = []
    
    # 2. Flatten the segments into a list of (text, style) tuples
    for item in segments:
        if isinstance(item, Segment):
            # Case 1: Raw Segment object -> convert to a (text, style) tuple
            all_segments.append((item.text, item.style))
        elif hasattr(item, 'segments'):
            # Case 2: Line object -> iterate over its internal segments.
            for text, style, *rest in item.segments:
                all_segments.append((text, style))
        
    # 3. Create the full Text object from the flattened list of segments
    full_text = Text.assemble(*all_segments)

    # 4. Split the full styled Text object into a list of new styled Text objects (lines)
    output_lines = full_text.split('\n')
    
    return output_lines

def print_markdown_line(text: str, delay_seconds: float = 0.05):
    """
    Take a string & Convert it to Markdown object.
    Print fully formatted Markdown content line-by-line with a delay.
    """
    output_lines = get_styled_lines(text)
    
    # Print the styled lines one by one with a delay
    for line in output_lines:
        console.print(line) 
        sleep(delay_seconds)

def print_markdown_word(text: str, delay_seconds: float = 0.09):
    """
    Prints fully formatted Markdown content word-by-word with a delay.
    Uses slicing and regex to preserve formatting and correct spacing.
    """
    output_lines = get_styled_lines(text)

    # 3. Print the styled content word by word
    console.show_cursor(False)
    for line in output_lines:
        if not str(line).strip():
            # If the line contains only whitespace or is empty, print a newline and continue
            console.print()
            continue
            
        line_content = str(line)
        # Use regex to split text into [word, space, word, space, ...]
        parts = WORD_AND_SPACE_PATTERN.split(line_content)
        
        current_pos = 0 
        
        for part in parts:
            if not part:
                continue
            
            part_length = len(part)
            
            # CRITICAL: Use slicing to get the styled segment
            styled_part_segment = line[current_pos : current_pos + part_length]
            
            # Print the part (could be a word or a space block), without a final newline
            console.print(styled_part_segment, end="")
            
            # Apply delay only if it's a word (non-whitespace)
            if part.strip():
                sleep(delay_seconds)
            
            current_pos += part_length

        # Print a final newline after the full line's content is printed
        console.print()
    
    console.show_cursor(True)

def print_markdown_char(text: str, delay_ms: float = 3):
    """
    Take a string & Convert it to Markdown object.
    Print fully formatted Markdown content character-by-character with a delay.
    """
    output_lines = get_styled_lines(text)
    
    if 'fast' in RESPONSE_EFFECT: wait = lambda: sleep_precise(delay_ms)
    elif 'slow' in RESPONSE_EFFECT: wait = lambda: sleep(0.01)
    else: wait = lambda: None

    # 3. Print the styled content character by character
    console.show_cursor(False) # Hide cursor during printing for a cleaner effect

    for line in output_lines:
        # Iterate over the length of the styled line object
        for i in range(len(line)):
            # Create a copy of the line and truncate it to just the current character (i to i+1)
            char_segment = line.copy()
            char_segment = line[i:i + 1]
            
            # Print the single, styled character without a final newline
            console.print(char_segment, end='')
            wait()
            
        # After printing all characters in the line, print a newline
        console.print() 

    console.show_cursor(True) # Restore the cursor

def quick_sleep(delay: float):
    """Sleeps for 'delay' seconds in non-blocking short chunks."""
    slept_time = 0.0
    while slept_time < delay:
        sleep(SLEEP_INTERVAL)
        slept_time += SLEEP_INTERVAL

def sleep_precise(milliseconds):
    """
    High precision sleep function at the cost of high CPU usage.
    Using busy-wait loop via time.perf_counter(), the CPU is constantly
    running the loop instead of sleeping.
    """
    end_time = perf_counter() + (milliseconds / 1000.0)
    while perf_counter() < end_time:
        pass

def clear_lines(lines_to_erase=1):
    """
    Simulates scanning and cleaning up previous empty lines by using 
    ANSI codes to move the cursor up and erase, then prints a separator.
    """
    # \033[A:  Move cursor Up one line
    # \033[2K: Erase the entire current line
    for _ in range(lines_to_erase):
        cprint('\033[A\033[2K', end='')

def visual_len(text_with_ansi):
    """Returns the visible length of a string, ignoring ANSI codes."""
    # ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')
    return len(ANSI_ESCAPE.sub('', text_with_ansi))

def separator(before='', after='', char='─', color=GRY, width=CONSOLE_WIDTH, end='\n'):
    """Display a line of hyphens."""
    # Used console.print() instead of print() and our defined cprint(), because
    # others have an issue of printing double new line after.
    console.print(color + before + char * width + after + RS,
                  end=end, no_wrap=True, soft_wrap=True, overflow='ignore')

def box(*texts, title='Message', border_color='', text_color='', secondary_color='', width=CONSOLE_WIDTH):
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
    # Define colors.
    BC = border_color    # For the box borders
    TC = text_color      # If the content has its colors, this will be overwritten.
    SC = secondary_color # Only for wrapped lines.
    
    # Wrap text to fit.
    message = '\n'.join(texts)
    wrapped = []
    for line in message.splitlines():
        if not line.strip():
            wrapped.append(' ')
            continue
            
        # Apply secondary color to wrapped lines
        wrapped_lines = textwrap.wrap(line, CONTENT_WIDTH)
        for index, line in enumerate(wrapped_lines):
            if index == 0: continue
            wrapped_lines[index] = SC + line
            
        wrapped.extend(wrapped_lines)
    
    # Prepare the box.
    box_string = ''
    
    # Header
    cprint()
    top = BC + '┌' + '─' * (CONTENT_WIDTH + 2) + '┐'
    title_line = top.replace('─' * (CONTENT_WIDTH + 2), f' {title} '.center(CONTENT_WIDTH + 2, '─'))
    box_string += title_line + RS + '\n'
    
    # Content Lines
    for line in wrapped:
        line_visual_len = visual_len(line)
        padding = ' ' * (CONTENT_WIDTH - line_visual_len)
        line = f'{BC}│{RS} {TC}{line}{padding} {BC}│{RS}'
        box_string += line + '\n'
        
    # Footer
    bottom = BC +'└' + '─' * (CONTENT_WIDTH + 2) + '┘'
    box_string += bottom
    
    cprint(box_string, wrap=False)

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

    terminal(CLEAR_COMMAND)
    separator()
    cprint(f"{GR}Welcome to {gemini_logo_string}{GR} Py-CLI! (An API-based chat)", wrap=False)
    cprint(f"Chat Initialized (Type '{UL}help{RS}{GR}' for a quick start.){RS}\n", wrap=False)
 
def help():
    """Print a quick cheatsheet."""
    MESSAGE = f"""
    1) First Thing First:
       -Get an API key from: {UL}https://aistudio.google.com/app/api-keys{RS}
        and paste it in 'settings.py' (first few lines). Remember, it's free,
        easy to get, and generous for the free tier (Just requires an account).
       -You can change other settings if you wish (e.g: The used Gemini model).
    
    2) Keyboard Shortcuts (While in Prompt):
       - ENTER to send.
       - CTRL-SPACE, SHIFT-TAB or CTRL-J to add a new line to your prompt
         (SHIFT-ENTER won't work, and it will submit your text!)
       - CTRL-C to clear/cancel a prompt, stop a response, or quit.
       - UP/DOWN arrows to navigate between input lines / history prompts,
         or to accept word suggestions.
    
    3) Special Commands:
       -Type 'quit' or 'exit' to quit.
       -Type 'clear' to clear the screen.
       -Type 'help' for this guide menu.
       
    5) More Shortcuts:
       - CTRL-Z/CTRL-Y to undo/redo.
       - CTRL-L to clear screen.
       - CTRL-R (Reverse Search) to search backward & find the most recent
         match in history, keep pressing to move.
       - CTRL-S (Forward Search) used after CTRL-R to find older matches,
         keep pressing to move.
    
    4) Limitations:
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
                if wrong_answer > 1: clear_lines()
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
    sys_exit(0)
 
 
 
 
 


# 5) Part V: Main Functions ----------------------------------------------------
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
    Checks the history file size. If > PROMPT_HISTORY_SIZE, it prunes the file
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
    
    # Discard the broken content, keep it intact, and remove unwanted characters
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
    global chat_saved
    # Condition 1: Chat session must be active.
    try: active = bool(chat)
    except NameError: return
        
    # Condition 2: Active session must not be empty.
    empty = chat.get_history() == []
    if empty: return
    
    # Condition 3: Active session must be a new chat or an extension to the saved one.
    serializable_history = None
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
            try:
                with open(CHAT_HISTORY_FILE, 'w') as f:
                    json.dump(serializable_history, f, indent=4)
                
                cprint(f"{GR}Chat history saved!{RS}")
                chat_saved = True
            
            except Exception as error:
                cprint(f"{RED}Failed to save chat history: {error}!{RS}")
                
        if down_separator: separator()
        return True

def load_chat_history():
    """Load chat history, if it meets the conditions."""
    global initial_history, confirm_separator
    initial_history = []
    
    # Check if the history file exist, and it's not empty.
    file_exist = os.path.exists(CHAT_HISTORY_FILE)
    empty, useful = None, None
    
    if file_exist:
        empty = os.path.getsize(CHAT_HISTORY_FILE) == 0
    
    if file_exist and not empty:
        with open(CHAT_HISTORY_FILE, 'r') as f:
            content = f.read().strip()
            useful = content != '[]'
    
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
                                clear_lines()
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
                if invalid_answer: clear_lines()
                answer = CYN + "Either 'Yes' or 'No' (y/n): " + RS
                invalid_answer = True
    
    elif not file_exist:
        cprint(f"{YLW}File '{CHAT_HISTORY_FILE}' not found, starting a new chat...{RS}")
    else:
        cprint(f"{YLW}File '{CHAT_HISTORY_FILE}' seems to be empty.{RS}")
    
    separator(end='')

def load_word_completer():
    """
    Reads a list of words from a file, one word per line.
    Use the words for realtime suggestions.
    """
    global word_completer
    
    try:
        with open(WORDLIST_FILE, 'r') as f:
            words = [line.strip() for line in f if line.strip()][4:]
        if words:
            word_completer = LimitedWordCompleter(words, ignore_case=True)
    
    except FileNotFoundError:
        pass

def setup_chat():
    """Initializes the Gemini client and chat session."""
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        catch_no_api_key()
        help()
        sys_exit(1)
    
    # Loading Screen
    clear_lines(3)
    print('+' + '-' * 78 + '+')
    print("| Loading chat..." + ' ' * 62 + '|')
    print('+' + '-' * 78 + '+')
    
    error_occurred = None
    attempts = 0
    
    while True:
        try:
            # raise ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            # raise ClientError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            # raise httpx.RemoteProtocolError(message='Test')
            
            # Client Initialization & API Validation
            timeout_config = httpx.Timeout(HTTP_TIMEOUT)
            http_client = httpx.Client(timeout=timeout_config)

            client = genai.Client(
                api_key=GEMINI_API_KEY,
                http_options=http_client,
            )
            
            if STARTUP_API_CHECK: client.models.list()
            
            # Welcome Screen & Notes...
            while True:
                try:
                    if WORD_SUGGESTION: load_word_completer()
                    welcome_screen()
                    load_chat_history()
                    if WORD_SUGGESTION and not word_completer:
                        # Don't ask why I print then clean then print, I personally don't know.
                        cprint('\033[2K')
                        cprint(f"{YLW}Word suggestion is ON, but '{WORDLIST_FILE}' file is missing!{RS}")
                        separator(end='')
                        
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
            return client, chat, http_client

        except ClientError as error:
            catch_client_error_startup(error)
            help()
            sys_exit(1)
        
        except ServerError as error:
            catch_server_error_startup(error_occurred, attempts)
            error_occurred = True
            attempts += 1
            continue
            
        except NetworkExceptions:
            catch_network_error()
            sys_exit(1)

def get_user_input():
    """
    Handle prompt_toolkit input and catch Ctrl-C/Ctrl-D.
    NOTE: User input will never be striped or trimmed, it'll be sent as it is,
    we only use some stripped copies of it to beautify the output.
    """
    # Set input options.
    rprompt = None
    if INFORMATIVE_RPROMPT:
        current_time = datetime.now().strftime('%I:%M %p')
        rprompt = f"[{GEMINI_MODEL} | {current_time}]"

    # Stream input.
    try:
        user_input = prompt(
            # Main options
            message=prompt_message,
            placeholder=prompt_placeholder,
            prompt_continuation='....... ',
            multiline=True,
            wrap_lines=True,
            
            # Other options
            style=prompt_style,
            key_bindings=keys,
            mouse_support=True,
            history=history,
            auto_suggest=auto_suggest,
            completer=word_completer,
            complete_while_typing=bool(word_completer),
            rprompt=rprompt,
            bottom_toolbar=prompt_bottom_toolbar,
            editing_mode=VIM_EMACS_MODE,
            reserve_space_for_menu=True,
        )
        
    except Interruption:
        farewell()
        return None
        
    # Return input.
    if user_input.strip():
        return user_input
    else:
        clear_lines(2)
        return None

def get_response():
    """Send the user input to AI and wait to receive the response."""
    try:
        # 1. Preparation.
        cprint()
        status_messages = [
            f'[bold {WAIT_1}]Sending message...[/bold {WAIT_1}]',
            f'[bold {WAIT_1}]Analysis...[/bold {WAIT_1}]',
            f'[bold {WAIT_1}]Thinking...[/bold {WAIT_1}]',
            f'[bold {WAIT_1}]Generating response...[/bold {WAIT_1}]',
            f'[bold {WAIT_1}]Receiving response...[/bold {WAIT_1}]',
            f'[bold {WAIT_2}]Response is taking longer than usual...[/bold {WAIT_2}]',
        ]
        
        response = None
        failed = False
        
        # First server error will be forgiven.
        for _ in range(2):
            try:
                # raise ClientError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
                # raise ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
                # raise httpx.HTTPError(message='Test' * 25)
                # raise Exception('Test' * 25)

                # Initialize the worker thread (A thread instance can only be started once, so we create it here).
                worker = GeminiWorker(chat, user_input)
                active = worker.is_alive
                worker.start()

                # Loop while the worker thread is still running & Update the status at random intervals.
                with console.status(status=status_messages[0], spinner=SPINNER) as status:
                    message_index = 0
                    while active():
                        # Sleep in short, responsive chunks.
                        delay = randint(*STATUS_UPDATE_DELAY)
                        slept_time = 0.0
                        while active() and (slept_time < delay):
                            worker.join(SLEEP_INTERVAL)
                            slept_time += SLEEP_INTERVAL
                        
                        if active() and (len(status_messages) == 1):
                            status.update(status=status_messages[0])

                        elif active() and (message_index < len(status_messages) - 1):
                            message_index += 1
                            status.update(status=status_messages[message_index])


                
                if worker.exception: raise worker.exception
                response = worker.response
                clear_lines()
                break

            except ServerError:
                if failed:
                    clear_lines()
                    raise
                else:
                    failed = True
                    status_messages = [f'[bold {WAIT_2}]Hold on, trying hard to get the response...[/bold {WAIT_2}]']
                    continue
            
            except:
                clear_lines()
                raise
                    
    except ServerError:
        response = catch_server_error_in_chat()
            
    except ClientError as error:
        catch_client_error_in_chat(error)

    except NetworkExceptions:
        catch_network_error()
 
    except Interruption:
        catch_keyboard_interrupt()
    
    except Exception as error:
        catch_exception(error)
    
    finally:
        if not response: clear_lines()
        
    return response

def print_response(response):
    """Print the AI response."""
    try:
        # raise EOFError
        # raise Exception
        
        # Prepare the response
        cprint(f"{GEM_BG}{GR}\n Gemini: {RS}")
        
        # Display response according to the effect.
        if RESPONSE_EFFECT == 'line':
            print_markdown_line(response.text)
        
        elif RESPONSE_EFFECT == 'word':
            print_markdown_word(response.text)
        
        elif 'char' in RESPONSE_EFFECT:
            print_markdown_char(response.text)
        
        else:
            formatted_response = Markdown(response.text)
            
            # Clear the hidden console & Print the response to it.
            temp_console.clear()
            temp_console.print(formatted_response)
            
            # Count the number of blank lines at the end of the output (Caused by Markdown() class).
            exported_text = temp_console.file.getvalue()
            lines = exported_text.splitlines()[-15:]
            
            lines_to_remove = 0
            for line in reversed(lines):
                striped_line = ANSI_ESCAPE.sub('', line).strip()
                if not striped_line: lines_to_remove += 1
                else: break
            
            # Print response.
            console.print(formatted_response)
            clear_lines(lines_to_remove)
            stdout_flush()
    
    except Interruption:
        cprint()
        box(
            f'{GR}Response blocked (but saved!), skipping the rest of it...',
            title='KEYBOARD INTERRUPTION',
            border_color=GR,
        )
        clear_lines()

    except Exception as error:
        catch_exception(error)
    
def run_chat():
    """Handles the user input and Gemini responses."""
    global user_input
    while True:
        try:
            # Get user input
            user_input = get_user_input()
            if not user_input: continue
            
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
                terminal(CLEAR_COMMAND)
                continue
            
            # Get & Print Response
            response = get_response()
            if not response: continue
            print_response(response)
     
        except Interruption:
            farewell()
            continue







# 6) Part VI: Remaining Global Objects & Start Point ---------------------------
# Define global variables.
confirm_separator = True                        # Before confirming to quit, print a separator only if no precedent one was already displayed.
word_completer = None                           # Has a True value only if the PROMPT_HISTORY_FILE is present and WORD_SUGGESTION is True.
keys = Keys().get_key_bindings()                # The custom keyboard shortcuts.
chat_saved = False                              # True after the chat has been saved.

# Define global constants.
CONTENT_WIDTH = CONSOLE_WIDTH - 4               # The width of characters inside box(), (4) is the sum of left & right borders.
CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[mK]')  # Used to clean a string from ANSI codes.
WORD_AND_SPACE_PATTERN = re.compile(r'(\s+)')   # Used split lines into words, for word-by-word animation.
HISTORY_PATTERN = re.compile(                   # Used to shrink PROMPT_HISTORY_FILE to a valid history step.
    r'^#\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+$',
    re.MULTILINE
)

# Assign modules functions (To avoid repeated name resolution/lookup).
terminal = os.system                            # Sends commands to the system.
sys_exit = sys.exit
stdout_write = sys.stdout.write                 # Write to stdout.
stdout_flush = sys.stdout.flush                 # Flush the stdout for immediate output displaying.

# Create necessary instances.
history = FileHistory(PROMPT_HISTORY_FILE)      # Prompt history file path (To cycle through history while streaming input).
if SUGGEST_FROM_HISTORY: auto_suggest = AutoSuggestFromHistory()
else: auto_suggest = None                       # Suggest words based on user prompt history.
console = Console(width=CONSOLE_WIDTH)          # Our main console, though not always used.
temp_console = Console(                         # A hidden console to capture uncertain output before displaying it.
    file=io.StringIO(),
    width=CONSOLE_WIDTH,
    force_terminal=True
)

prompt_message = FormattedText([                       # User prompt message.
    (f'bg:{PROMPT_BG} fg: black', '\n You > '),
    ('', ' '), # Unstyled part                                 
])

prompt_placeholder = FormattedText([                   # User prompt placeholder.
    (PROMPT_FG, 'Ask Gemini...')
])

prompt_bottom_toolbar = None                           # User prompt toolbar.
if BOTTOM_TOOLBAR:
    prompt_bottom_toolbar = '\nKeys: (UP/DOWN) history | (CTRL-SPACE) new line | (CTRL-Z/CTRL-Y) undo/redo'
    prompt_bottom_toolbar += '\nCommands: (quit/exit) leave | (clear) clear screen | (help) guide'

prompt_style = Style.from_dict({                       # User prompt style.
    'rprompt': PROMPT_FG, 
    'prompt-continuation': PROMPT_FG, 
    'bottom-toolbar': f'bg:{PROMPT_FG} fg: black', 
}) 



if __name__ == "__main__":
    try:
        # Load & Start chat client & session.
        client, chat, http_client = setup_chat()
        if chat:
            # raise ValueError('Test' * 25)
            # raise KeyboardInterrupt
            run_chat()
            
    except Interruption:
        farewell()
    
    except SystemExit:
        pass

    except Exception as error:
        try:
            catch_fatal_exception(error)
        except Interruption:
            separator('\n', color=RED)
            sys_exit(1)
    
    finally:
        # Release HTTP client.
        try: http_client.close()
        except: pass
        # Secret save.
        if not chat_saved:
            with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
                save_chat_history()
