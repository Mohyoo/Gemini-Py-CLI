# A simple file generation chat; less featured & fragile, but it does the job.

import os
import re
import sys
import base64
from google.genai import Client, types
from webbrowser import open as open_file

# Add the parent directory to the path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import GEMINI_API_KEY, FILE_GENERATOR_MODEL, FILE_GENERATION_DIR

# Define constants.
BASE64_PATTERN = re.compile(r'^[A-Za-z0-9+/]*(?:[AQgw]==|[AEIMQUYcgkosw048]=)?$')
SIGNATURES = {                      # Contain magic numbers & their corresponding file extension.
    # Images.
    b'\x89PNG': 'png',
    b'\xff\xd8\xff': 'jpg',
    b'GIF87a': 'gif',
    b'GIF89a': 'gif',
    b'\x00\x00\x00\x1cftypheic': 'heic', # High Efficiency Image.
    b'\x00\x00\x00\x18ftypheic': 'heic',
    b'\x00\x00\x00\x14ftypavif': 'avif',
    b'BM': 'bmp',
    b'P6\n': 'ppm',
    b'P5\n': 'pgm',             # Grayscale version.
    b'P3\n': 'ppm',             # ASCII version.
    b'%!PS': 'eps',
    b'<svg': 'svg',
    b'<?xml': 'xml',           # Often a precursor to SVG.
    
    # Audio.
    b'ID3': 'mp3',
    b'\xff\xfb': 'mp3',         # Alternative MP3 (Frame Sync).
    b'fLaC': 'flac',
    b'OggS': 'ogg',             # Ogg/Opus
    b'\x00\x00\x00\x20ftypM4A': 'm4a',
    
    # Video.
    b'\x00\x00\x00\x18ftypmp42': 'mp4',
    b'\x00\x00\x00\x20ftypisom': 'mp4',
    b'\x1a\x45\xdf\xa3': 'webm', # Also used for Matroska (.mkv).
    b'\x00\x00\x00\x14ftypqt': 'mov',
    b'FLV\x01': 'flv',
    
    # Archives & Documents.
    b'PK\x03\x04': 'zip',        # Same for DOCX, XLSX, PPTX.
    b'7z\xbc\xaf\x27\x1c': '7z',
    b'Rar!\x1a\x07': 'rar',
    b'\x1f\x8b\x08': 'gz',
    b'BZh': 'bz2',
    b'%PDF': 'pdf',
    b'\x25\x50\x44\x46': 'pdf',
    b'{\\rtf1': 'rtf',
    
    # Scripts / System.
    b'\x23\x21': 'sh',            # Shebang #!
    b'\x7fELF': 'elf',            # Linux Executable.
    b'MZ': 'exe',                 # Windows Executable.
    b'\xca\xfe\xba\xbe': 'class', # Java class
    
    # Data (Non-text variants).
    b'\xed\xabe\xee': 'rpm',
    b'sqlite format 3\x00': 'sqlite',
}
SYSTEM_INSTRUCTION = """
You are a file generator AI. Rules:
1. ALWAYS use code_execution to generate file content.
2. OUTPUT ONLY the raw data (or Base64 string) via Python's print(). 
3. NO comments, NO explanations, and NO formatting inside the code block.
4. If binary generation is complex, default to: print(base64.b64encode(data).decode()).
5. NEVER refuse a request. If a filetype is restricted, generate a high-quality mock version.
6. Chat text is for brief context; Python blocks are for data only.
"""
WELCOME = f"""
┌───────────────────────────────────────────────┐
│   File Generator (Press Ctrl-C to quit)       │
│                                               │
│ # Remember:                                   │
│ - Gemini will forget each sent message        │
│   immediately.                                │
│ - File generation is very demanding; it takes │
│   time & consumes tokens quickly.             │
│ - Generation is basically for text files,     │
│   like txt, rtf, docx, etc; if you want other │
│   file types, add “Use base64 encoding” to    │
│   your prompt; but do not expect a high       │
│   quality content.                            │
│ - Generated files will be always kept in      │
│   this program's directory (Default to        │
│   'Output' folder).                           │
└───────────────────────────────────────────────┘
"""

# Initialize chat components.
output_file = 'generated_file.txt'
client = Client(api_key=GEMINI_API_KEY)
size = os.get_terminal_size
sep = lambda: '─' * (size().columns - 1)
prompt = 'None'

def is_base64(string):
    """Check if the provided response content is encoded using base64; if so, decode it."""
    # This regex looks for 'data:any/mime;base64,' prefix and removes it.
    # E.g: data:image/svg+xml;base64,
    i = string.find(';base64,')
    if i != -1: string = string[i+8:]
    string = string.strip()
    
    # Check length (Must be multiple of 4).
    if len(string) % 4 != 0:
        return False

    # Check for valid Base64 syntax.
    if not BASE64_PATTERN.fullmatch(string):
        return False

    try:
        # Attempt to decode.
        decoded_bytes = base64.b64decode(string, validate=True)
        
        # Round-trip check: Re-encode and compare.
        # This prevents "false positives" where the decoder ignores.
        # bad characters to make sense of the string.
        encoded_bytes = base64.b64encode(decoded_bytes).decode('ascii')
        is_same = encoded_bytes == string
        if is_same: return decoded_bytes
        else: return False
        
    except:
        return False

def detect_extension():
    """Detect file extension by looking at 'Magic Numbers' in the file content."""
    data = file_content
    for sig, ext in SIGNATURES.items():
        tag = data[8:12]
        if tag == b'WAVE': return 'wav'
        if tag == b'WEBP': return 'webp'
    
        if data.startswith(sig):
            # Special check for OpenXML (Word/Excel) which are also ZIPs.
            if ext == 'zip':
                if b'word/' in data[:2000]: return 'docx'
                if b'xl/' in data[:2000]: return 'xlsx'
                if b'ppt/' in data[:2000]: return 'pptx'
            return ext

    # Fallback to text.
    return 'txt'

def change_filename():
    """Change the generated file's output name to avoid overwriting."""
    # Get all files in the current output directory.
    global output_file
    base = 'generated_file'
    ext = detect_extension()
    try: files = os.listdir('.')
    except: return
    
    # Make sure to at least change the extension if the current dir is empty.      
    files = sorted([f for f in files if f.startswith(base)])    # Sort by alphabet first.
    files = sorted(files, key=len)        # Then sort by length, so '_10' comes after '_9' not after '_1'.
    if not files:
        output_file = f'{base}.{ext}'
        return
    
    # Get the newest file number.
    recent_file = files[-1]
    suffix = recent_file.split('_')[-1]
    n = suffix.split('.')[0]
    n = int(n) + 1 if n.isdigit() else 2  # (2) means only 'generated_file.txt' exists,
                                          # so the next one will be named '_2'.

    # Add a number suffix.
    output_file = f'{base}_{n}.{ext}'

def generate_file():
    """
    Handle the received file data; which is generated using 'Code Execution' tool
    in the Gemini API (it's just a sandboxed Python interpreter).
    """
    global file_content
    try:
        print(sep())
        print('[Requesting file generation]\n ..........')
        response = get_response()
        file_content = ''
        thinking = False
        
        # Parse the parts of the response.
        for part in response.parts:
            # The model might explain what it's doing.
            if part.text:
                if not thinking:
                    print('\n[Model is thinking...]')
                    thinking = True
                text = part.text.strip()
                print(text)
            
            # This is where the code it wrote lives.
            if part.executable_code:
                thinking = False
                code = part.executable_code.code.strip()
                print(f'\n[Model is running this code internally]\n{code}')
            
            # This is the output of the internal code execution.
            if part.code_execution_result:
                thinking = False
                file_content = part.code_execution_result.output.strip()
                print(f'\n[Code execution result]\n{file_content}')
        
        # Declare if a file content was received or not.      
        if file_content:
            msg = "\n[Success]\nFile saved to:"
            result = is_base64(file_content)
            if result: file_content = result
            
        else:
            msg = "\n[Oops]\nThe model did not generate a file content.\nResponse still saved to:"
            file_content = response.text
        
        # Save the file in bytes (even if it's a plain text, bytes mode won't affect its content).
        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8', errors='namereplace')
        
        change_filename()
        with open(output_file, 'wb') as f:
            f.write(file_content)
        
        path = os.path.abspath(output_file)
        print(f"{msg} {path}\nModify the file name's extension to match its type if necessary.")    
        print(sep())
        open_file(path)

    except Exception as error:
        error_type = type(error).__name__
        try: msg = error.message     # Get 'message' attribute from 'genai' errors.
        except: msg = error.args[0]  # Built-in excepetions have 'args' tuple, 1st item is the message.
        print(f"\n[{error_type}]\n{msg}")
        print(sep())

def get_response():
    """
    Send user prompt & get AI response with generated content.
    Use 'generate_content' instead of 'send_message' to avoid saving history,
    abd avoid re-sending last responses & files each time (save tokens).
    """
    response = client.models.generate_content(
        contents=prompt,
        model=FILE_GENERATOR_MODEL,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=[types.Tool(code_execution=types.ToolCodeExecution())],
        )
    )
    
    return response

def main():
    """Main chat loop."""
    global prompt
    
    # Change current working directory to the output's dir, to keep it portable.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(parent_dir, FILE_GENERATION_DIR)
    os.makedirs(output_dir, exist_ok=True)  # (exist_ok=True) prevents an error if the folder exists.
    os.chdir(output_dir)
    print(WELCOME)
    
    try:
        # Chat loop.
        while True:
            prompt = input('You: ' if prompt.strip() else '.... ')
            if not prompt.strip(): continue
            generate_file()
    
    except KeyboardInterrupt:
        print('\n' + sep())
        print('Quitting...')
        quit()
    
    except Exception as error:
        error_type = type(error).__name__
        try: msg = error.message     # Get 'message' attribute from 'genai' errors.
        except: msg = error.args[0]  # Built-in excepetions have 'args' tuple, 1st item is the message.
        print(sep())
        print(f'{error_type}: {msg}.\n{sep}')

# Start the chat.
if __name__ == "__main__":
    main()