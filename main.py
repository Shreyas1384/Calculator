#!/usr/bin/env python3
"""
Entry point for the Modern Python Calculator.
Run this file to start the calculator server and automatically open the UI.
Usage:
    python main.py
    python main.py --port 5050
    python main.py --no-browser
"""

import sys
from app import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Calculator closed. Goodbye!")
        sys.exit(0)
