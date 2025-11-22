import os
import re
import sys
import logging
import threading
from settings import GLOBAL_LOG_FILE

# A quick cleanup.
try:
    with open(GLOBAL_LOG_FILE, 'w', encoding='utf-8'): pass
except:
    pass

# ANSI stripping regex - captures standard colors (CSI) AND Window Titles/Links (OSC).
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]|\].*?(?:\x07|\x1B\\))')

# Log options.
LOG_LEVEL_MAP = {
    'DEBUG':    logging.DEBUG,
    'INFO':     logging.INFO,
    'WARNING':  logging.WARNING,
    'ERROR':    logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

LOG_LEVEL_NAME = 'DEBUG'    # The level used for logging.
LOG_LEVEL_INT = LOG_LEVEL_MAP[LOG_LEVEL_NAME]
LOG_FORMAT = '%(asctime)s - T:%(threadName)-10s - %(levelname)-8s | %(message)s'
LOG_ROOT = False            # If True, it'll log main thread + other threads + libraries debugging messages.
LINE_SEPARATOR = '-'        # If LOG_ROOT is ON, this'll add a separator if the thread or the module who's logging changes.

original_stdout = None      # Used to keep console output intact.
console_logger = None       # An instance of the logger.


class StdoutTee:
    def __init__(self, original_stdout_stream, logger_instance, ignore_strings=None):
        self.original_stdout = original_stdout_stream
        self.logger = logger_instance
        self.ignore_strings = ignore_strings if ignore_strings else []
        self._logging_active = False
        self._buffer = ''

    def write(self, s):
        # 1. Write to the real console immediately
        self.original_stdout.write(s)

        # 2. Accumulate in buffer
        self._buffer += s

        # 3. Process lines ONLY when a newline occurs
        if not self._logging_active:
            self._logging_active = True
            try:
                while '\n' in self._buffer:
                    # Split the first available line
                    line, self._buffer = self._buffer.split('\n', 1)
                    
                    # FIX: Handle Carriage Returns (\r).
                    # Apps like 'Rich' or 'Prompt_toolkit' write: "Loading\rDone".
                    # We keep only the final state (the part after the last \r).
                    if '\r' in line:
                        line = line.rsplit('\r', 1)[-1]

                    # Clean ANSI codes
                    cleaned_line = ANSI_ESCAPE_PATTERN.sub('', line)

                    # FIX: Omit ignored strings
                    # We check 'if x in cleaned_line' so partial matches work
                    if self.ignore_strings and any(ignored in cleaned_line for ignored in self.ignore_strings):
                        continue

                    # We use rstrip() to remove trailing spaces but keep the line itself
                    log_method = getattr(self.logger, LOG_LEVEL_NAME.lower())
                    log_method(cleaned_line.rstrip())

            except Exception:
                # Failsafe to prevent logging errors from crashing the main app
                pass
            finally:
                self._logging_active = False

    def flush(self):
        self.original_stdout.flush()
        
    # FIX: The "Broken Words" Fix.
    # This method passes ANY attribute access (like 'columns', 'encoding', 'isatty')
    # straight to the original stdout. This tells 'Rich' the correct terminal width,
    # preventing it from chopping words like 'import' and 'os' onto separate lines.
    def __getattr__(self, name):
        return getattr(self.original_stdout, name)


class SeparatingFileHandler(logging.FileHandler):
    """
    A custom file handler that inserts a separator line 
    when the logging thread or the logging library changes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use a non-existent name initially
        self.last_thread_name = ''
        self.last_logger_name = ''
        self.switched = False
        
    def emit(self, record):
        """Write the separator."""
        current_thread_name = record.threadName
        current_logger_name = record.name
        
        # Define the possible names for your application's logger
        APP_LOGGER_NAMES = ('root', 'console_output_tee')
        
        # Check for change in thread OR logger
        thread_changed = current_thread_name != self.last_thread_name
        
        # Check for change in log source (App -> Lib or Lib -> App)
        is_app = current_logger_name in APP_LOGGER_NAMES
        last_is_app = self.last_logger_name in APP_LOGGER_NAMES if self.last_logger_name else True
        source_changed = self.switched and (is_app != last_is_app)
        
        if thread_changed or source_changed:
            if self.stream is None:
                self.stream = self._open()

            # Separate and label if there was a previous log entry
            if self.switched:
                if thread_changed and not source_changed:
                    separator_line = f"{LINE_SEPARATOR * 6} THREAD SWITCHED TO: {current_thread_name} {LINE_SEPARATOR * (18 - len(current_thread_name))}|{LINE_SEPARATOR * 100}\n"
                elif source_changed:
                    if is_app:
                        separator_line = f"{LINE_SEPARATOR * 6} APPLICATION LOGS RESUME {LINE_SEPARATOR * 15}|{LINE_SEPARATOR * 100}\n"
                    else:
                        separator_line = f"{LINE_SEPARATOR * 6} LIBRARY: {current_logger_name} {LINE_SEPARATOR * (29 - len(current_logger_name))}|{LINE_SEPARATOR * 100}\n"
                else: # Should only be a thread change
                    separator_line = f"{LINE_SEPARATOR * 6} THREAD SWITCHED TO: {current_thread_name} {LINE_SEPARATOR * (18 - len(current_thread_name))}|{LINE_SEPARATOR * 100}\n"
                
                # Write separator line
                self.stream.write(separator_line)

            # Update the trackers
            self.last_thread_name = current_thread_name
            self.last_logger_name = current_logger_name # <<< NEW TRACKER UPDATE
            self.switched = True
        
        super().emit(record)


def setup_global_console_logger(log_file=GLOBAL_LOG_FILE, ignore_strings=None):
    """
    Sets up the logger.
    ignore_strings: A list of substrings. If a line contains one, it is skipped.
    """
    global original_stdout, console_logger

    if original_stdout is not None:
        in_time_log("Global console logger is already set up.")
        return

    original_stdout = sys.stdout 
    
    if LOG_ROOT : console_logger = logging.getLogger()
    else: console_logger = logging.getLogger('console_output_tee')
    console_logger.setLevel(LOG_LEVEL_INT)
    
    # delay=True ensures the file is only created when we actually write to it
    if LOG_ROOT: file_handler = SeparatingFileHandler(log_file, encoding='utf-8', delay=True)
    else: file_handler = logging.FileHandler(log_file, encoding='utf-8', delay=True)
    
    # Simplified format: Just the timestamp and the message
    formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(LOG_LEVEL_INT)
    console_logger.addHandler(file_handler)
    
    # Inject the logger into StdoutTee
    sys.stdout = StdoutTee(original_stdout, console_logger, ignore_strings)
    in_time_log(f"Global logger initialized to '{log_file}'.")

def in_time_log(text: str):
    """Logs custom text directly to the file logger, bypassing the StdoutTee."""
    text = ANSI_ESCAPE_PATTERN.sub('', text)
    if console_logger:
        for line in text.splitlines():
            log_method = getattr(console_logger, LOG_LEVEL_NAME.lower())
            log_method(line)
