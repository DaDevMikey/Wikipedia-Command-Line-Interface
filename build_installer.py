import os
import subprocess
import shutil
import sys

def build_exe():
    print("Building executable with PyInstaller...")
    subprocess.run([
        'pyinstaller',
        '--name=wiki',
        '--onedir',
        '--clean',
        '--add-data=README.md;.',
        '--add-data=LICENSE;.',
        'wiki_cli/cli.py'
    ], check=True)

def build_installer():
    print("Building installer with Inno Setup...")
    # Assuming Inno Setup is installed in the default location
    inno_compiler = r'"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"'
    subprocess.run(f'{inno_compiler} install_script.iss', check=True)

def main():
    # Clean previous builds
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

    try:
        build_exe()
        build_installer()
        print("Installation package created successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 