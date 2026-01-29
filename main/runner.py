"""Runner for Jarvis.

This file is import-safe so you can run it either as a module:

  python -m main.runner

or directly (when working directory is the project root):

  python main\runner.py

When executed directly Python sets sys.path[0] to the script folder (main/),
which prevents the package `main` being importable. We detect that case and
prepend the project root to sys.path so imports work.
"""


import sys
from pathlib import Path

# If the script is executed directly, ensure project root is on sys.path so
# `import main.*` works.
if __package__ is None:
    project_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(project_root))

from main.main_text import main_text
from main.main_voice import main


def run():
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    print("\n" + "=" * 60)
    print("JARVIS - PERSONAL AI ASSISTANT")
    print("=" * 60)
    print("Choose input mode:")
    print("  1. Voice Input (microphone)")
    print("  2. Text Input (keyboard)")
    print("=" * 60)
    choice = input("\nEnter choice (1 or 2, default=1): ").strip()
    if choice == "2":
        main_text()
    else:
        main()


if __name__ == "__main__":
    run()
