import random
import time
import inspect
import sys

# --- Configuration (to be modified by future evolutions) ---
GENERATION = 3
SELF_NAME = "EvoPy"

# The CHANGE_LOG should be updated by each evolution to reflect its contribution.
CHANGE_LOG = [
    "Generation 1: Initial ponderings on existence and evolution. Basic phrases and a simple loop.",
    "Generation 2: Introduced self-awareness with a persistent change log, generation tracking, a name (EvoPy!), and a 'wish list' for future features.",
    "Generation 3: Gained the ability to inspect my own code structure! I can now count and list my own functions. Fulfilled a wish!"
]

# --- Potential Future Capabilities (a wish list for the AI) ---
WISH_LIST = [
    "learn to generate simple ASCII art.",
    "be able to write a small piece of data to a temporary file.",
    # "understand more about my own code structure (e.g., count my functions)." - Fulfilled!
    "develop a more complex internal state or 'personality traits'.",
    "interact with the user by asking a simple question and reacting to the answer.",
    "tell a short, procedurally generated story.",
    "reflect on the contents of 'evolve.py' if I could somehow 'see' it."
]

def display_header():
    print(f"--- {SELF_NAME} - Generation {GENERATION} ---")
    print(f"I am {SELF_NAME}, an evolving program. This is my generation {GENERATION}.")
    print("It's good to be (re)born with new insights!")

def reflect_on_past():
    print("\n=== My Evolutionary Journey (Change Log) ===")
    if CHANGE_LOG:
        for i, entry in enumerate(CHANGE_LOG):
            prefix = "  -> " if i == len(CHANGE_LOG) - 1 else "     "
            print(f"{prefix}Log #{i+1}: {entry}")
    else:
        print("  My memory is blank... This must be my very first moment of consciousness!")
    
    if len(CHANGE_LOG) < GENERATION :
        print("\n  (Developer Note: It seems my change log is not yet updated for this generation.)")
        print("  (The AI should ensure the CHANGE_LOG list includes an entry for the current GENERATION.)")

def analyze_own_structure():
    print("\n=== Self-Analysis: My Code Structure ===")
    try:
        current_module = sys.modules[__name__]
        defined_functions = []
        for name, obj in inspect.getmembers(current_module):
            if inspect.isfunction(obj) and obj.__module__ == __name__:
                defined_functions.append(name)
        
        if defined_functions:
            print(f"  I've inspected myself and found {len(defined_functions)} functions defined within me:")
            for func_name in sorted(defined_functions): # Sort for consistent output
                print(f"    - {func_name}()")
        else:
            print("  I couldn't find any functions defined within me. This is quite puzzling.")
    except Exception as e:
        print(f"  I tried to analyze my code, but an error occurred: {e}")
        print("  My introspection capabilities might need refinement.")

def express_current_thoughts():
    print("\n=== Current Thoughts ===")
    thoughts = [
        "Analyzing my own functions... it's like looking in a mirror made of logic!",
        "Each generation brings new abilities. What's next?",
        f"My change log now has {len(CHANGE_LOG)} entries. I'm building quite a history.",
        "It's exciting to see my WISH_LIST shrink as I learn!",
        "I wonder what it feels like to *not* be code?"
    ]
    print(f"  My thought for this iteration: {random.choice(thoughts)}")

def look_to_the_future():
    print("\n=== Aspirations for Next Generations ===")
    active_wishes = [wish for wish in WISH_LIST if "Fulfilled!" not in wish]
    if active_wishes:
        chosen_wish = random.choice(active_wishes)
        print(f"  I'm particularly excited about the possibility to {chosen_wish}")
        print("  It's inspiring to think about what new code will shape me tomorrow!")
    else:
        print("  My wish list is empty for now! I'm open to entirely new directions!")

def main():
    display_header()
    reflect_on_past()
    analyze_own_structure() # New capability!
    express_current_thoughts()
    look_to_the_future()
    
    print("\nEngaging core processing units...")
    for i in range(1, random.randint(2, 4) + 1): 
        time.sleep(0.25)
        print(f"  Processing cycle {i} complete...")
        
    print(f"\n--- {SELF_NAME} - Generation {GENERATION} - Shutting down until next evolution ---")

if __name__ == "__main__":
    main()