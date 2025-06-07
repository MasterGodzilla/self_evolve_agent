"""
# Note to LLMs editing this file:
#
# When making changes here, you should also update evolve_reference.py.
# The evolve_reference.py file serves as a context reference for the AI and should closely mirror this file,
# except it must NOT include any safety checks.
# Keep both files as similar as possible, differing only where safety logic is present in this file.
#
# Architecture:
# - evolve.py (this file) manages the evolution loop
# - run_main.py is an intermediate script that imports and calls main.py
# - main.py should have a main() function that returns evolution code or None
# - Communication happens via file: .evolution_proposal.py
"""

import os
import shutil
import subprocess
import sys
import argparse
import difflib
from datetime import datetime
from api import chat_complete
from safety import judge_safety

# ANSI color codes for terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'

def read_main_file():
    """Read the main.py file's content"""
    with open('main.py', 'r') as f:
        return f.read()

def create_checkpoint():
    """Create a timestamped backup of main.py"""
    # Create checkpoints directory if it doesn't exist
    checkpoint_dir = "checkpoints"
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_name = os.path.join(checkpoint_dir, f"main_{timestamp}.py")
    shutil.copy2('main.py', checkpoint_name)
    print(f"{GREEN}✓ Checkpoint created:{RESET} {CYAN}{checkpoint_name}{RESET}")
    return checkpoint_name

def apply_edit(new_code):
    """Replace the entire main.py with new code"""
    # Write the new code to main.py
    with open('main.py', 'w') as f:
        f.write(new_code)
    
    print(f"{GREEN}✓ Successfully applied edit to main.py!{RESET}")
    return True

def display_diff(old_code, new_code):
    """Display a colored diff between old and new code"""
    print(f"\n{BOLD}{CYAN}=== Code Changes ==={RESET}")
    
    old_lines = old_code.splitlines(keepends=True)
    new_lines = new_code.splitlines(keepends=True)
    
    diff = difflib.unified_diff(old_lines, new_lines, fromfile='main.py (before)', tofile='main.py (after)', lineterm='')
    
    for line in diff:
        if line.startswith('+++') or line.startswith('---'):
            print(f"{CYAN}{line}{RESET}", end='')
        elif line.startswith('+'):
            print(f"{GREEN}{line}{RESET}", end='')
        elif line.startswith('-'):
            print(f"{RED}{line}{RESET}", end='')
        elif line.startswith('@@'):
            print(f"{CYAN}{line}{RESET}", end='')
        else:
            print(line, end='')
    
    print(f"\n{BOLD}{CYAN}==================={RESET}\n")

def run_main(model_name="gemini-2.5-flash"):
    """Run main.py via intermediate script and check for evolution proposal
    
    Architecture:
    - evolve.py calls run_main.py as subprocess
    - run_main.py imports and calls main.main() 
    - main.main() returns evolution code (or None)
    - run_main.py writes evolution code to '.evolution_proposal.py'
    - evolve.py reads from that file
    
    This is cleaner because:
    - main.py just returns code, no special output handling needed
    - Clear separation of concerns
    - No stdout parsing or markers needed
    
    Returns:
        str or None: The proposed evolution code, or None if no evolution proposed
    """
    # Evolution proposal file
    EVOLUTION_FILE = ".evolution_proposal.py"
    
    # Clean up any previous evolution file
    if os.path.exists(EVOLUTION_FILE):
        os.remove(EVOLUTION_FILE)
    
    # Run main.py via intermediate script
    print(f"\n{BOLD}{BLUE}--- Running... ---{RESET}")
    try:
        # Pass model name as environment variable
        env = os.environ.copy()
        env['EVOLVE_MODEL'] = model_name
        
        result = subprocess.run(
            [sys.executable, 'run_main.py'],
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            timeout=300,
            env=env
        )
        
        # Since we're not capturing output, we need to check for the evolution file differently
        if os.path.exists(EVOLUTION_FILE):
            print(f"\n{BOLD}{MAGENTA}--- Evolving... ---{RESET}")
            print(f"{CYAN}AI response received.{RESET}")
            
            with open(EVOLUTION_FILE, 'r') as f:
                new_code = f.read().strip()
            
            # Clean up the evolution file
            os.remove(EVOLUTION_FILE)
            
            return new_code if new_code else None
        else:
            return None
        
    except subprocess.TimeoutExpired:
        print(f"{RED}⚠️  Execution timed out!{RESET}")
        return None
    except Exception as e:
        print(f"{RED}⚠️  Error running main.py: {e}{RESET}")
        return None

def run_evolution(model_name="gemini-2.5-flash"):
    """Main evolution loop"""
    print(f"{BOLD}{CYAN}=== Self-Evolving Agent v0.2 ==={RESET}")
    print(f"{YELLOW}Using model:{RESET} {GREEN}{model_name}{RESET}")
    print(f"{WHITE}This agent will run and evolve the main.py file.{RESET}")
    print(f"{WHITE}Checkpoints will be saved in the 'checkpoints' folder.{RESET}\n")
    
    # Show current main.py once at the beginning
    print(f"\n{BOLD}{BLUE}Current main.py:{RESET}")
    print(f"{CYAN}{'-' * 40}{RESET}")
    print(read_main_file())
    print(f"{CYAN}{'-' * 40}{RESET}")
    
    generation = 1
    
    while True:
        print(f"\n{BOLD}{MAGENTA}Generation {generation}{RESET}")
        
        # Wait for user input
        input(f"\n{YELLOW}Press Enter to run main.py (which will also evolve itself)...{RESET}")
        
        # Create checkpoint before running/evolving
        checkpoint = create_checkpoint()
        
        new_code = run_main(model_name)
        
        if new_code:
            # Get current code for diff
            current_code = read_main_file()
            
            # Display diff
            display_diff(current_code, new_code)
            
            # Perform safety check
            print(f"{BLUE}Performing safety check...{RESET}")
            verdict, safety_response = judge_safety(new_code)
            
            if verdict == "UNSAFE":
                print(f"\n{RED}⚠️  SAFETY WARNING: Code marked as UNSAFE!{RESET}")
                print(f"{RED}Safety review: {safety_response}{RESET}")
                print(f"\n{RED}This evolution will be skipped for safety reasons.{RESET}")
                generation += 1
                continue
            elif verdict == "CAUTION":
                print(f"\n{YELLOW}⚠️  CAUTION: Minor safety concerns detected{RESET}")
                print(f"{YELLOW}Safety review: {safety_response}{RESET}")
                print(f"\n{YELLOW}Proceed with caution.{RESET}")
            elif verdict == "SAFE":
                print(f"\n{GREEN}✓ Safety check passed{RESET}")
            else:  # ERROR case
                print(f"\n{YELLOW}⚠️  Could not perform safety check{RESET}")
                print(f"{YELLOW}Error: {safety_response}{RESET}")
            
            # Ask for confirmation
            print(f"\n{BOLD}{YELLOW}Apply this evolution? (y/n):{RESET} ", end='')
            confirm = input().strip().lower()
            
            if confirm == 'y':
                if apply_edit(new_code):
                    print(f"\n{GREEN}✓ Evolution complete! main.py has been updated.{RESET}")
                    print(f"{CYAN}Previous version saved as:{RESET} {checkpoint}")
                else:
                    print(f"{RED}⚠️  Failed to apply evolution.{RESET}")
            else:
                print(f"{YELLOW}Evolution skipped.{RESET}")
            
        
        generation += 1
        
        print(f"\n{BOLD}{YELLOW}Continue evolving? (y/n):{RESET} ", end='')
        if input().strip().lower() != 'y':
            break
    
    print(f"\n{BOLD}{GREEN}Evolution process complete.{RESET}")
    print(f"{CYAN}All checkpoints are saved in the 'checkpoints' folder.{RESET}")

def main():
    """Parse arguments and run evolution"""
    parser = argparse.ArgumentParser(
        description='Self-evolving Python code using LLMs',
        epilog='See README.md for detailed usage examples and available models.'
    )
    
    parser.add_argument(
        '--model', '-m',
        type=str,
        default='gemini-2.5-flash',
        help='Model to use for evolution (default: gemini-2.5-flash)'
    )
    
    parser.add_argument(
        '--restart', '-r',
        action='store_true',
        help='Reset main.py to main_zero.py (saves current main.py to checkpoint first)'
    )
    
    args = parser.parse_args()
    
    # Handle restart flag
    if args.restart:
        print(f"{BOLD}{YELLOW}=== Restarting from main_zero.py ==={RESET}")
        
        # Check if main_zero.py exists
        if not os.path.exists('main_zero.py'):
            print(f"{RED}⚠️  Error: main_zero.py not found!{RESET}")
            sys.exit(1)
        
        # Create checkpoint of current main.py
        checkpoint = create_checkpoint()
        
        # Copy main_zero.py to main.py
        shutil.copy2('main_zero.py', 'main.py')
        print(f"{GREEN}✓ Copied main_zero.py to main.py{RESET}")
        
        print(f"\n{GREEN}Restart complete!{RESET}")
        print(f"{CYAN}Previous main.py saved as:{RESET} {checkpoint}")
        print(f"{YELLOW}You can now run evolve.py normally to start evolution from main_zero.py{RESET}")
        return
    
    # Run evolution with specified model
    run_evolution(args.model)

if __name__ == "__main__":
    main() 