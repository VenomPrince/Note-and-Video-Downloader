import os
import sys
import subprocess

def install_dependencies():
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except Exception as e:
        print(f"Warning: Could not install dependencies: {e}")

def build_windows_exe():
    print("Building Windows Executable...")
    try:
        subprocess.check_call([
            'pyinstaller', 
            '--onefile', 
            '--windowed', 
            '--name', 'DevCompanion', 
            '--add-data', 'cli_app.py;.', 
            '--hidden-import', 'tkinter', 
            '--hidden-import', 'yt_dlp',
            'cli_app.py'
        ])
        print("Windows executable created successfully!")
        print(f"Executable location: {os.path.join(os.getcwd(), 'dist', 'DevCompanion.exe')}")
    except Exception as e:
        print(f"Error building Windows executable: {e}")

def build_mac_app():
    print("Building Mac Application...")
    try:
        # Create py2app setup script
        with open('setup_mac.py', 'w') as f:
            f.write('''
from setuptools import setup

APP = ['cli_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'yt_dlp'],
    'plist': {
        'CFBundleName': 'DevCompanion',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': 'True'
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
''')
        
        # Run py2app
        subprocess.check_call([
            sys.executable, 
            'setup_mac.py', 
            'py2app', 
            '-A'  # semi-standalone mode
        ])
        print("Mac application created successfully!")
    except Exception as e:
        print(f"Error building Mac application: {e}")

def main():
    # Detect platform and build accordingly
    install_dependencies()
    
    if sys.platform == 'win32':
        build_windows_exe()
    elif sys.platform == 'darwin':
        build_mac_app()
    else:
        print("Unsupported platform. Only Windows and Mac are supported.")

if __name__ == '__main__':
    main()
