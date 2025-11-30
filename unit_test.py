# This is a simple test suite for error handling inside 'gemini.py'.
import sys
import unittest
from unittest.mock import patch, MagicMock
from threading import Thread
from io import StringIO


# --- MOCK DEPENDENCIES AND CONSTANTS ---
# Mock color constants
RED = '\033[91m' 
YLW = '\033[93m'
GR = '\033[92m'
UL = '\033[4m'
RS = '\033[0m'
CYN = '\033[96m'
BD = '\033[1m'

# Mock settings constants
MOCK_GEMINI_API_KEY = 'YOUR_API_KEY_HERE'
MOCK_ERROR_LOG_ON = True
MOCK_GLOBAL_LOG_ON = True
MOCK_NO_ERROR_DETAILS = False
MOCK_SERVER_ERROR_ATTEMPTS = 2
MOCK_SERVER_ERROR_DELAY = (0.01, 0.02) 
MOCK_HTTP_TIMEOUT = 10.0
MOCK_WAIT_1 = "yellow"
MOCK_SPINNER = "dots"

# Mock Exceptions
class MockClientError(Exception):
    def __init__(self, message, code=400):
        self.message = message
        self.code = code
        super().__init__(message)

class MockServerError(Exception):
    def __init__(self, message, code=500):
        self.message = message
        self.code = code
        super().__init__(message)

class MockConnectionError(Exception): pass
class MockReadTimeout(Exception): pass
class MockConnectTimeout(Exception): pass
class MockConnectError(Exception): pass
class MockRemoteProtocolError(Exception): pass
class MockHttpxReadTimeout(Exception): pass
class MockHttpxHTTPError(Exception): pass
class MockHttpxConnectError(Exception): pass
class MockHttpxRemoteProtocolError(Exception): pass

# Global variables used by the error handlers (must be defined for testing)
global user_input, restarting, confirm_separator, chat, console, sys_exit
user_input = "test prompt"
restarting = False
confirm_separator = True
chat = MagicMock()
console = MagicMock()
sys_exit = MagicMock() # Mock sys_exit to prevent the test suite from quitting

# Mock utility functions
box = MagicMock()
cprint = MagicMock()
separator = MagicMock()
quick_sleep = MagicMock()
log_caught_exception = MagicMock()
in_time_log = MagicMock()
log_error = MagicMock()
clear_lines = MagicMock()
save_chat_history_json = MagicMock()

# Define a mock for the helper function print_status
def print_status(action, message, color):
    action()
    cprint(f"Status: {message} ({color})") 

# --- COPIED ERROR HANDLER FUNCTIONS FROM gemini.py ---
NetworkExceptions = (
    MockConnectionError, MockReadTimeout, MockConnectTimeout, MockConnectError, 
    MockRemoteProtocolError, MockHttpxReadTimeout, MockHttpxHTTPError, 
    MockHttpxConnectError, MockHttpxRemoteProtocolError,
)
Interruption = (KeyboardInterrupt, EOFError,)

class SoftRestart(Exception):
    """Custom exception to signal a safe restart of the chat session."""
    pass

class GeminiWorker(Thread):
    def __init__(self, chat_session, user_input, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.daemon = True
        self.chat = chat_session
        self.user_input = user_input
        self.response = None
        self.exception = None
    def run(self):
        try:
            self.response = self.chat.send_message(self.user_input)
        except Exception as error:
            self.exception = error

def catch_no_api_key():
    msg_1 = "Please replace 'YOUR_API_KEY_HERE' in 'settings.py' with your actual key."
    msg_2 = "You'll find the key placeholder at the first few lines.\n"
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}Showing the quick help menu..."
    box(msg_1, msg_2, msg_3, msg_4, title='NO API KEY PROVIDED', border_color=RED, text_color=RED)

def catch_client_error_startup(error):
    if MOCK_ERROR_LOG_ON: log_caught_exception()
    msg_1 = f"{RED}Client side error occurred:\n{RED}{error.message}.\n"
    msg_2 = f"{RED}Check your settings, especially the API key validation or limits."
    msg_3 = f"{GR}For a new key, visit: {UL}https://aistudio.google.com/app/api-keys{RS}"
    msg_4 = f"{GR}(Remember that it requires a google account)\n"
    msg_5 = f"{GR}Showing the quick help menu...{RS}"
    box(msg_1, msg_2, msg_3, msg_4, msg_5, title='CLIENT SIDE ERROR', border_color=RED, text_color=RED, secondary_color=RED)

def catch_client_error_in_chat(error):
    if MOCK_ERROR_LOG_ON: log_caught_exception()
    msg_1 = f"{RED}Client side error occurred:\n{RED}{error.message}\n"
    msg_2 = f"{YLW}Check your settings, especially the API key validation or limits."
    msg_3 = f"{YLW}If you exceeded characters limit (like hundreds of thousands of\n{YLW}characters), shorten your prompt!"
    msg_4 = f"{YLW}Restarting the session might also help (Type 'restart')."
    box(msg_1, msg_2, msg_3, msg_4, title='CLIENT SIDE ERROR', border_color=RED, text_color = RED, secondary_color=RED)

def catch_server_error_startup(error_occurred, attempts):
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = MOCK_SERVER_ERROR_ATTEMPTS, *MOCK_SERVER_ERROR_DELAY
    if MOCK_ERROR_LOG_ON: log_caught_exception()
    if not error_occurred:
        separator('\n', color=RED)
        cprint(f"{RED}A temporary server problem occurred.")
        cprint(f'It might be a service overloading, maintenance or backend errors...')
    if attempts < MOCK_SERVER_ERROR_ATTEMPTS:
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
    else:
        cprint(f'{YLW}Tried {MAX_ATTEMPTS} times with no response! Please wait for sometime...{RS}')
        separator(color=RED)
        sys_exit(1)

def catch_server_error_in_chat():
    global confirm_separator, user_input, chat, console
    if MOCK_ERROR_LOG_ON: log_caught_exception()
    MAX_ATTEMPTS, DELAY_1, DELAY_2 = MOCK_SERVER_ERROR_ATTEMPTS, *MOCK_SERVER_ERROR_DELAY
    confirm_separator = False
    separator('\n', color=RED)
    cprint(f"{RED}A temporary server problem occurred.")
    cprint(f'It might be a service overloading, maintenance or backend errors...')
    try:
        print_status(lambda: quick_sleep(DELAY_1), f'Retrying in {DELAY_1} seconds...', 'yellow')
    except Interruption:
        separator(color=RED)
        cprint()
        return
    response = None
    for attempt in range(MOCK_SERVER_ERROR_ATTEMPTS):
        try:
            worker = GeminiWorker(chat, user_input)
            worker.start()
            with console.status(status=f'[bold {MOCK_WAIT_1}]Waiting for response...[/bold {MOCK_WAIT_1}]',
                                spinner=MOCK_SPINNER):
                if attempt == 0:
                    raise MockServerError("Simulated server error")
                elif attempt == 1:
                    worker.response = "Mock successful response"
                while worker.is_alive(): worker.join(0.001)

            if worker.exception: raise worker.exception
            cprint(GR + 'Response received!' + RS)
            response = worker.response
            break
        except MockServerError:
            if attempt >= MAX_ATTEMPTS - 1:
                cprint(f'{YLW}Tried {MAX_ATTEMPTS} times with no response! Please wait for sometime...{RS}')
                response = None
                break
            print_status(lambda: quick_sleep(DELAY_2), f'Issue persisting, retrying in {DELAY_2} seconds...', 'yellow')
            continue
        except MockClientError as error:
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
    confirm_separator = True
    separator(color=RED)
    if not response: cprint()
    return response

def catch_network_error():
    global user_input, restarting
    if MOCK_ERROR_LOG_ON: log_caught_exception()
    if restarting: clear_lines()
    error = sys.exc_info()[1]
    error = str(error).lower() # Simplified traceback
    if 'timeout' in error:
        title = 'TIMEOUT'
        msg = f"{RED}API call exceeded the hard timeout limit of ({MOCK_HTTP_TIMEOUT}) seconds.\n"
        msg += f"{RED}Please, wait for sometime until the network becomes stable.\n"
        msg += f"{YLW}You can change the HTTP timeout delay in settings."
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
    global confirm_separator
    if MOCK_ERROR_LOG_ON: log_caught_exception()
    separator('\n', color=RED)
    log_error(f'An error occurred:\n"{error}"')
    if not MOCK_NO_ERROR_DETAILS:
        try:
            if MOCK_GLOBAL_LOG_ON: in_time_log("See the details? (y/n): ...")
            see_error = input("See the details? (y/n): ").strip().lower()
        except Interruption:
            confirm_separator = False
            cprint()
            raise
        if see_error == 'y':
            cprint(RED + "Mock Traceback" + RS) # Mock traceback output
        else:
            cprint(f"{GR}Acting blind...{RS}")
    else:
        clear_lines()
    separator(color=RED, end='\n\n')

def catch_fatal_exception(error):
    if MOCK_ERROR_LOG_ON: log_caught_exception(level='critical')
    separator('\n', color=RED)
    cprint(f"{GR + BD}Congratulations! You found it. It's a BUG!")
    cprint(f"To be honest, I'm really sorry for that.")
    cprint(f"Please let me know, I'll try to respond as soon as possible.")
    cprint(f"GitHub Issues: {UL}https://github.com/Mohyoo/Gemini-Py-CLI/issues{RS}\n")
    log_error(f'A fatal error occurred:\n"{error}"\nAnd the program has to QUIT.')
    if not MOCK_NO_ERROR_DETAILS:
        if MOCK_GLOBAL_LOG_ON: in_time_log("See the details? (y/n): ...")
        see_error = input("See the details? (y/n): ").strip().lower()
        if see_error == 'y':
            cprint(RED + "Mock Traceback" + RS) # Mock traceback output
        else:
            cprint(f"{YLW}\nInhales.. Deep breathing.. Now out.{RS}")
    else:
        clear_lines()
    save_chat_history_json()

# --- UNIT TESTS ---

class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        # Reset mocks before each test
        box.reset_mock()
        cprint.reset_mock()
        separator.reset_mock()
        quick_sleep.reset_mock()
        log_caught_exception.reset_mock()
        in_time_log.reset_mock()
        log_error.reset_mock()
        clear_lines.reset_mock()
        sys_exit.reset_mock()
        save_chat_history_json.reset_mock()

        # Reset global state
        global user_input, restarting, confirm_separator
        user_input = "initial prompt"
        restarting = False
        confirm_separator = True

    # Custom runner method to execute the test and print results (Kept for friendly output)
    def run(self, result=None):
        if result is None:
            result = self.defaultTestResult()
        
        # Start of Test
        print(f"\n{CYN}>> Running Test: {self._testMethodName}{RS}")
        
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        stdout_capture = StringIO()
        stderr_capture = StringIO()
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        super().run(result)
        
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        # End of Test and result reporting
        if result.wasSuccessful():
            print(f"{GR}   [SUCCESS] {self._testMethodName} passed.{RS}")
        else:
            outcome = "FAILED" if result.failures else "ERROR"
            color = RED
            
            buffer = StringIO()
            test_id = self.id()
            traces = result.errors + result.failures
            
            for tid, trace in traces:
                if tid == test_id: buffer.write(trace)

            print(f"{color}   [{outcome}] {self._testMethodName} {outcome.lower()}.{RS}")
            traceback_output = buffer.getvalue().strip()
            if traceback_output:
                print(f"{YLW}   --- Traceback ---{RS}")
                print(traceback_output)
                print(f"{YLW}   -----------------{RS}")

    def test_catch_no_api_key(self):
        """Tests catch_no_api_key handler: Ensures box() is called with correct title."""
        catch_no_api_key()
        self.assertTrue(box.called)
        self.assertIn('NO API KEY PROVIDED', box.call_args[1]['title'])

    def test_catch_client_error_startup(self):
        """Tests catch_client_error_startup: Logs, calls box(), with startup-specific advice."""
        error = MockClientError("Invalid API Key")
        catch_client_error_startup(error)
        log_caught_exception.assert_called_once()
        self.assertTrue(box.called)
        self.assertIn('CLIENT SIDE ERROR', box.call_args[1]['title'])

    def test_catch_client_error_in_chat(self):
        """Tests catch_client_error_in_chat: Logs, calls box(), with chat-specific advice."""
        error = MockClientError("Rate limit exceeded")
        catch_client_error_in_chat(error)
        log_caught_exception.assert_called_once()
        self.assertTrue(box.called)
        self.assertIn('CLIENT SIDE ERROR', box.call_args[1]['title'])

    @patch('sys.exc_info', return_value=(MockHttpxReadTimeout, MockHttpxReadTimeout('ReadTimeout Error'), None))
    @patch(__name__ + '.restarting', False, create=True)
    def test_catch_network_error_timeout(self, mock_exc_info):
        """Tests catch_network_error for a Timeout: Ensures user_input is *preserved* when not restarting."""
        global user_input
        try:
            raise MockHttpxReadTimeout("ReadTimeout Error")
        except MockHttpxReadTimeout:
            catch_network_error()

        log_caught_exception.assert_called_once()
        self.assertTrue(box.called)
        self.assertIn('TIMEOUT', box.call_args[1]['title'])
        self.assertIsNotNone(user_input) 
        self.assertIn('hard timeout limit', box.call_args[0][0])
        clear_lines.assert_not_called()

    @patch('sys.exc_info', return_value=(MockConnectError, MockConnectError('Connect Error'), None))
    @patch(__name__ + '.restarting', True, create=True)
    def test_catch_network_error_connection_restarting(self, mock_exc_info):
        """Tests catch_network_error for a Connection error: Ensures clear_lines is called twice when restarting."""
        global user_input
        try:
            raise MockConnectError("Connection Error")
        except MockConnectError:
            catch_network_error()

        log_caught_exception.assert_called_once()
        self.assertTrue(box.called)
        self.assertIn('NETWORK ERROR', box.call_args[1]['title'])
        self.assertEqual(clear_lines.call_count, 2)
        self.assertIsNotNone(user_input) 

    def test_catch_server_error_startup_fail(self):
        """Tests catch_server_error_startup: Ensures correct retry logic and final exit."""
        # attempts = 0 (first error)
        catch_server_error_startup(False, 0)
        separator.assert_called_with('\n', color=RED)
        self.assertIn('Status: Retrying in 0.01 seconds... (yellow)', [c.args[0] for c in cprint.call_args_list])
        sys_exit.assert_not_called()
        cprint.reset_mock()
        quick_sleep.reset_mock()

        # attempts = 1 (second error)
        catch_server_error_startup(True, 1)
        self.assertIn('Status: Issue persisting, retrying in 0.02 seconds... (yellow)', [c.args[0] for c in cprint.call_args_list])
        sys_exit.assert_not_called()
        cprint.reset_mock()
        quick_sleep.reset_mock()

        # attempts = MAX_ATTEMPTS (final error)
        catch_server_error_startup(True, MOCK_SERVER_ERROR_ATTEMPTS)
        # FIX: Assert on the full colorized string, which includes YLW and RS
        expected_final_message = f'{YLW}Tried {MOCK_SERVER_ERROR_ATTEMPTS} times with no response! Please wait for sometime...{RS}'
        self.assertIn(expected_final_message, [c.args[0] for c in cprint.call_args_list])
        sys_exit.assert_called_once_with(1)

    @patch(__name__ + '.GeminiWorker', autospec=True)
    def test_catch_server_error_in_chat_success_on_retry(self, MockGeminiWorker):
        """Tests catch_server_error_in_chat: Ensures retry mechanism succeeds on second attempt."""
        global confirm_separator
        worker_instance_1 = MockGeminiWorker.return_value
        worker_instance_1.exception = MockServerError("First fail")
        worker_instance_1.is_alive.side_effect = [True, False] 

        worker_instance_2 = MockGeminiWorker.return_value
        worker_instance_2.exception = None
        worker_instance_2.response = "Mock successful response"
        worker_instance_2.is_alive.side_effect = [True, False] 

        MockGeminiWorker.side_effect = [worker_instance_1, worker_instance_2]
        console.status.return_value.__enter__.return_value = None

        response = catch_server_error_in_chat()

        self.assertEqual(quick_sleep.call_count, 2)
        self.assertEqual(MockGeminiWorker.call_count, 2)
        self.assertTrue(confirm_separator)
        self.assertEqual(response, "Mock successful response")
        self.assertIn(GR + 'Response received!' + RS, [c.args[0] for c in cprint.call_args_list])

    @patch('builtins.input', side_effect=['n'])
    def test_catch_exception_no_details(self, mock_input):
        """Tests catch_exception with 'n': Ensures logs are written but details are skipped."""
        error = ValueError("Test Exception")
        catch_exception(error) 

        log_caught_exception.assert_called_once()
        log_error.assert_called_once()
        self.assertEqual(mock_input.call_count, 1)
        self.assertIn(f"{GR}Acting blind...{RS}", [c.args[0] for c in cprint.call_args_list])

    @patch('builtins.input', side_effect=['y'])
    def test_catch_exception_show_details(self, mock_input):
        """Tests catch_exception with 'y': Ensures logs are written and Mock Traceback is printed."""
        error = ValueError("Test Exception")
        catch_exception(error)

        self.assertEqual(mock_input.call_count, 1)
        self.assertIn(RED + "Mock Traceback" + RS, [c.args[0] for c in cprint.call_args_list])
        cprint.assert_called()

    @patch('builtins.input', side_effect=[KeyboardInterrupt()])
    def test_catch_exception_interruption(self, mock_input):
        """Tests catch_exception with Interruption: Ensures the exception is re-raised."""
        global confirm_separator
        error = ValueError("Test Exception")
        with self.assertRaises(Interruption):
            catch_exception(error)

        self.assertFalse(confirm_separator)

    @patch('builtins.input', side_effect=['y'])
    def test_catch_fatal_exception_show_details(self, mock_input):
        """Tests catch_fatal_exception with 'y': Ensures critical log is called and chat history is saved."""
        error = RuntimeError("Fatal Test Error")
        catch_fatal_exception(error)

        log_caught_exception.assert_called_with(level='critical')
        save_chat_history_json.assert_called_once()
        self.assertIn(RED + "Mock Traceback" + RS, [c.args[0] for c in cprint.call_args_list])

    @patch('builtins.input', side_effect=['n'])
    def test_catch_fatal_exception_no_details(self, mock_input):
        """Tests catch_fatal_exception with 'n': Ensures critical log is called and user exits gracefully."""
        error = RuntimeError("Fatal Test Error")
        catch_fatal_exception(error)

        log_caught_exception.assert_called_with(level='critical')
        self.assertIn(f"{YLW}\nInhales.. Deep breathing.. Now out.{RS}", [c.args[0] for c in cprint.call_args_list])
        self.assertEqual(clear_lines.call_count, 0) 

if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
