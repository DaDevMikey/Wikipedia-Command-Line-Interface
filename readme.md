# Wiki-CLI

A command-line interface for Wikipedia that allows you to search, read articles, and view ASCII art versions of images directly in your terminal.

[![Github All Releases](https://img.shields.io/github/downloads/DaDevMikey/Wikipedia-Command-Line-Interface/total.svg)]()

## Features

- Search Wikipedia articles
- Read full articles in the terminal
- View article images as ASCII art
- Browse external links
- Command history
- Tab completion for commands

## Installation

**As of February 9, 2025,** you can install Wiki-CLI on Windows using the attached installer available in the [latest release](https://github.com/DaDevMikey/Wikipedia-Command-Line-Interface/releases/latest).  We are actively working on improving the installation experience.

**Windows Installation (using the installer):**

1. Download the installer from the [latest release](https://github.com/DaDevMikey/Wikipedia-Command-Line-Interface/releases/latest) page.
2. Run the installer.

**Known Issue (Windows Installer):**

The installer may incorrectly report that Python is not installed even if it is present on your system. This is a known issue that we are actively working to resolve in future releases.  In the meantime, if you encounter this issue, please ensure you have a compatible version of Python installed (3.7+) and consider using the manual installation method described below. If the error message (python is not installed) does appear on your machine, press no to continue with the instalation anyways.

1. Clone the repository:
```bash
git clone https://github.com/DaDevMikey/Wikipedia-Command-Line-Interface.git
cd wiki-cli
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

3. Install the package:
```bash
pip install -e .
```

## Global Installation

To use the `wiki` command from anywhere on your system:

### Windows
1. Add the Python Scripts directory to your PATH:
   - Open System Properties (Win + Pause/Break)
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System Variables", find and select "Path"
   - Click "Edit"
   - Click "New"
   - Add the Python Scripts path (typically `C:\Users\<username>\AppData\Local\Programs\Python\Python3x\Scripts`)
   - Click "OK" on all windows

2. Open a new command prompt (cmd.exe) and verify the installation:
```bash
wiki --help
```

### Linux/macOS
The command should be automatically available after installation. If not:
```bash
which wiki  # Verify installation path
wiki --help
```

## Usage

```bash
wiki
```

### Available Commands

- `search <query>`: Search Wikipedia articles
- `view <title>`: View a specific article
- `<number>`: View article from search results
- `images`: List images in current article
- `image <number>`: View ASCII art of an image
- `links`: Show external links for current article
- `clear`: Clear the screen
- `help`: Show help message
- `exit`: Exit the application

### Examples

```bash
# Search for an article
wiki> search Python programming

# View a specific article
wiki> view Python (programming language)

# List images in current article
wiki> images

# View an image as ASCII art
wiki> image 1

# Show external links
wiki> links

# Get help
wiki> help
```

## Requirements

- Python 3.7+
- Required packages (automatically installed):
  - requests
  - aiohttp
  - pillow
  - rich
  - prompt_toolkit
  - click
  - python-dotenv

## License

MIT

## Contributing




To use the command globally on your device:

1. **For Windows users:**
   - After installation, the `wiki` command should be available in your Python Scripts directory
   - To make it available everywhere, you need to ensure your Python Scripts directory is in your system PATH
   - The Python Scripts directory is typically located at:
     - `C:\Users\<username>\AppData\Local\Programs\Python\Python3x\Scripts` (for system Python)
     - `C:\Users\<username>\Downloads\Wikipedia Command Line Interface\.venv\Scripts` (if using virtual environment)

2. **To add to PATH in Windows:**
   ```bash
   # First, find your Python Scripts directory
   where python
   ```
   Then:
   1. Open System Properties (Win + Pause/Break)
   2. Click "Advanced system settings"
   3. Click "Environment Variables"
   4. Under "System Variables", find and select "Path"
   5. Click "Edit"
   6. Click "New"
   7. Add the full path to your Python Scripts directory
   8. Click "OK" on all windows
   9. Open a new command prompt for changes to take effect

3. **To verify installation:**
   ```bash
   # Open a new command prompt and type:
   wiki --help
   ```

If you want to use the command without activating the virtual environment each time, you should install the package globally using:
```bash
pip install .
```
Instead of:
```bash
pip install -e .
```

Remember that global installation might require administrator privileges on Windows (run command prompt as administrator).
