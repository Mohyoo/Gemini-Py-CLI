import os
import sys
import logging
import traceback
from settings import ERROR_LOG_ON, ERROR_LOG_FILE
# (+1) import inside log_unhandled_exception().


# Logging Configuration.
LOG_FORMAT = (
    "%(asctime)s - %(levelname)s!"
    "\nLogger Address: %(name)s \nThread: %(threadName)s"
    "\nModule: %(module)s \nFunction: %(funcName)s \nLine: %(lineno)d"
    "\nMessage: %(message)s"
)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_SEPARATOR = '-' * 100
STACK_LEVEL = 4     # The N° of steps the logger goes back to see the origine of the error.


def setup_logger():
    """Configures the logging system."""
    # 1. Create a root logger & Set root level to capture all errors & warnings.
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)  

    # 2. File Handler configuration.
    file_handler = logging.FileHandler(ERROR_LOG_FILE, encoding='utf-8')
    file_handler.setLevel(logging.WARNING)
    
    # 3. Formatter.
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler.setFormatter(formatter)
    
    # 4. Add handler to the logger.
    logger.addHandler(file_handler)
    
    # 5. Optional: Log errors to console.
    # stream_handler = logging.StreamHandler(sys.stdout)
    # stream_handler.setLevel(logging.WARNING)
    # stream_handler.setFormatter(formatter)
    # logger.addHandler(stream_handler)
  
def get_private_traceback(traceback_lines):
    """
    Sanitize the traceback lines to remove full file paths.
    This is for user privacy, as we don't want to include personal paths.
    """
    # Remove full file paths.
    sanitized_traceback_lines = []
    for line in traceback_lines:
        if line.strip().startswith('File "'):
            # This line contains a file path; We replace it with just the base filename.
            parts = line.split('"')
            parts[1] = os.path.basename(parts[1])
            sanitized_line = '"'.join(parts)
            sanitized_traceback_lines.append(sanitized_line)
        else:
            # Other lines or code context lines are kept as-is.
            sanitized_traceback_lines.append(line)
    
    full_traceback = ''.join(sanitized_traceback_lines)
    return full_traceback
  
def log_caught_exception(message=None, level='error'):
    """
    Logs details of a currently handled exception (must be called inside an
    'except' block).
    """
    # Get error attribute + full traceback.
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    full_traceback = get_private_traceback(traceback_lines)
    
    if level == 'critical': log_message = "FATAL ERROR CAUGHT: "
    else: log_message = "CAUGHT ERROR: "
    log_message += f"{message or 'No specific message provided.'}\n"
    log_message += f"Exception Type: {exc_type.__name__}\n"
    log_message += f"Exception Value: {exc_value}\n"
    log_message += f"\nFull Traceback:\n{full_traceback}"
    log_message += LOG_SEPARATOR

    # Log the detailed message at ERROR level.
    log_method = getattr(logging, level.lower())
    log_method(log_message, stacklevel=STACK_LEVEL)

def log_unhandled_exception(exc_type, exc_value, exc_traceback):
    """
    Custom handler called automatically by Python for all uncaught exceptions.
    It logs the error details and then exits the program gracefully.
    """
    from gemini import console_width, EXTERNAL_EDITOR, save_chat_history_json, save_config_file, manage_editor_variable
    
    # Save the most important stuff.
    save_chat_history_json()
    save_config_file()
    if EXTERNAL_EDITOR: manage_editor_variable('restore')

    # Print error to console (standard behavior, with some customization).
    print('\n' + '─' * console_width)
    if issubclass(exc_type, (ImportError, ModuleNotFoundError)):
        print("Missing Dependency!")
        print(f"It looks like you're missing a module: {exc_value.name}")
        print(f"Please try running: pip install {exc_value.name}")
        print("Or, if the feature you tried to use is optional, stop using it to avoid this error.")
        
    elif issubclass(exc_type, (PermissionError, OSError)):
        file = getattr(exc_value, 'filename', 'Unknown file')
        print(f"System reported an issue with: {file}")
        print(f"Details: {exc_value}\n\nThis is likely a permission error.")
        print("Check if the file is locked, missing, or in a protected folder.")
        
    else:
        print('Unexpected error, program terminated!\n')
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        
    print('─' * console_width)
    
    # Use 'traceback.format_exception' to get the full traceback structure.
    traceback_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    full_traceback = get_private_traceback(traceback_lines)
    
    log_message = (f"CRITICAL UNCAUGHT ERROR: {exc_type.__name__}: {exc_value} - PROGRAM TERMINATED!!!\n")
    log_message += f"Exception Type: {exc_type.__name__}\n"
    log_message += f"Exception Value: {exc_value}\n"
    log_message += f"\nFull Traceback:\n{full_traceback}"
    log_message += LOG_SEPARATOR
    
    # Log the detailed message using the root logger & Ensure the log file buffer is flushed before exit.
    logging.critical(log_message, stacklevel=STACK_LEVEL)
    logging.shutdown()


# Initialize the logger & Register the custom hook for UNCAUGHT exceptions for automatic logging of fatal errors.
setup_logger()
sys.excepthook = log_unhandled_exception
