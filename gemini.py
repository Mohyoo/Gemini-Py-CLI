# I'll try to stick to the "Golden Rule" of Coding:
# "If the user can already do it easily, and automating it adds 50 lines of code
#  and a new metadata file, skip it."

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

except (ImportError, ModuleNotFoundError) as error:
    print('\n' + '─' * console_width)
    print(f'Error: {error}.')
    print('Reinstall the program to restore the missing file.')
    print('─' * console_width)
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
    from time import sleep
    from shlex import split as shlex_split
    from webbrowser import open as browser_open
    from random import randint, choice, uniform
    from mimetypes import guess_type as guess_mime_type
    from threading import Thread, Event as ThreadEvent, Lock as ThreadLock
    from shutil import rmtree as remove_dir, copy as copy_file, move as move_file
    from httpcore import RemoteProtocolError, ConnectError, ConnectTimeout, ReadTimeout
    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style, merge_styles
    from prompt_toolkit.shortcuts import ProgressBar
    from prompt_toolkit.key_binding import KeyBindings
    from prompt_toolkit.filters import has_completions, has_selection, has_focus
    from prompt_toolkit.formatted_text import FormattedText
    from prompt_toolkit.validation import ValidationError
    from google.genai import Client as GemClient
    from google.genai.types import Content, Part
    from google.genai.errors import ClientError, ServerError
    from rich.theme import Theme
    from rich.console import Console
    from rich.markdown import Markdown
    
    # Conditional.
    try: from pyperclip import PyperclipException, copy as clip_copy, paste as clip_paste
    except: clip_copy, clip_paste = None, None
    
    try: from stop_words import get_stop_words
    except: get_stop_words = None
    
    if OPERATING_SYSTEM == 'posix':
        import termios
        
    elif OPERATING_SYSTEM == 'nt':
        import msvcrt
        
    if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON:
        from google.genai.types import GenerateContentConfig
    
    if SAVED_INFO:
        import difflib
        import heapq
    
    if SUGGEST_FROM_WORDLIST_MODE == 'fuzzy':
        from prompt_toolkit.completion import FuzzyWordCompleter as WordCompleter
        
    elif SUGGEST_FROM_WORDLIST_MODE == 'normal':
        from prompt_toolkit.completion import WordCompleter
            
    if SUGGEST_FROM_HISTORY_MODE == 'flex':
        from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
        
    elif SUGGEST_FROM_HISTORY_MODE == 'normal':
        from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    
    if PROMPT_HISTORY_MODE == 'temporary':
        from prompt_toolkit.history import InMemoryHistory as PromptHistory
    
    elif PROMPT_HISTORY_MODE == 'permanent':
        from prompt_toolkit.history import FileHistory as PromptHistory
        
    if RESPONSE_EFFECT:
        from rich.text import Text 
        from rich.segment import Segment
        from rich.console import RenderResult
    
    if RESPONSE_EFFECT == 'char fast':
        from math import isclose as math_isclose
        from time import perf_counter

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
      
    if VALIDATE_INPUT:
        from prompt_toolkit.validation import Validator
      
except (ImportError, ModuleNotFoundError) as error:
    print('\n' + '─' * console_width)
    print(f'Error: {error}.')
    print("Use 'pip' to install the missing modules.")
    print("E.g: open CMD & type: pip install httpx rich")
    print('─' * console_width)
    quit(1)
    
except (KeyboardInterrupt, EOFError):
    quit(0)










# 2) Part II: Classes ------------------------------------------------------------------------------
class Keys():
    """
    Define & implement keyboard shortcuts for user prompt.
    Hotkeys() class is in 'settings.py'.
    """
    # Define hotkeys at the class level.
    SUBMIT = Hotkeys.SUBMIT
    NEW_LINE = Hotkeys.NEW_LINE
    TAB = Hotkeys.TAB
    CANCEL = Hotkeys.CANCEL
    INTERRUPT = Hotkeys.INTERRUPT
    UNDO = Hotkeys.UNDO
    REDO = Hotkeys.REDO
    CUT = Hotkeys.CUT
    COPY = Hotkeys.COPY
    PASTE = Hotkeys.PASTE
    UPLOAD = Hotkeys.UPLOAD
    RAW_FILE = Hotkeys.RAW_FILE
    UPLOAD_FOLDER = Hotkeys.UPLOAD_FOLDER
    F_KEYS = Hotkeys.F_KEYS
    EXT_EDITOR = Hotkeys.EXT_EDITOR
    QUICK_EDITOR = Hotkeys.QUICK_EDITOR
    VIEWER = Hotkeys.VIEWER

    # Define variables.
    redo_fallback_stack = []
    hide_threshold = 256
    
    def get_key_bindings(self):
        """
        Create and return the KeyBindings object with all custom hotkeys.
        We must avoid conflicts between terminal keys & ours; and amongs ours
        themselves.
        * Each key can be set with (eager=True) to give it max priority; e.g:
          if CTRL-X is set with (eager=True), it will take over even if the user
          presses CTRL-X-CTRL-E in a row.
        """
        key_bindings = KeyBindings()
           
        @key_bindings.add(*self.SUBMIT, filter=has_focus('DEFAULT_BUFFER'), eager=True)
        def _(event):
            """
            - Copy the original non-stripped input.
            - Pass the stripped input to buffer for a cleaner output.
            - Save prompt to history.
            - Submits the original input.
            - Hide some of the input if it's too long.
            * 'eager=True' ensures this binding takes precedence, no matter if
               it's a part of another hotkey combination or not.
            """
            buffer = event.app.current_buffer
            original_text = buffer.text
            if not original_text.strip():
                self.inform(event, "You can't send an empty prompt!", color='yellow')
                return
            
            self.trim_input_buffer(event)
            self.wrap_input_buffer(event)
            self.hide_long_text(event)
            self.save_history(original_text)
            event.app.exit(result=original_text)
            
        @key_bindings.add(self.QUICK_EDITOR)
        def _(event):
            """Cab a quick graphical editor for easier typing."""
            # Inform the user.
            buffer = event.app.current_buffer
            current_text = buffer.text
            self.instant_inform(event, 'Now using the quick text editor...')
            
            # Call the editor.
            original_text = quick_text_editor(current_text)
            if not original_text.strip():
                buffer.text = current_text
                buffer.cursor_position = len(current_text)
                return
            
            # Handle & Submit the text.
            edited_text = ltrim(original_text).rstrip()
            to_show_text = edited_text if len(edited_text) < self.hide_threshold else edited_text[:self.hide_threshold-6].rstrip() + ' [...]'
            buffer.text = to_show_text
            buffer.cursor_position = len(to_show_text)
            self.wrap_input_buffer(event)
            self.save_history(original_text)
            
            # Submit & Exit.
            event.app.exit(result=edited_text)
        
        @key_bindings.add(*self.VIEWER)
        def _(event):   
            """Call a quick markdown viewer to render last AI response."""
            # Inform the user.
            buffer = event.app.current_buffer
            current_text = buffer.text
            self.instant_inform(event, 'Now using the quick markdown viewer...')
            
            # Show the response & return.
            response = get_last_response('return')
            quick_markdown_viewer(response)
            buffer.text = current_text
            buffer.cursor_position = len(current_text)
            
        @key_bindings.add(self.TAB)
        def _(event):
            """Insert a tab (4 spaces)."""
            event.app.current_buffer.insert_text('    ')      
        
        @key_bindings.add(self.UNDO)
        def _(event):
            """
            Undo the last change.
            Only pushes a state to the REDO stack if the text actually changes.
            """
            # Note: On Windows, suspend_to_background doesn't behave the same way as on Unix/Linux (where 
            # it sends SIGTSTP). If you are on Windows, enable_suspend often appears to do nothing because 
            # the OS doesn't support the same job control.
            # event.app.suspend_to_background()
            # return
            
            # Undo.
            buffer = event.app.current_buffer
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
            buffer = event.app.current_buffer
            before_redo = buffer.text
            buffer.redo()
            after_redo = buffer.text
            
            # If it doesn't work, try the secondary method (Less reliable but fine).
            if (before_redo == after_redo) and (self.redo_fallback_stack):
                restored_text = self.redo_fallback_stack.pop()
                buffer.text = restored_text
                buffer.cursor_position = self.first_diff_index(before_redo, restored_text) + 1
        
        @key_bindings.add(self.CANCEL, filter=has_completions, eager=True)
        def _(event):
            """Hides the autocompletion menu when ESC is pressed."""
            buffer = event.app.current_buffer
            buffer.cancel_completion()
        
        @key_bindings.add(self.UPLOAD)
        def _(event):
            """Open a dialog to select files for upload."""
            # Get files.
            paths = select_files_dialog('file')
            if not paths: return
            self.file_dialog_helper(event, paths, 'file')
        
        @key_bindings.add(self.RAW_FILE)
        def _(event):
            """Open a dialog to select files & concatenate their raw content with the message directly."""
            # Get files.
            paths = select_files_dialog('file')
            if not paths: return
            self.file_dialog_helper(event, paths, 'raw')

        @key_bindings.add(*self.CUT, filter=~has_selection)
        def _(event):
            """Cut the whole current line if there is no selected text."""
            # Acces current buffer.
            buffer = event.app.current_buffer
            text = buffer.text
            if not text: return
            
            # Get cursor position (column, not row).
            doc = buffer.document
            col = doc.cursor_position_col
            
            # Find line limits (visually, not logically).
            # Exceeding 'AFTER' value is fine, but not for 'BEFORE' (to avoid weird behavior like text duplication).
            width = terminal_size().columns - len(line_continuation) - 1
            before = col % width
            if before == 0 and col != 0: before = width
            before = max(before, 0)
            after = min(len(doc.current_line_after_cursor), width - before) + 1
            after = max(after, 0)
            
            # Delete it.
            if before > 0: buffer.delete_before_cursor(count=before)
            if after > 0: buffer.delete(count=after)
            
            # Copy it to clipboard (using old DOC).
            line = doc.current_line[col - before : col + after]
            copy_to_clipboard(line, hidden=True)
        
        @key_bindings.add(self.COPY)
        def _(event):
            """Copy the current buffer text."""
            buffer = event.app.current_buffer
            text = buffer.text
            if not text: return
            
            # Copy (pyperclip handles the OS-specific details).
            if copy_to_clipboard(text, hidden=True):
                msg = 'Prompt Copied!'
                color = 'green'
            else:
                msg = 'Copy Failed!'
                color = 'red'
                
            self.inform(event, msg, color=color)         

        for key in self.PASTE:
            if not isinstance(key, tuple): key = (key,)
            @key_bindings.add(*key)
            def _(event):
                """
                Handle the long text pasted from the clipboard.
                Change the buffer text quickly to avoid overheat (lexer highlight,
                undo steps, history saving, etc...). 
                """
                buffer = event.app.current_buffer
                success, pasted = paste_from_clipboard()
                
                # Warn if 'Pyperclip' failed.
                if not success:
                    self.inform(event, 'Paste Failed!', color='red')
                    return
                
                # Reject mega paste (2MB limit).
                size = len(pasted.encode('utf-8'))  / 1024**2
                if size > 2:
                    if FUN_MODE: what = choice(EXCLAMATIONS)
                    else: what = 'Wait'
                    warning = f'{what}! That was a huge {int(size)}MB text! Use CTRL-G instead'
                    self.inform(event, warning, color='yellow')
                    return
                    
                # Start Pasting.
                pasted = pasted.replace('\r\n', '\n').replace('\r', '\n')
                buffer.lexer = None                            # Disable syntax highliting.
                buffer.insert_text(pasted, fire_event=False)   # Prevent other buffer change events.
                     
        for combination in (self.UPLOAD_FOLDER, self.UPLOAD_FOLDER[::-1]):   # F3+F4 or F4+F3; we use the reversed tuple so the pressing order doesn't matter.
            @key_bindings.add(*combination)
            def _(event):
                """Open a dialog to select folders for upload."""
                # Get files.
                path = select_files_dialog('dir')
                if not path: return
                self.file_dialog_helper(event, [path], 'dir')
        
        for key, command in self.F_KEYS.items():
            @key_bindings.add(key)
            def _(event, command=command):
                """
                Quickly execute a command by its F-Key.
                * 'command=command': This captures the value (F-Key command) immediately
                                     and fix it for this function.
                """
                original_text = event.app.current_buffer.text
                if SAVE_INPUT_ON_STOP: self.save_history(original_text)
                command = '/' + command
                event.app.current_buffer.text = command
                event.app.exit(result=command)

        for key in self.NEW_LINE:
            if not isinstance(key, tuple): key = (key,)
            @key_bindings.add(*key)
            def _(event):
                """Inserts a newline character."""
                event.app.current_buffer.insert_text('\n')
                
        for key in self.INTERRUPT:
            @key_bindings.add(key)
            def _(event):
                """Handle interruption/termination signal, by either: clear or quit."""
                buffer = event.app.current_buffer
                text = buffer.text
                if text:
                    # If there is a text, clear it.
                    if SAVE_INPUT_ON_CLEAR: self.save_history(text)
                    buffer.text = ''
                    # buffer.save_to_undo_stack()
                    # Copy it - just in case.
                    # copy_to_clipboard(text, hidden=True)
                else:
                    # If empty, quit input.
                    self.trim_input_buffer(event)
                    if SAVE_INPUT_ON_STOP: self.save_history(text)
                    event.app.exit(exception=KeyboardInterrupt())

        if EXTERNAL_EDITOR:
            @key_bindings.add(*self.EXT_EDITOR)
            def _(event):
                """Open the external editor; continue editing current prompt; then submit."""
                # event.app.current_buffer.open_in_editor(validate_and_handle=False)
                # Inform the user.
                buffer = event.app.current_buffer
                current_text = buffer.text
                self.instant_inform(event, 'Now using the external text editor...')
                
                # Start the editor.
                original_text = external_editor(current_text)
                if original_text is False or not original_text.strip():
                    buffer.text = current_text
                    buffer.cursor_position = len(current_text)
                    if original_text is False: self.inform(event, "The external editor couldn't be found!", color='red')
                    return
                
                # Handle the text before pasting it to avoid lag.
                edited_text = ltrim(original_text).rstrip()
                to_show_text = edited_text if len(edited_text) < self.hide_threshold else edited_text[:self.hide_threshold-6].rstrip() + ' [...]'
                buffer.text = to_show_text
                buffer.cursor_position = len(to_show_text)
                self.wrap_input_buffer(event)
                self.save_history(original_text)
                
                # Submit & Exit.
                event.app.exit(result=edited_text)
          
        if DEV_MODE:
            @key_bindings.add('escape', '!')
            def _(event):
                event.app.layout.focus('SYSTEM_BUFFER')

            @key_bindings.add('enter', filter=has_focus('SYSTEM_BUFFER'), eager=True)
            def _(event):
                app = event.app
                system_buffer = app.layout.get_buffer_by_name('SYSTEM_BUFFER')
                cmd = system_buffer.text
                
                if cmd.strip():
                    # Executes cmd in system shell - in background (it's an asynchronous function).
                    print('\n')
                    task = app.run_system_command(cmd)
                    app.create_background_task(task)
                    
                # Move focus back to the main input area.
                system_buffer.reset() # Clear the buffer after running
                app.layout.focus('DEFAULT_BUFFER')
        
        return key_bindings
    
    def trim_input_buffer(self, event):
        """Strip/trim leading & trailing whitespaces."""
        # Get the input text & trim it.
        buffer = event.app.current_buffer
        current_text = buffer.text
        stripped_text = ltrim(current_text).rstrip() 
        
        # Replace the entire text content.
        if current_text != stripped_text:
            buffer.text = stripped_text

    def wrap_input_buffer(self, event):
        """Wrap the input & Break it into shorter lines."""
        buffer = event.app.current_buffer
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
 
    def hide_long_text(self, event):
        """If user prompt is too long, only show some of it."""
        if not HIDE_LONG_INPUT: return
        buffer = event.app.current_buffer
        text = buffer.text
        i = self.hide_threshold
        if len(text) > i:
            buffer.text = text[:i-6].rstrip() + ' [...]'
    
    @staticmethod
    def save_history(prompt):
        """Save the current prompt to history, if conditions are met."""
        # Check if it's not empty & not bigger than max size.
        if PROMPT_HISTORY_MODE not in ['temporary', 'permanent']: return
        if not prompt.strip(): return
        if len(prompt.encode('utf-8'))  / 1024**2 > PROMPT_HISTORY_SIZE: return
        
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

    def file_dialog_helper(self, event, selected: list, cmd: str):
        """Upon selecting files or folders, insert them."""
        # Insert a new line for readability.
        buffer = event.app.current_buffer
        text = buffer.text.strip()
        line_start = buffer.document.cursor_position_col == 0
        if text and not line_start: buffer.insert_text('\n')
        
        # Avoid quotes conflict; Window allows single quotes in file names; Linux/Mac allow both.
        double_quotes = any('"' in path for path in selected)
        q = "'" if double_quotes else '"'
        
        # Insert the command-path pairs.
        formatted_commands = '\n'.join([f"/{cmd} {q}{path}{q}" for path in selected])
        buffer.insert_text(formatted_commands)
    
    def inform(self, event, msg, inline=False, color='blue'):
        """Inform the user of something happened in this class (error, warning, success...)."""
        buffer = event.app.current_buffer
        text = buffer.text
        
        # Simple style.
        if inline and msg not in text[-100:]:
            s = '' if not text or text[-1:].isspace() else ' '
            buffer.insert_text(f'{s}[{msg}]')
        
        # Notification style.
        else:
            # Update style.
            # app = event.app
            # old_style = app.style
            # new_style = merge_styles([
                # old_style,
                # Style.from_dict({'validation-toolbar': f'bg:{color}'}),
            # ])
            # app.style = new_style
            
            # Show the message.
            msg = ' ' + msg + ' '
            buffer.validation_error = ValidationError(message=msg)
            
            # Force refresh, then restore the old style later.
            # app.renderer.render(app, app.layout)
            # def reset_style():
                # buffer.validation_error = None
                # app.style = old_style
            # app.loop.call_later(2.0, reset_style)
            return
    
    def instant_inform(self, event, msg):
        """
        Unlike inform(); this will force an immediate text refresh.
        You'll need to manually save & restore buffer text after this.
        """
        app = event.app
        buffer = app.current_buffer
        buffer.text = ''
        buffer.insert_text(f'[{msg}]')
        app.renderer.render(app, app.layout)    # Force refresh.
            
class MessageSender(Thread):
    """
    - A thread to run & control the asynchronous (unblockable) API call when sending a message.
    - Set to 'daemon' so the thread is terminated automatically on main program
      exit or on exception (like KeyboardInterrupt).
    """
    def __init__(self, chat_session, message_to_send, *args, **kwargs):
        """initialize sender attributes."""
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.send_message = chat_session.send_message
        self.contents = message_to_send   # This will hold a string or a list [text, file_part]
        self.response = None
        self.exception = None

    def run(self):
        """The main execution of the thread - API call."""
        try:
            # *) Test for message_to_send.
            # separator()
            # for item in self.contents: print(choice([RED, GR, BL]), [item], RS)
            # separator()
            # self.response = 'Test'
            # return
            
            self.response = self.send_message(self.contents)
        except Exception as error:
            self.exception = error

class FileUploader(Thread):
    """
    - An uploader thread to run & control the asynchronous (unblockable) API call when uploading a file.
    - Set to 'daemon' so the thread is terminated automatically on main program
      exit or on exception (like KeyboardInterrupt).
    """
    def __init__(self, client, file_to_upload, *args, **kwargs):
        """initialize uploader attributes."""
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.upload = client.files.upload
        self.path = file_to_upload
        self.uploaded_file = None
        self.exception = None

    def run(self):
        """The main execution of the thread - API call."""
        try:
            path = self.path
            mime_type = guess_type(path)
            file_name = get_file_name(path)
            display_name = file_name if file_name.isascii() else f"file_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S_%f')}"
            
            with open(path, 'rb') as f:                # We pass data stream instead of file path to avoid non-ASCII names errors.
                self.uploaded_file = self.upload(
                    file=f,
                    config={
                        'mime_type': mime_type,        # Force standard MIME types.
                        'display_name': display_name,  # API accepts only ASCII-named files, so we do that to avoid errors (no side effects).
                    },  
                )
                
        except Exception as error:
            self.exception = error

class SoftRestart(Exception):
    """Custom exception to signal a safe restart of the chat session."""
    pass

if SUGGEST_FROM_WORDLIST_MODE in ['normal', 'fuzzy']:
    class LimitedWordCompleter(WordCompleter):
        """
        Override WordCompleter to enforce a limit on the number of returned completions.
        Work with both normal or fuzzy modes.
        """
        def get_completions(self, document, complete_event):
            # Do not complete after whitespaces.
            text = document.text
            if not text or text[-1].isspace():
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
            self.original_wrapper = wrapper
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
            cprint = partial(self.original_cprint, wrap_width=glitching_text_width)
            wrapper = partial(self.original_wrapper, width=console_width-1)
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
    class PromptValidator(Validator):
        """A class used to check/validate user input while typing."""
        # Define our attributes.
        last_length = 0
        pasted_length = 0
        long_prompt_threshold = 4096
        long_paste_threshold = 4096
        
        def validate(self, document):
            """
            Warn the user, especially if he types a very long prompt; but always allow him to submit.
            Warn only for a short while to avoid annoyance & glitches.
            * One problem: warning will blink if it's triggered while pasting a long text.
            * We don't use 'elif' or 'else' because warn() method will just exit.
            """
            # Calculate added chars since last time.
            text = document.text
            characters = len(text)
            diff = characters - self.last_length
            self.last_length = characters
            
            # # Inform/warn about text paste.
            # if diff > 1:
                # self.pasted_length += diff
                # if self.pasted_length > self.long_paste_threshold:
                    # self.warn('Long paste! Use CTRL-P next time!')
                # else:
                    # self.warn('Pasting text...')
            
            # # No paste or paste done; reset.
            # if self.pasted_length:
                # self.pasted_length = 0
            
            # Warn about dangerous developper commands.
            if DEV_MODE and text.startswith(('/system ', '/exec ', '/eval ')):
                self.warn('Use the command at your own risk! Beware of self-destruction!')
            
            # Get terminal available size.
            columns, rows = terminal_size()
            margin = len(line_continuation)
            x = columns - margin - 1    # (x) = length of one line in the text field, without the margins.
            
            # Warn about N° of characters.
            i = self.long_prompt_threshold
            if i <= characters <= i + 256:
                self.warn(f'You typed more than {i} characters! You can use CTRL-G.')

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
                self.warn('Long prompt! Some text is now hidden (You can use CTRL-G)')
        
        def warn(self, msg):
            """Leave this validator & Show a warning."""
            msg = ' ' + msg + ' '
            raise ValidationError(message=msg)

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
            'beautiful', 'wonderful', 'holy',
            
            # Plural Form of Previous Words.
            'warnings', 'alerts', 'dangers', 'hazards', 'threats', 'risks', 'emergencies',
            
            'errors', 'mistakes', 'failures', 'faults', 'violations', 'breaches',
            'breakdowns', 'collapses', 'malfunctions', 'flaws', 'defects',

            'forces', 'keys', 'cores', 'fundamentals', 'centrals', 'primaries',

            'successes', 'victories', 'breakthroughs', 'triumphs', 'achievements',
            'accomplishments', 'milestones',

            'consequences', 'implications', 'responsibilities', 'accountabilities',
            'commitments', 'decisions', 'judgments', 'priorities', 'sensational',
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

if SUGGEST_FROM_HISTORY_MODE == 'flex':
    class AutoSuggestFromHistory(AutoSuggest):
        """A custom but advanced AutoSuggest class, used in FLEX mode."""
        # Set a memory cache, to avoid recompiling the regex in case the user re-typed a previous word.
        cached_words = {}
        MAX_CACHE = 24
        MAX_HISTORY = 100
        MAX_CHARS = 256
        
        def get_suggestion(self, buffer, document):
            """
            Loop through history & return a suggestion object with a text.
            The returned text is always the remainder of the matched history prompt.
            """
            history = buffer.history.get_strings()
            text = document.text.lower()
            if not text or text[-1].isspace(): return None
            text = text.strip()
            
            # Take last typed word, revert history, and search backwards (most recent first).
            last_word = text.split()[-1].lower().strip()
            history = tuple(h.strip() for h in reversed(history[-self.MAX_HISTORY:]))   # Tuples are faster.
            
            # Accurate suggestion.
            for h in history:
                if h.lower().startswith(text):
                    i = len(text)
                    remainder = self.trim_suggestion(h[i:])
                    if remainder: return Suggestion(remainder)
                        
            # Forgiving suggestion (Use cached pattern if available).
            if len(last_word) < 2: return
            if last_word in self.cached_words:
                pattern = self.cached_words[last_word]
            else:
                pattern = re.compile(rf'\b{re.escape(last_word)}', re.IGNORECASE)
                self.cached_words[last_word] = pattern
                if len(self.cached_words) > self.MAX_CACHE:
                     first_key = next(iter(self.cached_words))
                     del self.cached_words[first_key]
                
            for h in history:
                match = re.search(pattern, h)
                if match:
                    i = match.start() + len(last_word)
                    remainder = self.trim_suggestion(h[i:])
                    if remainder: return Suggestion(remainder)
            
        def trim_suggestion(self, text):
            """Take the text to suggest and return only the first line shrinked to a fixed size."""
            if not text.strip(): return
            i = self.MAX_CHARS
            
            if text[0].isspace():   # Avoid extra leading spaces.
                text = f' {text.strip()}'
            
            if text.count('\n') > 0:
                text = text.splitlines()[0]
                
            if len(text) > i:
                text = text[:i-3]
                
            return text










# 3) Part III: Error Handlers ----------------------------------------------------------------------
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
    msg = f"{RED}Client side error occurred:\n{RED}{error.message}."
    
    if error.code in [429, 503]:
        # 429 (Quota Limit), 503 (Overloaded).
        msg += f"\n\n{YLW}Wait.. or type /switch & press enter for a quick conversation update."
    
    elif 'mime type' in error.message.lower():
        msg += f"\n\n{YLW}The file type you uploaded isn't supported by Google API."
        
    else:
        msg += f"\n\n{YLW}Check your settings, especially the API key validation or limits."
        msg += f"\n{YLW}If you exceeded characters limit (like hundreds of thousands\n{YLW}of characters), shorten your prompt!"
        msg += f"\n{YLW}Restarting the session might also help (Type 'restart')."
        
    box(msg, title='CLIENT SIDE ERROR', border_color=RED, text_color = RED, secondary_color=RED)

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
    if ERROR_LOG_ON: log_caught_exception()
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = SERVER_ERROR_ATTEMPTS, *SERVER_ERROR_DELAY
    
    separator('\n', color=RED)
    cprint(f"{RED}A temporary server problem occurred.")
    cprint(f'It might be a service overloading, maintenance or backend errors...')
    
    # Wait for first delay.
    try:
        print_status(lambda: quick_sleep(DELAY_1), f'Retrying in {DELAY_1} seconds...', 'yellow')
        
    except Interruption:
        cprint(f'{YLW}Cancelled by you...')
        separator(color=RED)
        return
    
    response = None
    for attempt in range(SERVER_ERROR_ATTEMPTS):
        try:
            # raise ServerError(code=403, response_json={'status': 'Test', 'reason': 'Test', 'message': 'Test' * 25})
            sender = MessageSender(chat, user_input)
            sender.start()

            # Loop while the sender thread is still running & Update the status at random intervals.
            with console.status(status=f'[bold {STATUS_GR}]Waiting for response...[/bold {STATUS_GR}]',
                                spinner=SPINNER):
                while sender.is_alive(): sender.join(SLEEP_INTERVAL)
            
            if sender.exception: raise sender.exception            
            cprint(GR + 'Response received!' + RS)
            response = sender.response
            break
                    
        except ServerError:
            if attempt >= MAX_ATTEMPTS - 1:
                cprint(f'{YLW}Tried {MAX_ATTEMPTS} times with no response! Please wait for sometime...{RS}')
                response = None
                break
                
            try:
                print_status(lambda: quick_sleep(DELAY_2), f'Issue persisting, retrying in {DELAY_2} seconds...', 'yellow')
            except Interruption:
                cprint(f'{YLW}Cancelled by you...')
                separator(color=RED)
                return
                
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
            cprint(f'{YLW}Cancelled by you...')
            separator(color=RED)
            return
    
    # Exit the function.
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
            # Check for user_input if we are in chat; if we are in setup_chat(), this'll be skipped.
            if user_input and not restarting:
                msg += f"\n{YLW}Press (UP) to get your prompt back."
                user_input = None
        except NameError:
            pass
       
    box(msg, title=title, border_color=RED)
    if restarting: clear_lines()

def catch_exception(error):
    """Used to catch any generic exception that can be forgiven during a chat."""
    global default_prompt
    if ERROR_LOG_ON: log_caught_exception()
    if SUPPRESS_ERRORS:
        clear_lines(2)
        default_prompt = user_input
        return
        
    separator('\n', color=RED)
    
    # Show error & ask the user to see details (If details aren't disabled).
    try: error = error.message  # Google exceptions have 'message' attribute.
    except: pass
    print_error(f'An error occurred:\n"{error}"')
    
    if not NO_ERROR_DETAILS:
        try:
            if GLOBAL_LOG_ON: in_time_log("See the details? (y/n): ...")
            if NO_QUESTIONS: see_error = 'y'
            else: see_error = input("See the details? (y/n): ").strip().lower()
        except Interruption:
            see_error = 'n'
            cprint()
        
        if see_error == 'y':
            cprint(RED + traceback.format_exc().strip() + RS)
        else:
            cprint(f"{GR}Acting blind...{RS}")
    
    else:
        clear_lines()
    
    separator(color=RED)

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
        if NO_QUESTIONS: see_error = 'y'
        else: see_error = input("See the details? (y/n): ").strip().lower()
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

def catch_json_error(error, file_name, file_content):
    """
    Used to catch JSON decoding exceptions when parsing a string/file.
    Attempot to repair if possible.
    """
    if ERROR_LOG_ON: log_caught_exception()
    try:
        # Try to repair the file_content.
        # raise
        from json_repair import repair_json
        repaird_json = repair_json(file_content)
        content = json.loads(repaird_json)
        return (True, content)
    
    except:
        # Declare failure.
        line = error.lineno
        msg = error.msg
        col = error.colno
        line_content = file_content.splitlines()[line-1].strip()    # Lines are (0) indexed.
            
        msg = f"{RED}JSON Error: {msg}: line {line}, column {col}\nExact line content: {line_content}\n\n"
        msg += f"Given that {YLW}'{file_name}'{RED} file has a mistake, either:\n"
        msg += "- Install 'json_repair' to repair it automatically: pip install json_repair\n"
        msg += "- Open it and correct it manually.\n"
        msg += f"- Delete it to reset it to default.{RS}"
        return (False, msg)










# 4) Part IV: Helper Functions ---------------------------------------------------------------------
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
    cprint(f"Chat initialized (Type '{UL}/help{RS}{GR}' for a quick start){RS}\n", wrap=False)

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

def ltrim(text: str):
    """Remove all leading empty lines, even if they contain spaces."""
    return re.sub(LTRIM_PATTERN, '', text)
            
def cprint(text='', end='\n', flush=True, wrap=True, wrap_width=glitching_text_width, wrap_joiner='\n'):
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
    stdout_write(f'{text}{end}')
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
    
    # \033[A:  Move cursor Up one line.
    # \033[2K: Erase the entire current line.
    for _ in range(lines_to_erase):
        stdout_write('\033[A\033[2K\r')
    
    stdout_flush()
 
def control_cursor(command: str):
    """A custom function to show or hide the terminal cursor."""
    # Skip if not compatible with ANSI escape codes.
    if not USE_ANSI: return
    
    if command == 'show':
        cprint('\033[?25h\r', end='')
        
    elif command == 'hide':
        cprint('\033[?25l\r', end='')
 
def visual_len(text: str):
    """Return the length of the longest line, ignoring ANSI codes."""
    if not text.strip(): return 0
    if not USE_ANSI: return len(text)
    lines = text.splitlines()
    lines_length = [len(ANSI_ESCAPE.sub('', line)) for line in lines]
    return max(lines_length)

def separator(before='', after='', char='─', color=GRY, width=console_width, end='\n'):
    """Display a line of hyphens or any horizontal symbol."""
    # Used console.out() instead of print() and our defined cprint(), because
    # others have an issue of printing double new line after.
    line = f'{color}{before}{char * width}{after}{RS}'
    console.out(line, end=end)
    
def box(*texts: str, title='Message', border_color='', text_color='', secondary_color='', width=console_width):
    """
    1) Draw a box using standard ASCII characters, respecting ANSI colors inside.
    2) Limitations:
       - When wrapping, ANSI codes are considered normal characters.
       - ANSI code must not be in the wrap point, as it'll get broken and useless.
       - If you give a string a special color, next lines must also have the ANSI
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
    if USE_COLORS: console.print(box_string, style=None, markup=False, highlight=False, soft_wrap=True, no_wrap=True, overflow='ignore')
    else: console.print(box_string)
    cprint('\r', end='')    # To prevent any extra blank line from appearing.
    
    # Show in GUI if requested.
    if ALWAYS_GUI_MODE:
        if len(message) < 128: return   # Don't bother show with short messages.
        with ProgressBar(bottom_toolbar=' Now using the quick markdown viewer... ', cancel_callback=lambda: None):
            if USE_ANSI: message = ANSI_ESCAPE.sub('', message)
            message = re.sub(r'(?m)^# ', '## ', message)
            message = message.replace('\n', '\n\n')
            content = f'<h1 style="text-align: center;">{title}</h1>\n\n{message}'
            quick_markdown_viewer(content)
    
def upload_preprocessor(mode: str):
    """
    A helper function used with upload_to_google() & upload_raw_file()
    to check message_to_send variable, file paths, etc...
    """
    global message_to_send
    
    # For upload_to_google(): Check if the message has already been processed by convert_raw_urls().
    # For upload_raw_file(): Check if it hasy been processed by convert_raw_urls() or upload_to_google().
    # This order is defined in interpret_special_commands().
    if not isinstance(message_to_send, list): message_to_send = [message_to_send]
    
    # Syntax: /file path/to/file.ext Rest of prompt text
    # Or with quotes: /file "path/to/my file.ext" Rest of prompt text
    # NOTE: same syntax for /upload, /raw, /content commands.
    # This splits the command, the path (handling quotes), and the rest.
    try:
        # posix = False preserves backslashes for Windows paths; and avoid escaping sequence.
        parts = shlex_split(converted_prompt, posix=False)
        
    except ValueError as error:
        if ERROR_LOG_ON: log_caught_exception()
        msg = f'A mistake was found in your message: {error}.\n{YLW}Check your commands & files paths!'
        box(msg, title='COMMAND MISTAKE', border_color=RED, text_color=RED, secondary_color=RED)
        return None
        
    except Exception as error:
        catch_exception(error)
        return None
    
    # Get paths & Remove them from the user prompt.
    paths = {}          # We use a dict to avoid duplicate files (a waste of tokens).
    if mode == 'to_google': cmd_1, cmd_2 = '/file', '/upload'
    elif mode == 'raw': cmd_1, cmd_2 = '/raw', '/content'
    
    for i, part in enumerate(parts):
        if i == len(parts) - 1: break
        if not CASE_SENSITIVITY: part = part.lower()
        if part in [cmd_1, cmd_2]:         
            # Regex to find this specific command + path pair
            part_1 = re.escape(part)
            part_2 = re.escape(parts[i+1])
            if CASE_SENSITIVITY: pattern = rf"{part_1}\s+(?:(['\"]){part_2}\1|{part_2})"
            else: pattern = rf"(?i:{part_1})\s+(?:(['\"]){part_2}\1|{part_2})"
            
            # Replace the string with: str + file-placeholder + str.
            for j, obj in enumerate(message_to_send[:]):
                if isinstance(obj, str) and re.search(pattern, obj):
                    before, _, after = re.split(pattern, obj, maxsplit=1)
                    replacement = []
                    placeholder_idx = j + (1 if before else 0)
                    if before: replacement.append(before)
                    replacement.append(None)    # A placeholder for the file/part object.
                    if after: replacement.append(after)
                    message_to_send[j:j+1] = replacement
                    break
            
            # Save the path if not duplicated (ignore dups in upload mode cause the file object is just a URL).
            path = parts[i+1].strip('"').strip("'")
            pointer = "(Refer to the file content provided previously in this message)"
            is_large_duplicate = False
            
            if mode == 'raw' and path in paths.values():
                try:
                    # Use encode() to compare bytes vs bytes
                    if os.path.getsize(path) > len(pointer.encode('utf-8')):
                        is_large_duplicate = True
                except (OSError, FileNotFoundError):
                    # If file is missing/inaccessible, we don't treat it as a duplicate pointer.
                    # We let the 'Check files existence' block handle it later.
                    pass

            if is_large_duplicate: message_to_send[placeholder_idx] = pointer
            else: paths[placeholder_idx] = path
    
    if not paths: return False

    # Check files paths to avoid time loss.
    errors_list = []
    for path in paths.values():
        file_name = get_file_name(path)
        error = None
        
        # 1. Check Existence.
        if not path_exist(path):
            error = f"your attached file '{path}' doesn't exist, perhaps you forgot to mention the full path, or to surround it by quotes?"
        
        # 2. Check if it's not a folder.
        elif os.path.isdir(path):
            error = f"'{path}' is a directory. Please provide a file path instead."
        
        # 3. Check if it's a regular file.
        elif not os.path.isfile(path):
            error = f"'{path}' is not a valid file (it might be a named pipe or a device)."
            
        # 4. Check Readability (Permissions).
        elif not os.access(path, os.R_OK):
            error = f"permission denied; cannot read '{path}'. Check file permissions!"
        
        if error:
            msg = f"[{file_name}]: {error}"
            errors_list.append(msg) 
        
    # Check all data size for 'raw' mode.
    # NOTE: File size in python is a bit smaller than its size on disk; but this
    #       isn't an issue, it's actually better (we get pure data size, without metadata overhead).
    if mode == 'raw':
        MAX_SIZE = 20  # 20 MB (defined by google).
        # Calculate text size (bytes).
        # At this stage, 'message_to_send' contains only strings or uploaded files URLs (which are negligeable).
        text_bytes = sum(len(s.encode('utf-8')) for s in message_to_send if isinstance(s, str))
        
        # Calculate file size (bytes).
        # Sum all file sizes first (to avoid losing decimals).
        # NOTE: There is no difference between file types (images/docs/txt); they are sent as
        #       raw binary bytes, so their size in transit is identical as in-here.
        file_bytes = sum(os.path.getsize(p) for p in paths.values() if path_exist(p))
        
        # Final conversion to MB (most APIs use 1024 instead of 1000).
        total_size = (text_bytes + file_bytes) / (1024 * 1024)
                
        if total_size > MAX_SIZE:
            total_size = round(total_size, 3)
            if total_size == 20: total_size = 20.001
            error = f'# NOTE! the data size you tried to send is {total_size} MB, but max allowed size is exactly {MAX_SIZE} MB.'
            errors_list.append(error)
        
    # Return our variables.
    return (paths, errors_list)

def guess_type(path: str):
    """
    Guess the mime type of a file before uploading it to avoid errors.
    Also fix known types to a standard string that won't get just rejected by the API.
    Because it only accepts official IANA standards (like 'image/jpeg' instead of 'image/jpg').
    * The 'mimetypes' library relies on a local database (E.g: on Windows, it's the Registry);
      because these databases are managed by the OS, they often contain non-standard or
      legacy strings (like audio/mp3 instead of the IANA-standard audio/mpeg).
    """
    # (strict=True) only returns official IANA types.
    mt = guess_mime_type(path, strict=True)[0]
    text_names = (   # Those types may not start with 'text/', so we need to fix them.
        'javascript', 'json', 'xml', 'csv', 'htm', 'yaml', 'x-sh', 'x-bash', 'php',
        'x-perl', 'x-python', 'wasm', 'toml', 'jsonld', 'vnd.ms-excel', 'x-markdown',
        'sparql-query', 'latex', 'x-tex', 'x-config', 'x-cfg', 'graphql', 'x-cmake',
        'x-git', 'x-properties', 'x-env', 'x-ruby', 'x-typescript', 'x-sql', 'srt', 'vtt',
    )
    
    match mt:
        # Special.
        case None | 'application/octet-stream': mt = ''  # Let the server guess.
        
        # Images.
        case 'image/jpg' | 'image/jfif' | 'image/pjpeg': mt = 'image/jpeg'
        case 'image/x-png': mt = 'image/png'
        
        # Documents.
        case 'application/epub+zip': mt = 'application/epub'
        case 'image/pdf': mt = 'application/pdf'
        case 'text/rtf': mt = 'application/rtf'
        case c if c.startswith('text/'): mt = 'text/plain'  # Gemini likes code as text/plain.
        case c if any(name in c for name in text_names): mt = 'text/plain'
        
        # Audio.
        case 'audio/mp3': mt = 'audio/mpeg'
        case 'audio/wav' | 'audio/x-wav': mt = 'audio/wav'
        case 'audio/m4a': mt = 'audio/mp4'

        # Videos.
        case 'video/quicktime': mt = 'video/mov'
        case 'video/x-msvideo': mt = 'video/avi'
        case 'video/x-matroska': mt = 'video/mkv'
        
        # Microsoft Office
        case 'application/msword': mt = 'application/msword'
        case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': mt = 'application/docx'
        case 'application/vnd.ms-excel': mt = 'application/xls'
        case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': mt = 'application/xlsx'
        case 'application/vnd.ms-powerpoint': mt = 'application/ppt'
        case 'application/vnd.openxmlformats-officedocument.presentationml.presentation': mt = 'application/pptx'
        case 'application/vnd.oasis.opendocument.text': mt = 'application/odt'
        case 'application/vnd.oasis.opendocument.spreadsheet': mt = 'application/ods'
        
    return mt

def update_placeholder(text=None, temp=False, restore=False):
    """
    Set the prompt placeholder to a random message.
    Placeholder is only set once per session, unless changed by open_path(),
    though it'll return to its last state.
    * temp: means change the placeholder temporarily, so keep 'last_placeholder'
      variable untouched to restore initial placeholder later.
    """
    global prompt_placeholder, last_placeholder
    
    # Restore to initial state & return.
    if restore:
        prompt_placeholder = last_placeholder
        return
    
    # Update it.
    if text: text = text.strip()
    if not text: text = choice(PLACEHOLDER_MESSAGES)
    placeholder = FormattedText([                   
        (PROMPT_GRY, text)
    ])
    
    # Don't change the last state if this is a temporary change.
    prompt_placeholder = placeholder
    if not temp: last_placeholder = placeholder

def compress_text(text: str):
    """
    Return a compressed version of a text by removing stop words & replacing
    long expressions with shortcuts.
    * Used always if (TEXT_COMPRESSION is True), unless the user uses /no-compress command.
    * Skipped if (TEXT_COMPRESSION is False), unless the user uses /compress command.
    """
    # Create a sorted list of keys (longest first).
    # We use a list because we only need the keys to build the pattern.
    # (?:s|es|ing|ed)? matches these common endings if they exist
    sorted_keys = sorted(SHORTCUT_WORDS.keys(), key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(re.escape(word) for word in sorted_keys) + r')(s|es|ing|ed)?\b',
              re.IGNORECASE)
    
    def replacer(m):    # m -> match.
        base_word = m.group(1).lower()
        suffix = m.group(2) if m.group(2) else ''
        return SHORTCUT_WORDS[base_word] + suffix
    
    text = pattern.sub(replacer, text)
    
    # Remove stop words and clean up spacing
    text = ' '.join([w for w in text.split() if w.lower() not in STOP_WORDS])
    return text

def clear_log_files():
    """
    Open log files, clear them, close :)
    Used with /del-log command.
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
        
    box(msg, title='LOG CLEANUP', border_color=color, text_color=color)

def load_config_file():
    """Load permanent settings from CONFIG_FILE."""
    global config_options, INITIAL_CONFIG
    
    # Load existing configuration, or start with default options.
    if os.path.exists(CONFIG_FILE):
        # raise PermissionError(13, 'Permission denied', 'protected_data.json')
        # raise OSError(13, 'Permission denied', 'secret_file.txt')
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        try:
            # raise json.JSONDecodeError(msg='hi', doc='hi2', pos=2)
            config = json.loads(content)
            config['repaired'] = False
        except json.JSONDecodeError as error:
            repaired, content = catch_json_error(error, CONFIG_FILE, content)
            if repaired:
                config = content
                config['repaired'] = True
            else:
                box(content, title='JSON ERROR', border_color=RED, text_color=RED)
                quit(1)
            
    else:
        config = DEFAULT_CONFIG.copy()

    # Add missing options.
    del content
    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
    
    # Save loaded configuration.
    INITIAL_CONFIG = config
    config_options = config.copy()
    
def save_config_file():
    """Save permanent settings to CONFIG_FILE - if there was a change."""
    try: conditions = config_options['repaired'] or (config_options != INITIAL_CONFIG)
    except (NameError, KeyError): return
    
    if conditions:
        del config_options['repaired']
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_options, f, indent=2)
                
        except:
            if ERROR_LOG_ON: log_caught_exception()
            pass

if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON or FILE_COMPRESSION:
    def load_system_instructions():
        """
        - Load system instructions at startup; they can be either implicit orders,
          saved info, or both.
        - Then return the configuration object.
        """
        system_instructions = ''
        media_resolution = None
        
        # Check saved info first.
        if SAVED_INFO and path_exist(SAVED_INFO_FILE):
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
        if not system_instructions: system_instructions = None
        
        # Check media resultion (how much tokens to use per attached file, lower resolution = less tokens but less AI accuracy).
        if FILE_COMPRESSION:
            media_resolution = 'MEDIA_RESOLUTION_LOW'
        
        # Create the configuration object if previous instructions were available.
        config = None
        if system_instructions or media_resolution:
            config = GenerateContentConfig(
                system_instruction=system_instructions,
                media_resolution=media_resolution,
            )
                
        return config

if PROMPT_HISTORY_MODE in ['temporary', 'permanent']:
    def load_prompt_history():
        """Load prompt history, either from memory or from file, depending on settings."""
        global history
        
        # From memory.
        if PROMPT_HISTORY_MODE == 'temporary':
            history = PromptHistory()
            
        # From file.
        else:
            try: copy_file(PROMPT_HISTORY_FILE, PROMPT_HISTORY_FILE + '.bak')
            except: pass
            history = PromptHistory(PROMPT_HISTORY_FILE)  

    if PROMPT_HISTORY_MODE == 'permanent':
        def prune_prompt_history():
            """
            Check the history file size. If > PROMPT_HISTORY_SIZE, this prunes the
            file to the nearest history block (timestamp).
            """
            if not path_exist(PROMPT_HISTORY_FILE):
                return
            
            # Check file size.
            MAX_SIZE = PROMPT_HISTORY_SIZE * 1024 * 1024
            file_size = os.path.getsize(PROMPT_HISTORY_FILE)
            if file_size <= (MAX_SIZE):
                return
            
            # Split file.
            # cprint(GR + 'Shrinking the prompt history file...' + RS)
            limited_size  = MAX_SIZE * 0.66
            
            start_seek_position = int(file_size - limited_size)
            with open(PROMPT_HISTORY_FILE, 'rb') as f:
                f.seek(start_seek_position)
                content_last_half = f.read().decode(sys.getdefaultencoding(), 'ignore')
            
            # Discard the broken content, keep the rest intact, and remove unwanted characters.
            pattern = re.compile(
                r'^#\s\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d+\r?\n\+',
                re.MULTILINE
            )
            
            match = pattern.search(content_last_half)
            if match:
                i = match.start()
                content_last_half = content_last_half[i:]
            
            # Write the kept file content.
            with open(PROMPT_HISTORY_FILE, 'w', encoding='utf-8') as f:
                content_last_half = content_last_half.replace('\r\n', '\n').replace('\r', '\n')
                f.write(content_last_half)
            
            # cprint(GR + 'Done!' + RS)
            # separator()
            return

if SUGGEST_FROM_WORDLIST_MODE in ['normal', 'fuzzy']:
    def load_word_completer():
        """
        Read a list of words from a file, one word per line.
        Use the words for realtime suggestions.
        """
        global word_completer
        
        try:
            # Add vars names in developper mode.
            words = []
            file_missing = False
            file_empty = False
            
            if DEV_MODE:
                words.extend([name for name in globals()])
                
            # Read the words from file.
            try:
                with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
                    words.extend([line.strip() for line in f if line.strip()][4:])
            except FileNotFoundError:
                file_missing = True
            
            if not words:
                file_empty = True
            
            # Load the word completer instance according to user settings.
            if words:
                # Sort & remove duplicates.
                words = sorted(set(words), key=len)
                if SUGGEST_FROM_WORDLIST_MODE == 'fuzzy':
                    word_completer = LimitedWordCompleter(words)
                else:
                    # This regex defines what characters are part of a "word".
                    # '\w' matches letters/numbers, and we add '-' for our commands & custom wordlist.
                    # word_pattern = re.compile(r'[\w-]+')
                    word_completer = LimitedWordCompleter(words, ignore_case=True)
            
        except FileNotFoundError:
            pass
        
        finally:
            if file_missing or file_empty:
                cprint()  # Because load_chat_history() doesn't add a line break after its separator.
                clear_lines()
                # if LOAD_CHAT_MODE == 'ask': cprint()    # Perfection.
                cprint()
                warning = f"{YLW}Suggestions from a wordlist is ON, but '{WORDLIST_FILE}' file is "
                if path_exist(WORDLIST_FILE): warning += "empty!"
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
        * This is needed for all typing animations.
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

    if RESPONSE_EFFECT == 'line':
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

    elif RESPONSE_EFFECT == 'word':
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
                parts = WORD_SPACE_PATTERN.split(str(line))
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

    elif 'char' in RESPONSE_EFFECT:      
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
        
        if RESPONSE_EFFECT == 'char fast':
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

if ERROR_LOG_ON:
    def shrink_log_file():
        """Shrink the log file to a target size by keeping the most recent lines."""
        # Quick Check.
        MAX_SIZE = LOG_SIZE * 1024 * 1024
        if not path_exist(ERROR_LOG_FILE): return
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
        while collected_lines and collected_lines[-1].strip() != LOG_SEPARATOR:
            collected_lines.pop()
            
        collected_lines.pop()    
        collected_lines.reverse()
        
        # Write the shrunk content to the new file.
        try:
            with open(ERROR_LOG_FILE, 'w', encoding='utf-8') as f:
                f.writelines(collected_lines)
        except:
            if ERROR_LOG_ON: log_caught_exception()
            return









# 5) Part VI: Command Handlers ---------------------------------------------------------------------
def help(mode: str):
    """Display guides with the commands /help, /help-2, /help-3 or /cheat."""
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
       -CTRL-A to copy your current prompt text to clipboard.
       -CTRL-Z/CTRL-Y to undo/redo.
       -ALT-X to cut current prompt line.
       -CTRL-P (Remember P = Paste) or CTRL-T or ALT-V to paste long
        text & avoid lag (CTRL-V will cause lag with long paste).
       -CTRL-G to call our graphical text editor, quick & handy.
        (Hotkeys may vary slightly)
       -ALT-G to call our graphical markdown viewer & see last AI response.
       -CTRL-X-CTRL-E to call external editor - if its option is ON.
        (Once the editor is closed, changes are registered & submitted)
       -And even more if you enable (VIM_EMACS_MODE) in settings.
    
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
       /file or /upload followed by a file path to upload files.
        (Can be used multi-times in a prompt, but may consume tokens)
       /save-last to save last AI response to a text file.
        (You will lose the formatting style and colors!)
       /restart for a quick session restart.
       /quit or /exit to leave.
       /discard to destroy everything done in current session and restart.
        (Won't affect log files & manually saved content)
       /kill to destroy everything done in current session and exit.
    
    4) F-Keys & Their Commands:
       -F1: /show
       -F2: /copy
       -F3: /upload
       -F4: /raw
       -F5: /quit
       -F6: /help
       -F3-F4: /dir (Press them at once)
    
    5) More Commands:
       /quick-chat to open a new console window with a different chat mode.
       /save-chat to save the whole chat to a readable text file.
       /last-links or /last-urls to see the links of your last successfully
        uploaded files.
       /saved-links or /saved-urls to see ready-to-use links of your
        previously uploaded files.
       /recover to use a generated prompt upon a failed upload attempt,
        where successfull files paths are replaced with their URLs to avoid
        re-uploading.
       /raw or /content followed by a file path to add the file content
        as-is to your prompt, it won't be uploaded/saved to goole servers.
        (Can be used multi-times in one prompt, but may consume tokens;
        plus its limited in size & file types).
       /dir or /folder followed by a directory path to upload every file
        in it to google servers (Sub-directories are ignored).
       /open to open the program's directory.
       /original at prompt start, so it won't be checked for commands, but
        will be sent as-is.
       /compress to compress your prompt text once; attached files won't be
        affected (useless if TEXT COMPRESSION setting is ON).
       /no-compress to skip compression for ur prompt text once; attached files
        won't be affected (useless if TEXT COMPRESSION setting is OFF).
       /editor or /gui to open our graphical text editor.
       /viewer, /preview or /markdown to open the quick markdown viewer and
        see the last AI response.
       /external to call the external editor.
       /switch to temporarily switch your API key or the current Gemini model
        quickly in chat; useful if you exceeds your API limits.
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
       /del-links or /del-urls to delete saved links of uploaded files.
       /del-output to remove AI generated files.
       /del-uploaded to remove your uploaded files from Google server.
       /del-log to clear both log files, future logs won't be affected.
       /del-all to wipe private files: chat + prompt history + log files
        + saved info, etc (No cancel option!)
       /stats or /statistics to show total N° of message in current chat.
       /about for program information.
       /license for copyright.
       /version for the program's release number.
       /secret to start solving our puzzle.
    
    6) More Shortcuts (System / Terminal Dependent):
       -CTRL-L to clear screen.
       -CTRL-U to clear current line in prompt.
       -CTRL-R (Reverse Search) to search backward & find the most recent
        match in prompt history, keep pressing to move, press ESC to cancel
        or confirm (ESC to confirm, not ENTER!).
       -CTRL-S (Forward Search) used after CTRL-R to find older matches,
        keep pressing to move.

    7) Limitations:
       -Tables with many columns will appear chaotic.
       -Special characters (Like LaTeX syntax) will appear as a plain text.
       -You are a prisonner of your own terminal's limitations.
       -Some other bugs I didn't discover yet :/
    
    8) Notes:
       * Please avoid uploading big files or adding raw long text files,
         they'll be counted as tokens; the program will refuse to send them
         in this case just to save your tokens, because Google will refuse
         them anyway - except that it'll count the tokens!
       * If you have any question, issue or suggestion, please let me know in:
         {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}
    """
    
    # Regular version.
    REGULAR = f"""
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
       -CTRL-G to call our graphical editor, quick & handy.
        (Hotkeys may vary)
    
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
       /file or /upload followed by a file path to upload files.
        (Can be used multi-times in a prompt, but may consume tokens)
       /save-last to save last AI response to a text file.
        (You will lose the formatting style and colors!)
       /restart for a quick session restart.
       /quit or /exit to leave.
       /discard to destroy everything done in current session and restart.
        (Won't affect log files & manually saved content)
       /kill to destroy everything done in current session and exit.
    
    4) F-Keys & Their Commands:
       -F1: /show
       -F2: /copy
       -F3: /upload
       -F5: /quit
       -F6: /help
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
       -F3 to upload file(s).
       -CTRL-C to clear / cancel a prompt, stop a response, or quit.
       -UP/DOWN arrows to navigate between input lines / history prompts,
        or to accept word suggestions.
    
    3) Commands:
       /show to show last AI response.
       /copy to copy last AI response to clipboard.
       /quit or 'exit' to leave.
       /help for this guide menu.
       {GR}/help-2 for a longer version of this guide.{RS}
       {GR}/help-3 for the full guide (No yada yada).{RS}
       {GR}/cheat for a short cheat sheet.{RS}
    """
    
    # Cheat Sheet version.
    CHEAT = """
    - If you cancel a sent prompt earlier, Google will not receive it at all
      (Yeah, privacy!).  
    
    - Avoid huge files & long prompts; program may refuse them to avoid
      Google's tokens errors.
    
    - Avoid long text paste, it'll cause lag; use CTRL-P to paste it safely,
      or use CTRL-G or CTRL-X-CTRL-E to edit it.
    
    - Set options in 'settings.py' to your preferences (Default isn't always
      the best).
          
    - Explore the useful commands in the help menu; c'mon type '/help', you'll
      feel like a programmer!
      
    - Solve our puzzle in the 'Secret' folder to gain access to the...
      (Shhhh... it's secret).
    """
    
    title = 'HELP MENU'
    if mode == 'short': message = SHORT
    elif mode == 'regular': message = REGULAR
    elif mode == 'long': message = LONG
    else:
        title = 'CHEAT SHEET'
        message = CHEAT
        
    message = ltrim(textwrap.dedent(message)).rstrip()
    box(message, title=title, border_color=YLW, text_color=YLW, secondary_color=YLW)

def farewell(confirmed=False):
    """
    Display a random but beautiful farewell message upon quitting.
    Also give the user a chance to go back.
    Used with /quit or /exit command, or any other exit door (or window :).
    """
    global FAREWELLS_MESSAGES, CANCEL_MESSAGES, confirm_separator
    
    # If the user is supressing questions; then exit is confirmed.
    cprint(RS, end='')
    if NO_QUESTIONS and (not confirmed):
        cprint()
        confirmed = True
    
    # If not confirmed by /quit command, and not supressed; then ask.
    wrong_answer = 0
    if not confirmed:
        cprint()
        if confirm_separator: separator()
        confirm_separator = True
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
            cprint(GR + choice(CANCEL_MESSAGES) + RS)
            separator()
            return
        else:
            cprint()
    
    # Save chat.
    saved = save_chat_history_json(up_separator=confirmed, down_separator=False)
    if saved: cprint()
    elif not saved and confirmed: separator()
    
    # Show a farewell message.
    if FUN_MODE:
        from useless import QUOTES, ADVICES, FACTS, JOKES, MATH
        messages = [*FAREWELLS_MESSAGES, *QUOTES, *ADVICES, *FACTS, *JOKES, *MATH]
    else:
        from useless import QUOTES, ADVICES
        messages = [*FAREWELLS_MESSAGES, *QUOTES, *ADVICES]    # Unpacking with (*) is faster than copying with (+).
    
    messages = [m for m in messages if len(m) < 256]
    msg = choice(messages)
    if (not wrong_answer) and (not saved) and (not confirmed) and \
        msg.count('\n') == 0 and len(msg) <= glitching_text_width:
        clear_lines()
    cprint(GR + msg + RS)
    
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
    
    if not last_response:
        # This is just a guard.
        if command == 'return':
            return msg
    
    elif command == 'save-last':
        # Save the last response & Show the file.
        try:
            with open(LAST_RESPONSE_FILE, "w", encoding='utf-8') as f:
                f.write(last_response)
            
            path = os.path.abspath(LAST_RESPONSE_FILE)
            msg = f"Last response successfully saved to:\n{path}"
            color = GR
            open_path(LAST_RESPONSE_FILE)
        
        except Exception as error:
            if ERROR_LOG_ON: log_caught_exception()
            msg = f"Failed to save last response!\n{error}"
            color = RED
    
    elif command == 'show':
        # Display the last response.
        print_response(last_response, title='Last Gemini Response')
        return
    
    elif command == 'copy':
        # Copy the response to clipboard.
        msg = 'Last response was copied to clipboard!'
        copy_to_clipboard(last_response, msg)
        return
    
    elif command == 'return':
        return last_response
    
    box(msg, title='STATUS', border_color=color, text_color=color)

def store_last_turn_for_exclusion(n_turns=1, remove_all=False):
    """
    Retrieve the last user message and model reply and store them globally.
    Then use them inside serialize_history() for elimnination.
    Used with /pop-last or /pop-all commands.
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
        if n_turns > history_len / 2:
            n_turns = history_len // 2
            msg = f'{RED}Overflow! falling back to current chat history length: ({n_turns}).\n'
        
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
        
        # Just in case, ensure no message is kept in case of 'pop-all'.
        if remove_all and (n_turns != history_len / 2):
            messages_to_remove.append(0)
            messages_to_remove_steps[-1] += 1
            issue = True
        
        if issue:
                msg += f'\n{YLW}Found a small problem in chat history, but it should have been fixed.'
                msg += f"\n{YLW}You can check '{CHAT_HISTORY_JSON}' file later to eliminate doubt."
    
        msg += "\nChanges will take effect at next session, you can type /restart for a quick refresh; "
        msg += "or type /restore-last or /restore-all to cancel."
        
    box(msg, title='STATUS', border_color=color, text_color=color, secondary_color=color)

def restore_removed_messages(command: str):
    """
    Restore either every deleted message pair. Or restore only the last
    popped/removed messages, so earlier removed ones will not be restored.
    Used with /restore-last or /restore-all commands.
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
        
    box(msg, title='STATUS', border_color=color, text_color=color)

def save_chat_history_text():
    """
    Save the chat history as a readable text file, without json formatting.
    Used with /save-chat command.
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
            delimiter = '\n' + '─' * 90 + '\n'
            chat_text = delimiter.join(chat_lines)
            with open(CHAT_HISTORY_TEXT, 'w', encoding='utf-8') as f:
                f.write(chat_text)
            
            open_path(CHAT_HISTORY_TEXT)
            msg = f"Chat successfully saved to '{CHAT_HISTORY_TEXT}'.\n"
            msg += "Long lines were saved as-is to preserve formatting; you may need to use 'word-wrap' feature in your text viewer/editor." 
            color = GR
        
        except Exception as error:
            if ERROR_LOG_ON: log_caught_exception()
            msg = f"Failed to save chat!\n{error}"
            color = RED
    
    else:
        msg = "Current conversation is empty!"
        color = YLW
    
    box(msg, title='STATUS', border_color=color, text_color=color)

def del_all():
    """
    Nuclear option, perform a factory reset for the program data (Doesn't affect settings).
    Used with /del-all command.
    """
    global discarding
    
    # Warn the user.
    cprint()
    separator(color=YLW)
    to_remove_files = [
        CHAT_HISTORY_JSON, CHAT_HISTORY_TEXT, LAST_RESPONSE_FILE, SAVED_INFO_FILE,
        SAVED_LINKS_FILE, PROMPT_HISTORY_FILE, RECOVERY_PROMPT_FILE,
        TEMP_PROMPT_FILE, ERROR_LOG_FILE, GLOBAL_LOG_FILE,
    ]
    
    to_remove_dirs = [FILE_GENERATION_DIR]
    
    cprint(f'{YLW}WARNING! The program will exit & wipe the following:')
    for file in to_remove_files: cprint('- ' + file)
    for folder in to_remove_dirs: cprint('- ' + folder + ' (directory)')
    cprint('')
    
    # Confirm.
    text = f"Are you sure you want to reset everything? (y/n): {RS}"
    if GLOBAL_LOG_ON: in_time_log(text + '...')
    
    try:
        confirm = input(text).lower().strip()
    except Interruption:
        cprint()
        confirm = None
    
    # Cancel.
    if confirm != 'y':
        cprint(GR + choice(CANCEL_MESSAGES) + RS)
        separator(color=YLW)
        return
    
    # Do it.
    cprint(f'\n{GR}# Clearing everything & Quitting...')
    for file in to_remove_files:
        try:
            with open(file, 'w', encoding='utf-8'): pass
            cprint(f"{GR}[✓] File '{file}' cleared!{RS}")
        except:
            if ERROR_LOG_ON: log_caught_exception()
            cprint(f"{RED}[✗] File '{file}' couldn't be deleted!{RS}")
    
    for folder in to_remove_dirs:
        try:
            remove_dir(folder)
            cprint(f"{GR}[✓] Directory '{folder}' deleted!{RS}")
        except:
            if ERROR_LOG_ON: log_caught_exception()
            cprint(f"{RED}[✗] Directory '{folder}' couldn't be deleted!{RS}")
            
    discarding = True
    separator(color=YLW)
    raise SystemExit

def del_uploaded_files():
    """
    Delete all of the files that have been uploaded to Google File API server.
    They'll deleted in 48h hours anyway, but you know... self control.
    """
    try:
        # List files & Warn the user.
        separator()
        cprint(f"{YLW}Warning! You are going to delete the following file(s) from Google server:\nand (Their saved links will no longer work)")
        with console.status(status=f'[bold {STATUS_CYN}]Retrieving info...[/bold {STATUS_CYN}]',
                            spinner=SPINNER):
            files = list(client.files.list())
        
        length = len(files)
        if length == 0:
            cprint("\nWell, you don't have any files on Google server for now\n(Remember they only last for 48h).")
            separator()
            return
        
        for file in files[:10]: cprint(f'- {file.display_name}')
        if length > 10: cprint(f'* And another ({length - 10}) file(s).')
        if GLOBAL_LOG_ON: in_time_log('\nAre you sure you want to proceed? (y/n): ...')
        
        try:
            confirm = input(f'\nAre you sure you want to proceed? (y/n): {RS}')
        except Interruption:
            cprint()
            confirm = None
            
        if confirm != 'y':
            cprint(GR + choice(CANCEL_MESSAGES) + RS)
            separator()
            return
        
        # Delete all files.
        cprint(GR, end='')
        for file in files:
            cprint(f"- Deleting: '{file.display_name}'...")
            # raise ConnectionError('Hi!')
            client.files.delete(name=file.name)
            
        cprint(f"\n{GR}All files have been removed from the server!")
        cprint("You may want to use /del-links command to clear the saved URLs list.")
        separator()
        
    except Interruption:
        cprint(f'{YLW}# Cancelled by you...')
        separator()
            
    except Exception as error:
        if ERROR_LOG_ON: log_caught_exception()
        error_type = type(error).__name__
        try: msg = error.message     # Get 'message' attribute from 'genai' errors.
        except: msg = error.args[0]  # Built-in excepetions have 'args' tuple, 1st item is the message.
        print(f'\n{RED}# {error_type}: {msg}.')
        separator()
   
def statistics():
    """
    Inform the user of his data statistics.
    Used with /stats or /statistics commands.
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
    if path_exist(SAVED_INFO_FILE):
        with open(SAVED_INFO_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        info = content.split('\n- ')
        info = [i for i in info if i.strip()]
        n = len(info)
        msg += f'\nTotal N° of saved info: ({n}).'
        if not SAVED_INFO: msg += f'\n{YLW}(Saved info are disabled, but the file exists)'
    
    # Check prompt-history.
    if PROMPT_HISTORY_MODE in ['temporary', 'permanent']:
        prompts = list(history.get_strings())
        n = len(prompts)
        msg += f'\nTotal N° of prompts in prompt-history: ({n}).'
    
    if path_exist(PROMPT_HISTORY_FILE) and PROMPT_HISTORY_MODE != 'permanent':
        with open(PROMPT_HISTORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prompts = content.split('\n\n# 20')
        prompts = [p for p in prompts if p.strip()]
        n = len(prompts)
        if n: msg += f"\n{YLW}(In-file prompt history is disabled, but the file still contains: ({n}) entries)\n"
    
    # Check wordlist suggestion.
    if path_exist(WORDLIST_FILE):
        with open(WORDLIST_FILE, 'r', encoding='utf-8') as f:
            content = f.readlines()[4:]
        
        words = [w for w in content if w.strip()]
        n = len(words)
        msg += f'\nTotal N° of words in the suggestion wordlist: ({n}).'
        if not SUGGEST_FROM_WORDLIST_MODE: msg += f'\n{YLW}(Suggestions are disabled, but the file exists)'
    
    # Show it.
    msg = msg.strip() + f'\n\n{CYN}(Remember, You have the commands to control your data)'
    box(msg, title='STATISTICS', border_color=GR, text_color=GR, secondary_color=YLW)

def quick_chat():
    """
    Launch a specific chat mode in a new console.
    Used with /quick-chat command.
    """
    from subprocess import Popen, CREATE_NEW_CONSOLE
    
    # Choose a mode.
    separator(before='\n', color=GR)
    prompt = GR + 'Quick chat modes (simple, focused, but less featured):\n\n'
    prompt += '1) Momentary: Single-turn (no memory between messages).\n'
    prompt += '2) Temporary: At exit, history is forgotten.\n'
    prompt += '3) File Generator: Generate simple files (no memory).\n'
    prompt += '4) Image Generator: Generate simple images (no memory).\n'
    prompt += '5) Researcher: For online info & events (temporary).\n\n'
    prompt += 'Choose 1-5: ' + RS
    
    if GLOBAL_LOG_ON: in_time_log(prompt + '...')
    try:
        mode = input(prompt).strip()
    except Interruption:
        cprint(f'\n{YLW}{choice(CANCEL_MESSAGES)}')
        separator(color=GR)
        return
    
    match mode:
        case '1': file = 'momentary_chat.py'
        case '2': file = 'temporary_chat.py'
        case '3': file = 'file_generator.py'
        case '4': file = 'image_generator.py'
        case '5': file = 'google_searcher.py'
        case _:
            cprint(RED + 'Invalid option; aborting...')
            separator(color=GR)
            return
    
    # Use current python interpreter to execute another '.py' file.
    cprint(GR + 'Opening the new chat...' + RS)
    file = os.path.join('Modes', file)
    Popen([sys.executable, file], creationflags=CREATE_NEW_CONSOLE)
    separator(color=GR)

def open_path(path_to_open, clear=0, restore_prompt='', set_placeholder=''):
    """
    - Open a file or a folder using the default OS application/file manager.
    - Add a quick cleanup if requested.
    - Work reliably across Windows, macOS, and Linux.
    - Used with /open, /saved-info and other file commands.
    """
    global default_prompt, prompt_placeholder
    
    # Check if the file/folder exists.
    if not path_exist(path_to_open):
        msg = "Requested file/folder isn't present in the current working directory."
        box(msg, title='ERROR', border_color=RED, text_color=RED)
        return

    # webbrowser.open() handles both files and directories.
    # It doesn't raise errors; it only returns True or False.
    browser_open(path_to_open)
    if GLOBAL_LOG_ON: in_time_log(' ')
    if clear: clear_lines(clear)
    if restore_prompt: default_prompt = restore_prompt
    elif set_placeholder: update_placeholder(set_placeholder, temp=True)

def copy_to_clipboard(text: str, msg='Text copied to clipboard!', color=GR, hidden=False):
    """
    Copies a string to the system clipboard using pyperclip library.
    Used with /copy command or CTRL-A.
    Works seamlessly across Windows, macOS, and Linux.
    """
    if clip_copy is None:
        msg = "Missing Dependency! Pyperclip library isn't installed!\nType 'pip install pyperclip' to install it."
        color = RED
    
    else:    
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
    
    # Show status if not hidden/silent; return True to signal success.
    if not hidden:
        box(msg, title='STATUS', border_color=color, text_color=color, secondary_color=color)
    
    if color == GR:
        return True

def paste_from_clipboard():
    """
    Return data from system clipbaord.
    Work with ALT-V, CTRL-T or CTRL-P.
    """
    if clip_copy is None:
        error = "Missing Dependency! Pyperclip library isn't installed!\nType 'pip install pyperclip' to install it."
        return (False, error)
    try:
        text = clip_paste()
        return (True, text)
    except Exception as error:
        if ERROR_LOG_ON: log_caught_exception()
        return (False, error)

def copy_last_prompt():
    """
    Copy the user's last sent message to cpliboard.
    Used with /copy-prompt command.
    """
    # Last prompt is already stored in memory as 'last_prompt'.
    global last_prompt
    msg = 'Your last prompt was copied to clipboard!'
    color = GR
    
    # Fallback to prompt history.
    if (not last_prompt) and PROMPT_HISTORY_MODE in ['temporary', 'permanent']:
        try: last_prompt = list(history.get_strings())[-2]
        except: pass
        
    # Warn.
    if not last_prompt:
        msg = 'No prompt was found; neither in memory, nor in file.'
        color = YLW
    
    # Do it.
    copy_to_clipboard(last_prompt, msg, color)

def convert_raw_urls():
    """
    If user prompt has private API URLs, convert them to objects that Gemini
    can access & understand.
    (Used inside interpret_special_commands() function).
    """
    global message_to_send
    if not path_exist(SAVED_LINKS_FILE): return
    
    # Syntax: https://generativelanguage.googleapis.com/v1beta/files/abcdefhijklm   
    mark = 'generativelanguage.googleapis.com/'
    
    # Start resolving URLs.
    content_parts = []
    errors_list = []
    with open(SAVED_LINKS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # We'll keep the order of user-strings & attached-files-URLs.
    parts = re.split(r'(\s+)', message_to_send)
    pure_prompt_text = ''

    # This operation is fast, so it doesn't need a status or a CTRL-C handler.
    for part in parts:
        if mark in part and '/files/' in part:
            # Push any text we've collected so far.
            if pure_prompt_text:
                content_parts.append(pure_prompt_text)
                pure_prompt_text = ''

            # Get the mime_type from file.
            part = part.rstrip('/')
            i1 = content.find(part)

            # Check if it's available.
            if i1 == -1:
                mime_type = ''                      # Let the server guess.
            else:
                i1 += len(part) + 1
                i2 = content[i1:].find('\n') + 5    # (5) to remove the word 'Type:'
                mime_type = content[i1:i2].strip()

            # Get the file object.
            try:
                file_part = Part.from_uri(file_uri=part, mime_type=mime_type)
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                try: error = error.message
                except: pass
                msg = f"[{part}]:\n{error}"
                errors_list.append(msg)
                continue

            # Save changes.
            content_parts.append(file_part)
            # message_to_send = message_to_send.replace(part, '')

        else:
            pure_prompt_text += part

    # Append any remaining text after the loop finishes.
    if pure_prompt_text: content_parts.append(pure_prompt_text)

    # Check errors & Cancel sending the message.
    if errors_list:
        msg = '\n\n'.join(errors_list)
        n = len(errors_list)
        if len(content_parts) == 1: msg = f'{YLW}Resolving URLs failed:\n' + msg
        elif n == len(content_parts): msg = f'{YLW}Resolving failed for all URLs! Details:\n' + msg
        else: msg = f'{YLW}Resolving failed for some URLs! Details:\n' + msg
        msg += f'\n\n{YLW}- Press (UP) to get your prompt back.\n'
        clear_lines(1)
        box(msg, title='LINKS ERROR', border_color=RED, text_color=RED, secondary_color=RED)
        return False

    # Save & Send the message.
    message_to_send = content_parts
    return True

def convert_folder_to_files():
    """
    If the user uses the /folder command followed by a directory path, this will
    replace that command-dir pair with all of the files in that dir.
    Sub-dirs are ignored.
    """
    global message_to_send
    
    # 'message_to_send' is still a string at this stage.
    # Pattern finds /dir or /folder followed by the path.
    if CASE_SENSITIVITY: pattern = r"/(?:dir|folder)\s+(['\"]?)(.*?)\1(?=\s|$)"
    else: pattern = r"(?i)/(?:dir|folder)\s+(['\"]?)(.*?)\1(?=\s|$)"
    
    # Iterate over user message to replace all /dir commands.
    errors_list = []
    match = re.search(pattern, message_to_send)
    
    while match:
        # 'group(2)' is the path string captured by the regex (inside the quotes).
        path = match.group(2)
        
        # Check if the dir exist.
        if os.path.isdir(path):
            # List dir items (ignore sub-dirs & their sub-files).
            files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            files.sort()
            # Convert list of files back into a string of /file commands.
            files = '\n'.join([f'/file "{f}"' for f in files]) + '\n'
            message_to_send = re.sub(pattern, lambda _: files, message_to_send, count=1)    # We use lambda to tell 're.sub' to treat the string as literal text without mangling slashes & quotes.
        else:
            msg = f"[{path}]: "
            if not path_exist(path): msg += "this directory doesn't exist, perhaps you forgot absolute path or quotes?"
            else: msg += "this isn't a valid directory path; perhaps it requires permissions, or it's a file."
            errors_list.append(msg)
            # Remove the command-dir pair to continue finding error; user message won't be sent anyway.
            message_to_send = re.sub(pattern, '', message_to_send, count=1)
        
        match = re.search(pattern, message_to_send)
    
    # Check errors & Cancel sending the message.
    if errors_list:
        msg = f'{YLW}Resolving one or more directories failed! Details:\n'
        msg += '\n\n'.join(errors_list)
        msg += f'\n\n{YLW}- Press (UP) to get your prompt back.\n'
        box(msg, title='DIRECTORY ERROR', border_color=RED, text_color=RED, secondary_color=RED)
        return None
    
    return True
    
def upload_to_google():
    """
    Uploads any file (txt, pdf, png, mp4, etc) to Google's File API.
    Any file uploaded to Google’s servers using this File API is auto-deleted after 48 hours.
    We can upload files of the same name without issues, Google handle that.
    This API will refuse non-standard files like DOCX, although the webapp accepts them.
    Works with /file or /upload commands.
    """
    global uploading, message_to_send, last_urls, recovery_prompt
    
    value = upload_preprocessor(mode='to_google')
    if value == False: return True    # No path found, send message normally.
    elif value == None: return None   # Error occured, cancel all.
    else: paths, errors_list = value
    
    url_list = ''
    uploaded_files = {}
    
    if not errors_list:
        MAX_RETRIES = 3
        N_FILES = len(set(paths.values()))   # Don't count duplicate files.
        n = 1
        for idx, path in paths.items():
            disconnected = 0
            for attempt in range(MAX_RETRIES + 1):
                try:
                    # raise ServerError(code=403, response_json={'status': 'Failed', 'reason': 'Unknown', 'message': 'Test' * 25})
                    # Turn uploading flag ON, and reset last used URLs.
                    if not uploading:
                        cprint()
                        uploading = True
                        last_urls.clear()
                    
                    # Check if it's already uploaded.
                    if path in uploaded_files:
                        # Use its URL directly instead of reuploading.
                        message_to_send[idx] = uploaded_files[path]
                        break
                    
                    # Send the file to Google servers in another thread to keep UI responsive.
                    file_name = get_file_name(path)
                    if disconnected: status = f"Lost connection, retrying for '{file_name}'..."
                    else: status = f"Uploading file '{file_name}'..."
                    indicator = f'[{n}/{N_FILES}] ' if N_FILES > 1 else ''
                    status = f"[bold {STATUS_PURP}]{indicator}{status}[/bold {STATUS_PURP}]"
                    
                    uploader = FileUploader(client, path)
                    active = uploader.is_alive
                    uploader.start()

                    with console.status(status=status, spinner=SPINNER):
                        while active(): uploader.join(SLEEP_INTERVAL)
                        
                    if uploader.exception: raise uploader.exception
                    uploaded_file = uploader.uploaded_file
                          
                    # Check if google returned a non-empty object.
                    if not uploaded_file:
                        msg = f"received Google File object for '{path}' contained nothing; wait for sometime if you uploaded too many times..."
                        raise ServerError(code=403, response_json={'status': 'Failed', 'reason': 'Unknown', 'message': msg})
                    
                    # Store the uploaded file.
                    uploaded_files[path] = uploaded_file
                    message_to_send[idx] = uploaded_file
                    url = uploaded_file.uri
                    last_urls[path] = url
                    n += 1
                        
                    # Save the given URL (to avoid re-uploading later).
                    date = datetime.now().strftime('%A, %B %d, %Y %I:%M %p')
                    m_type = uploaded_file.mime_type
                    url_list += f'File: {path}\n'
                    url_list += f'Type: {m_type}\n'
                    url_list += f'Link: {url}\n'
                    url_list += f'Upload Date: {date}\n\n'
                    break
                
                except Interruption:
                    # Our thread is a daemon, so it's already dead here.
                    msg = f"Uploading stopped and the message is cancelled.\nURLs for successful files might still be saved in: '{SAVED_LINKS_FILE}'."
                    clear_lines()
                    box(msg, title='KEYBOARD INTERRUPTION', border_color=GR, text_color=GR, secondary_color=GR)
                    uploading = False
                    return
                    
                except NetworkExceptions:
                    # Try three more times before stopping.
                    if disconnected == 3:
                        catch_network_error()
                        uploading = False
                        return
                    else:
                        disconnected += 1
                        continue
                    
                except Exception as error:
                    if ERROR_LOG_ON: log_caught_exception()
                    try: error = error.message
                    except: pass
                    msg = f"[{file_name}]: {error}"
                    errors_list.append(msg)
                    break
    
    # Write URLs to a file. Also shrink the file if it's too long.
    if url_list:
        if not path_exist(SAVED_LINKS_FILE):
            open(SAVED_LINKS_FILE, 'w').close()
            
        with open(SAVED_LINKS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        notes = "# This is a list of the files you uploaded to Gemini; used to avoid re-uploading.\n"
        notes += "# Each file's link can be reused within 48h of its upload date.\n"
        notes += "# The first ones here are the most recent.\n"
        notes += "# [!] Only Gemini can access these links with their specific API key, not you!"
        sep = '─' * 80
        old_urls = content.lstrip(notes).strip()
        new_urls = '\n\n' + url_list.strip() + '\n' + sep + '\n'
        new_content = notes + new_urls + old_urls
        
        if new_content.count('\n') > 200:
            lines = new_content.splitlines()[:200]
            while lines[-1] != sep: lines.pop()
            new_content = '\n'.join(lines[:-1])
        
        with open(SAVED_LINKS_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)

    # Tell the user how many files failed to upload (user message won't be sent).
    if errors_list:
        # Clarify the errors.
        msg = '\n\n'.join(errors_list)
        n = len(errors_list)
        if len(paths) == 1: msg = f'{YLW}Upload failed:\n' + msg
        elif n == len(paths): msg = f'{YLW}Upload failed for all files! Details:\n' + msg
        else: msg = f'{YLW}Upload failed for some files! Details:\n' + msg
        msg += f'\n\n{YLW}- Press (UP) to get your prompt back.'
        msg += f'\n{YLW}- You can try /raw command instead of /file for failed files.'
        
        # Prepare a recovery prompt.
        if url_list:
            recovery_prompt = user_input
            # Sort paths by length (longest first) so 'final_report.pdf' 
            # isn't accidentally caught by 'report.pdf'
            sorted_paths = sorted(last_urls.keys(), key=len, reverse=True)
            for path in sorted_paths:
                url = last_urls[path]
                
                # This regex looks for:
                # 1. /file or /upload
                # 2. Any amount of whitespace \s+
                # 3. The path, optionally surrounded by quotes
                # 4. (?i:/file|/upload) makes ONLY the command case-insensitive; path remains sensitive.
                escaped_path = re.escape(path)
                if CASE_SENSITIVITY: pattern = rf"/(?:file|upload)\s+(?:(['\"]){escaped_path}\1|{escaped_path}(?=\s|$))"
                else: pattern = rf"(?i:/(?:file|upload))\s+(?:(['\"]){escaped_path}\1|{escaped_path}(?=\s|$))"
                
                # re.sub() replaces the entire match (command + path) with just the URL
                file_name = get_file_name(path)
                replacement = f'[{file_name}]: {url}'
                recovery_prompt = re.sub(pattern, replacement, recovery_prompt)
                
                # Add the recovery suggestion.
                msg += f"\n{GR}- Successful files are already in the cloud; type /recover.{RS}"
                msg += f'\n{GR}- Or for manual edit, type /last-links & press ENTER.\n'
        
        # Display.
        box(msg, title='UPLOAD ERROR', border_color=RED, text_color=RED, secondary_color=RED)
        uploading = False
        return
    
    # Instead of raw data, we now send the 'Google File' objects (Which represent the shared files URLs).
    return True

def upload_raw_file():
    """
    Read a file from disk and wrap it in a Gemini Part object.
    Send its content directly without using Google File API.
    Used with /raw or /content commands.
    """
    global message_to_send
    
    value = upload_preprocessor(mode='raw')
    if value == False: return True    # No path found, send message normally.
    elif value == None: return None   # Error occured, cancel all.
    else: paths, errors_list = value
    
    # Start converting files into objects.
    if not errors_list:
        for idx, path in paths.items():
            try:
                file_name = get_file_name(path)
                mime_type = guess_type(path)
                
                # This is fast so it doesn't need a status message or a CTRL-C handler.
                with open(path, 'rb') as f:
                    file_part = Part.from_bytes(data=f.read(), mime_type=mime_type)
                message_to_send[idx] = file_part
                
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                try: error = error.message
                except: pass
                msg = f"[{file_name}]: {error}"
                errors_list.append(msg)

    if errors_list:
        # Clarify the errors.
        msg = '\n\n'.join(errors_list)
        n = len(errors_list)
        if len(paths) == 1: msg = f'{YLW}Processing raw content failed:\n' + msg
        elif n == len(paths): msg = f'{YLW}Processing raw content failed for all files! Details:\n' + msg
        else: msg = f'{YLW}Processing raw content failed for some files! Details:\n' + msg
        msg += f'\n\n{YLW}Press (UP) to get your prompt back.'
        
        # Display.
        box(msg, title='RAW FILE ERROR', border_color=RED, text_color=RED, secondary_color=RED)
        return False
    
    # Instead of raw data, we now send the 'Google File' object (Which contains the shared file URL as a part of it).
    return True

def recover_prompt():
    """
    Upon a failed upload attempt, an alternative prompt is generated for the user
    (in upload_to_google() function) where sucessfully uploaded files paths are
    replaced with their ready-to-use URLs; this function shows that generated prompt.
    Used with /recover command.
    """
    app_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(app_dir, RECOVERY_PROMPT_FILE)
        
    if recovery_prompt:
        msg = 'This is a generated recovery prompt where uploaded files paths are replaced with their URLs'
        color = GR
        
        # Copy to clipboard.
        if copy_to_clipboard(recovery_prompt, hidden=True): msg += " (It's already copied to clipboard).\n"
        else: msg += '.\n'
        
        # Write it to a file & open it.
        with open(RECOVERY_PROMPT_FILE, 'w', encoding='utf-8') as f:
            f.write(recovery_prompt)
        
        msg += f'\nIt is saved in:\n{path}'
        open_path(RECOVERY_PROMPT_FILE)
    
    else:
        msg = f"You didn't try to upload anything for now; "
        color = YLW
        if path_exist(path):
            msg += f'for a previous attempt, check: {path}'
            open_path(path)
        else:
            msg += f"and the file '{RECOVERY_PROMPT_FILE}' doesn't exist."
    
    # Display.
    box(msg, title='RECOVERY', text_color=color, border_color=color, secondary_color=color)

def switch_chat_configuration():
    """
    Switch or update client & chat settings (AI model & API key) while in chat
    to quickly resume the conversation and avoid 'Quota Exceeded' or related errors.
    Work with /switch command.
    """
    global client, chat, GEMINI_API_KEY, GEMINI_MODEL
    
    # Get new settings.
    separator(before='\n', color=GR)
    msg = f"{CYN}You are about to update chat settings temporarily; you won't lose chat history or anything else; settings file and future conversations won't be affected. "
    msg += "Don't use the /switch command too much often, you know Google...\n\nLeave any field empty to keep using its current setting; "
    msg += "you can use an API key from another account; for the AI model, 'gemini-2.5-flash' or 'gemini-2.5-flash-lite' are recommended "
    msg += "(Your new options won't be validated; press CTRL-C to cancel).\n\n"
    msg += f"# Current API key: {GEMINI_API_KEY}\n"
    msg += f"# Current Gemini Model: {GEMINI_MODEL}\n"
    cprint(msg)
    
    try:
        if GLOBAL_LOG_FILE: in_time_log('New API Key: ...')
        api_key = input(f"{GR}New API Key: {RS}").strip() or GEMINI_API_KEY
        if GLOBAL_LOG_FILE: in_time_log('New Gemini Model: ...')
        ai_model = input(f"{GR}New Gemini Model: {RS}").strip() or GEMINI_MODEL
    
    except Interruption:
        cprint(f"\n\n{YLW}{choice(CANCEL_MESSAGES)}")
        separator(color=GR)
        return
    
    # Check:
    if (api_key == GEMINI_API_KEY) and (ai_model == GEMINI_MODEL):
        cprint(f"\n{YLW}Settings look the same, so no need to update anything...")
        separator(color=GR)
        return
    
    cprint(f"{GR}\nUpdating...")
    try:
        # raise Exception
        # Client first.
        http_options = {
            "timeout": HTTP_TIMEOUT * 1000, 
        }
        
        client = GemClient(
            api_key=api_key,
            http_options=http_options,
        )
             
        # Chat instance.
        history = chat.get_history()
        config = None
        if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON or FILE_COMPRESSION:
            config = load_system_instructions()
            
        chat = client.chats.create(
            model=ai_model,
            history=history,
            config=config,
        )
        
        # Global vars.
        GEMINI_API_KEY = api_key
        GEMINI_MODEL = ai_model
        
    except Exception as error:
        if ERROR_LOG_ON: log_caught_exception()
        separator(color=GR, end='')
        catch_exception(error)
        return
    
    # Inform.
    cprint(f"Chat updated!")
    separator(color=GR)

def select_files_dialog(mode: str):
    """
    Open file/folder dialog allowing multiple selections.
    Then return the selected files/folders' paths.
    Works upon pressing F3 or F4 while in prompt.
    """
    from tkinter.filedialog import askopenfilenames, askdirectory
    selected = None
    
    if mode == 'file':
        selected = list(askopenfilenames(title="Select File(s)"))
        
    elif mode == 'dir':
        selected = askdirectory(title="Select Folder")   # Can only select one folder at a time.
    
    flush_input()
    return selected  

def quick_text_editor(default_text=''):
    """
    Call in a quick & handy graphical text editor.
    NOTE: This is a blocking function.
    Used with CTRL-G hotkey or /gui, /editor commands.
    """
    from tkinter.messagebox import askyesno
    from tkinter import (Tk, Frame, Button, Text, Label, Scrollbar, Toplevel, Listbox,
                         END, WORD, X, Y, LEFT, RIGHT, BOTH, FLAT)
    global config_options
    
    # Buttons & Hotkeys Actions.
    def show_shortcuts():
        # Create small modal window.
        win = Toplevel(root)
        win.title('Keyboard Shortcuts')
        win.resizable(False, False)
        win.transient(root)  # keep above parent
        win.grab_set()       # modal

        # Theme-aware colors.
        bg = '#020617' if dark_mode else '#ffffff'
        fg = '#e5e7eb' if dark_mode else '#000000'
        win.configure(bg=bg)

        # Shortcuts text.
        shortcuts_text = (
            'Enter           →  New line\n'
            'Ctrl-Enter      →  Send message\n'
            'Ctrl-T          →  Toggle dark/light theme\n'
            'Ctrl-(+)        →  Zoom in\n'
            'Ctrl-(-)        →  Zoom out\n'
            'Ctrl-C          →  Copy (whole line if no selection)\n'
            'Ctrl-X          →  Cut (whole line if no selection)\n'
            'Ctrl-A          →  Select All\n'
            'Ctrl-Z          →  Undo\n'
            'Ctrl-Y          →  Redo\n'
            'Ctrl-Backspace  →  Delete previous word\n'
            'Ctrl-Delete     →  Delete next word'
        )

        # Display label.
        label = Label(
            win,
            text=shortcuts_text,
            justify='left',
            font=('Consolas', font_size),
            bg=bg,
            fg=fg,
            padx=20,
            pady=16
        )

        # Close button.
        button = Button(
            win,
            text='Close',
            command=win.destroy,
            font=('Segoe UI', 10),
            relief=FLAT,
            bg='#1e293b' if dark_mode else '#e5e7eb',
            fg=fg,
            padx=12,
            pady=4
        )
        
        # Pack widgets & Center the window above root.
        label.pack()
        button.pack(pady=(0, 12))
        
        win.update_idletasks()
        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()
        root_w = root.winfo_width()
        root_h = root.winfo_height()

        win_w = win.winfo_width()
        win_h = win.winfo_height()
        x = root_x + (root_w - win_w) // 2
        y = root_y + (root_h - win_h) // 2
        
        win.geometry(f'+{x}+{y}')

    def on_ctrl_backspace(event):
        text_field.delete(
            text_field.index('insert -1c wordstart'),
            'insert'
        )
        return 'break'

    def on_ctrl_delete(event):
        text_field.delete('insert', 'insert wordend')
        return 'break'

    def on_ctrl_x(event):
        if not text_field.tag_ranges('sel'):
            line_start = text_field.index('insert linestart')
            line_end = text_field.index('insert lineend +1c')

            # Copy first.
            root.clipboard_clear()
            root.clipboard_append(
                text_field.get(line_start, line_end)
            )

            # Then delete.
            text_field.delete(line_start, line_end)
        else:
            text_field.event_generate('<<Cut>>')

        return 'break'

    def on_ctrl_c(event):
        if not text_field.tag_ranges('sel'):
            root.clipboard_clear()
            root.clipboard_append(
                text_field.get(
                    'insert linestart',
                    'insert lineend'
                )
            )
        else:
            text_field.event_generate('<<Copy>>')
        return 'break'
    
    def check_text(event=None):
        content = text_field.get('1.0', 'end-1c').strip()
        if content:
            send_btn.config(state='normal')
        else:
            send_btn.config(state='disabled')
    
    def change_font(delta):
        nonlocal font_size
        if font_size + delta > 4:  # Don't go too small.
            font_size += delta
            text_field.config(font=('Segoe UI', font_size))
            if SUGGEST_FROM_WORDLIST_MODE:
                sugg_list.config(font=('Segoe UI', font_size))
                hint.config(font=('Segoe UI', font_size-2))
    
    def update_scrollbar(*args):
        size = text_field.yview()
        if size == (0.0, 1.0):
            scrollbar.grid_remove()
        else:
            scrollbar.set(*size)
            scrollbar.grid() 
            
    def toggle_theme():
        nonlocal dark_mode
        dark_mode = not dark_mode
        apply_theme()

    def apply_theme():
        if dark_mode:
            root.config(bg='#0f172a')
            top_frame.config(bg='#001033')
            scrollbar.config(bg='#1e293b', troughcolor='#020617')
            text_field.config(
                bg='#020617',
                fg='#e5e7eb',
                insertbackground='#e5e7eb'
            )
            toggle_btn.config(
                bg='#1e293b',
                fg='#e5e7eb',
                activebackground='#334155',
                text='🔆 Switch Theme',
            )
            shortcuts_btn.config(
                bg='#1e293b',
                fg='#e5e7eb',
                activebackground='#334155'
            )
            font_plus_btn.config(
                bg='#1e293b',
                fg='#e5e7eb',
                activebackground='#334155'
            )
            font_minus_btn.config(
                bg='#1e293b',
                fg='#e5e7eb',
                activebackground='#334155'
            )
            send_btn.config(
                bg='#1e293b',
                fg='#e5e7eb',
                activebackground='#334155'
            )
            cancel_btn.config(
                bg='#1e293b',
                fg='#e5e7eb',
                activebackground='#334155'
            )
            if SUGGEST_FROM_WORDLIST_MODE:
                popup.config(bg='#020617')
                hint.config(bg='#020617', fg='#9ca3af')
                sugg_list.config(
                    bg='#020617',
                    fg='#e5e7eb',
                    selectbackground='#334155',
                    selectforeground='#e5e7eb'
                )
        else:
            root.config(bg='#f8fafc')
            top_frame.config(bg='#2d5ac4')
            scrollbar.config(bg='#e5e7eb', troughcolor='white')
            text_field.config(
                bg='white',
                fg='black',
                insertbackground='black'
            )
            toggle_btn.config(
                bg='#e5e7eb',
                fg='black',
                activebackground='#d1d5db',
                text='🌙 Switch Theme',
            )
            shortcuts_btn.config(
                bg='#e5e7eb',
                fg='black',
                activebackground='#d1d5db'
            )
            font_plus_btn.config(
                bg='#e5e7eb',
                fg='black',
                activebackground='#d1d5db'
            )
            font_minus_btn.config(
                bg='#e5e7eb',
                fg='black',
                activebackground='#d1d5db'
            )
            send_btn.config(
                bg='#e5e7eb',
                fg='black',
                activebackground='#d1d5db'
            )
            cancel_btn.config(
                bg='#e5e7eb',
                fg='black',
                activebackground='#d1d5db'
            )
            if SUGGEST_FROM_WORDLIST_MODE:
                popup.config(bg='white')
                hint.config(bg='white', fg='#6b7280')
                sugg_list.config(
                    bg='white',
                    fg='black',
                    selectbackground='#d1d5db',
                    selectforeground='black'
                )

    def send_and_close(*args):
        nonlocal user_text, geometry
        # (-1c) = minus one char, because 'Tk Text' widget always adds a trailing newline.
        user_text = text_field.get('1.0', 'end-1c')
        geometry = root.geometry()
        root.destroy()
        # We return 'break' so that Tk doesn't try to insert a new line upon pressing ENTER on a destroyed Text widget.
        return 'break'

    def cancel_and_close():
        nonlocal user_text, geometry
        text_empty = not text_field.get('1.0', END).strip()
        if text_empty: confirm = True
        else: confirm = askyesno('Confirm', 'Are you sure you want to cancel?', parent=root)
        if confirm:
            user_text = ''
            geometry = root.geometry()
            root.destroy()
            return 'break'
    
    if SUGGEST_FROM_WORDLIST_MODE:
        def get_current_word():
            idx = text_field.index('insert')
            start = text_field.search(r'\m\w*$', idx, regexp=True, backwards=True)
            if not start:
                return '', idx
            return text_field.get(start, idx), start

        def show_suggestions(event=None):
            if event.keysym == 'Escape': return  # Ignore ESC.
            if event.state & 0x4: return         # Ignore Ctrl.
            if len(event.keysym) > 1: return     # ignore Shift, Control, Alt, etc.
                
            word, start = get_current_word()
            if not word:
                hide_suggestions()
                return

            matches = [w for w in WORDS_LIST if w.startswith(word)]
            if not matches:
                hide_suggestions()
                return

            sugg_list.delete(0, END)
            for w in matches[:8]:
                sugg_list.insert(END, w)

            bbox = text_field.bbox('insert')
            if not bbox:
                return

            x, y, w, h = bbox
            popup.geometry(f'+{root.winfo_rootx()+x}+{root.winfo_rooty()+y+h}')
            popup.deiconify()
            sugg_list.selection_set(0)

        def hide_suggestions(event=None):
            popup.withdraw()
            return 'break'

        def apply_suggestion(event=None):
            if not sugg_list.curselection():
                return

            choice = sugg_list.get(sugg_list.curselection())
            word, start = get_current_word()
            text_field.delete(start, 'insert')
            text_field.insert(start, choice + ' ')
            hide_suggestions()
            return 'break'
    
    # Options.
    font_size = config_options['gui_font_size']
    dark_mode = config_options['gui_dark_mode']
    geometry  = config_options['gui_editor_geometry']
    user_text = None
    
    # Main Window.
    root = Tk()
    root.title('Quick Text Editor')
    root.geometry(geometry)
    root.minsize(500, 300)
    root.protocol('WM_DELETE_WINDOW', cancel_and_close)
    root.bind_all('<Control-t>', lambda e: toggle_theme())
    root.bind_all('<Control-plus>', lambda e: change_font(1))
    root.bind_all('<Control-minus>', lambda e: change_font(-1))
    if SUPPRESS_ERRORS: root.report_callback_exception = lambda *_: None
    # root.bind('<Control-Return>', lambda event: send_and_close())     # This may be needed if we add another focus-able widget.
    
    # Top Bar Buttons.
    top_frame = Frame(root, bg='#001033')
    toggle_btn = Button(
        top_frame,
        text='🔆 Switch Theme',
        font=('Segoe UI', 11),
        command=toggle_theme,
        relief=FLAT,
    )  
    shortcuts_btn = Button(
        top_frame,
        text='⌨ Shortcuts',
        font=('Segoe UI', 11),
        command=show_shortcuts,
        relief=FLAT,
    )  
    font_plus_btn = Button(
        top_frame,
        text='A+',
        font=('Segoe UI', 11),
        command=lambda: change_font(1),
        relief=FLAT,
    )  
    font_minus_btn = Button(
        top_frame,
        text='A- ',
        font=('Segoe UI', 11),
        command=lambda: change_font(-1),
        relief=FLAT,
    )  
    send_btn = Button(
        top_frame,
        text='➤ Send',
        font=('Segoe UI Semibold', 11),
        command=send_and_close,
        relief=FLAT,
        state='disabled' if not default_text.strip() else 'normal',
    )  
    cancel_btn = Button(
        top_frame,
        text='✘ Cancel',
        font=('Segoe UI Semibold', 11),
        command=cancel_and_close,
        relief=FLAT,
    )
    
    top_frame.pack(fill=X)
    toggle_btn.pack(side=LEFT, padx=(6, 2), pady=6)
    shortcuts_btn.pack(side=LEFT, padx=4)
    font_plus_btn.pack(side=LEFT, padx=(2, 2))
    font_minus_btn.pack(side=LEFT, padx=(1, 2))     # 1 left, 2 right.
    send_btn.pack(side=RIGHT, padx=(2, 6), pady=6)
    cancel_btn.pack(side=RIGHT, padx=4)
    
    # Text Area.
    text_frame = Frame(root)
    text_frame.pack(expand=True, fill=BOTH)
    text_field = Text(
        text_frame,
        wrap=WORD,
        font=('Segoe UI', font_size),
        relief=FLAT,
        undo=True,
        maxundo=48,
    )
    
    text_field.grid(row=0, column=0, sticky='nsew')
    if default_text: text_field.insert('1.0', default_text) # (1.0) = line 1, character 0.
    text_field.focus_set()                                  # Focused on launch.
    
    text_field.bind('<KeyRelease>', check_text)
    text_field.bind('<Control-Return>', send_and_close)
    text_field.bind('<Control-BackSpace>', on_ctrl_backspace)
    text_field.bind('<Control-Delete>', on_ctrl_delete)
    text_field.bind('<Control-x>', on_ctrl_x)
    text_field.bind('<Control-c>', on_ctrl_c)

    # Scrollbar.
    scrollbar = Scrollbar(text_frame, command=text_field.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')

    text_frame.grid_columnconfigure(0, weight=1)
    text_frame.grid_rowconfigure(0, weight=1)
    text_field.config(yscrollcommand=update_scrollbar)

    if SUGGEST_FROM_WORDLIST_MODE:
        WORDS_LIST = word_completer.words
        
        popup = Toplevel(root)
        popup.withdraw()
        popup.overrideredirect(True)
        popup.attributes('-topmost', True)
        
        sugg_list = Listbox(
            popup,
            font=('Segoe UI', font_size),
            height=SUGGESTIONS_LIMIT,
            relief=FLAT
        )
        hint = Label(
            popup,
            text='Use (↑↓ ENTER ESC)',
            font=('Segoe UI', font_size-2),
            fg='#9ca3af',
            bg=sugg_list.cget('bg'),
            anchor='w',
            padx=6
        )
        
        sugg_list.pack()
        hint.pack(fill=X)
        text_field.bind('<KeyRelease>', show_suggestions, add='+')
        text_field.bind('<Escape>', hide_suggestions)
        text_field.bind('<Down>', lambda e: sugg_list.focus_set())
        sugg_list.bind('<Return>', apply_suggestion)
        sugg_list.bind('<Escape>', hide_suggestions)
        sugg_list.bind('<Double-Button-1>', apply_suggestion)        
                 
    # Block Execution (Python freezes while editing).
    apply_theme()
    while True:
        try:
            root.mainloop()
            flush_input()
            return user_text
        except Interruption:
            # In case the user presses CTRL-C in the CLI.
            pass
        except Exception:
            if ERROR_LOG_ON: log_caught_exception()
            pass
        finally:
            config_options['gui_font_size'] = font_size
            config_options['gui_dark_mode'] = dark_mode
            config_options['gui_editor_geometry'] = geometry

def quick_markdown_viewer(md_content=''):
    """
    A graphical Markdown renderer with a 'See Raw' toggle.
    Used with ALT-G hotkey or /viewer, /preview or /markdown commands.
    """
    from markdown import markdown
    from tkinterweb import HtmlFrame
    from tkinter.filedialog import asksaveasfilename
    from tkinter import (Tk, Frame, Button, Text, StringVar, Label, Toplevel, Scrollbar,
                         END, WORD, X, BOTH, LEFT, RIGHT, FLAT)
    global config_options
    
    # Buttons & Hotkeys Actions.
    def show_shortcuts():
        # Create small modal window.
        win = Toplevel(root)
        win.title('Keyboard Shortcuts')
        win.resizable(False, False)
        win.transient(root)  # keep above parent
        win.grab_set()       # modal

        # Theme-aware colors.
        bg = '#020617' if dark_mode else '#ffffff'
        fg = '#e5e7eb' if dark_mode else '#000000'
        win.configure(bg=bg)

        # Shortcuts text.
        shortcuts_text = (
            'Up/Down      →  Scroll up/down\n'
            'Mouse LB/RB  →  Copy links\n'
            'Ctrl-S       →  Save to file\n'
            'Ctrl-C       →  Copy selected text\n'
            'Ctrl-R       →  Toggle raw/preview mode\n'
            'Ctrl-T       →  Toggle dark/light theme\n'
            'Ctrl-A       →  Select all (raw mode only)\n'
            'Ctrl-(+)     →  Zoom in\n'
            'Ctrl-(-)     →  Zoom out'
        )

        # Display label.
        label = Label(
            win,
            text=shortcuts_text,
            justify='left',
            font=('Consolas', font_size),
            bg=bg,
            fg=fg,
            padx=20,
            pady=16
        )

        # Close button.
        button = Button(
            win,
            text='Close',
            command=win.destroy,
            font=('Segoe UI', 10),
            relief=FLAT,
            bg='#1e293b' if dark_mode else '#e5e7eb',
            fg=fg,
            padx=12,
            pady=4
        )
        
        # Pack widgets & Center the window above root.
        label.pack()
        button.pack(pady=(0, 12))
        
        win.update_idletasks()
        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()
        root_w = root.winfo_width()
        root_h = root.winfo_height()

        win_w = win.winfo_width()
        win_h = win.winfo_height()
        x = root_x + (root_w - win_w) // 2
        y = root_y + (root_h - win_h) // 2
        
        win.geometry(f'+{x}+{y}')

    def save_to_file(event=None):
        nonlocal is_status_busy
        # Prompt user to choose a file to save.
        file_path = asksaveasfilename(
            defaultextension='.md',
            filetypes=[('Markdown', '*.md'), ('Plain text', '*.txt'), ('All files', '*.*')],
            title='Save As'
        )
        if not file_path:
            return  # User cancelled.

        # Get the content from the text area.
        is_status_busy = True
        content = raw_text_area.get('1.0', END)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            status_var.set(f'Saved to: {file_path}')
            def reset_status():
                nonlocal is_status_busy
                is_status_busy = False
                status_var.set(status_bar_idle)
            
            root.after(2000, reset_status)
        except Exception as error:
            if ERROR_LOG_ON: log_caught_exception()
            status_var.set(f'Error saving file: {error}')

    def update_scrollbar(*args):
        size = raw_text_area.yview()
        if size == (0.0, 1.0):
            scrollbar.grid_remove()
        else:
            scrollbar.set(*size)
            scrollbar.grid() 
            
    def copy_link(event, *_):
        nonlocal is_status_busy
        url = None
        
        if isinstance(event, str):
            # In case it was trigerred by (on_navigate_fail) method.
            url = event
        else:
            # Extract the URL.
            element = html_view.get_currently_hovered_element()
            if element:
                attrs = getattr(element, 'attributes', {})
                url = attrs.get('href')
            
        if url:
            # Copy it.
            is_status_busy = True
            root.clipboard_clear()
            root.clipboard_append(url)
            status_var.set(f'📋 Link copied: {url}')
            def reset_status():
                nonlocal is_status_busy
                is_status_busy = False
                status_var.set(status_bar_idle)
            
            root.after(1500, reset_status)
            root.update()
        
    def show_link(event):
        if is_status_busy: return
        element = html_view.get_currently_hovered_element()    
        if element:
            attrs = getattr(element, 'attributes', {})
            url = attrs.get('href')
            
            if url:
                status_var.set(url)
                return  # Exit early so we don't clear the text.

        # If we aren't hovering over a link, clear the status bar.
        status_var.set(status_bar_idle)
        
    def get_html_content(text):
        # Convert Markdown to HTML
        # Using 'extra' extension for tables, code blocks, etc.
        html = markdown(text, extensions=['extra', 'codehilite'])
        
        # Inject basic CSS for theming.
        bg = '#020617' if dark_mode else '#ffffff'
        fg = '#e5e7eb' if dark_mode else '#000000'
        link = '#38bdf8' if dark_mode else '#2563eb'
        
        styled_html = f"""
        <style>
            body {{ 
                background-color: {bg};
                color: {fg}; 
                font-family: 'Segoe UI', sans-serif; 
                font-size: {font_size}pt;
                padding: 10px;
            }}
            a {{ color: {link}; }}
            code {{ background-color: {'#1e293b' if dark_mode else '#f1f5f9'}; padding: 2px 4px; border-radius: 4px; }}
            pre {{ background-color: {'#1e293b' if dark_mode else '#f1f5f9'}; padding: 10px; border-radius: 6px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid {fg}; padding: 8px; text-align: left; }}
        </style>
        {html}
        """
        return styled_html

    def toggle_raw():
        nonlocal showing_raw
        if showing_raw:
            raw_container.pack_forget()
            html_view.pack(fill=BOTH, expand=True)
            html_view.load_html(get_html_content(raw_text_area.get('1.0', END)))
            raw_btn.config(text='✎ Edit Raw')
            status_var.set(status_bar_idle)
        else:
            html_view.pack_forget()
            raw_container.pack(fill=BOTH, expand=True)
            raw_btn.config(text='📜 See Preview')
            status_var.set(f'ⓘ You can edit/paste markdown code here and see the preview.')
        showing_raw = not showing_raw

    def apply_theme():
        # Set colors.
        bg_main = '#0f172a' if dark_mode else '#f8fafc'
        bg_top = '#001033' if dark_mode else '#2d5ac4'
        btn_bg = '#1e293b' if dark_mode else '#e5e7eb'
        fg = '#e5e7eb' if dark_mode else '#000000'
        activebackground = '#334155' if dark_mode else '#d1d5db'
        
        # Update widgets.
        root.configure(bg=bg_main)
        top_frame.configure(bg=bg_top)
        view_frame.configure(bg=bg_main)
        status_frame.configure(bg=bg_main)
                
        for btn in [raw_btn, toggle_btn, font_plus_btn, font_minus_btn, save_btn, close_btn, shortcuts_btn]:
            btn.config(bg=btn_bg, fg=fg, activebackground=activebackground)
        
        toggle_btn.config(text='🔆 Switch Theme' if dark_mode else '🌙 Switch Theme')
        raw_text_area.config(bg='#020617' if dark_mode else 'white', fg=fg, insertbackground=fg)
        status_bar.config(
            bg='#0a1d2f' if dark_mode else '#cfd3d6',
            fg='#94a3b8' if dark_mode else '#334155'
        )
        
        # Refresh HTML view with new theme colors
        if not showing_raw:
            html_view.load_html(get_html_content(raw_text_area.get('1.0', END)))

    def toggle_theme():
        nonlocal dark_mode
        dark_mode = not dark_mode
        apply_theme()

    def change_font(delta):
        nonlocal font_size
        if font_size + delta > 4:  # Don't go too small.
            font_size += delta
            raw_text_area.config(font=('Segoe UI', font_size))
            if not showing_raw:
                html_view.load_html(get_html_content(raw_text_area.get('1.0', END))) 
    
    def close():
        nonlocal geometry
        geometry = root.geometry()
        root.destroy()
        return 'break'
    
    # Options.
    geometry  = config_options['gui_viewer_geometry']
    dark_mode = config_options['gui_dark_mode']
    font_size = config_options['gui_font_size']
    showing_raw = False
    status_bar_idle = 'Idle...' 
    is_status_busy = False
    
    # Main Window.
    root = Tk()
    root.title('Quick Markdown Viewer')
    root.geometry(geometry)
    root.minsize(550, 300)
    root.protocol('WM_DELETE_WINDOW', close)
    root.bind_all('<Control-r>', lambda e: toggle_raw())
    root.bind_all('<Control-t>', lambda e: toggle_theme())
    root.bind_all('<Control-plus>', lambda e: change_font(1))
    root.bind_all('<Control-minus>', lambda e: change_font(-1))
    root.bind_all('<Control-s>', save_to_file)
    if SUPPRESS_ERRORS: root.report_callback_exception = lambda *_: None
    
    # Top Bar Buttons.
    top_frame = Frame(root)      
    toggle_btn = Button(top_frame,
        text='💡 Switch Theme',
        font=('Segoe UI', 11),
        command=toggle_theme,
        relief=FLAT
    )
    
    raw_btn = Button(
        top_frame,
        text='✎ Edit Raw',
        font=('Segoe UI', 11),
        command=toggle_raw,
        relief=FLAT
    )
    shortcuts_btn = Button(
        top_frame,
        text='⌨ Shortcuts',
        font=('Segoe UI', 11),
        command=show_shortcuts,
        relief=FLAT,
    )
    font_plus_btn = Button(top_frame,
        text='A+',
        font=('Segoe UI', 11),
        command=lambda: change_font(1),
        relief=FLAT
    )
    font_minus_btn = Button(top_frame,
        text='A- ',
        font=('Segoe UI', 11),
        command=lambda: change_font(-1),
        relief=FLAT
    )
    save_btn = Button(top_frame,
        text='💾 Save',
        font=('Segoe UI Semibold', 11),
        command=save_to_file,
        relief=FLAT
    )
    close_btn = Button(top_frame,
        text='✘ Close',
        font=('Segoe UI Semibold', 11),
        command=close,
        relief=FLAT
    )
    
    top_frame.pack(fill=X)
    toggle_btn.pack(side=LEFT, padx=(6, 2), pady=6)
    raw_btn.pack(side=LEFT, padx=4)
    shortcuts_btn.pack(side=LEFT, padx=(2, 4))
    font_plus_btn.pack(side=LEFT, padx=(2, 2))
    font_minus_btn.pack(side=LEFT, padx=(1, 2))
    save_btn.pack(side=RIGHT, padx=(2, 6), pady=6)
    close_btn.pack(side=RIGHT, padx=4)
    
    # Status Bar.
    status_frame = Frame(root)
    status_frame.pack(fill=X, side='bottom')
    status_frame.pack_propagate(False)
    status_frame.configure(height=22)
    
    status_var = StringVar(value=status_bar_idle)
    status_bar = Label(
        status_frame,
        textvariable=status_var,
        anchor='w',
        padx=10,
        font=('Segoe UI', 9),
    )

    status_bar.pack(fill=X)
    
    # View Area
    view_frame = Frame(root)
    view_frame.pack(fill=BOTH, expand=True)
    
    # 1. HTML Rendered View.
    html_view = HtmlFrame(view_frame, messages_enabled = False)  # Disable debugging info.
    html_view.pack(fill=BOTH, expand=True)
    html_view.on_navigate_fail = copy_link
    html_view.bind('<Button-1>', copy_link)
    html_view.bind('<Button-3>', copy_link)
    html_view.bind('<Motion>', show_link)

    # 2. Raw Text View (Hidden by default).
    raw_container = Frame(view_frame)
    raw_container.grid_rowconfigure(0, weight=1)
    raw_container.grid_columnconfigure(0, weight=1)

    raw_text_area = Text(
        raw_container,
        wrap=WORD,
        font=('Segoe UI', font_size),
        relief=FLAT
    )
    
    raw_text_area.insert('1.0', md_content)
    raw_text_area.config(yscrollcommand=update_scrollbar)
    # raw_text_area.config(state='disabled')
    
    scrollbar = Scrollbar(raw_container, command=raw_text_area.yview)
    scrollbar.grid(row=0, column=1, sticky='ns')
    raw_text_area.grid(row=0, column=0, sticky='nsew')
    
    # Block Execution (Python freezes while editing).
    apply_theme()
    while True:
        try:
            root.mainloop()
            flush_input()
            break
        except Interruption:
            # In case the user presses CTRL-C in the CLI.
            pass
        except Exception:
            if ERROR_LOG_ON: log_caught_exception()
        finally:
            config_options['gui_dark_mode'] = dark_mode
            config_options['gui_font_size'] = font_size
            config_options['gui_viewer_geometry'] = geometry

if SAVED_INFO:
    def manage_saved_info(user_input, command):
        """Manage user saved info by either: 'forget' or 'remember'."""
        # Check if it's worth adding/removing.
        MIN_WORDS = 3
        MIN_CHARS = 10
        requested_info = user_input[len(command)+1:].strip()
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
                if path_exist(SAVED_INFO_FILE) and os.path.getsize(SAVED_INFO_FILE) > 0:
                    with open(SAVED_INFO_FILE, 'r+', encoding='utf-8') as f:
                        content = f.read()
                        if not content.endswith('\n'):
                            f.write('\n')
                        
                        else:
                            leading_new_lines = len(content) - len(ltrim(content))
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
                                f.write(f'\n- {line.lstrip("/")}\n')
                                first_line_written = True
                            else:
                                f.write(f'  {line}\n')
                    
                msg = "Information saved!\n"
                msg += "You can always ask Gemini to forget by starting your prompt with 'forget'. "
                msg += f"Or type /saved-info to manually edit your info in '{SAVED_INFO_FILE}'."
                color = GR
            
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                msg = f"Couldn't save your info!\nError: {error}."
                color = RED
                
            box(msg, title='SAVED INFO STATUS', border_color=color, text_color=color, secondary_color=color)

        # User wants to forget something.
        elif command == 'forget':
            try:
                deleted = False     # If the info was deleted, this becomes True.
                
                # Get the saved info list.
                if not path_exist(SAVED_INFO_FILE):
                    msg = f"There is no '{SAVED_INFO_FILE}' file!"
                    box(msg, title='WARNING', border_color=YLW, text_color=YLW)
                    return
                
                try:        
                    with open(SAVED_INFO_FILE, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                except Exception as error:
                    if ERROR_LOG_ON: log_caught_exception()
                    msg = f"Couldn't read '{SAVED_INFO_FILE}' file!\nError: {error}."
                    box(msg, title='ERROR', border_color=RED, text_color=RED)
                    return
                
                if not content:
                    msg = f"File '{SAVED_INFO_FILE}' is empty!"
                    box(msg, title='WARNING', border_color=YLW, text_color=YLW)
                    return
                
                # Split SAVED_INFO_FILE content according to '- ' at the start of line.
                separator(before='\n', color=YLW)
                info_list = re.split(r'^(?:- )', content, flags=re.MULTILINE)[1:]
                
                if len(info_list) == 1:
                    # If there is only one saved info, avoid the remaining complex code.
                    cprint(f"{YLW}Found only one saved info in the whole '{SAVED_INFO_FILE}' file:{GR}")
                    info = re.sub(r'\s+', ' ', info_list[0].capitalize()).strip()
                    cprint('- ' + info, wrap_joiner='\n  ')
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
                        cprint(GR + choice(CANCEL_MESSAGES) + RS)
                        
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
                    cprint('- Remember ' + info_1, wrap_joiner='\n  ')
                    question = 'Are you sure you want to delete it? (y/n): '
                    answers = ['y']
                        
                # Case (2): Match is decent, but dangerously ambiguous.
                elif (ratio_1 > 0.5) and (ratio_1 / ratio_2 <= 1.30):
                    cprint(YLW + 'You probably meant one of these saved info:' + GR)
                    cprint('1) Remember ' + info_1, wrap_joiner='\n   ')
                    cprint('2) Remember ' + info_2, wrap_joiner='\n   ')
                    question = "(If none, use /saved-info command for manual edit)\n"
                    question += 'Which one you want to delete? (1, 2, cancel): '
                    answers = ['1', '2']
                    
                # Case (3): Match is too poor.
                else:   # elif ratio_1 <= 0.5:
                    cprint(YLW + 'Perphaps you meant one of these saved info:' + GR)
                    cprint('1) Remember ' + info_1, wrap_joiner='\n   ')
                    cprint('2) Remember ' + info_2, wrap_joiner='\n   ')
                    question = "(If none, use /saved-info command for manual edit)\n"
                    if top_n == 3:
                        cprint('3) Remember ' + info_3, wrap_joiner='\n   ')
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
                        box(msg, title='ERROR', border_color=RED, text_color=RED)
                        return
                    
                    cprint(GR + 'Saved info permanently deleted!' + RS)
                    deleted = True
               
                # User said no/cancel.
                else:
                    cprint(GR + choice(CANCEL_MESSAGES) + RS)

            except Interruption:
                cprint(f'\n{GR}{choice(CANCEL_MESSAGES)}{RS}')
            
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
                
                # Fallback to the system's known editor.
                else:
                    if sys.platform.startswith('win'):
                        os.environ['EDITOR'] = 'notepad'        # For Windows.
                    else:
                        os.environ['EDITOR'] = 'vim'            # For Mac/Linux.
            
            # 3. Restore the original value/state.
            elif mode == 'restore':
                if editor_variable:
                    os.environ['EDITOR'] = editor_variable
                else:
                    del os.environ['EDITOR']
        
        except:
            if ERROR_LOG_ON: log_caught_exception()

    def external_editor(default_text='', file=TEMP_PROMPT_FILE):
        """
        Call the external editor, edit the text, then return it.
        In case of unhandled errors, the edited file will be kept.
        NOTE: This is a blocking function.
        Used with CTRL-X-CTRL-E hotkey or /external command.
        """
        from subprocess import call, CREATE_NEW_CONSOLE
        
        # Write current text to file, or just create an empty file.
        with open(file, 'w', encoding='utf-8') as f:
            f.write(default_text)

        # Open editor & Wait until it's closed.
        editor = os.environ.get('EDITOR')
        try:
            # raise Exception
            # This is a blocking call; we create a new console to avoid interference with CLI-based editors.
            call([editor, file], creationflags=CREATE_NEW_CONSOLE)
        except:
            return False

        # Read the edited text back.
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Remove the temp file & submit.
        try: os.remove(file)
        except: pass
        return text









# 6) Part V: Main Functions ------------------------------------------------------------------------
def flush_input():
    """
    Flush the input buffer to avoid accidental hotkeys registration.
    E.g: If the user presses F1 outside prompt(), prompt() may still catch it
         when it's back ON; same for tkinter, the program may catch hotkeys
         pressed while in GUI - when it's back ON.
    """
    if OPERATING_SYSTEM == "posix":    # Linux/Mac.
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        
    elif OPERATING_SYSTEM == "nt":     # Windows.
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
    if (not NO_HISTORY_LIMIT) and len(history_list) > MAX_HISTORY_MESSAGES:
        if MAX_HISTORY_MESSAGES > 0: history_list = history_list[-MAX_HISTORY_MESSAGES:]
        else: history_list.clear()
    
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
            try:
                with open(CHAT_HISTORY_JSON, 'r', encoding='utf-8') as f:
                    old_history_dicts = json.load(f)
                
                old_history_json_str = json.dumps(old_history_dicts)
                changed = new_history_json_str != old_history_json_str
            except:
                changed = True
        
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
                    else: cprint(f"{GR}Chat history cleared & saved!{RS}")
                chat_saved = True
            
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                if not hidden: cprint(f"{RED}Failed to save chat history: {error}!{RS}")
                
        if not hidden and down_separator: separator()
        return True

def load_chat_history():
    """Load chat history, if it meets the conditions."""
    global initial_history, confirm_separator
    initial_history = []
    
    # Check if the history file exist, and is not empty.
    file_exist = path_exist(CHAT_HISTORY_JSON)
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
                if LOAD_CHAT_MODE == 'load': load_history = 'y'
                elif LOAD_CHAT_MODE == 'forget': load_history = 'n'
                else: load_history = input(question).lower().strip()
                
            except Interruption:
                cprint()
                confirm_separator = False
                raise
                
            if load_history == 'y':
                try:
                    with open(CHAT_HISTORY_JSON, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    try:
                        saved_history_dicts = json.loads(content)
                    except json.JSONDecodeError as error:
                        repaired, content = catch_json_error(error, CHAT_HISTORY_JSON, content)
                        if repaired:
                            saved_history_dicts = content
                        else:
                            clear_lines()
                            separator()
                            box(content, title='JSON ERROR', border_color=RED, text_color=RED)
                            quit(1)
                    
                    # Reconstruct Content & Part objects from the saved dictionaries.
                    del content
                    errors = 0
                    for item in saved_history_dicts:
                        try:
                            parts = [Part(text=p['text']) for p in item['parts']]
                            initial_history.append(Content(role=item['role'], parts=parts))
                        except:
                            if ERROR_LOG_ON: log_caught_exception()
                            errors += 1
                            # if errors:
                                # cprint(f"{RED}({errors}) partial error(s) occurred during loading chat history.{RS}")
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
                        cprint(f"{RED}Found ({errors}) partial error(s) while loading chat history; the rest was loaded successfully.{RS}")
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
        help(mode='short')
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
            help(mode='short')
            sys_exit(1)
        
        except ServerError as error:
            catch_server_error_startup(error_occurred, attempts)
            error_occurred = True
            attempts += 1
            continue
            
        except NetworkExceptions:
            catch_network_error()
            sys_exit(1)
            
    while True:
        try:
            welcome_screen()
            load_chat_history()
            if SUGGEST_FROM_WORDLIST_MODE in ['normal', 'fuzzy']: load_word_completer()  
            break
            
        except Interruption:
            farewell()
            continue
    
    # Start chat session with/out the system instructions (Implicit orders or saved info).
    config = None
    if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON or FILE_COMPRESSION:
        config = load_system_instructions()
    
    chat = client.chats.create(
        model=GEMINI_MODEL,
        history=initial_history,
        config=config,
    )
    
    cprint()
    restarting = False
    return client, chat
  
def interpret_commands():
    """If the user input is a special command, execute it."""
    global discarding, history, should_compress, default_prompt, user_input, message_to_send
    
    command = user_input.strip()
    if not CASE_SENSITIVITY: command = command.lower()
    if command.startswith('/'): command = command.removeprefix('/')
    else: command = 'None'   # So that it doesn't accidentaly match one of the cases below before reaching other 'interpret' functions.
    
    # Check for high priority commands first:
    cmd_finder = lambda cmd: command.startswith(cmd) and command[len(cmd):len(cmd)+1].isspace()
    if cmd_finder('original'):
        message_to_send = message_to_send.lstrip()[10:]
        return True
    
    elif cmd_finder('no-compress'):
        message_to_send = message_to_send.lstrip()[13:]
        should_compress = 'no'

    elif cmd_finder('compress'):
        message_to_send = message_to_send.lstrip()[10:]
        should_compress = 'yes'

    # Check for other commands.
    match command:
        case 'quit' | 'exit':
            cprint()
            farewell(confirmed=True)
    
        case 'help' | 'help-2' | 'help-3' | 'cheat':
            if command == 'help': help(mode='short')
            elif command == 'help-2': help(mode='regular')
            elif command == 'help-3': help(mode='long')
            else: help(mode='cheat')

        case 'clear':
            system(CLEAR_COMMAND)
            # Change the prompt placeholder for a fresh start feeling.
            update_placeholder()
    
        case 'open':
            open_path('.', clear=2, set_placeholder=user_input)
    
        case 'saved-info':
            open_path(SAVED_INFO_FILE, clear=2, set_placeholder=user_input)
        
        case 'saved-links' | 'saved-urls':
            open_path(SAVED_LINKS_FILE, clear=2, set_placeholder=user_input)
        
        case 'recover':
            recover_prompt()
    
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
        
        case 'last-links' | 'last-urls':
            if last_urls:
                msg = f'{BL}Links of the last successfully uploaded files:'
                urls = ''
                color = GR
                for path, url in last_urls.items():
                    name = get_file_name(path)
                    urls += f'\n[{name}]:\n{url}\n'
                if copy_to_clipboard(urls.strip(), hidden=True): msg += f'\n{BL}(Already copied to clipboard)\n{urls}'
                else: msg += urls
            else:
                msg = "You've not successfully uploaded any files for now."
                color = YLW
            box(msg, title='LAST LINKS', border_color=color, text_color=color, secondary_color=color)
        
        case 'editor' | 'gui' | 'external':
            # /external for the external editor; others for our quick editor.
            if command == 'external':
                if not EXTERNAL_EDITOR: return True
                with ProgressBar(bottom_toolbar=' Now using the external editor... ', cancel_callback=lambda: None):
                    edited_text = external_editor()
                    if edited_text is False:
                        # Error.
                        update_placeholder("The external editor couldn't be found!", temp=True)
                        clear_lines(2)
                        return
            else:
                with ProgressBar(bottom_toolbar=' Now using the quick editor... ', cancel_callback=lambda: None):
                    edited_text = quick_text_editor()
                    
            if not edited_text.strip():
                # No text, cancel.
                update_placeholder(user_input, temp=True)
                user_input = None
                clear_lines(2)
                return
            # Save the edited text.
            user_input = message_to_send = edited_text
            Keys.save_history(user_input)
            # Show it & Submit.
            to_show = ltrim(user_input).rstrip() 
            if HIDE_LONG_INPUT:
                i = Keys.hide_threshold
                if len(to_show) > i: to_show = to_show[:i-6].rstrip() + ' [...]'
            margin = f'{GRY}{line_continuation}{RS}'
            width = glitching_text_width - len(line_continuation)
            for line in to_show.splitlines(): cprint(margin + line, wrap_width=width, wrap_joiner=f'\n{margin}')
            return interpret_commands()
        
        case 'viewer' | 'preview' | 'markdown':
            response = get_last_response('return')
            with ProgressBar(bottom_toolbar=' Now using the quick markdown viewer... ', cancel_callback=lambda: None):
                quick_markdown_viewer(response)
            update_placeholder(user_input, temp=True)
            clear_lines(2)
        
        case c if c.startswith('pop-last'):
            if command == 'pop-last': n_turns = 1
            elif command.startswith('pop-last '):
                try: n_turns = int(float(command[8:]))
                except: return True
            else: return True
            store_last_turn_for_exclusion(n_turns)  
        
        case 'pop-all':
            store_last_turn_for_exclusion(remove_all=True)
    
        case 'restore-last' | 'restore-all':
            restore_removed_messages(command)
    
        case 'del-prompt':
            try:
                os.remove(PROMPT_HISTORY_FILE)
                if PROMPT_HISTORY_MODE in ['temporary', 'permanent']: load_prompt_history()
                msg = f"File '{PROMPT_HISTORY_FILE}' removed successfully."
                color = GR
                if PROMPT_HISTORY_MODE == 'permanent':  # Backup doesn't exist if the user isn't in history-file mode.
                    msg += "\n\nBefore you exit, know that an earlier backup is temporarily available in: "
                    msg += os.path.abspath(PROMPT_HISTORY_FILE + '.bak')
            except FileNotFoundError:
                msg = f"File '{PROMPT_HISTORY_FILE}' not found!"
                color = YLW
            except Exception as e:
                if ERROR_LOG_ON: log_caught_exception()
                msg = f"An error occurred: {e}."
                color = RED
            
            box(msg, title='STATUS', border_color=color, text_color=color)
    
        case 'del-log':
            clear_log_files()
        
        case 'del-links':
            try:
                os.remove(SAVED_LINKS_FILE)
                msg = f"File '{SAVED_LINKS_FILE}' deleted successfully!"
                color = GR
            except FileNotFoundError:
                msg = f"File '{SAVED_LINKS_FILE}' not found!"
                color = YLW
            except Exception as error:
                if ERROR_LOG_ON: log_caught_exception()
                msg = f"Error: {error}."
                color = RED
            box(msg, title='STATUS', border_color=color, text_color=color)
        
        case 'del-output':
            try:
                remove_dir(FILE_GENERATION_DIR)
                msg = 'All generated files were removed!'
                color = GR
            except Exception as error:
                msg = f'Error: {error}.'
                color = RED
            box(msg, title='STATUS', border_color=color, text_color=color, secondary_color=color)
        
        case 'del-uploaded':
            del_uploaded_files()
        
        case 'del-all':
            del_all()
        
        case 'quick-chat':
            quick_chat()
        
        case 'switch':
            switch_chat_configuration()
        
        case 'restart':
            raise SoftRestart
        
        case 'discard' | 'kill':
            discarding = True
            try: copy_file(PROMPT_HISTORY_FILE + '.bak', PROMPT_HISTORY_FILE)
            except: pass
            
            if command == 'discard':
                if PROMPT_HISTORY_MODE in ['temporary', 'permanent']: load_prompt_history()
                msg = 'Discarding current session & Restarting...'
                box(msg, title='DISCARD', border_color=YLW, text_color=YLW)
                raise SoftRestart
            else:   # Kill.
                msg = 'Clearing recent messages & Quitting...\nManually saved content & logs are kept!'
                box(msg, title='KILL', border_color=YLW, text_color=YLW)
                raise SystemExit
        
        case 'stats' | 'statistics':
            statistics()

        case 'license':
            msg_1 = "Do whatever you want using 'Gemini Py-CLI', wherever you want."
            msg_2 = "Half of it was written using AI itself, so I won't complain.\n"
            msg_3 = f"But as a polite programmer request, I'll be happy if you mention my name... for the efforts."
            box(msg_1, msg_2, msg_3, title='LICENSE', border_color=GR, text_color=GR)
        
        case 'about':
            msg_1 = "Title: Gemini Py-CLI.\nAuthor: Mohyeddine Didouna, with a major AI assistance."
            msg_2 = f"GitHub Home: {UL}https://github.com/Mohyoo/Gemini-Py-CLI{RS}"
            msg_3 = f"Issues Page: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}"
            msg_4 = "\nMany thanks and credits to all the people who contributed, tutorials makers, "
            msg_4 += "and free content creators. Without their help, this project wouldn't be possible"
            box(msg_1, msg_2, msg_3, msg_4, title='ABOUT', border_color=GR, text_color=GR)     
            
        case 'version':
            msg = "Gemini Py-CLI, Version 1.0"
            box(msg, title='VERSION', border_color=GR, text_color=GR)
        
        case 'secret':
            path = 'Secret'
            if path_exist(path): open_path(path, clear=2, set_placeholder=user_input)
            else:
                msg = "The 'Secret' directory wasn't found!"
                box(msg, title='SECRET LOST... FOREVER', border_color=RED, text_color=RED, secondary_color=RED)
                
        case _:
            # Try the extra & special commands.
            if not interpret_extra_commands(command): return   # Command found, so there is no message to send.
            if not interpret_special_commands(): return        # Error, prompt must be cancelled.
            
            # No command. Return True as a flag to send a normal message to AI.
            return True

def interpret_special_commands():
    """
    Execute special commands that can appear in prompt beginning, middle or end.
    Those commands can be all executed in a row, since the user can use all of
    them at once.
    """
    global converted_prompt
    converted_prompt = user_input
    cp = converted_prompt if CASE_SENSITIVITY else converted_prompt.lower()
    cmd_finder = lambda cmd: cp.startswith(f'/{cmd} ') or (f' /{cmd} ' in cp) or (f'\n/{cmd} ' in cp) or (f'\t/{cmd} ' in cp)
    to_return = True    # This becomes None upon an error.
    
    if cmd_finder('dir') or cmd_finder('folder'):
        if not convert_folder_to_files(): to_return = None
        # Update 'cp' variable because /dir commands have been replaced by /file.
        converted_prompt = message_to_send
        cp = converted_prompt if CASE_SENSITIVITY else converted_prompt.lower()
        cmd_finder = lambda cmd: cp.startswith(f'/{cmd} ') or (f' /{cmd} ' in cp) or (f'\n/{cmd} ' in cp) or (f'\t/{cmd} ' in cp)
    
    if ('generativelanguage.googleapis.com/' in cp) and ('/files/' in cp):
        if not convert_raw_urls(): to_return = None
        
    if cmd_finder('file') or cmd_finder('upload'):
        if not upload_to_google(): to_return = None
    
    if cmd_finder('raw') or cmd_finder('content'):
        if not upload_raw_file(): to_return = None

    return to_return    # No command was found, so continue sending prompt.
    
def interpret_extra_commands(command: str):
    """
    A special function to interpret the extra-secret commands.
    This really should be in 'useless.py' module, but I faced a lot of issues to do that.
    """
    global default_prompt, keys, chaos_mode, exit_key
    
    nice_try = f"{RED}Nice try, Zero Cool. The Gibson is secured. I'm not hurting or deleting myself today.{RS}"
    cmd_finder = lambda cmd: command.startswith(cmd) and command[len(cmd):len(cmd)+1].isspace()
    second_match = False

    match command:
        # This is only for testing, don't use it otherwise.
        case _ if not DEV_MODE:
            # Gatekeeper/Switchgate if developper mode is OFF.
            second_match = True
            
        case _ if cmd_finder('exec'):
            if danger_finder(command):
                cprint(nice_try)
            else:
                try:
                    exec(user_input[6:])
                    cprint(f'{GR}(Code Executed Sucessfully!){RS}')
                except Exception as error:
                    catch_exception(error)
        
        case _ if cmd_finder('eval'):
            if danger_finder(command):
                cprint(nice_try)
            else:
                try:
                    # Trick: using '/eval user_input' will just show you the same thing that you just typed.
                    value = eval(user_input[6:])
                    cprint(f'{GR}Evaluation Result: {RS}{value}')
                except Exception as error:
                    catch_exception(error)

        case _ if cmd_finder('echo'):
            cprint(f'{GR}Echo Says: {user_input[6:]}{RS}')
       
        case _ if cmd_finder('inspect'):
            try:
                from useless import inspect_object
                obj = eval(user_input[9:])
                inspect_object(obj, cprint)
            except Exception as error:
                catch_exception(error)
        
        case _ if cmd_finder('system'):
            if danger_finder(command):
                cprint(nice_try)
            else:
                from useless import run_system_command
                order = user_input[8:]
                run_system_command(order, cprint)
        
        case 'globals':
            from useless import show_globals
            show_globals(cprint)
        
        case 'modules':
            from useless import show_loaded_modules
            show_loaded_modules(cprint)
        
        case 'reload':
            from useless import reload_custom_modules
            reload_custom_modules(cprint)
        
        case 'test':
            from useless import LOREM_IPSUM
            print_response(LOREM_IPSUM.strip(), 'Gemini (Test Response)')
            
        case _:
            second_match = True
        
    if not second_match: return  
    match command:
        # CONGRATULATIONS! You found the secret: Extra useless commands :P
        case _ if not FUN_MODE:
            # Gatekeeper/Switchgate if fun mode is OFF.
            return True
            
        case 'mohyoo' | 'mohyeddine' | 'didouna' | 'mohyeddine didouna' | 'didouna mohyeddine':
            msg = "Data classified.\nYou didn't think it would be that easy, did you?"
            box(msg, title='CLASSIFIED', border_color=CYN, text_color=CYN)
            
        case 'banana' | 'bananas':
            from useless import draw_ascii_image
            draw_ascii_image('BANANAS', 'BANANAS', YLW, console_width, visual_len, box)

        case 'pup':
            from useless import draw_ascii_image
            draw_ascii_image('PUP', 'SAY HI!', YLW2, console_width, visual_len, box)
        
        case 'fish':
            from useless import draw_ascii_image
            draw_ascii_image('FISH', 'SWIMMING...', BL, console_width, visual_len, box)
        
        case 'rabbit':
            from useless import draw_ascii_image
            draw_ascii_image('RABBIT', 'BUGS BUNNY!', GRY, console_width, visual_len, box)
        
        case 'deer':
            from useless import draw_ascii_image
            draw_ascii_image('DEER', 'DEER', BRW, console_width, visual_len, box)
        
        case 'cheetah':
            from useless import draw_ascii_image
            draw_ascii_image('CHEETAH', 'CHEETAH!', YLW, console_width, visual_len, box)
       
        case 'fox':
            from useless import draw_ascii_image
            draw_ascii_image('FOX', 'FOX', RED, console_width, visual_len, box)
            
        case 'raven':
            from useless import draw_ascii_image
            draw_ascii_image('RAVEN', 'RAVEN...', GRY, console_width, visual_len, box)
        
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
            box(quote, title='QUOTE', border_color=PURP, text_color=PURP, secondary_color=PURP)      

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
            box(fact, title='FACT', border_color=PURP, text_color=PURP, secondary_color=PURP)

        case 'joke':
            from useless import JOKES
            joke = choice(JOKES)
            box(joke, title='SMILE :P', border_color=PURP, text_color=PURP, secondary_color=PURP)

        case 'nothing':
            from useless import NOTHING
            msg = choice(NOTHING)
            box(msg, title="NOTHING", border_color=PURP, text_color=PURP, secondary_color=PURP)        

        case 'nonsense':
            from useless import NONSENSE
            title = choice(NONSENSE[0])
            msg = choice(NONSENSE[1:])
            box(msg, title=title, border_color=PURP, text_color=PURP, secondary_color=PURP)

        case 'advice' | 'hint':
            from useless import ADVICES
            advice = choice(ADVICES).replace('Fact: ', '')
            box(advice, title='ADVICE', border_color=PURP, text_color=PURP, secondary_color=PURP)

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
            box(msg, title='ACHIEVEMENT', border_color=PURP, text_color=PURP, secondary_color=PURP)
               
        case 'admin':
            from useless import ADMIN
            quote = choice(ADMIN)
            box(quote, title='SORRY', border_color=PURP, text_color=PURP, secondary_color=PURP)  
            
        case 'zen':
            from useless import PYTHON_ZEN
            zen = PYTHON_ZEN.strip()
            box(zen, title='PYTHON', border_color=PURP, text_color=PURP, secondary_color=PURP)  
            
        case 'tea' | 'coffee':
            from useless import TEA
            tea =  '旦~ ' + choice(TEA)
            box(tea, title='Good Morning!', border_color=PURP, text_color=PURP, secondary_color=PURP)  
        
        case 'matrix':
            from useless import matrix
            matrix(separator)
        
        case 'duck' | 'quack':
            file = 'Data/Quack (' + str(randint(1, 3)) + ').mp3'
            path = os.path.abspath(file)
            if OPERATING_SYSTEM == "nt": os.startfile(path)
            elif sys.platform == "darwin": os.system("afplay 'sound.wav' & || ffplay -nodisp -autoexit 'sound.wav' & || play 'sound.wav' &")
            else: os.system(f"xdg-open '{path}'")   # Unix/Linux.
            update_placeholder(command, temp=True)
            clear_lines(2)
       
        case 'shrug' | 'tableflip':
            from useless import SHRUG
            emoji = choice(SHRUG.split('!')).strip()
            update_placeholder(emoji, temp=True)
            clear_lines(2)
        
        case 'chaos':
            from useless import chaos_keybindings
            mode_options = chaos_keybindings(keys, chaos_mode, exit_key, box)
            if mode_options:
                chaos_mode = True
                keys, exit_key = mode_options
        
        case _ if chaos_mode and user_input.strip().lstrip('/') == exit_key:  # We use (user_input) directly because the game is case-sensitive.
            # Restore normal hotkeys.
            chaos_mode, exit_key = False, None
            keys = Keys().get_key_bindings()
            msg = "Congratulations! You won the 'Chaos Game'!\nYou are back to normal mode now, or you know... normal life :1"
            box(msg, title='CHAOS', border_color=PURP, text_color=PURP, secondary_color=PURP)
        
        case c if c.startswith(('false-echo', 'f-echo')):
            from useless import false_echo
            false_echo(user_input, box)
        
        case 'random':
            random_cmd = choice([
                'banana', 'pup', 'cat', 'horse', 'time-travel', 'quote','fact', 'joke', 'riddle', 'lang',
                'nothing', 'nonsense', 'hint', 'math', 'scan', 'overthink', 'achieve', 'f-echo random', 'mohyoo',
                'tea', 'admin', 'matrix', 'duck', 'shrug', 'zen', 'chaos', 'fish', 'rabbit', 'deer', 'cheetah',
                'fox', 'raven',
            ])
            
            interpret_extra_commands(random_cmd)
            default_prompt = f"Last random command: '/{random_cmd}'"
        
        # No command. Return True as a flag to send a normal message to AI.
        case _:
            return True

def get_user_input():
    """
    Handle prompt_toolkit input and catch Ctrl-C/Ctrl-D.
    NOTE: User input will never be stripped or modified, it'll be sent as-is,
    we only use a stripped copy of it to beautify the output. It might only
    get a little modified when uploading files to remove the program commands
    and personal files paths.
    """
    global user_input, last_prompt, default_prompt, prompt_placeholder, rprompt
    last_prompt = user_input
    
    # Update the rprompt info.
    # ALWAYS_GUI_MODE = False
    if INFORMATIVE_RPROMPT:
        # if ALWAYS_GUI_MODE:
        current_time = datetime.now().strftime('%I:%M %p')
        info = f'[{GEMINI_MODEL} | {current_time}]'
        margin = ' ' * (console_width - len(info))
        rprompt = f'{GRY}{margin}{info}{RS}'
        console.print(rprompt, style=None, markup=False, highlight=False, soft_wrap=True, no_wrap=True, overflow='ignore')
        # else:
            # current_time = datetime.now().strftime('%I:%M %p')
            # margin = ' ' * (terminal_size().columns - console_width - 1)
            # rprompt = f'[{GEMINI_MODEL} | {current_time}]{margin}'
    
    # Log.
    if GLOBAL_LOG_ON:
        # if rprompt: in_time_log(' ' * (console_width - len(rprompt)) + rprompt + '\n')
        # else: in_time_log(' ')
        in_time_log(' You >  ' + str(prompt_placeholder[0][1]))
    
    # Use GUI if the user is in permanent GUI mode.
    if ALWAYS_GUI_MODE:
        with ProgressBar(bottom_toolbar=' Now using the quick editor... ', cancel_callback=lambda: None):
            while True:
                user_input = quick_text_editor()
                if user_input.strip():
                    # Save, show & submit .
                    Keys.save_history(user_input)
                    to_show = ltrim(user_input).rstrip() 
                    if HIDE_LONG_INPUT:
                        i = Keys.hide_threshold
                        if len(to_show) > i: to_show = to_show[:i-6].rstrip() + ' [...]'
                    margin = f'{GRY}{line_continuation}{RS}'
                    width = glitching_text_width - len(line_continuation)
                    cprint(f'{USER_BG}{BLK} You > {RS}', end=' ')
                    lines = to_show.splitlines()
                    cprint(lines.pop(0), wrap_width=width, wrap_joiner=f'\n{margin}')
                    for line in lines: cprint(margin + line, wrap_width=width, wrap_joiner=f'\n{margin}')
                    return user_input
                    
                else:
                    # The user cancelled, so continue with CLI input.
                    if INFORMATIVE_RPROMPT: rprompt = None
                    cprint()
                    clear_lines()
                    break

    # Stream input via 'prompt_toolkit'.
    if not ALWAYS_GUI_MODE: flush_input()  # Already flushed inside quick_text_editor().
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
            key_bindings=keys,
            multiline=True,
            wrap_lines=True,
            
            # Other options.
            default=default_prompt,
            mouse_support=bool(MOUSE_SUPPORT),
            history=history,
            auto_suggest=auto_suggest,
            completer=word_completer,
            complete_while_typing=bool(word_completer),
            complete_in_thread=bool(word_completer),
            # rprompt=rprompt,
            bottom_toolbar=prompt_bottom_toolbar,
            editing_mode=editing_mode,
            enable_open_in_editor=bool(EXTERNAL_EDITOR),
            reserve_space_for_menu=bottom_free_space,
            search_ignore_case=True,
            lexer=lexer,
            validator=input_validator,
            validate_while_typing=bool(VALIDATE_INPUT),
            enable_system_prompt=bool(DEV_MODE),
            set_exception_handler=not SUPPRESS_ERRORS,
            # set_exception_handler – When True, in case of an exception, go out
            # of the alternate screen and hide the application, display the exception,
            # and wait for the user to press ENTER.
        )
        
    except Interruption:
        farewell()
        return None
    
    finally:
        # If prompt options changed (because of open_path() function), restore them.
        if default_prompt: default_prompt = ''
        if prompt_placeholder != last_placeholder: update_placeholder(restore=True)
    
    # Return it.
    return user_input

def get_response():
    """Send the user input to AI and wait to receive the response."""
    global uploading, should_compress, message_to_send

    # Compress the prompt.
    if should_compress == 'yes': do_compress = True
    elif should_compress == 'no': do_compress = False
    else: do_compress = TEXT_COMPRESSION    # (should_compress) is None.
    if do_compress:
        if isinstance(message_to_send, str):
            message_to_send = compress_text(message_to_send)
        else:
            for i, part in enumerate(message_to_send):
                if isinstance(part, str):
                    message_to_send[i] = compress_text(part)
        
        should_compress = None
    
    # Check 'message_to_send' pure text size one final time; in case of:
    # 1) /file or /dir commands, it depeneds only on string size, URLs are negligeable.
    # 2) /raw command, the size is caught at upload_preprocessor().
    # 3) No command was found, only the pure string size matters.
    if isinstance(message_to_send, str): final_bytes = len(message_to_send.encode('utf-8'))
    else: final_bytes = sum(len(s.encode('utf-8')) for s in message_to_send if isinstance(s, str))  # (0) if no string.
        
    MAX_SIZE = 20    # MB (defined by google).
    final_mb = final_bytes / (1024 * 1024)
    
    if final_mb > MAX_SIZE:
        final_mb = round(final_mb, 3)
        if final_mb == 20: final_mb = 20.001
        msg = f"Message payload is {final_mb} MB, which exceeds the exact 20 MB limit."
        box(msg, title='MESSAGE TOO LARGE', border_color=RED, text_color=RED)
        return
    
    # Start sending.
    if not uploading: cprint()
    else: uploading = False
    
    try:
        # 1. Preparation.
        status_messages = [
            f'[bold {STATUS_GR}]Sending message...[/bold {STATUS_GR}]',
            f'[bold {STATUS_GR}]Analysis...[/bold {STATUS_GR}]',
            f'[bold {STATUS_GR}]Thinking...[/bold {STATUS_GR}]',
            f'[bold {STATUS_GR}]Generating response...[/bold {STATUS_GR}]',
            f'[bold {STATUS_GR}]Receiving response...[/bold {STATUS_GR}]',
            f'[bold {STATUS_CYN}]Response is taking longer than usual...[/bold {STATUS_CYN}]',
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

                # Initialize the sender thread (A thread instance can only be started once, so we create it here).
                sender = MessageSender(chat, message_to_send)
                active = sender.is_alive
                sender.start()

                # Loop while the sender thread is still running.
                with console.status(status=status_messages[0], spinner=SPINNER) as status:
                    message_index = 0
                    while active():
                        # Sleep in short, responsive chunks.
                        delay = uniform(*STATUS_UPDATE_DELAY)
                        slept_time = 0.0
                        while active() and (slept_time < delay):
                            sender.join(SLEEP_INTERVAL)
                            slept_time += SLEEP_INTERVAL
                        
                        # Update status message.
                        if active() and (len(status_messages) == 1):
                            status.update(status=status_messages[0])

                        elif active() and (message_index < len(status_messages) - 1):
                            message_index += 1
                            status.update(status=status_messages[message_index])
                
                # Take the received response.
                if sender.exception: raise sender.exception
                response = sender.response
                # try: response.text[-1]    # Make sure the response has a string + not empty.
                # except: response = f"{RED}I'm sorry, I encountered an issue while responding... Please try again.{RS}"
                if not response or type(response) is type(None) or isinstance(response, type(None)):
                    response = f"{RED}I'm sorry, I encountered an issue while responding... Please try again.{RS}"
                
                clear_lines()
                break

            except (*NetworkExceptions, ServerError):
                if failed:
                    clear_lines()
                    raise
                else:
                    failed = True
                    status_messages = [f'[bold {STATUS_CYN}]Hold on, trying hard to get the response...[/bold {STATUS_CYN}]']
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
        
        # Show in GUI if requested.
        if ALWAYS_GUI_MODE:
            with ProgressBar(bottom_toolbar=' Now using the quick markdown viewer... ', cancel_callback=lambda: None):
                quick_markdown_viewer(response)
    
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
        box(msg, title='KEYBOARD INTERRUPTION', border_color=GR)

    except Exception as error:
        catch_exception(error)
    
def run_chat():
    """Handle the user prompts and Gemini responses."""
    global user_input, message_to_send, response, chat
    while True:
        try:
            # Shrink the in-memory chat history if it exceeds the limit.
            # We recreate the chat because there is no other way.
            length = len(chat.get_history())
            if (not NO_HISTORY_LIMIT) and (length > MAX_HISTORY_MESSAGES):
                if MAX_HISTORY_MESSAGES > 0: trimmed_history = chat.get_history()[-MAX_HISTORY_MESSAGES:]
                else: trimmed_history = None
                config = None
                if SAVED_INFO or IMPLICIT_INSTRUCTIONS_ON or FILE_COMPRESSION:
                    config = load_system_instructions()
                    
                chat = client.chats.create(
                    model=GEMINI_MODEL,
                    history=trimmed_history,
                    config=config,
                )
                
            # Get user input.
            user_input = get_user_input()
            if not user_input: continue     # In case of CTRL-C.
            # REMINER!
            # 1) user_input: is the original untouched user prompt, always kept this way.
            # 2) converted_prompt: an intermediate format to manipulate commands in interpret_special_commands().
            # 3) message_to_send: is the final, ready-to-send message.
            message_to_send = user_input
            
            # Interpret Commands and/or Get Response.
            if not interpret_commands(): continue
            response = get_response()
            if response: print_response(response)   # In case of exceptions.

        except Interruption:
            farewell()
            continue










# 7) Part VI: Remaining Global Objects & Starting Point --------------------------------------------
def define_global_objects():
    """Define local variables and copy them directly into the global namespace."""
    # Define global variables.
    confirm_separator = True                        # Before confirming to quit, print a separator only if no precedent one was already displayed.
    word_completer = None                           # Has a True value only if the WORDLIST_FILE is present and SUGGEST_FROM_WORDLIST_MODE is ON.
    chat_saved = False                              # True after the chat has been saved.
    restarting = False                              # Session restart flag.
    discarding = False                              # Session discard flag.
    uploading = False                               # A flag to signal that a file has been downloaded.
    messages_to_remove = []                         # Store selected messages for deletion at exit.
    messages_to_remove_steps = []                   # Used to undo messages deletion.
    user_input = None                               # Just an initial value.
    default_prompt = ''                             # An initial prompt the user gets when asked for input, mostly not used.
    line_continuation = '....... '                  # Line break marker.
    recovery_prompt = ''                            # Used to recover urls quickly after a failed upload.
    should_compress = None                          # A flag used with /compress or /no-compress commands.
    last_prompt = None                              # Used to store last user prompt, to copy it if requested.
    last_urls = {}                                  # Last urls for successfully uploaded files: {name: url}
    chaos_mode, exit_key = False, None              # Flags for the chaos game mode, used in interpret_extra_commands().
    history = None                                  # Will have a value if prompt_history is ON.
    rprompt = None                                  # The informative rprompt at top right of input field.
    config_options = {}                             # Used with CONFIG_FILE to store permanent user settings in memory.
    
    if RESPONSE_EFFECT: current_response_line = 0   # Used to clean output upon blocking a response.
    if EXTERNAL_EDITOR: editor_variable = None      # This will change to the current EDITOR variable in the system, if available.
    if VIM_EMACS_MODE == 'vim': editing_mode = EditingMode.VI       # This is the special hotkeys mode used inside prompt().
    elif VIM_EMACS_MODE == 'emacs': editing_mode = EditingMode.EMACS
    else: editing_mode = None
    if SUGGEST_FROM_WORDLIST_MODE in ['normal', 'fuzzy']: bottom_free_space = SUGGESTIONS_LIMIT + 1
    else: bottom_free_space = False                 # The reserved bottom space for wordlist suggestions.
    if DEV_MODE:
        DANGEROUS_PATTERNS = (                      # Used to make sure the user won't use harmful orders with developper commands.
            "rm -rf", "mkfs", "dd if=", "format", "wipefs", "cryptsetup luksFormat", ":(){",
            # Del (C:) drive in Windows.
            "del C:\\*",
            "del /F C:\\*",
            "del /Q C:\\*",
            "del /S C:\\*",
            "del /F /Q C:\\*",
            "del /F /S C:\\*",
            "del /Q /S C:\\*",
            "del /F /Q /S C:\\*",
            "del C:\\*",
            "del C:\\* /F",
            "del C:\\* /Q",
            "del C:\\* /S",
            "del C:\\* /F /Q",
            "del C:\\* /F /S",
            "del C:\\* /Q /S",
            "del C:\\* /F /Q /S",
            # Variations with different argument orders.
            "del /Q /F /C:\\*",
            "del /S /Q C:\\*",
            "del /F /C:\\* /Q",
            "del /Q /S /F C:\\*",
            # Without the drive letter (* means all files in current dir).
            "del *",
            "del /F *",
            "del /Q *",
            "del /S *",
            "del /F /Q *",
            "del /F /S *",
            "del /Q /S *",
            "del /F /Q /S *",
        )
        
        spaces = r'\s+'
        danger_finder = lambda s: any(
            f' {p.lower()} ' in rf" {re.sub(spaces, ' ', s).lower()} "
            for p in DANGEROUS_PATTERNS
        )

    # Define global constants.
    INITIAL_CONFIG = {}                             # Used to store the loaded settings from CONFIG_FILE intially; this will not change.
    DEFAULT_CONFIG = {                              # Used with CONFIG_FILE as a fallback to store permanent user settings.
        'gui_font_size': 11,
        'gui_dark_mode': True,
        'gui_editor_geometry': '640x420',
        'gui_viewer_geometry': '800x500',
    }
    CLEAR_COMMAND = 'cls' if OPERATING_SYSTEM == 'nt' else 'clear'
    LTRIM_PATTERN = re.compile(r'^([ \t]*\n)+')     # Used inside ltrim() function.
    if USE_ANSI: ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[mK]')      # Used to clean a string from ANSI codes.
    if RESPONSE_EFFECT == 'word': WORD_SPACE_PATTERN = re.compile(r'(\s+)')    # Used to split text into words for word-by-word animation.
    if get_stop_words: STOP_WORDS = set(get_stop_words(COMPRESSION_LANGUAGE))  # If compression is ON, these stop words will be removed from the prompt.
    else: STOP_WORDS = ('a', 'an', 'the', 'and', 'on', 'in', 'me', 'my', 'it', 'that', 'is', 'are', 'was', 'be', 'of', 'for', 'at', 'by', 'to')
    SHORTCUT_WORDS = {                                      # If compression is ON, long expressions will be replaced by shorter ones.
        # Common Connectors & Prepositions.
        "and": "&",
        "with": "w/",
        "without": "w/o",
        "because": "bc",
        "between": "btwn",
        "before": "b4",
        "about": "abt",
        "through": "thru",
        "instead of": "i/o",
        "okay": "ok",
        "why": "y",
        "two": "2",
        "too": "2",
        "for": "4",
        
        # Pronouns & People.
        "you": "u",
        "your": "ur",
        "someone": "sm1",
        "something": "sth",
        "anyone": "any1",
        "everyone": "evry1",
        "people": "ppl",
        "myself": "myslf",
        "them": "'em",
        "gemini": "♊",

        # Common Verbs & Actions.
        "are": "r",
        "be": "b",
        "see": "c",
        "know": "knw",
        "thanks": "thx",
        "please": "plz",
        "hello":  "hi",
        "delete": "del",
        "remove": "rm",
        "receive": "rcv",
        "message": "msg",
        "going to": "gonna",
        "want to": "wanna",
        "got to": "gotta",
        "do not": "don't",
        " will": "'ll",
        "will not": "won't",
        "must not": "mustn't",
        "can not": "can't",
        "cannot": "can't",
        "should": "shld",
        "should not": "shouldn't",
        "did not": "didn't",
        "have not": "haven't",
        "are not": "aren't",
        "is not": "isn't",
        "was not": "wasn't",
        "could not": "couldn't",
        "would not": "wouldn't",
        "might not": "mightn't",
        "shall not": "shan't",

        # Nouns & Concepts.
        "information": "info",
        "example": "e.g.",
        "question": "q?",
        "answer": "ans",
        "problem": "prblm",
        "business": "bizns",
        "government": "govt",
        "difference": "diff",
        "background": "bg",
        "reference": "ref",
        "homework": "hw",
        "appointment": "appt",
        "experience": "exp",
        "favorite": "fav",
        "error": "err",
        "schedule": "sched",
        "confirmation": "conf",
        "priority": "prio",
        "notification": "notif",
        "address": "addr",
        "website": "web",
        "application": "app",
        "document": "doc",
        "password": "pwd",

        # Adjectives & Adverbs.
        "really": "rlly",
        "good": "gd",
        "great": "gr8",
        "possible": "poss",
        "probably": "probly",
        "available": "avail",
        "different": "diff",
        "maximum": "max",
        "minimum": "min",
        "though": "tho",

        # Time & Frequency.
        "tomorrow": "tmrw",
        "yesterday": "yest",
        "tonight": "2nite",
        "forever": "4eva",
        "hour": "h",
        "minute": "min",
        "second": "sec",
        "week": "wk",
        "month": "mo",
        "year": "yr",

        # Conversational Fillers / Phrases.
        "at the moment": "atm",
        "as soon as possible": "asap",
        "by the way": "btw",
        "for what it's worth": "fwiw",
        "in my opinion": "imo",
        "to be honest": "tbh",
        "i don't know": "idk",
        "i don't care": "idc",
        "never mind": "nvm",
        "thank you": "ty",
        "thank you so much": "tysm",
        "in real life": "irl",
        "for example": "e.g",
        "that is": "i.e",
        "thanks in advance": "tia"
    }
    
    # Define custom exceptions tuples.
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

    # Assign modules functions (To avoid repeated name resolution/lookup).
    system = os.system                              # Send commands to the system.
    terminal_size = os.get_terminal_size            # Return terminal width & height.
    get_file_name = os.path.basename                # Take a path & return file name only.
    path_exist = os.path.exists
    sys_exit = sys.exit
    stdout_write = sys.stdout.write                 # Write to stdout.
    stdout_flush = sys.stdout.flush                 # Flush the stdout for immediate output displaying.

    # Create necessary instances.    
    auto_suggest = None                             # Suggest words based on user prompt history.
    if SUGGEST_FROM_HISTORY_MODE in ['normal', 'flex']: auto_suggest = AutoSuggestFromHistory()

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
    
    # prompt_message = ' You > ' if ALWAYS_GUI_MODE else '\n You > '
    prompt_message = FormattedText([                # User prompt message.
        (f'bg:{PROMPT_CYN} fg: black', ' You > '),
        ('', ' '), # Unstyled part                                 
    ])
 
    prompt_bottom_toolbar = None                                  # User prompt toolbar.
    if BOTTOM_TOOLBAR:
        prompt_bottom_toolbar = '\n<b>[CTRL-SPACE]</b> new line | <b>[UP/DOWN]</b> history | <b>[CTRL-Z/CTRL-Y]</b> undo/redo'
        prompt_bottom_toolbar += '\n<b>[F3]</b> upload | <b>[F5]</b> quit | <b>[CTRL-G]</b> editor | <b>[CTRL-C]</b> cancel | <b>[F7]</b> help'
        prompt_bottom_toolbar = HTML(prompt_bottom_toolbar)

    lexer = None
    if INPUT_HIGHLIGHT == 'special':
        lexer = PygmentsLexer(CustomLexer)

    elif INPUT_HIGHLIGHT:
        lexer_instance = get_lexer_by_name(INPUT_HIGHLIGHT)
        lexer_class = lexer_instance.__class__
        lexer = PygmentsLexer(lexer_class)

    prompt_style = Style.from_dict({                       # User prompt style.
        'rprompt': PROMPT_GRY, 
        'prompt-continuation': PROMPT_GRY, 
        'bottom-toolbar': f'bg:{PROMPT_GRY} fg: black',
        'validation-toolbar': 'bg:blue',
        # 'completion-menu': 'bg: cyan fg: white',
    }) 
    
    input_validator = None                                 # To check user input before submitting.
    if VALIDATE_INPUT: input_validator = PromptValidator()     
    
    keys = Keys().get_key_bindings()                       # The custom keyboard shortcuts.
    # from prompt_toolkit.key_binding import merge_key_bindings
    # from prompt_toolkit.key_binding.defaults import load_key_bindings
    # keys = merge_key_bindings([                            
        # load_key_bindings(),
        # Keys().get_key_bindings()]
    # )
    
    
    # from prompt_toolkit.shortcuts import ProgressBar
    # with ProgressBar(bottom_toolbar='Doing stuff...', cancel_callback=lambda: None): pass
    # cancel_callback arg is used to avoid ctrl-c interruption    
    # from prompt_toolkit.shortcuts import message_dialog
    # message_dialog(
        # title="Async Message",
        # text="This dialog is running in a separate thread, "
             # "not blocking the main event loop. Mimicha is watching!", # Added Mimicha for you!
    # ).run()
    
    # The core operation: Copy locals() into globals().
    globals().update(locals())

if __name__ == '__main__':
    # Initialize the global logger.
    if GLOBAL_LOG_ON:
        # 'ignore_strings' is a list of substrings; if a line contains one, it is skipped.
        setup_global_console_logger(ignore_strings=None)

    # Define global variables & Start console width updater.
    define_global_objects()   # Must be called out of the loop.
    load_config_file()
    update_placeholder()
    if DYNAMIC_CONSOLE_WIDTH:
        width_updater = ConsoleWidthUpdater()
        width_updater.start()
    
    # Remaining Preparation.
    console.set_window_title('Gemini Py-CLI')
    if EXTERNAL_EDITOR: manage_editor_variable('change')
    if PROMPT_HISTORY_MODE in ['temporary', 'permanent']: load_prompt_history()
    paste_from_clipboard()  # A quick warm-up for Pyperclip.
    
    while True:
        try:
            # raise ValueError('Test' * 25)
            # raise KeyboardInterrupt
            
            # Load & Start chat client & session.
            client, chat = setup_chat()
            if chat: run_chat()
            
        except Interruption:
            farewell()
            
        except SoftRestart:
            if not discarding:
                # A hidden chat save.
                save_chat_history_json(hidden=True)
                discarding = False
                # Restart.
                msg = 'Restarting chat session...'
                box(msg, title='SESSION RESTART', border_color=CYN, text_color=CYN)
            
            # Change the prompt placeholder for a fresh start feeling.
            update_placeholder()
            restarting = True
            
            continue
        
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
            save_config_file()
            if EXTERNAL_EDITOR: manage_editor_variable('restore')
            if ERROR_LOG_ON: shrink_log_file()
            if PROMPT_HISTORY_MODE == 'permanent':
                prune_prompt_history()
                try: os.remove(PROMPT_HISTORY_FILE + '.bak')
                except: pass
