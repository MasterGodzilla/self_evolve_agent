#!/usr/bin/env python3
"""
Intermediate runner for main.py that handles subprocess communication.

This script:
1. Imports and calls main.py's main() function
2. Receives the evolution code as a return value
3. Writes it to a file for evolve.py to read
"""

import sys
import os

# Import main from main.py
from main import main

EVOLUTION_FILE = ".evolution_proposal.py"

def run():
    """Run main.py and handle evolution proposal"""
    try:
        # Call main() - it should return the evolution code or None
        new_code = main()
        
        # If evolution code was returned, write it to file
        if new_code:
            with open(EVOLUTION_FILE, 'w') as f:
                f.write(new_code)
            print(f"\n[Evolution proposal saved to {EVOLUTION_FILE}]")
        
        return 0
        
    except Exception as e:
        print(f"Error in run_main.py: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(run()) 