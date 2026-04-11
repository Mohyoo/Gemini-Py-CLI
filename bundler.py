# Before running this script, make sure you remove yoru API key from settings.
# This script is supposed to remove the API key but only if one API_KEY variable exists.

import os
import shutil
import platform
from time import sleep
from pathlib import Path
from settings import MODES_DIR, PROGRAM_DATA_DIR, WORDLIST_FILE
from settings_editor import read_file_lines, restore_default

# A quick reminder.
print("(!) First, make sure to run this script in an elevated terminal (admin\n    or root privileges). This is required for symlinks creation in Windows.")
print("(!) Settings will be reset to default before bundling, but they will\n    be restored after.")
print("(!) Existing bundles - if any - will be skipped and won't be updated.\n    Delete them from the 'dist' folder to re-bundle them.")
print("(!) The final bundled folder will be overwritten if it already exists!")
print('    Proceeding in 3 seconds...')
sleep(3)

# Define constants.
SETTINGS_BACKUP = 'settings_bundling_backup.py'
MODE_FILES = [
    'momentary_chat.py',
    'temporary_chat.py',
    'image_generator.py',
    'file_generator.py',
    'google_searcher.py',
]
FINAL_DIR = 'FINAL_GEMINI'
MISSING_LIBS_DIR = 'missing_libs'
SOURCE_ELEMENTS = [
    'gemini.py',
    'error_logger.py',
    'global_logger.py',
    'settings.py',
    'useless.py',
    WORDLIST_FILE,
    MODES_DIR,
    PROGRAM_DATA_DIR,
]

# Change current working directory to the script's dir, to keep it portable.
print('\nChanging current working directory to here...')
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
    
# Backup current settings first, then factory-reset them.
if not os.path.exists(SETTINGS_BACKUP):
    print("Backing up 'settings.py'...")
    shutil.copy2('settings.py', SETTINGS_BACKUP)
    file_lines = read_file_lines()
    restore_default(external_invoke=True, external_lines=file_lines)

# Call PyInstaller to bundle each PY file individually.
print("Starting PyInstaller packaging & Skipping existing packages...\n")
os.rename('settings.py', 'settings.py.temporarily.hidden')
if not os.path.exists(os.path.join('dist', 'gemini')):
    os.system(f'python -m PyInstaller --onedir --contents-directory . --icon "{PROGRAM_DATA_DIR}/Gemini Icon.ico" gemini.py')
    os.remove('gemini.spec')
if not os.path.exists(os.path.join('dist', 'settings_editor')):
    os.system(f'python -m PyInstaller --onedir --contents-directory . --icon "{PROGRAM_DATA_DIR}/Settings Icon.ico" settings_editor.py')
    os.remove('settings_editor.spec')

os.chdir(MODES_DIR)
for file in MODE_FILES:
    if not os.path.exists(os.path.join('dist', file.removesuffix('.py'))):
        os.system(f'python -m PyInstaller --onedir --contents-directory . --icon "../{PROGRAM_DATA_DIR}/Gemini Icon.ico" "{file}"')
        os.remove(file.removesuffix('.py') + '.spec')
os.chdir('..')
os.rename('settings.py.temporarily.hidden', 'settings.py')

# Copy & Merge the bundled programs.
print('\nMerging packages...')
if os.path.exists(FINAL_DIR):
    for _ in range(20):
        try:
            shutil.rmtree(FINAL_DIR)
            break
        except:
            sleep(1)
            continue

while os.path.exists(FINAL_DIR):
    input(f"\n[!] Couldn't delete '{FINAL_DIR}' folder.\n    Please delete manually it then press ENTER to continue...")

for folder in ('gemini', 'settings_editor'):
    for _ in range(20):
        try:
            shutil.copytree(os.path.join('dist', folder), FINAL_DIR, dirs_exist_ok=True)
            break
        except:
            sleep(1)
            continue

os.chdir(MODES_DIR)
for file in MODE_FILES:
    program = file.removesuffix('.py')
    shutil.copytree(os.path.join('dist', program), os.path.join('..', FINAL_DIR, MODES_DIR), dirs_exist_ok=True)
os.chdir('..')

# Add missing elements from source.
print('Adding missing elements from source...')
for item in SOURCE_ELEMENTS:
    if os.path.isdir(item):
        shutil.copytree(item, os.path.join(FINAL_DIR, item), dirs_exist_ok=True)
    else:
        new_location = os.path.join(FINAL_DIR, item)
        new_folder = Path(new_location).parent
        if not os.path.exists(new_folder): os.mkdir(new_folder)
        shutil.copy2(item, new_location)

# Adding libraries that were not auto detected by PyInstaller.
if os.path.exists(MISSING_LIBS_DIR) and os.listdir(MISSING_LIBS_DIR):
    print("Adding missing libraries that PyInstaller didn't detect...")
    for item in os.listdir(MISSING_LIBS_DIR):
        relative_path = os.path.join(MISSING_LIBS_DIR, item)
        if os.path.isdir(relative_path):
            new_folder = os.path.join(FINAL_DIR, MODES_DIR, item)
            shutil.copytree(relative_path, new_folder, dirs_exist_ok=True)
        else:
            new_file = os.path.join(FINAL_DIR, MODES_DIR, item)
            shutil.copy2(relative_path, new_file)

# Merge main & modes directory to save space, then create symlinks so that the modes executables find their data.
print("\nAlmost done, do you want to create symlinks to shared libraries?")
os.chdir(FINAL_DIR)
save_space = input("This will save space, but the program's dir should never be moved (y/n): ").strip().lower()

if save_space == 'y':
    os.chdir(MODES_DIR)
    system = platform.system()
    if system == 'Windows':
        current_items = [item for item in os.listdir() if not item.endswith(('.exe', '.py'))]
    else:
        current_items = []
        for item in os.listdir():
            if item.endswith('.py'):
                continue
            if os.path.isfile(item) and os.access(item, os.X_OK):
                continue
            current_items.append(item)

    try:
        for item in current_items:
            symlink_location = Path(item)         # Where the symlink lives.
            target_location = Path('..') / item   # To where the symlink points.
            shutil.move(item, target_location)
            symlink_location.symlink_to(target_location, target_is_directory=target_location.is_dir())
    except Exception as error:
        print(f"\n[!] Error: {error}")
        print("You probably need to run this script from an elevated terminal.")
        print("Relaunch the terminal as root/admin and re-run this script.\nBundling won't be repeated so it'll be fast.")
        quit()
    os.chdir('..')
    
# Clean up non-needed files.
print("Cleaning up...")
for path in ('dist', 'build', os.path.join(MODES_DIR, 'dist'), os.path.join(MODES_DIR, 'build')):
    try: shutil.rmtree(path)
    except: pass
    
# Hide verbose itnernal program files.
print("\nDo you want to hide the program's internal files & folders?")
hide = input("So that its directory will look clean and easy to modify (y/n): ").strip().lower()

if hide == 'y':
    system = platform.system()
    if system == 'Windows':
        import ctypes
        FILE_ATTRIBUTE_HIDDEN = 0x02
        current_items = [item for item in os.listdir() if not item.endswith(('.exe', '.py', MODES_DIR, PROGRAM_DATA_DIR, 'Secret'))]
        for item in current_items:
            ctypes.windll.kernel32.SetFileAttributesW(item, FILE_ATTRIBUTE_HIDDEN)
        os.chdir(MODES_DIR)
        current_items = [item for item in os.listdir() if not item.endswith(('.exe', '.py'))]
        for item in current_items:
            ctypes.windll.kernel32.SetFileAttributesW(item, FILE_ATTRIBUTE_HIDDEN)
            
        # Create helper batch files.
        root_items = [item for item in os.listdir('..') if not item.endswith(('.exe', '.py', MODES_DIR, PROGRAM_DATA_DIR, 'Secret'))]
        modes_items = [item for item in os.listdir() if not item.endswith(('.exe', '.py'))]

        # 2. Create the HIDE batch string.
        hide_bat_content = "@echo off\n"
        hide_bat_content += f'echo Hiding...\n'
        for item in root_items:
            hide_bat_content += f'attrib +h "{item}"\n'
        hide_bat_content += f'pushd "{MODES_DIR}"\n'
        for item in modes_items:
            hide_bat_content += f'attrib +h /l "{item}"\n'
        hide_bat_content += "popd\n"

        # 3. Create the UNHIDE batch string.
        unhide_bat_content = "@echo off\n"
        unhide_bat_content += f'echo Revealing...\n'
        for item in root_items:
            unhide_bat_content += f'attrib -h "{item}"\n'
        unhide_bat_content += f'pushd "{MODES_DIR}"\n'
        for item in modes_items:
            unhide_bat_content += f'attrib -h /l "{item}"\n'
        unhide_bat_content += "popd\n"
        
        # 4. Save batch scripts.
        with open(os.path.join('..', 'Hide Internal Files.bat'), 'w', encoding='utf-8') as f:
            f.write(hide_bat_content)
        with open(os.path.join('..', 'Reveal Internal Files.bat'), 'w', encoding='utf-8') as f:
            f.write(unhide_bat_content)
            
    elif system == 'Darwin':
        import subprocess
        current_items = [item for item in os.listdir() if (not item.endswith(('.py', MODES_DIR, PROGRAM_DATA_DIR, 'Secret')) or (not os.path.isfile(item) and os.access(item, os.X_OK)))]
        for item in current_items:
            subprocess.run(['chflags', 'hidden', item], check=False)
        os.chdir(MODES_DIR)
        current_items = [item for item in os.listdir() if (not item.endswith('.py') or (not os.path.isfile(item) and os.access(item, os.X_OK)))]
        for item in current_items:
            subprocess.run(['chflags', 'hidden', item], check=False)

    else:     # Linux
        current_items = [item for item in os.listdir() if (not item.endswith(('.py', MODES_DIR, PROGRAM_DATA_DIR, 'Secret')) or (not os.path.isfile(item) and os.access(item, os.X_OK)))]
        with open('.hidden', 'w', encoding='utf-8') as f:
            f.write('\n'.join(current_items) + '\n')
        os.chdir(MODES_DIR)
        current_items = [item for item in os.listdir() if (not item.endswith('.py') or (not os.path.isfile(item) and os.access(item, os.X_OK)))]
        with open('.hidden', 'w', encoding='utf-8') as f:
            f.write('\n'.join(current_items) + '\n')
    
    os.chdir('..')

# Final touches.
os.chdir('..')
print("Adding final touches...")
for folder in ('Licenses', 'Wiki', 'Secret'):
    if os.path.exists(folder):
        shutil.copytree(folder, os.path.join(FINAL_DIR, folder), dirs_exist_ok=True)

# Restore settings file to its pre-bundling state.
try: shutil.move(SETTINGS_BACKUP, 'settings.py')
except Exception as error: print(f'[!] Error: {error}')
print(f"\nRestored 'settings.py' & Finished bundling.\nCheck the '{FINAL_DIR}' folder.")