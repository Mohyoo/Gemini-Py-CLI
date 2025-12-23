# 1) Part I: Initialization ------------------------------------------------------------------------
if __name__ == '__main__':
    # Loading Screen.
    from settings import console_width
    print('\n┌' + '─' * (console_width - 2) + '┐')
    print('│ Loading libraries. Just a moment...' + ' ' * (console_width - 38) + '│')
    print('└' + '─' * (console_width - 2) + '┘')

    # Change current working directory to the script's dir, to keep it portable.
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

# Import Custom Modules.
try:
    from settings import *
    if ERROR_LOG_ON: from error_logger import log_caught_exception, LOG_SEPARATOR
    if GLOBAL_LOG_ON: from global_logger import setup_global_console_logger, in_time_log

except ImportError as error:
    print(f'\nError: {error}.')
    print('Reinstall the program to restore the missing file.')
    quit(1)
    
except (KeyboardInterrupt, EOFError):
    quit(0)

# Import Libraries.
try:
    # Necessary (The slowest one to import here is google.genai, others are negligeable).
    import re
    import io
    import sys
    import json
    import httpx
    import textwrap
    import traceback
    from webbrowser import open as browser_open
    from random import randint, choice, uniform
    from time import sleep, perf_counter, time as now_time
    from shutil import copy as copy_file, move as move_file
    from pyperclip import PyperclipException, copy as clip_copy
    from threading import Thread, Event as ThreadEvent, Lock as ThreadLock
    from subprocess import Popen as NewProcess, CREATE_NEW_CONSOLE as NEW_CONSOLE_FLAG
    from httpcore import RemoteProtocolError, ConnectError, ConnectTimeout, ReadTimeout
    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.formatted_text import FormattedText
    from prompt_toolkit.validation import Validator, ValidationError
    from google.genai import Client as GemClient
    from google.genai.types import Content, Part
    from google.genai.errors import ClientError, ServerError
    from rich.theme import Theme
    from rich.console import Console
    from rich.markdown import Markdown
    
    # Conditional.
    if os.name == 'posix':
        import termios
        
    elif os.name == 'nt':
        import msvcrt
        
    if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON:
        from google.genai.types import GenerateContentConfig
    
    if SAVED_INFO:
        import difflib
        import heapq
    
    if SUGGEST_FROM_WORDLIST and SUGGEST_FROM_WORDLIST_FUZZY:
        from prompt_toolkit.completion import FuzzyWordCompleter as WordCompleter
        
    elif SUGGEST_FROM_WORDLIST:
        from prompt_toolkit.completion import WordCompleter
            
    if SUGGEST_FROM_HISTORY:
        from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    
    if PROMPT_HISTORY_ON and PROMPT_HISTORY_MEMORY:
        from prompt_toolkit.history import InMemoryHistory as PromptHistory
    
    elif PROMPT_HISTORY_ON:
        from prompt_toolkit.history import FileHistory as PromptHistory
        
    if RESPONSE_EFFECT:
        from rich.text import Text 
        from rich.segment import Segment
        from rich.console import RenderResult
    
    if RESPONSE_EFFECT == 'char fast':
        from math import isclose as math_isclose

    if INPUT_HIGHLIGHT == 'special':
        from prompt_toolkit.lexers import PygmentsLexer
        from pygments.lexer import RegexLexer, words
        from pygments.token import Comment, Operator, Keyword, String, Generic, Text as Plain

    elif INPUT_HIGHLIGHT:   
        from prompt_toolkit.lexers import PygmentsLexer
        from pygments.lexers import get_lexer_by_name
    
    if VIM_EMACS_MODE:
        from prompt_toolkit.enums import EditingMode
    
    if BOTTOM_TOOLBAR:
        from prompt_toolkit.formatted_text import HTML
    
    if INFORMATIVE_RPROMPT:
        from datetime import datetime
    
    if DYNAMIC_CONSOLE_WIDTH: 
        from functools import partial
    
except ImportError as error:
    print(f'\nError: {error}.')
    print("Use 'pip' to install the missing modules.")
    print("E.g: open CMD & type: pip install httpx rich")
    quit(1)
    
except (KeyboardInterrupt, EOFError):
    quit(0)


# Prepare the global logger.
if GLOBAL_LOG_ON:
    # Define the visual clutter to hide from global log.
    OMIT_LIST = [
        # "Keys: (UP/DOWN)",
        # "Commands: (quit/exit)",
    ]

    # Initialize.
    setup_global_console_logger(ignore_strings=OMIT_LIST)









# 2) Part II: Classes ------------------------------------------------------------------------------
class Keys():
    """
    Define & implement keyboard shortcuts for user prompt.
    Hotkeys() class is in 'settings.py'.
    """
    # Define constants at the class level.
    if ENTER_NEW_LINE:
        SUBMIT = Hotkeys.SUBMIT
        NEW_LINE = Hotkeys.NEW_LINE
    else:
        SUBMIT = Hotkeys.SUBMIT
        NEW_LINE = Hotkeys.NEW_LINE

    TAB = Hotkeys.TAB
    CANCEL = Hotkeys.CANCEL
    INTERRUPT = Hotkeys.INTERRUPT
    UNDO = Hotkeys.UNDO
    REDO = Hotkeys.REDO
    COPY = Hotkeys.COPY
    F_KEYS = Hotkeys.F_KEYS

    # Define variables.
    redo_fallback_stack = []
    
    def get_key_bindings(self):
        """Create and return the KeyBindings object with all custom bindings."""
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
            self.wrap_input_buffer(event)
            self.save_history(original_text)
            event.cli.exit(result=original_text)
            
        # @key_bindings.add('c-v', eager=True)
        # def _(event):
            # """
            # Handle text paste instead of the terminal.
            # To avoid long text lag and help show long paste warning.
            # """
            # # Stop the terminal from also handling Ctrl+V
            # event.prevent_default()
    
            # # Access the clipboard.
            # clipboard = event.cli.clipboard
            # text = clipboard.get_data().text
            # if not text: return
            
            # # Insert it into the current buffer, split it to avoid lag.
            # j = 100
            # chunks = [text[i:i+j] for i in range(0, len(text), j)]
            # for chunk in chunks: event.current_buffer.insert_text(chunk)
        
        @key_bindings.add(self.TAB)
        def _(event):
            """Insert a tab (4 spaces)."""
            event.cli.current_buffer.insert_text('    ')        
        
        @key_bindings.add(self.UNDO)
        def _(event):
            """
            Undo the last change.
            Only pushes a state to the REDO stack if the text actually changes.
            """
            # Undo.
            buffer = event.cli.current_buffer
            before_undo = buffer.text
            buffer.undo()
            
            # Store the change for fallback redo.
            after_undo = buffer.text
            if before_undo != after_undo:
                self.redo_fallback_stack.append(before_undo)
                length = len(self.redo_fallback_stack)
                if length >= 100: self.redo_fallback_stack.pop(0)
            
        @key_bindings.add(self.REDO)
        def _(event):
            """
            Redo the last undone change.
            Use a manual method if the original one fails.
            """
            # Try the original method.
            buffer = event.cli.current_buffer
            before_redo = buffer.text
            buffer.redo()
            after_redo = buffer.text
            
            # If it doesn't work, try the secondary method (Less reliable but fine).
            if (before_redo == after_redo) and (self.redo_fallback_stack):
                restored_text = self.redo_fallback_stack.pop()
                buffer.text = restored_text
                buffer.cursor_position = self.first_diff_index(before_redo, restored_text) + 1
        
        @key_bindings.add(self.COPY)
        def _(event):
            """Copy the current buffer text."""
            buffer = event.cli.current_buffer
            text = buffer.text
            if not text: return
            if not text[-1].isspace(): buffer.insert_text(' ')        
            
            try:
                # Copy (pyperclip handles the OS-specific details).
                clip_copy(text)
                buffer.insert_text('[Prompt Copied!]')        
                    
            except:
                if ERROR_LOG_ON: log_caught_exception()
                buffer.insert_text('[Copy Error!]')        

        
        @key_bindings.add(self.CANCEL, eager=True)
        def _(event):
            """Hides the autocompletion menu when ESC is pressed."""
            buffer = event.cli.current_buffer

            # If the suggestion menu is currently open/active, cancel & close the menu.
            if SUGGEST_FROM_WORDLIST and buffer.complete_state:
                buffer.cancel_completion()
        
        for key, command in self.F_KEYS.items():
            @key_bindings.add(key)
            def _(event, command=command):
                """
                Quickly execute a command by its F-Key.
                * 'command=command': This captures the value (F-Key command) immediately
                                     and fix it for this function.
                """
                original_text = event.cli.current_buffer.text
                if SAVE_INPUT_ON_STOP: self.save_history(original_text)
                command = '/' + command
                event.cli.current_buffer.text = command
                event.cli.exit(result=command)

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
                    # If there is a text, clear it.
                    if SAVE_INPUT_ON_CLEAR: self.save_history(original_text)
                    buffer.text = ''
                    buffer.cursor_position = 0
                    buffer.save_to_undo_stack()
                else:
                    # If empty, quit input.
                    self.trim_input_buffer(event)
                    if SAVE_INPUT_ON_STOP: self.save_history(original_text)
                    event.cli.exit(exception=KeyboardInterrupt())
        
        return key_bindings
    
    def trim_input_buffer(self, event):
        """Strip/trim leading & trailing whitespaces."""
        # Get the input text & trim it.
        buffer = event.cli.current_buffer
        current_text = buffer.text
        stripped_text = current_text.lstrip('\n').rstrip() 
        
        # Replace the entire text content.
        if current_text != stripped_text:
            buffer.text = stripped_text

    def wrap_input_buffer(self, event):
        """Wrap the input & Break it into shorter lines."""
        buffer = event.cli.current_buffer
        WRAP_WIDTH = console_width - 8
        wrapped_segments = []

        for line in buffer.text.splitlines():
            if line.strip():
                wrapped_line = textwrap.wrap(line, width=WRAP_WIDTH)
                wrapped_segments.extend(wrapped_line)
            else:
                wrapped_segments.append(' ')
        
        wrapped_text = '\n'.join(wrapped_segments)
        buffer.text = wrapped_text
 
    def save_history(self, prompt):
        """Save the current prompt to history, if conditions are met."""
        if not prompt.strip(): return
        history_prompts = list(history.get_strings())
        if not history_prompts:
            # Prompt history is empty, save directly.
            history.append_string(prompt)
        else:
            # Prompt history isn't empty, check for duplication.
            last_saved_prompt = history_prompts[-1]
            if prompt.strip() != last_saved_prompt.strip():
                history.append_string(prompt)
    
    def first_diff_index(self, s1, s2):
        """Return the exact point that two strings differ at."""
        min_len = min(len(s1), len(s2))
        for i in range(min_len):
            if s1[i] != s2[i]: return i
        
        return min_len

class GeminiWorker(Thread):
    """
    - A worker thread to run & control the asynchronous (unblockable) API call.
    - Set to 'daemon' so the thread is terminated automatically on main program
      exit or on exception (like KeyboardInterrupt).
    """
    def __init__(self, chat_session, user_input, *args, **kwargs):
        """initialize worker attributes."""
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.send_message = chat_session.send_message
        self.user_input = user_input
        self.response = None
        self.exception = None

    def run(self):
        """The main execution of the thread - API call."""
        try:
            self.response = self.send_message(self.user_input)
        except Exception as error:
            self.exception = error

class SoftRestart(Exception):
    """Custom exception to signal a safe restart of the chat session."""
    pass

if SUGGEST_FROM_WORDLIST:
    class LimitedWordCompleter(WordCompleter):
        """Override WordCompleter to enforce a limit on the number of returned completions."""
        def get_completions(self, document, complete_event):
            # Do not complete after whitespaces.
            if document.text.endswith((' ', '\t', '\n', '\r', '\x0b', '\x0c')):
                return
                
            # Call the base class's method to get all completions.
            all_completions = super().get_completions(document, complete_event)

            # Iterate over the generator and only yield the first limited set of completions.
            for i, completion in enumerate(all_completions):
                if i >= SUGGESTIONS_LIMIT: break
                yield completion

if DYNAMIC_CONSOLE_WIDTH:  
    class ConsoleWidthUpdater(Thread):
        """
        A separate thread class to monitor the console width variable and keep it lower
        than MAX_CONSOLE_WIDTH, which itself is lower than the real terminal size.
        So always ensure: console_width <= MAX_CONSOLE_WIDTH < real terminal size.
        """
        def __init__(self):
            """Initialize attributes."""
            super().__init__()
            self.daemon = True
            self.interval = 0.2
            self._stop_event = ThreadEvent()
            self.lock = ThreadLock()
            self.last_terminal_width = terminal_size().columns
            
            # Store the original copy of modiffied functions to avoid infinite nesting of partial objects.
            self.original_cprint = cprint
            self.original_separator = separator
            self.original_box = box

        def update_console_width(self):
            """Keep updating the console width as the terminal size changes."""
            global console_width, glitching_text_width, console, temp_console, \
                   cprint, separator, box
            
            # Do nothing if the terminal width didn't change.
            current_width = terminal_size().columns
            if (current_width == self.last_terminal_width) and \
               (console_width <= MAX_CONSOLE_WIDTH < current_width):
                return

            # Also do nothing if terminal became wider, but our console width is already in its MAX value.
            elif (current_width > self.last_terminal_width) and \
                 (console_width == MAX_CONSOLE_WIDTH):
                self.last_terminal_width = current_width
                return

            # Start Updating.
            self.last_terminal_width = current_width

            # Update the console width variable and its derived variables & attributes.
            console_width = min(MAX_CONSOLE_WIDTH, current_width - 1)
            glitching_text_width = min(console_width, 79)
            console.width = console_width
            temp_console.width = console_width

            # Update functions' default width parameter.
            cprint = partial(self.original_cprint, wrap_width=console_width-1)
            separator = partial(self.original_separator, width=console_width)
            box = partial(self.original_box, width=console_width)

        def run(self):
            """
            The main loop for the continuous check of the console width variable.
            Sleep for a short duration to avoid the CPU busy-loop (spin-wait).
            """
            # Loop until the stop event is set or the main program exits (daemon).
            while not self._stop_event.is_set():
                with self.lock: self.update_console_width()
                sleep(self.interval)

        def stop(self):
            """Method to externally signal the thread to stop."""
            self._stop_event.set()

if VALIDATE_INPUT:
    class LengthValidator(Validator):
        """A class used to check/validate user input while typing."""
        last_length = 0
        last_diff = 0
        
        def validate(self, document):
            """
            Warn the user if he types a very long prompt, but still allow him to submit.
            Warn only for a short while to avoid annoyance & glitches.
            """
            # Get terminal size & text length.
            columns, rows = terminal_size()
            marker = len(line_continuation)
            x = columns - marker - 1    # (x) = one line of the text field, without the margins.
            text = document.text
            characters = len(text)
            
            # Warn about long paste.
            difference = characters - self.last_length
            self.last_length = characters
            self.last_diff = difference
            if difference > 48 and self.last_diff > 48:
                self.warn('Long paste! Might feel slow & hide upper text...')
            
            # Warn about N° of characters.
            if 4096 <= characters <= 4256:
                self.warn('WARNING! You typed more than 4000 characters!')

            # Calculate occupied terminal rows (text lines + rprompt + toolbar).
            used_rows = 0
            lines = text.splitlines()
            for line in lines:
                used_rows += len(line) // x + 1
            
            if BOTTOM_TOOLBAR: used_rows += 3
            if INFORMATIVE_RPROMPT: used_rows += 1
            # raise ValidationError(message=f'{used_rows}/{rows}')
   
            # Warn if terminal space isn't enough for text.
            if 0 <= used_rows - rows <= 3:
                self.warn('Long prompt! Some text is now hidden (You can use CTRL+X-CTRL+E)')
        
        def warn(self, message):
            """Leave this validator & Show a warning."""
            raise ValidationError(message=message)

if INPUT_HIGHLIGHT == 'special':
    class CustomLexer(RegexLexer):
        """
        A custom syntax highlighting lexer for user prompts.
        Accept both normal strings and regex.
        """
        # Define the special words first. Then other characters.
        KEYWORDS = [
            # Articles & Determiners.
            'the', 'a', 'an',
            'this', 'that', 'these', 'those',
            'each', 'every', 'some', 'any', 'all',
            'another', 'such', 'certain', 'particular', 'specific',
            'none', 'many', 'few', 'more', 'most', 'less', 'least', 'much', 'enough',

            # Personal Pronouns.
            'I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',

            # Possessive Pronouns & Adjectives.
            'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs',

            # Reflexive Pronouns.
            'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves',

            # Indefinite Pronouns.
            'anyone', 'someone', 'everyone', 'anybody', 'everybody', 'nobody',
            'anything', 'something', 'everything', 'nothing',

            # Relative / Interrogative Pronouns.
            'who', 'whom', 'whose', 'which', 'what', 'whoever', 'whomever', 'whichever', 'whatever',

            # Prepositions.
            'of', 'at', 'in', 'for', 'with', 'on', 'to', 'from', 'by',
            'about', 'as', 'into', 'like', 'through', 'after', 'over',
            'out', 'against', 'without', 'before', 'under', 'around',
            'among', 'above', 'near', 'beyond', 'within', 'along',
            'across', 'behind', 'below', 'beneath', 'beside', 'between',
            'during', 'except', 'inside', 'outside', 'per',
            'toward', 'upon', 'versus', 'via',
            'onto', 'amid', 'amidst', 'off', 'past',
            'throughout', 'till',

            # Coordinating.
            'and', 'but', 'or', 'so', 'yet', 'nor',

            # Subordinating.
            'although', 'because', 'since', 'unless', 'while', 'whereas', 'if', 'else', 'though',

            # Correlative.
            'either', 'neither', 'both', 'whether',

            # Time Adverbs.
            'now', 'then', 'soon', 'still', 'today', 'tomorrow', 'yesterday',
            'once', 'until', 'already', 'almost', 'meanwhile',

            # Frequency Adverbs.
            'always', 'never', 'often', 'sometime', 'sometimes', 'rarely',

            # Degree / Emphasis Adverbs.
            'too', 'also', 'only', 'rather', 'quite', 'really', 'especially', 'very',

            # Logical / Discourse Adverbs.
            'however', 'therefore', 'thus', 'otherwise',

            # Main Verb Forms.
            'do', 'does', 'did', 'doing', 'done',
            'have', 'has', 'had', 'having',
            'be', 'am', 'is', 'are', 'was', 'were', 'been', 'being',

            # Modal Verbs.
            'can', 'could', 'will', 'would',
            'shall', 'should', 'may', 'might',
            'must', 'ought',
            "don't", "doesn't", "didn't",
            "can't", "couldn't",
            "won't", "wouldn't",
            "isn't", "aren't", "wasn't", "weren't",
            "haven't", "hasn't", "hadn't",
            "shouldn't", "mustn't", "ain't",

            # Question / Relative Adverbs.
            'where', 'when', 'why', 'how', 'wherever', 'whenever', 'however',

            # Quantity / Order / Sequence Words.
            'several', 'first', 'second', 'last', 'next', 'previous',
            'moreover', 'likewise',

            # Miscellaneous.
            'maybe', 'perhaps',
            'here', 'there',
            'not', 'no',
            'instead', 'than',
        ]
    
        NAMES = [
            # People.
            'Muhammed', 'Muhammad', 'Adam', 'Eve', 'Noah', 'Abraham', 'Moses',
            'David', 'Solomon', 'Joseph', 'Jacob', 'Isaac', 'Aaron', 'Jesus',
            'Mary', 'Daniel', 'Ishmael', 'Gabriel', 'Michael ',

            # Animals.
            'cat', 'dog', 'horse', 'cow', 'sheep', 'goat', 'chicken', 'duck', 'pig',
            'rabbit', 'mouse', 'rat', 'lion', 'tiger', 'elephant', 'bear', 'wolf', 'fox',
            'monkey', 'deer', 'camel', 'donkey', 'buffalo', 'zebra', 'giraffe', 'kangaroo',
            'panda', 'leopard', 'cheetah', 'eagle', 'hawk', 'owl', 'parrot', 'pigeon',
            'sparrow', 'fish', 'shark', 'whale', 'dolphin', 'turtle', 'snake', 'lizard',
            'frog', 'bee', 'butterfly', 'ant', 'spider',

            # Things.
            'earth', 'sun', 'moon', 'sky', 'star', 'world', 'land', 'sea', 'ocean', 'water',
            'river', 'mountain', 'stone', 'rock', 'fire', 'light', 'dark', 'time', 'day',
            'night', 'life', 'death', 'wind', 'rain', 'tree', 'forest', 'leaf', 'root',
            'seed', 'flower', 'fruit', 'food', 'home', 'house', 'family', 'mother',
            'father', 'friend', 'heart', 'mind', 'soul', 'body', 'book', 'story', 'path',
            'road', 'hand', 'eye', 'face', 'blood', 'gold', 'silver', 'iron',

            # Plural Animals.
            'cats', 'dogs', 'horses', 'cows', 'sheep', 'goats', 'chickens', 'ducks', 'pigs',
            'rabbits', 'mice', 'rats', 'lions', 'tigers', 'elephants', 'bears', 'wolves', 'foxes',
            'monkeys', 'deer', 'camels', 'donkeys', 'buffaloes', 'zebras', 'giraffes', 'kangaroos',
            'pandas', 'leopards', 'cheetahs', 'eagles', 'hawks', 'owls', 'parrots', 'pigeons',
            'sparrows', 'fish', 'sharks', 'whales', 'dolphins', 'turtles', 'snakes', 'lizards',
            'frogs', 'bees', 'butterflies', 'ants', 'spiders',

            # Plural Things.
            'earths', 'suns', 'moons', 'skies', 'stars', 'worlds', 'lands', 'seas', 'oceans', 'waters',
            'rivers', 'mountains', 'stones', 'rocks', 'fires', 'lights', 'darks', 'times', 'days',
            'nights', 'lives', 'deaths', 'winds', 'rains', 'trees', 'forests', 'leaves', 'roots',
            'seeds', 'flowers', 'fruits', 'foods', 'homes', 'houses', 'families', 'mothers',
            'fathers', 'friends', 'hearts', 'minds', 'souls', 'bodies', 'books', 'stories', 'paths',
            'roads', 'hands', 'eyes', 'faces', 'bloods', 'golds', 'silvers', 'irons',
        ]
        
        HEAVY_WORDS = [
            # 🚨 Urgency / Danger.
            'warning', 'alert', 'critical', 'danger', 'hazard', 'threat', 'risk',
            'emergency', 'fatal', 'catastrophic', 'lethal', 'deadly', 'unsafe',

            # ❌ Failure / Consequences.
            'error', 'mistake', 'failure', 'fault', 'violation', 'breach',
            'breakdown', 'collapse', 'malfunction', 'flaw', 'defect',

            # 🔒 Authority / Severity.
            'strict', 'mandatory', 'required', 'forbidden', 'prohibited',
            'enforced', 'force',

            # 📌 Importance.
            'important', 'essential', 'necessary', 'vital', 'crucial', 'key',
            'core', 'fundamental', 'central', 'primary',

            # ⚠️ Intensity / Extremes.
            'extreme', 'intense', 'severe', 'drastic', 'brutal', 'overwhelming',
            'relentless', 'immense', 'massive', 'colossal',

            # ⭐ Success / Achievement.
            'success', 'victory', 'breakthrough', 'triumph', 'achievement',
            'accomplishment', 'milestone',

            # 🌟 Impact / Praise (attention-grabbing positives).
            'special', 'exceptional', 'remarkable', 'extraordinary',
            'outstanding', 'phenomenal', 'legendary', 'iconic',

            # 🎯 Precision / Certainty.
            'exact', 'exactly', 'precise', 'definitive', 'conclusive',
            'undeniable', 'absolute', 'certain', 'final',

            # 🔴 Serious Thought / Weight.
            'consequence', 'implication', 'responsible', 'responsibility',
            'accountability', 'commitment', 'decision', 'judgment', 'priority',

            # 🚀 Awe / Power Words.
            'amazing', 'awesome', 'fantastic', 'incredible', 'mindblowing',
            'jawdropping', 'unstoppable', 'dominant','great', 'brilliant',
            'beautiful', 'wonderful',
            
            # Plural Form of Previous Words.
            'warnings', 'alerts', 'dangers', 'hazards', 'threats', 'risks', 'emergencies',
            
            'errors', 'mistakes', 'failures', 'faults', 'violations', 'breaches',
            'breakdowns', 'collapses', 'malfunctions', 'flaws', 'defects',

            'forces', 'keys', 'cores', 'fundamentals', 'centrals', 'primaries',

            'successes', 'victories', 'breakthroughs', 'triumphs', 'achievements',
            'accomplishments', 'milestones',

            'consequences', 'implications', 'responsibilities', 'accountabilities',
            'commitments', 'decisions', 'judgments', 'priorities',
        ]
        
        PUNCTUATION = r'.,;،؛:!?…'
        PARENTHESES = r'\[\]\(\)\{\}'
        SYMBOLS = r'\-+*/%=×÷<>^&|~@$_\\'

        # Define colors (In fact, these aren't colors but tokens that work under a specific style/theme, I'm just simplifying it).
        WHITE = Plain
        RED  = String
        PURPLE = Generic.Subheading
        BLUE = Operator.Word
        CYAN = Keyword
        GRAY_BLUE = Comment
        GRAY = Operator
        
        # Set the tokenization system.
        tokenize = lambda wordlist: words(set(wordlist), prefix=r'\b', suffix=r'\b')  # We use prefix & suffix to add boundaries.
        flags = re.IGNORECASE 
        tokens = {
                'root': [
                    # Wordlists.
                    (tokenize(HEAVY_WORDS), RED),
                    (tokenize(KEYWORDS), PURPLE),
                    (tokenize(NAMES), CYAN),
                    # Digits & Quotes.
                    (r'\d+', GRAY_BLUE),
                    (r'([\"`])(.*?)\1', BLUE),  # "" or ``
                    (fr"(?:(?<=^)|(?<=[\s{PUNCTUATION}{PARENTHESES}{SYMBOLS}#\d]))'(.*?)'(?:(?=$)|(?=[\s{PUNCTUATION}{PARENTHESES}{SYMBOLS}#\d+]))", BLUE), # ''
                    (fr"(?:(?<=^)|(?<=[\s{PUNCTUATION}{PARENTHESES}{SYMBOLS}#\d]))‘(.*?)’(?:(?=$)|(?=[\s{PUNCTUATION}{PARENTHESES}{SYMBOLS}#\d+]))", BLUE), # ‘’
                    (r'“([^”]*)”', BLUE), # “”
                    # Punctuation • Parentheses • Other Symbols • Hashtags.
                    (fr'[{PUNCTUATION}]+', GRAY),
                    (fr'[{PARENTHESES}]+', GRAY),
                    (fr'[{SYMBOLS}]+', GRAY),
                    (r'#\s*(\w+)', GRAY),
                    # Match everything else as standard text.
                    (r'\s+', WHITE),
                    (r'.', WHITE),
                ]
            }




# 3) Part III: Error Handlers ----------------------------------------------------------------------
NetworkExceptions = (
    ConnectionError,
    ReadTimeout,
    ConnectTimeout,
    ConnectError,
    RemoteProtocolError,
    httpx.ReadTimeout,
    httpx.HTTPError,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
)

Interruption = (
    KeyboardInterrupt,
    EOFError,
)

def catch_no_api_key():
    """Used in setup_chat() if the API key placeholder wasn't changed."""
    msg_1 = "Please replace 'YOUR_API_KEY_HERE' in 'settings.py' with your actual key."
    msg_2 = "You'll find the key placeholder at the first few lines.\n"
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}Showing the quick help menu..."
    box(msg_1, msg_2, msg_3, msg_4, title='NO API KEY PROVIDED', border_color=RED, text_color=RED)

def catch_client_error_startup(error):
    """Used in setup_chat() if STARTUP_API_CHECK is True & the API validation encounters a client side error."""
    if ERROR_LOG_ON: log_caught_exception()
    msg_1 = f"{RED}Client side error occurred:\n{RED}{error.message}.\n"
    msg_2 = f"{RED}Check your settings, especially the API key validation or limits."
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}(Remember that it requires a google account)\n"
    msg_5 = f"{GR}Showing the quick help menu...{RS}"
    box(msg_1, msg_2, msg_3, msg_4, msg_5, title='CLIENT SIDE ERROR', border_color=RED, text_color=RED, secondary_color=RED)

def catch_client_error_in_chat(error):
    """Used in get_response() upon a client side error."""
    if ERROR_LOG_ON: log_caught_exception()
    msg_1 = f"{RED}Client side error occurred:\n{RED}{error.message}\n"
    msg_2 = f"{YLW}Check your settings, especially the API key validation or limits."
    msg_3 = f"{YLW}If you exceeded characters limit (like hundreds of thousands of\n{YLW}characters), shorten your prompt!"
    msg_4 = f"{YLW}Restarting the session might also help (Type 'restart')."
    box(msg_1, msg_2, msg_3, msg_4, title='CLIENT SIDE ERROR', border_color=RED, text_color = RED, secondary_color=RED)

def catch_server_error_startup(error_occurred, attempts):
    """Used in setup_chat() if STARTUP_API_CHECK is True & the API validation encounters a google server error."""
    if ERROR_LOG_ON: log_caught_exception()
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = SERVER_ERROR_ATTEMPTS, *SERVER_ERROR_DELAY
    if not error_occurred:
        separator('\n', color=RED)
        cprint(f"{RED}A temporary server problem occurred.")
        cprint(f'It might be a service overloading, maintenance or backend errors...')
    
    # Try to reconnect within limited attempts.
    if attempts < SERVER_ERROR_ATTEMPTS:
        try:
            if not error_occurred: print_status(lambda: quick_sleep(DELAY_1), f'Retrying in {DELAY_1} seconds...', 'yellow')
            else: print_status(lambda: quick_sleep(DELAY_2), f'Issue persisting, retrying in {DELAY_2} seconds...', 'yellow')
        
        except NetworkExceptions:
            separator(color=RED)
            catch_network_error()
            sys_exit()
            
        except Interruption:
            cprint(f'{GR}Quitting...{RS}')
            separator(color=RED)
            sys_exit(1)
    
    # All attempts failed.
    else:
        cprint(f'{YLW}Tried {MAX_ATTEMPTS} times with no response! Please wait for sometime...{RS}')
        separator(color=RED)
        sys_exit(1)
    
def catch_server_error_in_chat():
    """Used in get_response() upon a google server error."""
    global confirm_separator
    if ERROR_LOG_ON: log_caught_exception()
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = SERVER_ERROR_ATTEMPTS, *SERVER_ERROR_DELAY
    
    confirm_separator = False
    separator('\n', color=RED)
    cprint(f"{RED}A temporary server problem occurred.")
    cprint(f'It might be a service overloading, maintenance or backend errors...')
    
    # Wait for first delay.
    try:
        print_status(lambda: quick_sleep(DELAY_1), f'Retrying in {DELAY_1} seconds...', 'yellow')
        
    except Interruption:
        separator(color=RED)
        cprint()
        return
    
    response = None
    for attempt in range(SERVER_ERROR_ATTEMPTS):
        try:
            # raise ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
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
            return
        
        except NetworkExceptions:
            separator(color=RED)
            catch_network_error()
            return
        
        except Interruption:
            separator(color=RED)
            cprint()
            return
    
    # Exit the function.
    confirm_separator = True
    separator(color=RED)
    if not response: cprint()
    return response

def catch_network_error():
    """Used to catch general network issues (System disconnection, DNS, timeout, etc)."""
    global user_input
    if ERROR_LOG_ON: log_caught_exception()
    if restarting: clear_lines()
    error = traceback.format_exc().lower()
    
    # Catch special timeout errors.
    if 'timeout' in error:
        title = 'TIMEOUT'
        msg = f"{RED}API call exceeded the hard timeout limit of ({HTTP_TIMEOUT}) seconds.\n"
        msg += f"{RED}Please, wait for sometime until the network becomes stable.\n"
        msg += f"{YLW}You can change the HTTP timeout delay in settings."
    
    # Catch other network issues.
    else:
        title = 'NETWORK ERROR'
        msg = f"{RED}Failed to connect, check your network or firewall!"
        try:
            if user_input and not restarting:
                msg += f"\n{YLW}Press (UP) to get your prompt back."
                user_input = None
        except NameError:
            pass
       
    box(msg, title=title, border_color=RED)
    if restarting: clear_lines()

def catch_exception(error):
    """Used to catch any generic exception that can be forgiven during a chat."""
    global confirm_separator
    if ERROR_LOG_ON: log_caught_exception()
    separator('\n', color=RED)
    
    # Show error & ask the user to see details (If details aren't disabled).
    print_error(f'An error occurred:\n"{error}"')
    if not NO_ERROR_DETAILS:
        try:
            if GLOBAL_LOG_ON: in_time_log("See the details? (y/n): ...")
            see_error = input("See the details? (y/n): ").strip().lower()
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
        
    separator(color=RED, end='\n')

def catch_fatal_exception(error):
    """Used to catch any critical generic exception that bypassed all of the handlers."""
    if ERROR_LOG_ON: log_caught_exception(level='critical')
    separator('\n', color=RED)
    
    # Condolence.
    cprint(f"{GR + BD}Congratulations! You found it. It's a BUG!")
    cprint(f"To be honest, I'm really sorry for that.")
    cprint(f"Please let me know, I'll try to respond as soon as possible.")
    cprint(f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}\n")
    
    print_error(f'A fatal error occurred:\n"{error}"\nAnd the program has to QUIT.')
    
    # Ask to see details if the details options isn't OFF.
    if not NO_ERROR_DETAILS:
        if GLOBAL_LOG_ON: in_time_log("See the details? (y/n): ...")
        see_error = input("See the details? (y/n): ").strip().lower()
        if see_error == 'y':
            cprint(RED + traceback.format_exc().strip() + RS)
        else:
            cprint(f"{YLW}Inhales.. Deep breathing.. Now out.{RS}")
    
    else:
        clear_lines()
        
    save_chat_history_json(hidden=True)
    separator(color=RED)
    sys_exit(1)

def catch_keyboard_interrupt():
    """
    Used in get_response() if the user wants to cancel sending his prompt.
    Google still has a chance to receive the prompt if the cancellation was late.
    """
    msg_1 = f"Prompt cancelled, skipping..."
    msg_2 = f'Rest assured, Google has no idea about what you just sent (probably ;-;).'
    box(msg_1, msg_2, title='KEYBOARD INTERRUPTION', border_color=GR, text_color=GR, secondary_color=GR)








# 4) Part IV: Helper Functions ---------------------------------------------------------------------
def wrapper(text: str, width=console_width-1, joiner='\n'):
    """Wrap a given text to a given line width."""
    lines = text.split('\n')
    wrapped_lines = []
    
    for line in lines:
        if not line.strip():
            wrapped_lines.append(' ')
            continue
            
        new_lines = textwrap.wrap(line, width=width)   # Only wrap if length >= width.
        wrapped_lines.extend(new_lines)
    
    text = joiner.join(wrapped_lines)
    return text
    
def cprint(text='', end='\n', flush=True, wrap=True, wrap_width=console_width-1, wrap_joiner='\n'):
    """
    - A custom print function that writes directly to stdout and guarantees an
      immediate display by forcing a flush.
    - Also wraps the text with optionally a custom width and wrapped lines joiner.
    """
    # Wrap even if (length = console_width) so that '\n' stays in the same line.
    text = str(text)
    if wrap and (visual_len(text) > wrap_width):
        text = wrapper(text, width=wrap_width, joiner=wrap_joiner)
    
    # Print.
    stdout_write(text + end)
    if flush: stdout_flush()

def print_status(action: callable, text='Waiting...', color='green'):
    """
    Display a vital text so that the program doesn't feel stuck.
    The text is temporary & will disappear at the end.
    """
    with console.status(status=f"[bold {color}]{text}[/bold {color}]",
                        spinner=SPINNER):
        action()

def print_error(text: str, style='red', offset=3):
    """
    Display a special message for errors, including time and line.
    
    1) '_stack_offset' argument tells 'Rich' to look further up the call stack
       to find the true originator of the log message. Default to (3): from this
       print_error() -> catch_error_name() -> except statement (what we want).
       
    2) Using quotes inside quotes (e.g: '""') will give the internal quotes
       a special color.
    """
    cprint(RS, end='')
    console.log(text, style=style, _stack_offset=offset, end='\n\n')

def quick_sleep(delay: float):
    """
    Sleep for 'delay' seconds in non-blocking short chunks.
    This allows for the KeyboardInterrupt error to be raised immediately.
    """
    slept_time = 0.0
    while slept_time < delay:
        sleep(SLEEP_INTERVAL)
        slept_time += SLEEP_INTERVAL

def clear_lines(lines_to_erase=1):
    """
    Simulate scanning and cleaning up previous empty lines by using ANSI codes
    to move the cursor up and erase.
    """
    # Skip if not compatible with ANSI escape codes.
    if not USE_ANSI: return
    
    # \033[A:  Move cursor Up one line
    # \033[2K: Erase the entire current line
    for _ in range(lines_to_erase):
        cprint('\033[A\033[2K', end='')
    
def visual_len(text_with_ansi: str):
    """Return the length of the longest line, ignoring ANSI codes."""
    if not text_with_ansi.strip(): return 0
    lines = text_with_ansi.splitlines()
    lines_length = [len(ANSI_ESCAPE.sub('', line)) for line in lines]
    return max(lines_length)

def separator(before='', after='', char='─', color=GRY, width=console_width, end='\n'):
    """Display a line of hyphens or any horizontal symbol."""
    # Used console.print() instead of print() and our defined cprint(), because
    # others have an issue of printing double new line after.
    console.print(color + before + char * width + after + RS,
                  end=end, no_wrap=True, soft_wrap=True, overflow='ignore')

def box(*texts: str, title='Message', border_color='', text_color='', secondary_color='',
         width=console_width, clear_line=0, new_line=True):
    """
    1) Draw a box using standard ASCII characters, respecting ANSI colors inside.
    2) Limitations:
       - When wrapping, ANSI codes are considered normal characters.
       - ANSI code must not be in the wrap point, as it'll get broken and useless.
       - If your give a string a special color, next lines must also have the ANSI
         color code, and not depend on the the previous line.
       - You have to rewrite the ANSI code after '\n' inside strings.
       - Wrapped lines will lose their colors! thus 'secondary_color' is an
         optional argument that is applied only to the wrapped lines.
    """
    # Define colors.
    BC = border_color     # For the box borders
    TC = text_color       # If the content has its colors, this will be overwritten.
    SC = secondary_color  # Only for wrapped lines.
    
    # Wrap text to fit.
    CONTENT_WIDTH = width - 4   # (4) reserve for borders.
    message = '\n'.join(texts)
    wrapped = []
    
    for line in message.splitlines():
        if not line.strip():
            wrapped.append(' ')
            continue
            
        # Apply secondary color to wrapped lines.
        wrapped_lines = textwrap.wrap(line, CONTENT_WIDTH)
        for index, line in enumerate(wrapped_lines):
            if index == 0: continue
            wrapped_lines[index] = SC + line
        wrapped.extend(wrapped_lines)
    
    # Prepare the box.
    box_string = ''
    
    # Header.
    cprint()
    top = BC + '┌' + '─' * (CONTENT_WIDTH + 2) + '┐'
    title_line = top.replace('─' * (CONTENT_WIDTH + 2), f' {title} '.center(CONTENT_WIDTH + 2, '─'))
    box_string += title_line + RS + '\n'
    
    # Content Lines.
    for line in wrapped:
        line_visual_len = visual_len(line) or 1
        padding = ' ' * (CONTENT_WIDTH - line_visual_len)
        line = f'{BC}│{RS} {TC}{line}{padding} {BC}│{RS}'
        box_string += line + '\n'
        
    # Footer.
    bottom = BC +'└' + '─' * (CONTENT_WIDTH + 2) + '┘'
    box_string += bottom
    
    # Show the box (Idk why I have to separate cases based on colors, but bugs forced me).
    box_string = box_string.strip()
    if not USE_COLORS:
        console.print(box_string)   # Other print functions cause glitches.
        cprint('\r', end='')        # console.print() might add a blank line.
    
    else:
        cprint(box_string, wrap=False)
        # Sometimes our function adds an extra blank line, especially if the console width is high.
        # Also if the console width is low we have to manually add a blank line, Idk why (it's complicared).
        if clear_line and console_width > 79: clear_lines(clear_line)
        elif clear_line: cprint('\r', end='')
        elif new_line and console_width <= 79: cprint()

def control_cursor(command: str):
    """A custom function to show or hide the terminal cursor."""
    # Skip if not compatible with ANSI escape codes.
    if not USE_ANSI: return
    
    if command == 'show':
        cprint('\033[?25h', end='')
        
    elif command == 'hide':
        cprint('\033[?25l', end='')

def welcome_screen():
    """Display a short welcoming screen."""
    gemini_logo = (
        f"{BD}"
        f"{BL}G"
        f"{RED}o"
        f"{YLW}o"
        f"{BL}g"
        f"{GR}l"
        f"{RED}e"
        f"{RS} | "
        f"{PURP}♊ "
        f"{BD}"
        f"{BL}GEMINI"
        f"{RS}"
    )

    system(CLEAR_COMMAND)
    separator()
    cprint(f"{GR}Welcome to {gemini_logo}{GR} Py-CLI! (API-based chat)", wrap=False)
    cprint(f"Chat Initialized (Type '{UL}help{RS}{GR}' for a quick start){RS}\n", wrap=False)

if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON:
    def load_system_instructions():
        """
        - Load system instructions at startup; they can be either implicit orders,
          saved info, or both.
        - Then return the configuration object.
        """
        system_instructions = ''
        
        # Check saved info first.
        if SAVED_INFO and os.path.exists(SAVED_INFO_FILE):
            try:
                with open(SAVED_INFO_FILE, 'r', encoding='utf-8') as f:
                    saved_info_content = f.read().strip()
                if saved_info_content: 
                    system_instructions += '# User Saved Information:\n' + saved_info_content + '\n\n\n'
            except:
                if ERROR_LOG_ON: log_caught_exception()
                pass
        
        # Check implicit orders.
        if IMPLICIT_INSTRUCTIONS_ON and IMPLICIT_INSTRUCTIONS.strip():
            system_instructions += '# Your Implicit Instructions as AI:\n' + IMPLICIT_INSTRUCTIONS.strip()
        
        # Create the configuration object if previous instructions were available.
        config = None
        if system_instructions:
            config = GenerateContentConfig(system_instruction=system_instructions)
                
        return config

if PROMPT_HISTORY_ON:
    def load_prompt_history():
        """Load prompt history, either from memory or from file, depeing on settings."""
        global history
        history = None
        
        # From memory.
        if PROMPT_HISTORY_MEMORY:
            history = PromptHistory()
            
        # From file.
        else:
            try: copy_file(PROMPT_HISTORY_FILE, PROMPT_HISTORY_FILE + '.bak')
            except: pass
            history = PromptHistory(PROMPT_HISTORY_FILE)  

if PROMPT_HISTORY_ON and not PROMPT_HISTORY_MEMORY:
    def prune_prompt_history():
        """
        Check the history file size. If > PROMPT_HISTORY_SIZE, this prunes the
        file to the nearest history block (timestamp).
        """
        if not os.path.exists(PROMPT_HISTORY_FILE):
            return
        
        # Check file size.
        file_size = os.path.getsize(PROMPT_HISTORY_FILE)
        if file_size <= (PROMPT_HISTORY_SIZE * 1024 * 1024):
            return
        
        # Split file.
        cprint(GR + 'Shrinking the prompt history file...' + RS)
        while file_size > 1:
            file_size = file_size // 2
        
        start_seek_position = file_size
        with open(PROMPT_HISTORY_FILE, 'rb') as f:
            f.seek(start_seek_position)
            content_last_half = f.read().decode(sys.getdefaultencoding(), 'ignore')
        
        # Discard the broken content, keep the rest intact, and remove unwanted characters.
        match = HISTORY_PATTERN.search(content_last_half)
        if match:
            start_index = match.start()
            content_last_half = content_last_half[start_index:]
        
        # Write the kept file content.
        with open(PROMPT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            content_last_half = content_last_half.replace('\r\n', '\n').replace('\r', '\n')
            f.write(content_last_half)
        
        cprint(GR + 'Done!\n' + RS)

if SUGGEST_FROM_WORDLIST:
    def load_word_completer():
        """
        Read a list of words from a file, one word per line.
        Use the words for realtime suggestions.
        """
        global word_completer
        
        try:
            # Read the words.
            with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f if line.strip()][4:]
            if words:
                # Load the word completer instance according to user settings.
                if SUGGEST_FROM_WORDLIST_FUZZY:
                    word_completer = LimitedWordCompleter(words)
                else:
                    word_completer = LimitedWordCompleter(words, ignore_case=True)
        
        except FileNotFoundError:
            pass
        
        finally:
            if not word_completer:
                # Don't ask why clean then print, I personally don't know, but it works to avoid glitches.
                cprint('\033[2K')
                warning = f"{YLW}Suggestions from a wordlist is ON, but '{WORDLIST_FILE}' file is "
                if os.path.exists(WORDLIST_FILE): warning += "empty!"
                else: warning += "missing!"
                cprint(warning + RS)
                separator(end='')

if RESPONSE_EFFECT:
    def get_styled_lines(markdown: Markdown) -> list[Text]:
        """
        Take raw Markdown text, render it into rich segments, flatten the result,
        assemble it into a single styled Text object, and return it splitted into 
        a list of styled lines. This is the shared core logic for all typewriter effects.
        * If you didn't understand this, fine, nor did I.
        """
        # 1. Render the Markdown object to internal segments.
        segments: RenderResult = list(console.render(
            markdown,
            console.options
        ))
        
        all_segments = []
        
        # 2. Flatten the segments into a list of (text, style) tuples.
        for item in segments:
            if isinstance(item, Segment):
                # Case 1: Raw Segment object -> convert to a (text, style) tuple.
                all_segments.append((item.text, item.style))
            elif hasattr(item, 'segments'):
                # Case 2: Line object -> iterate over its internal segments.
                for text, style, *rest in item.segments:
                    all_segments.append((text, style))
            
        # 3. Create the full Text object from the flattened list of segments.
        full_text = Text.assemble(*all_segments)

        # 4. Split the full styled Text object into a list of new styled Text objects (lines).
        output_lines = full_text.split('\n')
        return output_lines

    def print_markdown_line(markdown: Markdown, delay_seconds: float = 0.05):
        """Print fully formatted Markdown content line-by-line with a delay."""
        global current_response_line
        output_lines = get_styled_lines(markdown)
        console.show_cursor(False)
        current_response_line = 0
        
        # Print the styled lines one by one with a delay.
        for line in output_lines:
            console.print(line)
            current_response_line += 1
            sleep(delay_seconds)

    def print_markdown_word(markdown: Markdown, delay_seconds: float = 0.09):
        """
        Print fully formatted Markdown content word-by-word with a delay.
        Use slicing and regex to preserve formatting and correct spacing.
        """
        global current_response_line
        output_lines = get_styled_lines(markdown)
        console.show_cursor(False)
        current_response_line = 0

        # Print the styled content word by word.
        for line in output_lines:
            if not str(line).strip():
                # If the line contains only whitespace or is empty, print a newline and continue.
                console.print()
                continue
                
            # Use regex to split text into [word, space, word, space, ...].
            parts = WORD_AND_SPACE_PATTERN.split(str(line))
            current_pos = 0
            
            for part in parts:
                if not part: continue
                part_length = len(part)
                
                # Use slicing to get the styled segment.
                styled_part_segment = line[current_pos : current_pos + part_length]
                
                # Print the part (could be a word or a space block), without a final newline.
                console.print(styled_part_segment, end='')
                if not current_pos: current_response_line += 1
                
                # Apply delay only if it's a word (non-whitespace).
                if part.strip(): sleep(delay_seconds)
                
                current_pos += part_length

            # Print a final newline after the full line's content is printed.
            console.print()
        
    def print_markdown_char(markdown: Markdown, delay_ms: float = 2.5):
        """Print fully formatted Markdown content character-by-character with a delay."""
        global current_response_line
        output_lines = get_styled_lines(markdown)
        console.show_cursor(False)
        current_response_line = 0
        
        # Set the delay according to user settings.
        if 'fast' in RESPONSE_EFFECT: wait = lambda: sleep_precise(delay_ms)
        elif 'slow' in RESPONSE_EFFECT: wait = lambda: sleep(0.01)
        else: wait = lambda: None

        # Print the styled content character by character.
        for line in output_lines:
            # Iterate over the length of the styled line object.
            current_response_line += 1
            for i in range(len(line)):
                # Create a copy of the line and truncate it to just the current character (i to i+1).
                char_segment = line[i:i + 1]
                
                # Print the single, styled character without a final newline.
                console.print(char_segment, end='')
                wait()
                
            # After printing all characters in the line, print a newline.
            console.print()
    
    def sleep_precise(milliseconds):
        """
        High precision sleep function at the cost of high CPU usage.
        Using busy-wait loop via time.perf_counter(), the CPU is constantly
        running the loop instead of sleeping.
        """
        end_time = perf_counter() + (milliseconds / 1000.0)
        while perf_counter() < end_time:
            current_time = perf_counter()
            # Use math.isclose() due to float inaccuracies.
            if math_isclose(current_time, end_time): break
            pass

if ERROR_LOG_ON and GLOBAL_LOG_ON:
    def clear_log_files():
        """
        Open log files, clear them, close :)
        Used with 'del-log' command.
        """
        error_log = 0
        global_log = 0
        
        try:
            with open(ERROR_LOG_FILE, 'w', encoding='utf-8'): pass
        except:
            error_log += 1
        
        try:
            with open(GLOBAL_LOG_FILE, 'w', encoding='utf-8'): pass
        except:
            global_log += 1
        
        if error_log and global_log:
            msg = "Couldn't delete log files!"
            color = RED
            
        elif error_log:
            msg = f"File '{ERROR_LOG_FILE}' was deleted.\nBut '{GLOBAL_LOG_FILE}' wasn't!"
            
        elif global_log:
            msg = f"File '{GLOBAL_LOG_FILE}' was deleted.\nBut '{ERROR_LOG_FILE}' wasn't!"
            
        else:
            msg = 'Log files cleared!'
            color = GR
            
        box(msg, title='LOG CLEANUP', border_color=color, text_color=color, clear_line=1)

if ERROR_LOG_ON:
    def shrink_log_file():
        """Shrink the log file to a target size by keeping the most recent lines."""
        # Quick Check.
        MAX_SIZE = LOG_SIZE * 1024 * 1024
        if not os.path.exists(ERROR_LOG_FILE): return
        file_size = os.path.getsize(ERROR_LOG_FILE) * 10
        if file_size <= (MAX_SIZE): return
        
        # Open the log file.
        try:
            with open(ERROR_LOG_FILE, 'r', encoding='utf-8', errors='ignore') as f:
                all_lines = f.readlines()
        
        except:
            if ERROR_LOG_ON: log_caught_exception()
            return
            
        # Collect lines from the end in reverse order.
        collected_lines = []
        current_size = 0
        
        # Iterate over lines in reverse order (from newest to oldest).
        for line in reversed(all_lines):
            line_size = len(line.encode('utf-8'))
            
            # Check if adding the current line would exceed the target size.
            if (current_size + line_size) > MAX_SIZE:
                break
                
            collected_lines.append(line)
            current_size += line_size
        
        # Shrink the lines to a valid log point & Reverse them to restore chronological order.
        while collected_lines[-1].strip() != LOG_SEPARATOR:
            collected_lines.pop()
            
        collected_lines.pop()    
        collected_lines.reverse()
        
        # Write the shrunk content to the new file.
        with open(ERROR_LOG_FILE, 'w', encoding='utf-8') as f:
            f.writelines(collected_lines)








# 5) Part VI: Command Attached-Functions ----------------------------------------------------------- 
def help(short=False):
    """Display a quick cheat sheet with the commands 'help' or 'help-2'."""
    # Long version.
    LONG = f"""
    1) First Thing First:
       -Get an API key from: {UL}https://aistudio.google.com/app/api-keys{RS}
        and run 'python settings_editor.py' to paste it. Remember, it's free,
        easy to get, and generous for the free tier (Just requires an account).
       -You can change other settings if you wish (e.g: The Gemini model).
    
    2) Keyboard Shortcuts (While in Prompt):
       -ENTER to send.
       -CTRL-SPACE, SHIFT-TAB or CTRL-J to add a new line to your prompt
        (SHIFT-ENTER won't work, and it will submit your text!)
       -CTRL-C or CTRL-D to clear / cancel a prompt, stop a response, or quit.
        (If you press it earlier upon submitting a prompt, you will have a
        chance that google won't receive it at all)
       -UP/DOWN arrows to navigate between input lines / history prompts,
        or to accept word suggestions.
       -CTRL-Z/CTRL-Y to undo/redo.
       -CTRL-X-CTRL-E to call external editor - if its option is ON.
        (Once the editor is closed, changes are registered & submitted)
    
    3) Special Commands (While in Prompt):
       /clear to clear the screen.
       /show to show last AI response.
       /copy to copy last AI response to clipboard.
       /copy-prompt to copy your last prompt.
        (Can also be copied by pressing UP then CTRL-A)
       /remember at prompt start to save it with high priority.
        (Saved info are shared across all chat sessions)
       /forget at prompt start to delete a saved info.
       /saved-info to open the saved info file for manual edit.
        (Changes take effect at next session)
       /save-last to save last AI response to a text file.
        (You will lose the formatting style and colors!)
       /save-chat to save the whole chat to a readable text file.
       /restart for a quick session restart.
       /quit or /exit to leave.
       /discard to destroy everything done in current session and restart.
        (Won't affect log files & manually saved content)
       /kill to destroy everything done in current session and exit.
       /quick-chat to open another window for a temporary chat.
    
    4) F-Keys & Their Commands:
       -F1: /show
       -F2: /copy
       -F3: /restart
       -F4: /quit
       -F5: /discard
       -F6: /kill
       -F7: /help
    
    5) More Commands:
       /open to open the program's directory.
       /pop-last to remove the last message pair from history; you can use
        it multiple times to remove messages in a row, or type '/pop-last 3'
        for example to remove last (3) messages pairs.
        (Permanent, takes effect at next session)
       /pop-all to clear chat history, future messages won't be affected.
        (May cause an extra delay at exit)
       /restore-last to restore last removed message(s) pair(s), you can use
        it multiple times if you deleted many times.
       /restore-all to restore all of the deleted messages before chat end.
       /del-prompt to delete the whole prompt history file, and lose all
        past history, future prompts won't be affected (No cancel option!).
       /del-all to wipe private files: chat + prompt history + log files
        + saved info (No cancel option!)
       /del-log to clear both log files, future logging won't be affected.
       /stats or /statistics to show total N° of message in current chat.
       /about for program information.
       /license for copyright.
    
    6) More Shortcuts (System / Terminal Dependent):
       -CTRL-L to clear screen.
       -CTRL-R (Reverse Search) to search backward & find the most recent
        match in prompt history, keep pressing to move, press ESC to cancel
        or confirm (ESC to confirm, not ENTER!).
       -CTRL-S (Forward Search) used after CTRL-R to find older matches,
        keep pressing to move.

    7) Limitations:
       -Tables with many columns will appear chaotic.
       -Special characters (Like LaTeX syntax) will appear as a plain text.
       -Some other bugs I didn't discover yet :/
    """
    
    # Short version.
    SHORT = f"""
    1) First:
       -Get an API key from: {UL}https://aistudio.google.com/app/api-keys{RS}
        and paste it in 'settings.py' (first few lines). it's free,
        easy to get, and generous (Just requires an account).
    
    2) Hotkeys:
       -ENTER to send.
       -CTRL-SPACE to add a new line to your prompt.
       -CTRL-C to clear / cancel a prompt, stop a response, or quit.
       -UP/DOWN arrows to navigate between input lines / history prompts,
        or to accept word suggestions.
    
    3) Commands:
       /show to show last AI response.
       /copy to copy last AI response to clipboard.
       /quit or 'exit' to leave.
       /help for this guide menu.
       {GR}/help-2 for the full guide (No yada yada).{RS}
    """
    
    message = SHORT if short else LONG
    message = textwrap.dedent(message).lstrip('\n').rstrip()
    box(message, title='HELP MENU', border_color=YLW, text_color=YLW, secondary_color=YLW)

def farewell(confirmed=False):
    """
    Display a random but beautiful farewell message upon quitting.
    Also give the user a chance to go back.
    """
    global FAREWELLS_MESSAGES, CONTINUE_MESSAGES, confirm_separator

    # Confirm.
    cprint(RS, end='')
    if not confirmed:
        cprint()
        if confirm_separator: separator()
        confirm_separator = True
        wrong_answer = 0
        text = f"{YLW}Are you sure you want to quit? (y/n): {RS}"
        if GLOBAL_LOG_ON: in_time_log(text + '...')
        
        while True:
            try:
                confirm = input(text).lower().strip()
                break
            except Interruption:
                # Stubborn Mode (To avoid accidental exit).
                wrong_answer += 1
                if wrong_answer > 1: clear_lines()
                if wrong_answer == 1:
                    text = f"\n{YLW}Either 'Yes' or 'No' (y/n): {RS}"
                else:
                    # NOTE: I suspect this line will -sometimes- cause the console to show an extra blanc line, Idk why.
                    #       that's why I used console.print() inside separator() instead of print() or cprint() to avoid the double new line.
                    text = f"\r{YLW}Are you sure you want to quit? (y/n):\nEither 'Yes' or 'No' (y/n): {RS}"
        
        if confirm != 'y':
            cprint(GR + choice(CONTINUE_MESSAGES) + RS)
            separator()
            return
        else:
            cprint()
    
    # Save chat.
    saved = save_chat_history_json(up_separator=confirmed, down_separator=False)
    if saved: cprint()
    elif not saved and confirmed: separator()
    
    # Show a farewell message..
    from useless import QUOTES, FACTS, JOKES, ADVICES, MATH
    message = choice(FAREWELLS_MESSAGES + QUOTES + FACTS + JOKES + ADVICES + MATH)
    if (not saved) and (not confirmed) and message.count('\n') == 0 and len(message) <= glitching_text_width: clear_lines()
    cprint(GR + message + RS, wrap_width=glitching_text_width)     # Fixed width to avoid glitchs on wide consoles.
    
    # Exit.
    separator()
    sys_exit(0)

def get_last_response(command: str):
    """
    Get the last response that the user has received from AI.
    Either 'save', 'copy' or 'show' it, depending on the command.
    """
    last_response = None
    msg = 'Checked both active & history messages, but current conversation is empty!'
    color = YLW
    
    # Get last response from current session, if it's not active, check chat history.
    try:
        last_response = response.text
    
    except (NameError, AttributeError):
        history = chat.get_history()
        if history:
            # Find the last AI model message & Retrieve text attribute from the first Part object.
            last_model_message = next(
                (msg for msg in reversed(history) if msg.role == 'model' and msg.parts),
                None
            )
            
            if last_model_message:
                last_response = last_model_message.parts[0].text
    
    if command == 'save-last' and last_response:
        # Save the last response.
        try:
            with open(LAST_RESPONSE_FILE, "w", encoding='utf-8') as f:
                f.write(last_response)
            
            msg = f"Last response saved successfully to '{LAST_RESPONSE_FILE}'."
            color = GR
        
        except Exception as error:
            if ERROR_LOG_ON: log_caught_exception()
            msg = f"Failed to save last response!\n{error}"
            color = RED
    
    elif command == 'show' and last_response:
        # Display the last response.
        print_response(last_response, title='Last Gemini Response')
        return
    
    elif command == 'copy' and last_response:
        # Copy the response to clipboard.
        msg = 'Last response was copied to clipboard!'
        copy_to_clipboard(last_response, msg)
        return
    
    box(msg, title='STATUS', border_color=color, text_color=color, clear_line=1)

def store_last_turn_for_exclusion(n_turns=1, remove_all=False):
    """
    Retrieve the last user message and model reply and store them globally.
    Then use them inside serialize_history() for elimnination.
    Used with 'pop-last' or 'pop-all' commands.
    """
    global messages_to_remove
    history = chat.get_history()
    history_len = len(history) - len(messages_to_remove)
    if remove_all: n_turns = history_len // 2
    
    # To remove the last completed turn, we need at least 2 messages.
    if history_len == 0:
        msg = 'Current conversation is empty :/'
        color = YLW
        
    elif history_len == 1:
        messages_to_remove.append(0)
        messages_to_remove_steps.append(1)
        msg = "Found only one message in the whole chat, from one side: '"
        msg += 'You' if history[0].role == 'user' else 'Gemini'
        msg += "'.\nSo chat history was cleared."
        color = YLW
        
    else:
        # Check for overflow (N° of requested messages to delete > available messages).
        msg = ''
        overflow = None
        if n_turns > history_len / 2:
            n_turns = history_len // 2
            msg = f'{RED}Overflow! falling back to current chat history length: ({n_turns}).\n'
            overflow = True
        
        messages_to_remove_steps.append(0)
        issue = None   
        
        for n in range(n_turns):
            # Check for a complete turn (user + model).
            last_role = history[-(1 + 2 * n)].role
            second_to_last_role = history[-(2 + 2 * n)].role
            
            if last_role == 'model' and second_to_last_role == 'user':
                i1 = history_len - (1 + 2 * n)
                i2 = history_len - (2 + 2 * n)
                messages_to_remove.extend([i1, i2])
                messages_to_remove_steps[-1] += 2
            
            else:
                # Something must be wrong.
                issue = True
                i = history_len - (1 + 2 * n)
                messages_to_remove.append(i)     # Remove the last chat message, weither user or model.
                messages_to_remove_steps[-1] += 1
                
                while history[-1].role == 'user':
                    i = history_len - (1 + 2 * n)
                    messages_to_remove.append(i) # Ensure the last chat message is the model response.
                    messages_to_remove_steps[-1] += 1
                
        if n_turns == 1: msg += 'Last message pair removed!'
        else: msg += f'Last ({n_turns}) messages pairs removed!'
        color = GR
        
        if n_turns == history_len / 2:
            if remove_all: msg += f"\n{YLW}Remember! you've cleared the chat history."
            else: msg += f"\n{YLW}But know that you've removed all available chat messages."
        
        # Just in case, ensure the first message isn't kept in case of overflow.
        if overflow and (n_turns != history_len / 2):
            messages_to_remove.append(0)
            messages_to_remove_steps[-1] += 1
            issue = True
        
        if issue:
                msg += f'\n{YLW}Found a small problem in chat history, but it should have been fixed.'
                msg += f"\n{YLW}You can check '{CHAT_HISTORY_JSON}' file later to eliminate doubt."
    
        msg += "\nChanges will take effect at next session, you can type 'restart' for a quick refresh."
        
    box(msg, title='STATUS', border_color=color, text_color=color, secondary_color=color, clear_line=1)

def restore_removed_messages(command: str):
    """
    Restore either every deleted message pair. Or restore only the last
    popped/removed messages, so earlier removed ones will not be restored.
    Used with 'restore-last' or 'restore-all' commands.
    """
    global messages_to_remove, messages_to_remove_steps
    
    if messages_to_remove_steps:
        # Restore only the last deleted message(s).
        if command == 'restore-last':
            n = messages_to_remove_steps[-1]
            for _ in range(n): messages_to_remove.pop()
            messages_to_remove_steps.pop()
            
            x = int(n / 2)
            if x == 1: msg = 'Last removed message pair was restored!'
            else: msg = f'Last ({x}) removed messages pairs were restored!'
            color = GR
        
        # Cancel the deletion of any message.
        elif command == 'restore-all':
            n = len(messages_to_remove)
            messages_to_remove.clear()
            messages_to_remove_steps.clear()
            x = int(n / 2)
            if x == 1: msg = 'Found only (1) deleted message, and it was restored.'
            else:  msg = f'All ({x}) removed messages pairs were restored!'
            color = GR
        
    else:
        msg = "You didn't remove any message in current session."
        color = YLW
        
    box(msg, title='STATUS', border_color=color, text_color=color, clear_line=1)
    
def del_all():
    """
    Nuclear option, perform a factory reset for the program data (Doesn't affect settings).
    Used with 'del-all' command.
    """
    global discarding
    
    # Warn the user.
    cprint()
    separator(color=YLW)
    to_remove_files = [
        CHAT_HISTORY_JSON, CHAT_HISTORY_TEXT, LAST_RESPONSE_FILE,
        PROMPT_HISTORY_FILE, SAVED_INFO_FILE, ERROR_LOG_FILE, GLOBAL_LOG_FILE
    ]
    
    cprint(f'{YLW}WARNING! The program will exit & wipe the following files:')
    for file in to_remove_files: cprint('- ' + file)
    cprint('')
    
    # Confirm.
    text = f"Are you sure you want to reset everything? (y/n): {RS}"
    if GLOBAL_LOG_ON: in_time_log(text + '...')
    confirm = None
    
    while True:
        try:
            confirm = input(text).lower().strip()
            break
        except Interruption:
            cprint()
            break
    
    # Cancel.
    if confirm != 'y':
        cprint(GR + choice(CONTINUE_MESSAGES) + RS)
        separator(color=YLW)
        return
    
    # Do it.
    cprint(GR + 'Clearing everything & Quitting...')
    separator(color=YLW)
    discarding = True
    for file in to_remove_files:
        try:
            with open(file, 'w', encoding='utf-8'): pass
        except:
            if ERROR_LOG_ON: log_caught_exception()
            pass
    
    raise SystemExit

def statistics():
    """
    Inform the user of his data statistics.
    Used with 'stats' or 'statistics' commands.
    """
    # Check chat history.
    length = len(chat.get_history())
    half = length // 2
    msg = f'Total N° of message in this chat: ({length}).\n'
    msg += f'({half}) from your side, and ({half}) from AI.'
    if half * 2 != length:
        rest = length - half * 2
        msg += f"\n{YLW}Seems like there are ({rest}) extra non-structured messages in "
        msg += f"current chat, but they won't cause any trouble. Sorry, it's a bug."
    
    msg += '\n'
    
    # Check saved-info.
    if os.path.exists(SAVED_INFO_FILE):
        with open(SAVED_INFO_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = content.split('\n- ')
        info = [i for i in info if i.strip()]
        n = len(info)
        msg += f'\nTotal N° of saved info: ({n}).'
        if not SAVED_INFO: msg += f'\n{YLW}(Saved info are disabled, but the file exists)'
    
    # Check prompt-history.
    if PROMPT_HISTORY_ON:
        prompts = list(history.get_strings())
        n = len(prompts)
        msg += f'\nTotal N° of prompts in prompt-history: ({n}).'
    
    if os.path.exists(PROMPT_HISTORY_FILE) and (PROMPT_HISTORY_MEMORY or not PROMPT_HISTORY_ON):
        with open(PROMPT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prompts = content.split('\n\n# 20')
        prompts = [p for p in prompts if p.strip()]
        n = len(prompts)
        msg += f"\n{YLW}(In-file prompt history is disabled, but the file still contains: ({n}) entries)"
    
    # Check wordlist suggestion.
    if os.path.exists(WORDLIST_FILE):
        with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
            content = f.readlines()[4:]
        
        words = [w for w in content if w.strip()]
        n = len(words)
        msg += f'\nTotal N° of words in the suggestion wordlist: ({n}).'
        if not SUGGEST_FROM_WORDLIST: msg += f'\n{YLW}(Suggestions are disabled, but the file exists)'
    
    # Show it.
    msg = msg.strip() + f'\n\n{CYN}(Remember, You have the commands to control your data)'
    box(msg, title='STATISTICS', border_color=GR, text_color=GR, secondary_color=YLW, clear_line=1)

def quick_chat():
    """
    Open another console window in quick chat mode.
    Used with 'quick-chat' command.
    """
    # Choose a mode.
    separator(before='\n', color=GR)
    prompt = GR + 'Quick Chat Modes:\n'
    prompt += '1) Momentary: With each new message, previous one is forgotten.\n'
    prompt += '2) Temporary: At exit, everything is forgotten.\n\n'
    prompt += 'Choose 1 or 2: ' + RS
    
    if GLOBAL_LOG_ON: in_time_log(prompt)
    mode = input(prompt).strip()
    
    if mode == '1':
        file = 'gemini_momentary.py'
    elif mode == '2':
        file = 'gemini_temporary.py'
    else:
        cprint(RED + 'Invalid option; aborting...')
        separator(color=GR)
        return
    
    # Use current python interpreter to execute another '.py' file.
    cprint(GR + 'Opening the new chat...' + RS)
    NewProcess([sys.executable, file], creationflags=NEW_CONSOLE_FLAG)
    separator(color=GR)

def open_path(path_to_open ,clear=0, restore_prompt='', set_placeholder=''):
    """
    - Open a file or folder using the default OS application/file explorer.
    - Used with 'open' or 'saved-info' commands.
    - Add a quick cleanup if requested.
    - Work reliably across Windows, macOS, and Linux.
    """
    global default_prompt, prompt_placeholder
    
    # Check if the file/folder exists.
    if not os.path.exists(path_to_open):
        msg = "Requested file/folder isn't present in the current working directory."
        box(msg, title='ERROR', border_color=RED, text_color=RED, clear_line=1)
        return

    # webbrowser.open() handles both files and directories.
    browser_open(path_to_open)
    if GLOBAL_LOG_ON: in_time_log(' ')
    if clear: clear_lines(clear)
    if restore_prompt: default_prompt = restore_prompt
    elif set_placeholder: prompt_placeholder = FormattedText([(PROMPT_FG, set_placeholder)])

def copy_to_clipboard(text: str, msg='Text copied to clipboard!', color=GR):
    """
    Copies a string to the system clipboard using pyperclip library.
    Used with 'copy' command.
    Works seamlessly across Windows, macOS, and Linux.
    """
    try:
        # Copy (pyperclip handles the OS-specific details).
        clip_copy(text)
            
    except PyperclipException as error:
        # This catch is mainly for Linux environments where xclip, xsel, or wl-copy might be missing.
        if ERROR_LOG_ON: log_caught_exception()
        msg = "Could not access the clipboard!\n"
        msg += f"Details: {error}."
        color = RED
        
        error = str(error).lower()
        if 'xclip' in error or 'xsel' in error:
            msg += "\n\nYou likely need to install a command-line clipboard utility like 'xclip' or 'xsel'; "
            msg += "try: 'sudo apt install xclip' or 'sudo yum install xclip'"
    
    except Exception as error:
        if ERROR_LOG_ON: log_caught_exception()
        msg = "An error occured when copying to clipboard!\n"
        msg += f"Details: {error}."
        color = RED

    box(msg, title='STATUS', border_color=color, text_color=color, secondary_color=color, clear_line=1)

def copy_last_prompt():
    """
    Copy the user's last sent message to cpliboard.
    Used with 'copy-prompt' command.
    """
    # Last prompt is already stored in memory as 'last_prompt'.
    global last_prompt
    msg = 'Your last prompt was copied to clipboard!'
    color = GR
    
    # Fallback to prompt history file.
    if (not last_prompt) and PROMPT_HISTORY_ON:
        try: last_prompt = list(history.get_strings())[-2]
        except: pass
        
    # Warn.
    if not last_prompt:
        msg = 'No prompt was found; neither in memory, nor in file.'
        color = YLW
    
    # Do it.
    copy_to_clipboard(last_prompt, msg, color)
   
if SAVED_INFO:
    def manage_saved_info(user_input, command):
        """Manage user saved info by either: 'forget' or 'remember'."""
        # Check if it's worth adding/removing.
        MIN_WORDS = 3
        MIN_CHARS = 10
        requested_info = user_input[len(command):].strip()
        word_count = len(requested_info.split())  # split() uses space as default delimiter.
        char_count = len(requested_info)
        
        if (word_count < MIN_WORDS) and (char_count < MIN_CHARS):
            # Too useless to consider - no enough words & no enough characters.
            return
        
        # User wants to remember something.
        if command == 'remember':
            try:
                # A quick cleanup for the saved info file.
                clean_file = False
                if os.path.exists(SAVED_INFO_FILE) and os.path.getsize(SAVED_INFO_FILE) > 0:
                    with open(SAVED_INFO_FILE, 'r+', encoding='utf-8') as f:
                        content = f.read()
                        if not content.endswith('\n'):
                            f.write('\n')
                        
                        else:
                            leading_new_lines = len(content) - len(content.lstrip('\n'))
                            trailing_new_lines = len(content) - len(content.rstrip('\n'))
                            if (trailing_new_lines > 1) or (leading_new_lines > 1):
                                clean_file = True

                if clean_file:
                    with open(SAVED_INFO_FILE, 'w', encoding='utf-8') as f:
                        f.truncate(0)
                        f.write('\n' + content.strip() + '\n')

                # Save the info by wrapping it into short lines.
                first_line_written = False
                with open(SAVED_INFO_FILE, 'a', encoding='utf-8') as f:
                    for line in user_input.splitlines():
                        wrapped_lines = textwrap.wrap(line, width=80)
                        for line in wrapped_lines:
                            if not first_line_written:
                                f.write(f'\n- {line}\n')
                                first_line_written = True
                            else:
                                f.write(f'  {line}\n')
                    
                msg = "Information saved!\n"
                msg += "You can always ask Gemini to forget by starting your prompt with 'forget'. "
                msg += f"Or type 'saved-info' to manually edit your info in '{SAVED_INFO_FILE}'."
                color = GR
            
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                msg = f"Couldn't save your info!\nError: {error}."
                color = RED
                
            box(msg, title='SAVED INFO STATUS', border_color=color, text_color=color, secondary_color=color, clear_line=1)

        # User wants to forget something.
        elif command == 'forget':
            try:
                deleted = False     # If the info was deleted, this becomes True.
                
                # Get the saved info list.
                if not os.path.exists(SAVED_INFO_FILE):
                    msg = f"There is no '{SAVED_INFO_FILE}' file!"
                    box(msg, title='WARNING', border_color=YLW, text_color=YLW, clear_line=1)
                    return
                
                try:        
                    with open(SAVED_INFO_FILE, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                except Exception as error:
                    if ERROR_LOG_ON: log_caught_exception()
                    msg = f"Couldn't read '{SAVED_INFO_FILE}' file!\nError: {error}."
                    box(msg, title='ERROR', border_color=RED, text_color=RED, clear_line=1)
                    return
                
                if not content:
                    msg = f"File '{SAVED_INFO_FILE}' is empty!"
                    box(msg, title='WARNING', border_color=YLW, text_color=YLW, clear_line=1)
                    return
                
                # Split SAVED_INFO_FILE content according to '- ' at the start of line.
                separator(before='\n', color=YLW)
                info_list = re.split(r'^(?:- )', content, flags=re.MULTILINE)[1:]
                
                if len(info_list) == 1:
                    # If there is only one saved info, avoid the remaining complex code.
                    cprint(f"{YLW}Found only one saved info in the whole '{SAVED_INFO_FILE}' file:{GR}")
                    info = re.sub(r'\s+', ' ', info_list[0].capitalize()).strip()
                    cprint('- ' + info, wrap_width=console_width, wrap_joiner='\n  ')
                    if GLOBAL_LOG_ON: in_time_log('\nDelete it? (y/n): ...')
                    user_choice = input(YLW + '\nDelete it? (y/n): ' + RS).strip().lower()
                    
                    if user_choice == 'y':
                        try:
                            with open(SAVED_INFO_FILE, 'w', encoding='utf-8'): pass
                            cprint(GR + 'Saved info permanently deleted!' + RS)
                        except Exception as error:
                            if ERROR_LOG_ON: log_caught_exception()
                            cprint(f"Couldn't edit '{SAVED_INFO_FILE}' file!\nError: {error}.")
                    else: 
                        cprint(GR + choice(CONTINUE_MESSAGES) + RS)
                        
                    separator(color=YLW)
                    return
                
                # Remove whitespaces & initial 'remember' word for better comparison.
                cleaned_infos = []
                for entry in info_list:
                    entry = re.sub(r'remember', ' ', entry, count=1, flags=re.IGNORECASE)
                    entry = re.sub(r'\s+', ' ', entry).strip()
                    cleaned_infos.append(entry)
                    
                # Compare & Get ordered top matches.
                results = compare_texts(requested_info, cleaned_infos)
                top_n = 3 if len(info_list) >= 3 else len(info_list)
                top_results = heapq.nlargest(top_n, results.items(), key=lambda item: item[1])
                
                if top_n == 3:
                    info_1, info_2, info_3 = top_results[0][0], top_results[1][0], top_results[2][0]
                    ratio_1, ratio_2, ratio_3 = top_results[0][1], top_results[1][1], top_results[2][1]
                
                elif top_n == 2:
                    info_1, info_2 = top_results[0][0], top_results[1][0]
                    ratio_1, ratio_2 = top_results[0][1], top_results[1][1]
                
                # Case (1): High confidence, almost sure.
                if (ratio_1 > 0.7) and (ratio_1 / ratio_2 > 1.25):
                    cprint(CYN + 'Saved Info found:' + GR)
                    cprint('- Remember ' + info_1, wrap_width=console_width, wrap_joiner='\n  ')
                    question = 'Are you sure you want to delete it? (y/n): '
                    answers = ['y']
                        
                # Case (2): Match is decent, but dangerously ambiguous.
                elif (ratio_1 > 0.5) and (ratio_1 / ratio_2 <= 1.30):
                    cprint(YLW + 'You probably meant one of these saved info:' + GR)
                    cprint('1) Remember ' + info_1, wrap_width=console_width, wrap_joiner='\n   ')
                    cprint('2) Remember ' + info_2, wrap_width=console_width, wrap_joiner='\n   ')
                    question = "(If none, use 'saved-info' command for manual edit)\n"
                    question += 'Which one you want to delete? (1, 2, cancel): '
                    answers = ['1', '2']
                    
                # Case (3): Match is too poor.
                else:   # elif ratio_1 <= 0.5:
                    cprint(YLW + 'Perphaps you meant one of these saved info:' + GR)
                    cprint('1) Remember ' + info_1, wrap_width=console_width, wrap_joiner='\n   ')
                    cprint('2) Remember ' + info_2, wrap_width=console_width, wrap_joiner='\n   ')
                    question = "(If none, use 'saved-info' command for manual edit)\n"
                    if top_n == 3:
                        cprint('3) Remember ' + info_3, wrap_width=console_width, wrap_joiner='\n   ')
                        question += f'Which one you want to delete? (1, 2, 3, cancel): '
                        answers = ['1', '2', '3']
                    else:
                        question += f'Which one you want to delete? (1, 2, cancel): '
                        answers = ['1', '2']
                
                # Track the targeted saved-info back to the file content & remove it if the user said so.
                if GLOBAL_LOG_ON: in_time_log(f'\n{question}...')
                user_choice = input(f'\n{YLW}{question}{RS}').strip().lower()
                if user_choice in answers:
                    if user_choice.isdigit(): idx = cleaned_infos.index(locals()[f'info_{user_choice}'])
                    elif user_choice == 'y': idx = cleaned_infos.index(info_1)
                    to_remove = '- ' + info_list[idx]
                    new_content = content.replace(to_remove, '').strip()
                    
                    try:
                        with open(SAVED_INFO_FILE, 'w', encoding='utf-8') as f:
                            f.write('\n' + new_content)
                    except Exception as error:
                        if ERROR_LOG_ON: log_caught_exception()
                        msg = f"Couldn't edit '{SAVED_INFO_FILE}' file!\nError: {error}."
                        box(msg, title='ERROR', border_color=RED, text_color=RED, clear_line=1)
                        return
                    
                    cprint(GR + 'Saved info permanently deleted!' + RS)
                    deleted = True
               
                # User said no/cancel.
                else:
                    cprint(GR + choice(CONTINUE_MESSAGES) + RS)

            except Interruption:
                cprint(f'\n{GR}{choice(CONTINUE_MESSAGES)}{RS}')
            
            finally:
                separator(color=YLW)
                if deleted: return True
                else: return False

    def simple_stem(word):
        """
        Reduce a word to its base stem by stripping common non-essential suffixes.
        Used with 'forget' command.
        """
        word = word.lower()
        if word.endswith('ment') and len(word) > 6:
            return word[:-4]
        elif word.endswith('tion') and len(word) > 6:
            return word[:-3]
        elif word.endswith(('ing', 'ous', 'ism')) and len(word) > 5:
            return word[:-3]
        elif word.endswith(('ed', 'es', 'er', 'ly', 'al')) and len(word) > 3:
            return word[:-2]
        elif word.endswith('s') and len(word) > 3:
            return word[:-1]
        return word

    def compare_texts(text: str, compare_list: list):
        """
        Compare a string against a list of strings.
        Return compared strings with their ratios.
        Used with 'forget' command.
        """    
        # Pre-calculate tokens and stems for the given text.
        source_word_tokens = re.findall(r'\b\w+\b', text.lower())
        source_stem_tokens = [simple_stem(word) for word in source_word_tokens]
        
        # Define stop words to avoid similarity matching being diluted or dominated by them.
        # This is positive for long strings, but negative for short ones.
        STOP_WORDS = set([
            'a', 'an', 'the', 'i', 'am', 'is', 'are', 'was', 'were', 'my', 'me', 'you', 
            'your', 'about', 'that', 'this', 'it', 'its', 'of', 'for', 'in', 'on', 'at', 
            'and', 'or', 'to', 'from', 'but', 'by', 'do', 'don', 't', 's', 'can'
        ])
        STOP_WORDS_THRESHOLD = 7    # Minimum N° of words allowed to remove stop words.
        
        # Define weighting for priority.
        WEIGHT_FULL_WORD = 0.75
        WEIGHT_STEM = 0.25
        
        results = {}
        
        for string in compare_list:
            # Calculate both sets of tokens for the strings.
            target_word_tokens = string.lower().split()
            target_stem_tokens = [simple_stem(word) for word in target_word_tokens]
            
            # Remove stop words from source and target tokens.
            if len(source_word_tokens) > STOP_WORDS_THRESHOLD:
                source_word_tokens = [w for w in source_word_tokens if w not in STOP_WORDS]
                source_stem_tokens = [w for w in source_stem_tokens if w not in STOP_WORDS]
                target_word_tokens = [w for w in target_word_tokens if w not in STOP_WORDS]
                target_stem_tokens = [w for w in target_stem_tokens if w not in STOP_WORDS]

            # Calculate full-word similarity & stem similarity.
            full_word_ratio = difflib.SequenceMatcher(None, source_word_tokens, target_word_tokens).ratio()
            stem_ratio = difflib.SequenceMatcher(None, source_stem_tokens, target_stem_tokens).ratio()

            # Combine & Save scores using weighted average.
            combined_ratio = (full_word_ratio * WEIGHT_FULL_WORD) + (stem_ratio * WEIGHT_STEM)
            combined_ratio = min(combined_ratio * 1.5, 1.0)    # Just cheating, for now the match is inaccurate.
            if not combined_ratio: combined_ratio = 0.001      # To avoid ZeroDivisionError.
            results[string] = combined_ratio
        
        return results

if EXTERNAL_EDITOR:
    def manage_editor_variable(mode='change'):
        """
        Check for the EDITOR environment variable in the OS.
        Modifies it if necessary, then restores the original value at exit.
        This is used if the EXTERNAL_EDITOR option is ON, upon clicking CTRL-X-CTRL-E.
        """
        global editor_variable
        # 1. Check if EDITOR is present and store the original state/value.
        editor_variable = os.environ.get('EDITOR')
        
        # * If there is already an EDITOR variable, and the user didnt set it in settings, then do nothing.
        if editor_variable and not FAVORITE_EDITOR:
            return
        
        # 2. Modify the variable.
        try:
            if mode == 'change':
                # The user has set his own editor.
                if FAVORITE_EDITOR:
                    os.environ['EDITOR'] = FAVORITE_EDITOR
                
                # Fallback to the system's available editor.
                else:
                    if sys.platform.startswith('win'):
                        os.environ['EDITOR'] = 'notepad'        # For Windows.
                    else:
                        os.environ['EDITOR'] = 'vim'            # For MacOS/Linux.
            
            # 3. Restore the original value/state.
            elif mode == 'restore':
                if editor_variable:
                    os.environ['EDITOR'] = editor_variable
                else:
                    del os.environ['EDITOR']
        
        except:
            if ERROR_LOG_ON: log_caught_exception()








# 6) Part V: Main Functions ------------------------------------------------------------------------
def flush_input():
    """
    Flush the input buffer to avoid accidental hotkeys registration.
    E.g: If the user presses F1 outside prompt(), prompt() may still catch it
         when it's back ON.
    """
    if os.name == "posix":    # Linux/Mac.
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        
    elif os.name == "nt":     # Windows.
        while msvcrt.kbhit(): msvcrt.getch()

def serialize_history():
    """Convert active chat history into json format to save it later."""
    global messages_to_remove
    # Get history & Exclude removed messages.
    history_list = chat.get_history()
    
    if messages_to_remove:
        history_list = [item for idx, item in enumerate(history_list) if idx not in messages_to_remove]
        messages_to_remove.clear()
    
    if not history_list: return []
    
    # Respect history max limit.
    if not NO_HISTORY_LIMIT:
        if len(history_list) > MAX_HISTORY_MESSAGES:
            messages_to_keep = history_list[-MAX_HISTORY_MESSAGES:]
            history_list = messages_to_keep
    
    # Serialize it.
    serializable_history = [
        {
            'role': content.role,
            'parts': [{'text': p.text} for p in content.parts if hasattr(p, 'text') and p.text],
        }
        for content in history_list
    ]
    
    return serializable_history

def save_chat_history_json(up_separator=True, down_separator=True, hidden=False):
    """Save the chat history as a json file before quitting."""
    global chat_saved, messages_to_remove
    # Condition 1: Chat session must be active.
    try: active = bool(chat)
    except NameError: return
        
    # Condition 2: Active session must not be empty.
    empty = chat.get_history() == []
    if empty: return
    
    # Condition 3: Active session must be a new chat or a modification to the saved one.
    try:
        if messages_to_remove:
            # Case 1: Messages were deleted.
            changed = bool(messages_to_remove)
            serializable_history = None
        
        else:
            # Case 2: Messages were added.
            serializable_history = serialize_history()
            new_history_json_str = json.dumps(serializable_history)
            with open(CHAT_HISTORY_JSON, 'r', encoding='utf-8') as f:
                old_history_dicts = json.load(f)
            
            old_history_json_str = json.dumps(old_history_dicts)
            changed = new_history_json_str != old_history_json_str
        
    except:
        serializable_history = None
        changed = True
    
    # Perform the save.
    if active and not empty and changed:
        if not hidden and up_separator: separator()
        if not hidden: cprint(GR + 'Saving chat history, one moment...' + RS)
        
        # Serialize history if not already done.
        if serializable_history == None:
            try:
                serializable_history = serialize_history()
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                if not hidden: cprint(f"{RED}Failed to save chat history: {error}!{RS}")
        
        # Save chat, weither messages were added, removed or the entire chat was cleared.
        if serializable_history or serializable_history == []:
            try:
                # Write to a temporary file, to avoid data corruption upong pressing CTRL-C.
                temp_file = CHAT_HISTORY_JSON + '.tmp'
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(serializable_history, f, indent=2)
                os.replace(temp_file, CHAT_HISTORY_JSON)
                
                if not hidden:
                    if serializable_history: cprint(f"{GR}Chat history saved!{RS}")
                    else: cprint(f"{GR}Chat history saved & cleared!{RS}")
                chat_saved = True
            
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                if not hidden: cprint(f"{RED}Failed to save chat history: {error}!{RS}")
                
        if not hidden and down_separator: separator()
        return True

def save_chat_history_text():
    """
    Save the chat history as a readable text file, without json formatting.
    Used with 'save-chat' command.
    """
    history = chat.get_history()
    chat_lines = []
    
    if history:
        # Retrieve sender + text from chat history.
        for msg in history:
            sender = 'You' if msg.role == 'user' else 'Gemini'

            # Loop through all parts in the message.
            text_parts = []
            for part in msg.parts:
                if part.text: text_parts.append(part.text)
                
            # Join the text parts with a newline, if multiple parts exist.
            content = '\n'.join(text_parts)
            chat_lines.append(f'>>> {sender}:\n{content}')
        
        # Save the chat.
        try:
            delimiter = '\n\n\n'
            chat_text = delimiter.join(chat_lines)
            with open(CHAT_HISTORY_TEXT, "w", encoding='utf-8') as f:
                f.write(chat_text)
            
            msg = f"Chat saved successfully to '{CHAT_HISTORY_TEXT}'."
            color = GR
        
        except Exception as error:
            if ERROR_LOG_ON: log_caught_exception()
            msg = f"Failed to save chat!\n{error}"
            color = RED
    
    else:
        msg = "Current conversation is empty!"
        color = YLW
    
    box(msg, title='STATUS', border_color=color, text_color=color, clear_line=1)

def load_chat_history():
    """Load chat history, if it meets the conditions."""
    global initial_history, confirm_separator
    initial_history = []
    
    # Check if the history file exist, and is not empty.
    file_exist = os.path.exists(CHAT_HISTORY_JSON)
    empty, useful = None, None
    
    if file_exist:
        empty = os.path.getsize(CHAT_HISTORY_JSON) == 0
    
    if file_exist and not empty:
        with open(CHAT_HISTORY_JSON, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            useful = content != '[]'
    
    if file_exist and not empty and useful:
        question = f"{CYN}Chat history available, load it? (y/n):{RS} "
        if GLOBAL_LOG_ON: in_time_log(question + '...')
        invalid_answer = False
        
        while True:
            try:
                if ALWAYS_LOAD_CHAT: load_history = 'y'
                else: load_history = input(question).lower().strip()
                
            except Interruption:
                cprint()
                confirm_separator = False
                raise
                
            if load_history == 'y':
                try:
                    with open(CHAT_HISTORY_JSON, 'r', encoding='utf-8') as f:
                        saved_history_dicts = json.load(f)
                    
                    # Reconstruct Content & Part objects from the saved dictionaries.
                    errors = 0
                    for item in saved_history_dicts:
                        try:
                            parts = [Part(text=p['text']) for p in item['parts']]
                            initial_history.append(Content(role=item['role'], parts=parts))
                        except:
                            if ERROR_LOG_ON: log_caught_exception()
                            errors += 1
                            if errors == 1:
                                cprint(f"{RED}({errors}) partial error occurred during loading chat history.{RS}")
                            else:
                                clear_lines()
                                cprint(f"{RED}({errors}) partial errors occurred during loading chat history.{RS}")
                            continue
                    
                    # Inform the user of the loading status.
                    loaded_messages = len(initial_history)
                    if loaded_messages:
                        n = len(initial_history)
                        cprint(f"{CYN}Loaded ({n}) history steps / ({int(n / 2)}) messages pairs from '{CHAT_HISTORY_JSON}'.{RS}")
                    elif not loaded_messages and not errors:
                        cprint(f"{YLW}File '{CHAT_HISTORY_JSON}' seems to be empty.{RS}")
                    elif not loaded_messages and errors:
                        cprint(f"{YLW}Failed to load any history messages (0 loaded).{RS}")
                        
                    if errors:
                        cprint(f"{RED}Found ({errors}) errors while loading the history, the rest was loaded successfully.{RS}")
                    break
                    
                except Exception as error:
                    if ERROR_LOG_ON: log_caught_exception()
                    cprint(f"{RED}Failed to load chat history ({error}).\n{YLW}Starting a new chat...{RS}")
                    initial_history = []
                    break
            
            elif load_history == 'n':
                cprint(f"{YLW}Ignoring history...")
                cprint(f"History will be overwritten at exit, if you send a message.{RS}")
                break
                
            else:
                if invalid_answer: clear_lines()
                question = CYN + "Either 'Yes' or 'No' (y/n): " + RS
                invalid_answer = True
    
    elif not file_exist:
        cprint(f"{YLW}File '{CHAT_HISTORY_JSON}' not found, starting a new chat...{RS}")
    else:
        cprint(f"{YLW}File '{CHAT_HISTORY_JSON}' seems to be empty.{RS}")
    
    separator(end='')

def setup_chat():
    """
    Initialize the Gemini client and chat session.
    Also prepare additiional objects.
    """
    global restarting, chat_saved
    if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        catch_no_api_key()
        help(short=True)
        sys_exit(1)
    
    # Loading Screen.
    if not restarting:
        print()
        clear_lines(4)
        print('┌' + '─' * (console_width - 2) + '┐')
        print('│ Loading chat...' + ' ' * (console_width - 18) + '│')
        print('└' + '─' * (console_width - 2) + '┘')
    else:
        chat_saved = False
    
    error_occurred = None
    attempts = 0
    
    while True:
        try:
            # if attempts == 0: raise ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            # raise ClientError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            # raise httpx.RemoteProtocolError(message='Test')

            # Client Initialization.
            http_options = {
                "timeout": HTTP_TIMEOUT * 1000, 
            }
            
            client = GemClient(
                api_key=GEMINI_API_KEY,
                http_options=http_options,
            )
            
            # API Validation.
            if STARTUP_API_CHECK:
                try:
                    # if attempts == 0: raise ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
                    if attempts: cprint(GR + '◊ Sending request...' + RS)
                    client.models.list()
                    if attempts:
                        clear_lines()
                        cprint(GR + 'Response received!' + RS)
                        separator(color=RED)
                
                except ServerError:
                    if attempts: clear_lines()
                    raise    
                    
                except:
                    if attempts: separator(color=RED)
                    raise
                    
            elif attempts:
                cprint(GR + 'Response received!' + RS)
                separator(color=RED)
                
            break
        
        except ClientError as error:
            catch_client_error_startup(error)
            help(short=True)
            sys_exit(1)
        
        except ServerError as error:
            catch_server_error_startup(error_occurred, attempts)
            error_occurred = True
            attempts += 1
            continue
            
        except NetworkExceptions:
            catch_network_error()
            sys_exit(1)

    # Preparation & Welcome Screen...
    console.set_window_title('Gemini Py-CLI')
    if EXTERNAL_EDITOR: manage_editor_variable('change')
    if PROMPT_HISTORY_ON: load_prompt_history()
            
    while True:
        try:
            welcome_screen()
            load_chat_history()
            if SUGGEST_FROM_WORDLIST: load_word_completer()  
            break
            
        except Interruption:
            farewell()
            continue
    
    # Start chat session with/out the system instructions (Implicit orders or saved info).
    config = None
    if IMPLICIT_INSTRUCTIONS_ON or SAVED_INFO:
        config = load_system_instructions()
    
    chat = client.chats.create(
        model=GEMINI_MODEL,
        history=initial_history,
        config=config,
    )
    
    cprint()
    restarting = False
    return client, chat

def interpret_commands(user_input: str):
    """If the user input is a special command, execute it."""
    global discarding, history, default_prompt
    
    command = user_input.strip().lower()
    if not command.startswith('/'): return True
    else: command = command.lstrip('/')
    
    match command:
        case 'quit' | 'exit':
            cprint()
            farewell(confirmed=True)
    
        case 'help' | 'help-2':
            if command == 'help': help(short=True)
            else: help()    # Long version.
            clear_lines()    

        case 'clear':
            system(CLEAR_COMMAND)
    
        case 'open':
            open_path('.', clear=2, set_placeholder=user_input)
    
        case 'saved-info':
            open_path(SAVED_INFO_FILE, clear=2, set_placeholder=user_input)
    
        case c if c.startswith('remember ') and SAVED_INFO:
            manage_saved_info(user_input, 'remember')
            return True
        
        case c if c.startswith('forget ') and SAVED_INFO:
            deleted = manage_saved_info(user_input, 'forget')
            # True for deletion, None for error, False for user cancellation (promot won't be sent if False).
            if deleted in [True, None]: return True
    
        case 'save-last' | 'show' | 'copy':
            get_last_response(command)
        
        case 'copy-prompt':
            copy_last_prompt()
        
        case 'save-chat':
            save_chat_history_text()

        case c if c.startswith('pop-last'):
            if len(command) > 8: n_turns = int(float(command[8:]))
            else: n_turns = 1
            store_last_turn_for_exclusion(n_turns)  
        
        case c if c.startswith('pop-all'):
            store_last_turn_for_exclusion(remove_all=True)
    
        case 'restore-last' | 'restore-all':
            restore_removed_messages(command)
    
        case 'del-prompt':
            try:
                os.remove(PROMPT_HISTORY_FILE)
                if PROMPT_HISTORY_ON: load_prompt_history()
                msg = f"File '{PROMPT_HISTORY_FILE}' removed successfully."
                msg += "\nIf you ever cancel, type 'discard', else it'll be permanently lost."
                color = GR
            except FileNotFoundError:
                msg = f"File '{PROMPT_HISTORY_FILE}' not found!"
                color = YLW
            except Exception as e:
                if ERROR_LOG_ON: log_caught_exception()
                msg = f"An error occurred: {e}."
                color = RED
            
            box(msg, title='STATUS', border_color=color, text_color=color, clear_line=1)
    
        case 'del-log':
            clear_log_files()
    
        case 'discard' | 'kill':
            discarding = True
            try: move_file(PROMPT_HISTORY_FILE + '.bak', PROMPT_HISTORY_FILE)
            except: pass
            
            if command == 'discard':
                if PROMPT_HISTORY_ON: load_prompt_history()
                msg = 'Discarding current session & Restarting...'
                box(msg, title='DISCARD', border_color=YLW, text_color=YLW, clear_line=1)
                raise SoftRestart
            else:   # Kill.
                msg = 'Clearing recent messages & Quitting...\nManually saved content & logs are kept!'
                box(msg, title='KILL', border_color=YLW, text_color=YLW, clear_line=1)
                raise SystemExit
    
        case 'del-all':
            del_all()
        
        case 'quick-chat':
            quick_chat()
        
        case 'restart':
            raise SoftRestart
        
        case 'stats' | 'statistics':
            statistics()

        case 'license':
            msg_1 = "Do whatever you want using 'Gemini Py-CLI', wherever you want."
            msg_2 = "Half of it was written using AI itself, so I won't complain.\n"
            msg_3 = f"But as a polite programmer request, I'll be happy if you mention my name... for the efforts."
            box(msg_1, msg_2, msg_3, title='LICENSE', border_color=GR, text_color=GR, clear_line=1)
        
        case 'about':
            msg_1 = "Title: Gemini Py-CLI.\nAuthor: Mohyeddine Didouna, with a major AI assistance."
            msg_2 = f"GitHub Home: {UL}https://github.com/Mohyoo/Gemini-Py-CLI{RS}"
            msg_3 = f"Issues Page: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}"
            msg_4 = "\nMany thanks and credits to all the people who contributed, tutorials makers, "
            msg_4 += "and free content creators. Without their help, this project wouldn't be possible"
            box(msg_1, msg_2, msg_3, msg_4, title='ABOUT', border_color=GR, text_color=GR, clear_line=1)     
            
        case 'version':
            msg = "Gemini Py-CLI, Version 1.0"
            box(msg, title='VERSION', border_color=GR, text_color=GR, clear_line=1)
            
        case _:
            # Try the extra commands.
            if interpret_extra_commands(command):
                # No command. Return True as a flag to send a normal message to AI.
                return True

def interpret_extra_commands(command: str):
    """
    A special function to interpret the extra-secret commands.
    This really should be in 'useless.py' module, but I faced a lot of issues to do that.
    """
    global user_input, default_prompt

    match command:
        # This is only for testing, don't use it otherwise.
        case c if c.startswith(('exec ', 'exec\n')):
            try:
                exec(user_input[6:])
                cprint(f'{GR}(Code Executed Sucessfully!){RS}')
            except Exception as error:
                error_type = type(error).__name__
                cprint(f'{RED}{error_type}: {error}{RS}')
        
        case c if c.startswith('eval '):
            try:
                value = eval(user_input[6:])
                cprint(f'{GR}Evaluation Result: {value}{RS}')
            except Exception as error:
                error_type = type(error).__name__
                cprint(f'{RED}{error_type}: {error}{RS}')

        case c if c.startswith('echo '):
            cprint(f'{GR}Echo Says: {user_input[6:]}{RS}')
        
        # CONGRATULATIONS! You found the secret: Extra useless commands :P
        case 'mohyoo' | 'mohyeddine' | 'didouna' | 'mohyeddine didouna' | 'didouna mohyeddine':
            msg = "Data classified.\nYou didn't think it would be that easy, did you?"
            box(msg, title='CLASSIFIED', border_color=CYN, text_color=CYN, clear_line=1)
            
        case 'banana' | 'bananas':
            from useless import draw_ascii_image
            draw_ascii_image('BANANAS', 'BANANAS', YLW, console_width, visual_len, box)

        case 'dog':
            from useless import draw_ascii_image
            draw_ascii_image('DOG', 'SAY HI!', YLW2, console_width, visual_len, box)
        
        case 'cat':
            from useless import draw_ascii_animation
            title = "Shhhh, Mimicha is sleeping...\nPress CTRL-C to wake him up!\n"
            draw_ascii_animation('CAT', title, CYN, 0.2, 3, separator, control_cursor, clear_lines)

        case 'horse':
            from useless import draw_ascii_animation
            title = "Must... achieve... maximum... wind... through... mane!\nPress CTRL-C to take a break!\n"
            draw_ascii_animation('HORSE', title, BRW, 0.08, 2, separator, control_cursor, clear_lines)

        case c if c == 'time-travel' or c.startswith('time-travel '):
            from useless import time_travel
            time_travel(command, box)

        case 'quote':
            from useless import QUOTES
            quote = choice(QUOTES)
            box(quote, title='QUOTE', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1, new_line=False)      

        case 'lang' | 'language':
            from useless import language
            language(box)

        case 'riddle' | 'puzzle' | 'mystery' | 'r-answer' | 'riddle-answer':
            from useless import riddle
            show_soluion = True if command in ['r-answer', 'riddle-answer'] else False
            riddle(box, wrapper, open_path, show_soluion, user_input)

        case 'fact':
            from useless import FACTS
            fact = choice(FACTS).replace('Fact: ', '')
            box(fact, title='FACT', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1, new_line=False)

        case 'joke':
            from useless import JOKES
            joke = choice(JOKES)
            box(joke, title='SMILE :P', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1, new_line=False)

        case 'nothing':
            from useless import NOTHING
            msg = choice(NOTHING)
            box(msg, title="NOTHING", border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)        

        case 'nonsense':
            from useless import NONSENSE
            title = choice(NONSENSE[0])
            msg = choice(NONSENSE[1:])
            box(msg, title=title, border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)

        case 'advice' | 'hint':
            from useless import ADVICES
            advice = choice(ADVICES).replace('Fact: ', '')
            box(advice, title='ADVICE', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1, new_line=False)

        case 'math' | 'headache':
            from useless import mathematics
            mathematics(box)

        case 'scan' | 'clean':
            from useless import fake_scan
            fake_scan(console.status, separator)

        case 'overthink' | 'overthinking':
            from useless import overthink
            overthink(box)

        case 'achieve' | 'achievement':
            from useless import ACHIEVEMENTS
            msg = "Achievement Unlocked: " + choice(ACHIEVEMENTS)
            box(msg, title='ACHIEVEMENT', border_color=PURP, text_color=PURP, secondary_color=PURP, clear_line=1)
        
        case c if c.startswith(('false-echo', 'f-echo')):
            from useless import false_echo
            false_echo(user_input, box)
        
        case 'random':
            random_cmd = choice([
                'banana', 'dog', 'cat', 'horse', 'time-travel', 'quote','fact', 'joke', 'riddle', 'lang',
                'nothing', 'nonsense', 'hint', 'math', 'scan', 'overthink', 'achieve', 'f-echo random', 'mohyoo',
            ])
            
            user_input = random_cmd
            interpret_extra_commands(random_cmd)
            default_prompt = f"Last random command: '\{random_cmd}'"
        
        # No command. Return True as a flag to send a normal message to AI.
        case _:
            return True

def get_user_input():
    """
    Handle prompt_toolkit input and catch Ctrl-C/Ctrl-D.
    NOTE: User input will never be stripped or modified, it'll be sent as-is,
    we only use a stripped copy of it to beautify the output.
    """
    global last_prompt, default_prompt, prompt_placeholder
    
    # Store last user prompt.
    try: last_prompt = user_input
    except: pass
    
    # Set input options.
    # 1. RPrompt.
    rprompt = None
    if INFORMATIVE_RPROMPT:
        current_time = datetime.now().strftime('%I:%M %p')
        margin = ' ' * (terminal_size().columns - console_width - 1)
        rprompt = f"[{GEMINI_MODEL} | {current_time}]{margin}"
        
    # 2. Hotkeys editing mode.
    if VIM_EMACS_MODE == 'vim': editing_mode = EditingMode.VI
    elif VIM_EMACS_MODE == 'emacs': editing_mode = EditingMode.EMACS
    else: editing_mode = None
    
    # 3. Others.
    error_handler = lambda *args, **kwargs: log_caught_exception() if ERROR_LOG_ON else None
    bottom_free_space = SUGGESTIONS_LIMIT + 1 if SUGGEST_FROM_WORDLIST else False
    
    # Log.
    if GLOBAL_LOG_ON:
        if rprompt: in_time_log(' ' * (console_width - len(rprompt)) + rprompt + '\n')
        else: in_time_log(' ')
        in_time_log(' You >  ' + str(prompt_placeholder[0][1]))

    # Stream input.
    flush_input()
    try:
        # Just a reference - Possible prompt() args:
        # ['message', 'history', 'editing_mode', 'refresh_interval', 'vi_mode', 'lexer', 'completer'
        # , 'complete_in_thread', 'is_password', 'key_bindings', 'bottom_toolbar', 'style', 
        # 'color_depth', 'cursor', 'include_default_pygments_style', 'style_transformation', 
        # 'swap_light_and_dark_colors', 'rprompt', 'multiline', 'prompt_continuation', 'wrap_lines', 
        # 'enable_history_search', 'search_ignore_case', 'complete_while_typing', 
        # 'validate_while_typing', 'complete_style', 'auto_suggest', 'validator', 'clipboard', 
        # 'mouse_support', 'input_processors', 'placeholder', 'reserve_space_for_menu', 
        # 'enable_system_prompt', 'enable_suspend', 'enable_open_in_editor', 'tempfile_suffix', 
        # 'tempfile', 'show_frame', 'default', 'accept_default', 'pre_run', 'set_exception_handler', 
        # 'handle_sigint', 'in_thread', 'inputhook']
        
        user_input = prompt(
            # Main options.
            style=prompt_style,
            message=prompt_message,
            placeholder=prompt_placeholder,
            prompt_continuation=line_continuation,
            multiline=True,
            wrap_lines=True,
            key_bindings=keys,
            
            # Other options.
            default=default_prompt if default_prompt else '',
            mouse_support=MOUSE_SUPPORT,
            history=history,
            auto_suggest=auto_suggest,
            completer=word_completer,
            complete_while_typing=bool(word_completer),
            complete_in_thread=bool(word_completer),
            rprompt=rprompt,
            bottom_toolbar=prompt_bottom_toolbar,
            editing_mode=editing_mode,
            enable_open_in_editor=EXTERNAL_EDITOR,
            reserve_space_for_menu=bottom_free_space,
            search_ignore_case=True,
            lexer=lexer,
            validator=input_validator,
            set_exception_handler=error_handler,
            # tempfile=tempfile,
            # pre_run=,
        )
        
    except Interruption:
        farewell()
        return None
    
    finally:
        # If prompt options changed (because of open_path() function), restore them.
        if default_prompt: default_prompt = None
        if 'Ask Gemini...' not in repr(prompt_placeholder): prompt_placeholder = FormattedText([(PROMPT_FG, 'Ask Gemini...')])
        
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
        
        # First server/network error will be forgiven.
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

                # Loop while the worker thread is still running.
                with console.status(status=status_messages[0], spinner=SPINNER) as status:
                    message_index = 0
                    while active():
                        # Sleep in short, responsive chunks.
                        delay = uniform(*STATUS_UPDATE_DELAY)
                        slept_time = 0.0
                        while active() and (slept_time < delay):
                            worker.join(SLEEP_INTERVAL)
                            slept_time += SLEEP_INTERVAL
                        
                        # Update status message.
                        if active() and (len(status_messages) == 1):
                            status.update(status=status_messages[0])

                        elif active() and (message_index < len(status_messages) - 1):
                            message_index += 1
                            status.update(status=status_messages[message_index])

                if worker.exception: raise worker.exception
                response = worker.response
                clear_lines()
                break

            except (*NetworkExceptions, ServerError):
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
        # Our thread is a daemon, so it's already killed here.
        catch_keyboard_interrupt()
    
    except Exception as error:
        catch_exception(error)
    
    finally:
        if not response: clear_lines()
        
    return response

def print_response(response, title='Gemini'):
    """Print the AI response with/out effects."""
    try:
        # raise EOFError
        # raise Exception
        
        # Prepare the response.
        if not isinstance(response, str): response = response.text
        cprint(f"{GEM_BG}{GR}\n {title}: {RS}")
        formatted_response = Markdown(response)
        
        # Clear the hidden console & Print the response to it.
        temp_console.clear
        temp_console.print(formatted_response)
        
        # Count the number of blank lines at the end of the output (Caused by Markdown() class).
        exported_text = temp_console.file.getvalue()
        lines = exported_text.splitlines()[-15:]
        
        lines_to_remove = 0
        for line in reversed(lines):
            striped_line = ANSI_ESCAPE.sub('', line).strip()
            if not striped_line: lines_to_remove += 1
            else: break
        
        # Display the response according to the effect.
        if RESPONSE_EFFECT:
            try:
                if RESPONSE_EFFECT == 'line':
                    print_markdown_line(formatted_response)
                
                elif RESPONSE_EFFECT == 'word':
                    print_markdown_word(formatted_response)
                
                elif 'char' in RESPONSE_EFFECT:
                    print_markdown_char(formatted_response)
            
            except Interruption:
                raise
            
            except:
                # Fallback to no effect.
                if ERROR_LOG_ON: log_caught_exception()
                console.print(formatted_response)
                cprint('\r', end='')
        
        # Print response without animation.
        else:    
            console.print(formatted_response)
            cprint('\r', end='')
        
        # A quick cleanup.
        clear_lines(lines_to_remove)
        if INFORMATIVE_RPROMPT: cprint()
        else: stdout_flush()
    
    except Interruption:
        # Clear empty lines from blocked response.
        if RESPONSE_EFFECT != 'line': cprint()
        if RESPONSE_EFFECT and current_response_line:
            blocked_response = reversed(exported_text.splitlines()[:current_response_line])
            for line in blocked_response:
                striped_line = ANSI_ESCAPE.sub('', line).strip()
                if not striped_line: clear_lines()
                else: break
        
        # Inform.
        msg = f'{GR}Response blocked (but saved!), skipping the rest of it...'
        box(msg, title='KEYBOARD INTERRUPTION', border_color=GR, clear_line=1)

    except Exception as error:
        catch_exception(error)
    
def run_chat():
    """Handle the user prompts and Gemini responses."""
    global user_input, response
    while True:
        try:
            # Get user input.
            user_input = get_user_input()
            if not user_input: continue
            
            # Interpret commands.
            if not interpret_commands(user_input): continue

            # Get & Print Response.
            response = get_response()
            if not response or type(response) is type(None) or isinstance(response, type(None)): continue
            print_response(response)

        except Interruption:
            farewell()
            continue








# 7) Part VI: Remaining Global Objects & Starting Point --------------------------------------------
def define_global_objects():
    """Define local variables and copy them directly into the global namespace."""
    # Define global variables.
    glitching_text_width = min(console_width, 79)   # Width used for some messages like farewell and saved info, used to avoid glitches.
    confirm_separator = True                        # Before confirming to quit, print a separator only if no precedent one was already displayed.
    word_completer = None                           # Has a True value only if the WORDLIST_FILE is present and SUGGEST_FROM_WORDLIST is True.
    chat_saved = False                              # True after the chat has been saved.
    restarting = False                              # Session restart flag.
    discarding = False                              # Session discard flag.
    messages_to_remove = []                         # Store selected messages for deletion at exit.
    messages_to_remove_steps = []                   # Used to undo messages deletion.
    default_prompt = None                           # An initial prompt the user gets when asked for input, mostly not used.
    last_prompt = None                              # Used to store last user prompt, to copy it if requested.
    line_continuation = '....... '                  # Line break marker.
    if RESPONSE_EFFECT: current_response_line = 0   # Used to clean output upon blocking a response.
    if VIM_EMACS_MODE: editor_variable = None       # This will change to the current EDITOR variable in the system, if available.

    # Define global constants.
    CLEAR_COMMAND = 'cls' if os.name == 'nt' else 'clear'
    ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[mK]')  # Used to clean a string from ANSI codes.
    WORD_AND_SPACE_PATTERN = re.compile(r'(\s+)')   # Used to split lines into words, for word-by-word animation.
    HISTORY_PATTERN = re.compile(                   # Used to shrink PROMPT_HISTORY_FILE to a valid history step.
        r'^#\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+$',
        re.MULTILINE
    )

    # Assign modules functions (To avoid repeated name resolution/lookup).
    system = os.system                              # Send commands to the system.
    terminal_size = os.get_terminal_size            # Return terminal width & height.
    sys_exit = sys.exit
    stdout_write = sys.stdout.write                 # Write to stdout.
    stdout_flush = sys.stdout.flush                 # Flush the stdout for immediate output displaying.

    # Create necessary instances.    
    auto_suggest = None                             # Suggest words based on user prompt history.
    if SUGGEST_FROM_HISTORY: auto_suggest = AutoSuggestFromHistory()

    console_theme = Theme({                         # Hyperlinks may not be clear, so we make them brighter.
        "markdown.link": "bold magenta", 
        "markdown.link_url": "italic bright_magenta",
        "link": "bold magenta",
        "repr.url": "italic bright_magenta",
    })

    console = Console(                              # Our main console, used mainly to display AI responses or line separators.
        width=console_width,
        theme=console_theme,
        no_color=not USE_COLORS,
        highlight=USE_COLORS,
        # color_system arg controls the overall color support, accepts:
        # "auto", "standard", "256", "truecolor", or None to disable all color output.
    )

    temp_console = Console(                         # A hidden console to capture uncertain output before displaying it.
        file=io.StringIO(),
        width=console_width,
        force_terminal=True,
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
        prompt_bottom_toolbar = '\n<b>[CTRL-SPACE]</b> new line | <b>[UP/DOWN]</b> history | <b>[CTRL-Z/CTRL-Y]</b> undo/redo'
        prompt_bottom_toolbar += '\n<b>[F3]</b> restart | <b>[F4]</b> quit | <b>[CTRL-L]</b> clear | <b>[CTRL-C]</b> cancel | <b>[F7]</b> help'
        prompt_bottom_toolbar = HTML(prompt_bottom_toolbar)

    lexer = None
    if INPUT_HIGHLIGHT == 'special':
        lexer = PygmentsLexer(CustomLexer)

    elif INPUT_HIGHLIGHT:
        lexer_instance = get_lexer_by_name(INPUT_HIGHLIGHT)
        lexer_class = lexer_instance.__class__
        lexer = PygmentsLexer(lexer_class)

    prompt_style = Style.from_dict({                       # User prompt style.
        'rprompt': PROMPT_FG, 
        'prompt-continuation': PROMPT_FG, 
        'bottom-toolbar': f'bg:{PROMPT_FG} fg: black',
        'validation-error': 'fg:yellow bold',
        # 'completion-menu': 'bg: cyan fg: white',
    }) 
    
    input_validator = None                                 # To check user input before submitting.
    if VALIDATE_INPUT: input_validator = LengthValidator()     
    
    keys = Keys().get_key_bindings()                       # The custom keyboard shortcuts.
    # from prompt_toolkit.key_binding import merge_key_bindings
    # from prompt_toolkit.key_binding.defaults import load_key_bindings
    # keys = merge_key_bindings([                            
        # load_key_bindings(),
        # Keys().get_key_bindings()]
    # )
    
    
    # The core operation: Copy locals() into globals().
    globals().update(locals())

if __name__ == '__main__':
    # Define global variables & Start console width updater.
    define_global_objects()   # Must be called out of the loop.
    if DYNAMIC_CONSOLE_WIDTH:
        width_updater = ConsoleWidthUpdater()
        width_updater.start()
    
    while True:
        try:
            # raise ValueError('Test' * 25)
            # raise KeyboardInterrupt
            
            # Load & Start chat client & session.
            client, chat = setup_chat()
            if chat: run_chat()
        
        except SoftRestart:
            if not discarding:
                # A hidden chat save.
                save_chat_history_json(hidden=True)
                discarding = False
                # Restart.
                msg = 'Restarting chat session...'
                box(msg, title='SESSION RESTART', border_color=CYN, text_color=CYN)
            
            restarting = True
            continue
                
        except Interruption:
            farewell()
        
        except SystemExit:
            break

        except Exception as error:
            try:
                catch_fatal_exception(error)
            except Interruption:
                separator('\n', color=RED)
                sys_exit(1)
        
        finally:
            # Save chat history & Clean log file & prompt history.
            if not chat_saved and not discarding: save_chat_history_json(hidden=True)  
            if EXTERNAL_EDITOR: manage_editor_variable('restore')
            if ERROR_LOG_ON: shrink_log_file()
            if PROMPT_HISTORY_ON and not PROMPT_HISTORY_MEMORY:
                prune_prompt_history()
                try: os.remove(PROMPT_HISTORY_FILE + '.bak')
                except: pass
