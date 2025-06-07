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
    print(f"Checkpoint created: {checkpoint_name}")
    return checkpoint_name

def apply_edit(new_code):
    """Replace the entire main.py with new code"""
    # Write the new code to main.py
    with open('main.py', 'w') as f:
        f.write(new_code)
    
    print("Successfully applied edit to main.py!")
    return True

def display_diff(old_code, new_code):
    """Display a colored diff between old and new code"""
    # ANSI color codes for terminal
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    
    print("\n=== Code Changes ===")
    
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
    
    print("\n===================\n")

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
    print("\n--- Running... ---")
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
            print("\n--- Evolving... ---")
            print("AI response received.")
            
            with open(EVOLUTION_FILE, 'r') as f:
                new_code = f.read().strip()
            
            # Clean up the evolution file
            os.remove(EVOLUTION_FILE)
            
            return new_code if new_code else None
        else:
            return None
        
    except subprocess.TimeoutExpired:
        print("Execution timed out!")
        return None
    except Exception as e:
        print(f"Error running main.py: {e}")
        return None

def run_evolution(model_name="gemini-2.5-flash"):
    """Main evolution loop"""
    print("=== Self-Evolving Agent v0.1 ===")
    print(f"Using model: {model_name}")
    print("This agent will run and evolve the main.py file.")
    print("Checkpoints will be saved in the 'checkpoints' folder.\n")
    
    # Show current main.py once at the beginning
    print("\nCurrent main.py:")
    print("-" * 40)
    print(read_main_file())
    print("-" * 40)
    
    generation = 1
    
    while True:
        print(f"\nGeneration {generation}")
        
        # Wait for user input
        input("\nPress Enter to run main.py (which will also evolve itself)...")
        
        # Create checkpoint before running/evolving
        checkpoint = create_checkpoint()
        
        new_code = run_main(model_name)
        
        if new_code:
            # Get current code for diff
            current_code = read_main_file()
            
            # Display diff
            display_diff(current_code, new_code)
            
            # Perform safety check
            print("Performing safety check...")
            verdict, safety_response = judge_safety(new_code)
            
            # ANSI color codes
            RED = '\033[91m'
            YELLOW = '\033[93m'
            GREEN = '\033[92m'
            RESET = '\033[0m'
            
            if verdict == "UNSAFE":
                print(f"\n{RED}⚠️  SAFETY WARNING: Code marked as UNSAFE!{RESET}")
                print(f"Safety review: {safety_response}")
                print(f"\n{RED}This evolution will be skipped for safety reasons.{RESET}")
                os.remove(checkpoint)  # Remove unnecessary checkpoint
                generation += 1
                continue
            elif verdict == "CAUTION":
                print(f"\n{YELLOW}⚠️  CAUTION: Minor safety concerns detected{RESET}")
                print(f"Safety review: {safety_response}")
                print(f"\n{YELLOW}Proceed with caution.{RESET}")
            elif verdict == "SAFE":
                print(f"\n{GREEN}✓ Safety check passed{RESET}")
            else:  # ERROR case
                print(f"\n{YELLOW}⚠️  Could not perform safety check{RESET}")
                print(f"Error: {safety_response}")
            
            # Ask for confirmation
            print("\nApply this evolution? (y/n): ", end='')
            confirm = input().strip().lower()
            
            if confirm == 'y':
                if apply_edit(new_code):
                    print(f"\nEvolution complete! main.py has been updated.")
                    print(f"Previous version saved as: {checkpoint}")
                else:
                    print("Failed to apply evolution.")
            else:
                print("Evolution skipped.")
                os.remove(checkpoint)  # Remove unnecessary checkpoint
            
        
        generation += 1
        
        print("\nContinue evolving? (y/n): ", end='')
        if input().strip().lower() != 'y':
            break
    
    print("\nEvolution process complete.")
    print(f"All checkpoints are saved in the 'checkpoints' folder.")

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
    
    args = parser.parse_args()
    
    # Run evolution with specified model
    run_evolution(args.model)

if __name__ == "__main__":
    main() 