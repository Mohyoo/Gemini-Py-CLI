# A simple image generation chat; less featured & fragile, but it does the job.

import os
import sys
from google.genai import Client, types
from webbrowser import open as open_file
from resvg_py import svg_to_bytes
from tkinter import Tk, Label
from tksvg import SvgImage

# Add the parent directory to the path.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import GEMINI_API_KEY, FILE_GENERATOR_MODEL, FILE_GENERATION_DIR

# Define constants.
SYSTEM_INSTRUCTION = """
You are an image generator AI. Rules:
1. If the user doesn't ask for something related to images, skip these rules.
2. ALWAYS use code_execution to generate SVG images - if the user asks for images. 
3. OUTPUT ONLY the SVG's XML code via Python's print(). 
4. NO comments, NO explanations, and NO formatting inside the code block.
5. NEVER refuse a request. Always return an SVG image markup code in the python execution output.
"""
WELCOME = f"""
┌───────────────────────────────────────────────────────────────────┐
│               Image Generator (Press Ctrl-C to quit)              │
│                                                                   │
│ # Remember:                                                       │
│ - Gemini will forget each sent message immediately.               │
│ - Image generation is very demanding; it takes time & consumes    │
│   tokens quickly; and the results aren't realistic; but good for  │
│   general art, like desktop wallapers, or icons.                  │
│ - Generated images will be always kept in this program's          │
│   directory (Default to 'Output' folder).                         │
│ - Result is always an SVG-PNG images pair.                        │
│ * SVG (Scalable Vector Graphics): infinite scaling & quality, but │
│   limited app support.                                            │
│ * PNG (Portable Network Graphics): portable, & high-quality; for  │
│   everyday use.                                                   │
└───────────────────────────────────────────────────────────────────┘
"""
PNG_WIDTH = 2048

# Initialize chat components.
client = Client(api_key=GEMINI_API_KEY)
output_file = 'generated_image.svg'
size = os.get_terminal_size
sep = lambda: '─' * (size().columns - 1)
prompt = 'None'

def convert_svg_to_png(svg_code, output_path):
    """Convert the generated SVG image to PNG for portability & conveniance."""
    # Convert to PNG bytes.
    png_bytes = svg_to_bytes(svg_string=svg_code, width=PNG_WIDTH)

    # Save the bytes to a file.
    if png_bytes:
        with open(output_path, "wb") as f:
            f.write(png_bytes)
        
        return True

def show_svg(path):
    """Show the generated SVG image in a simple Tkinter window."""
    root = Tk()
    root.title("SVG Viewer")
    root.configure(bg="black")

    # Create the SVG image object.
    # Because of 'tksvg.SvgImage', this works just like 'tk.PhotoImage'.
    svg_image = SvgImage(master=root, file=path)

    # Put it in a Label.
    text = 'This is just a low quality preview; SVG images have limitless quality.\n'
    text += 'Use a web browser or any specialized image viewer to see the full details.\n'
    text += 'Close this window to see the standard PNG version of this image.'
    note = Label(root, text=text, fg="white", bg="black", font=("calibri", 14))
    note.pack(pady=(10, 0))
    image = Label(root, image=svg_image)
    image.image = svg_image   # Keep a reference so Python doesn't delete it.
    image.pack(padx=5, pady=5)

    root.mainloop()

def change_filename():
    """Change the generated file's output name to avoid overwriting."""
    # Get all files in the current output directory.
    global svg_file
    base = 'generated_image'
    try: files = os.listdir('.')
    except: return
    
    # Make sure to at least change the extension if the current dir is empty.
    files = sorted([f for f in files if f.startswith(base)])    # Sort by alphabet first.
    files = sorted(files, key=len)        # Then sort by length, so '_10' comes after '_9' not after '_1'.
    if not files:
        svg_file = f'{base}.svg'
        return
    
    # Get the newest file number.
    recent_file = files[-1]
    suffix = recent_file.split('_')[-1]
    n = suffix.split('.')[0]
    n = int(n) + 1 if n.isdigit() else 2  # (2) means only 'generated_image.svg' exists,
                                          # so the next one will be named '_2'.

    # Add a number suffix.
    svg_file = f'{base}_{n}.svg'

def generate_image():
    """
    Handle the received SVG data; which is generated using 'Code Execution'
    tool in the Gemini API (it's just a sandboxed Python interpreter).
    """
    global output_file, file_content
    try:
        print(sep())
        print('[Requesting image generation]\n ..........')
        response = get_response()
        file_content = ''
        
        # Take the last part of the code execution because it is the most completed.
        for part in reversed(response.parts):
            if part.code_execution_result:
                file_content = part.code_execution_result.output.strip()
                break
        
        # Declare if a file content was received or not, and it's an SVG.
        change_filename()
        svg_content = file_content.lower()
        if file_content and (svg_content.startswith('<svg') or '<svg' in svg_content[:100]) and svg_content.endswith('</svg>'):
            # Save SVG image as text (it's already text-based).
            with open(svg_file, 'w') as f:
                f.write(file_content)
            
            svg_path = os.path.abspath(svg_file)
            print(f'\n[Success]\nSVG image saved to:\n{svg_path}')    
            show_svg(svg_file)
                        
            # Save the PNG image as bytes.
            png_file = svg_file.replace('.svg', '.png')
            png_path = svg_path.replace(svg_file, png_file)
            print('\nGenerating a PNG version...')
            if convert_svg_to_png(file_content, png_file):
                print(f'PNG image saved to:\n{png_path}')
                open_file(png_file)
            else:
                print("Oops! Couldn't create a PNG version.")
            
        else:
            # Fallback if no code was executed, or executed but no image output.
            output_file = svg_file.replace('.svg', '.txt')
            content = response.text
            if file_content: content += '\n' + file_content
            with open(output_file, 'w') as f:
                f.write(content)
                
            path = os.path.abspath(output_file)
            print(f"\n[Oops]\nThe model did not generate any image.\nResponse still saved to: {path}")
            open_file(output_file)
            
        print(sep())

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
            generate_image()
    
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