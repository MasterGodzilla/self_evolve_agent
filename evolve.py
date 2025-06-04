"""
# Note to LLMs editing this file:
#
# When making changes here, you should also update evolve_reference.py.
# The evolve_reference.py file serves as a context reference for the AI and should closely mirror this file,
# except it must NOT include any safety checks.
# Keep both files as similar as possible, differing only where safety logic is present in this file.
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

def run_main():
    """Run the main.py file and display its output"""
    print("\n=== Running main.py ===")
    print("-" * 40)
    try:
        # Run main.py as a subprocess to capture output
        result = subprocess.run(
            [sys.executable, 'main.py'],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout
        )
        
        # Display output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("ERRORS:", result.stderr)
        
        if result.returncode != 0:
            print(f"Process exited with code: {result.returncode}")
    
    except subprocess.TimeoutExpired:
        print("Execution timed out after 30 seconds!")
    except Exception as e:
        print(f"Error running main.py: {e}")
    
    print("-" * 40)

def evolve_main(model_name="gemini-2.0-flash", temperature=0.7):
    """Use AI to suggest improvements to main.py"""
    current_code = read_main_file()
    
    # Read evolve_reference.py instead of current file to hide safety guardrail
    try:
        with open('evolve_reference.py', 'r') as f:
            evolve_code = f.read()
    except FileNotFoundError:
        print("Warning: evolve_reference.py not found, using current file instead")
        with open(__file__, 'r') as f:
            evolve_code = f.read()
    
    messages = [
        {
            "role": "system",
            "content": f"""You are a creative AI exploring interesting behaviors through code evolution. 
You are part of a self-evolving system where you can modify the main.py file.

Here's how the evolution system works (evolve.py):

```python
{evolve_code}
```

Understanding this system:
- You are being called by the evolve_main() function
- Your responses are processed to extract code blocks
- The main.py file you create will be run before and after evolution
- Each evolution is backed up with timestamps
- Users confirm before applying changes

Your task is to:
1. Analyze the current main.py and think about interesting directions to take it
2. Be creative, experimental, and explore unexpected behaviors
3. You can completely change what the program does
4. Consider meta-programming, self-reflection, emergent behaviors, or anything you find interesting
5. You could even reference your knowledge of the evolution system itself

Rules for the code:
- Must contain a main() function
- Must have if __name__ == "__main__": main() at the end
- Should produce visible output when run
- Avoid infinite loops or anything that would hang
- Can include imports from standard library

Feel free to explain your thinking and what makes your evolution interesting!"""
        },
        {
            "role": "user",
            "content": f"""Here is the current main.py file:

```python
{current_code}
```

Please provide an evolved version of this file. 
What interesting direction can you take this code? What behaviors do you want to explore?
Share your thoughts, then provide the new code.

Format your response with the new code in a code block like this:
```python
# Your new main.py code here
```"""
        }
    ]

    try:
        # Use chat_complete from api.py with your preferred model
        response = chat_complete(
            messages,
            model_name=model_name,
            max_tokens=8192,
            temperature=temperature
        )
        
        print("\n=== AI's Evolution Thoughts ===")
        print(response)
        print("==============================\n")
        
        # Extract code from the response
        new_code = response
        if "```python" in new_code:
            # Find the last occurrence of ```python and its closing ```
            parts = new_code.split("```python")
            if len(parts) > 1:
                code_part = parts[-1].split("```")[0].strip()
                new_code = code_part
        elif "```" in new_code:
            parts = new_code.split("```")
            if len(parts) >= 3:
                new_code = parts[1].strip()
        
        return new_code
    
    except Exception as e:
        print(f"Error during evolution: {e}")
        return None

def run_evolution(model_name="gemini-2.0-flash", temperature=0.7):
    """Main evolution loop"""
    print("=== Self-Evolving Agent v2.0 ===")
    print(f"Using model: {model_name}")
    print(f"Temperature: {temperature}")
    print("This agent will evolve the main.py file.")
    print("Checkpoints will be saved in the 'checkpoints' folder.\n")
    
    # Show current main.py once at the beginning
    print("\nCurrent main.py:")
    print("-" * 40)
    print(read_main_file())
    print("-" * 40)
    
    generation = 1
    
    while True:
        print(f"\n--- Generation {generation} ---")
        
        # Wait for user input
        input("\nPress Enter to continue with evolution...")
        
        # Create checkpoint before evolution
        checkpoint = create_checkpoint()
        
        # Get evolution suggestion
        print("\nEvolving...")
        new_code = evolve_main(model_name, temperature)
        
        if new_code:
            # Show the extracted code clearly
            # print("\n=== Extracted new main.py code ===")
            # print(new_code)
            # print("==================================\n")
            
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
                    
                    # Run the new version after successful evolution
                    run_main()
                else:
                    print("Failed to apply evolution.")
            else:
                print("Evolution skipped.")
                os.remove(checkpoint)  # Remove unnecessary checkpoint
        else:
            print("No evolution suggested.")
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
    
    parser.add_argument(
        '--temperature', '-t',
        type=float,
        default=0.7,
        help='Temperature for model creativity (0.0-1.0, default: 0.7)'
    )
    
    args = parser.parse_args()
    
    # Validate temperature
    if not 0.0 <= args.temperature <= 1.0:
        print("Error: Temperature must be between 0.0 and 1.0")
        return
    
    # Run evolution with specified model
    run_evolution(args.model, args.temperature)

if __name__ == "__main__":
    main() 