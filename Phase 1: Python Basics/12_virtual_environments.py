"""
Virtual Environments in Python.

This file demonstrates the concept of virtual environments
and shows how to create and manage them programmatically.
"""
import subprocess
import sys
import venv
import os
import shutil


def explain_venv():
    """Explain what virtual environments are."""
    print("=== Virtual Environments ===")
    print("""
Virtual environments isolate Python dependencies per project.
    
Commands:
  python -m venv .venv        Create a virtual environment
  source .venv/bin/activate   Activate (Unix/macOS)
  .venv\\Scripts\\activate      Activate (Windows)
  pip install <package>        Install packages
  pip freeze > requirements.txt  Export dependencies
  pip install -r requirements.txt  Install dependencies
  deactivate                  Deactivate the environment
""")


def list_installed_packages():
    """List all installed packages using pip."""
    print("=== Installed Packages ===")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "list", "--format=columns"],
        capture_output=True, text=True
    )
    print(result.stdout)


def check_python_info():
    """Display Python environment info."""
    print("=== Python Environment Info ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    print(f"Path: {sys.path[:3]}")


def main():
    explain_venv()
    check_python_info()
    list_installed_packages()


if __name__ == "__main__":
    main()
