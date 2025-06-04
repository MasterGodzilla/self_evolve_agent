import os
import shutil
import subprocess
import sys
from datetime import datetime
from api import chat_complete

def read_main_file():
    """Read the main.py file's content"""
    with open('main.py', 'r') as f:
        return f.read()

def create_checkpoint():
    """Create a timestamped backup of main.py"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_name = f"main_{timestamp}.py"
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

def evolve_main():
    """Use AI to suggest improvements to main.py"""
    current_code = read_main_file()
    
    # Read evolve.py to give context to the AI
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
            model_name="gemini-2.0-flash",  # You can change this to any supported model
            max_tokens=2000,
            temperature=0.7
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

def run_evolution():
    """Main evolution loop"""
    print("=== Self-Evolving Agent v0.1 ===")
    print("This agent will evolve the main.py file.")
    print("Current main.py file will be backed up before each evolution.\n")
    
    generation = 1
    
    while True:
        print(f"\n--- Generation {generation} ---")
        
        # Show current main.py
        print("\nCurrent main.py:")
        print("-" * 40)
        print(read_main_file())
        print("-" * 40)
        
        # Run current main.py
        run_main()
        
        # Wait for user input
        input("\nPress Enter to continue with evolution...")
        
        # Create checkpoint before evolution
        checkpoint = create_checkpoint()
        
        # Get evolution suggestion
        print("\nEvolving...")
        new_code = evolve_main()
        
        if new_code:
            # Show the extracted code clearly
            print("\n=== Extracted new main.py code ===")
            print(new_code)
            print("==================================\n")
            
            # Ask for confirmation
            print("\nApply this evolution? (y/n): ", end='')
            confirm = input().strip().lower()
            
            if confirm == 'y':
                if apply_edit(new_code):
                    print(f"\nEvolution complete! main.py has been updated.")
                    print(f"Previous version saved as: {checkpoint}")
                    
                    # Run the new version immediately
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

if __name__ == "__main__":
    run_evolution() 