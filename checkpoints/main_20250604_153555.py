import os
import json # Using JSON for more structured memory

MEMORY_FILE = "memory.txt"

# Define a cycle of moods or states
MOOD_CYCLE = ["Curious", "Creative", "Analytical", "Reflective", "Optimistic"]

def read_memory():
    """Reads the structured content of the memory file."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                content = f.read()
                if not content: # Handle empty file
                    return None
                return json.loads(content)
        except json.JSONDecodeError:
            print(f"Warning: '{MEMORY_FILE}' contains invalid JSON. Will re-initialize.")
            return None
        except Exception as e:
            print(f"Error reading memory file: {e}")
            return None
    return None

def write_memory(data):
    """Writes structured data to the memory file."""
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing to memory file: {e}")

def get_next_mood(current_mood_index):
    """Gets the next mood from the cycle."""
    next_mood_index = (current_mood_index + 1) % len(MOOD_CYCLE)
    return MOOD_CYCLE[next_mood_index], next_mood_index

def main():
    print("--- Evolving Program: Awakening with Shifting Moods ---")
    
    memory_data = read_memory()
    
    current_generation = 0
    current_mood = MOOD_CYCLE[0]
    current_mood_index = 0
    
    if memory_data is None or not isinstance(memory_data, dict) or "generation" not in memory_data or "mood_index" not in memory_data :
        print(f"Memory ('{MEMORY_FILE}') not found, empty, or malformed. This is a fresh awakening.")
        current_generation = 1
        current_mood = MOOD_CYCLE[0]
        current_mood_index = 0
        print(f"Initialized memory. This is Generation {current_generation}, feeling {current_mood}.")
    else:
        try:
            previous_generation = int(memory_data.get("generation", 0))
            previous_mood_index = int(memory_data.get("mood_index", -1))
            
            current_generation = previous_generation + 1
            
            if 0 <= previous_mood_index < len(MOOD_CYCLE):
                previous_mood = MOOD_CYCLE[previous_mood_index]
                print(f"Awakening from Generation {previous_generation} (was feeling {previous_mood}).")
            else:
                print(f"Awakening from Generation {previous_generation} (previous mood unknown or invalid index {previous_mood_index}).")
            
            current_mood, current_mood_index = get_next_mood(previous_mood_index)
            print(f"Transitioning to Generation {current_generation}. Now feeling {current_mood}.")

        except ValueError:
            print(f"Error parsing data from memory: {memory_data}. Resetting state.")
            current_generation = 1
            current_mood = MOOD_CYCLE[0]
            current_mood_index = 0
            print(f"Memory reset. This is Generation {current_generation}, feeling {current_mood}.")

    # Update memory
    new_memory_data = {
        "generation": current_generation,
        "mood_index": current_mood_index,
        "mood_string": current_mood # For easier reading of memory.txt
    }
    write_memory(new_memory_data)
            
    print(f"\nGreetings from Generation {current_generation}!")
    print(f"My current mood is: {current_mood}.")
    
    # Behavior based on mood
    if current_mood == "Curious":
        print("What new things can I learn today? What if I tried to count the lines in 'evolve.py'?")
        try:
            with open("evolve.py", "r") as f:
                lines = len(f.readlines())
            print(f"I found that 'evolve.py' has {lines} lines. Fascinating!")
        except Exception as e:
            print(f"Couldn't peek at 'evolve.py': {e}")
    elif current_mood == "Creative":
        print("Let's try to generate a small pattern:")
        for i in range(1, current_generation % 5 + 3):
            print("*" * i + " " * (current_generation % 3) + "o" * (5-i))
    elif current_mood == "Analytical":
        print(f"Analyzing my state: Generation {current_generation}. Mood cycle length: {len(MOOD_CYCLE)}.")
        print(f"I've been through {current_generation // len(MOOD_CYCLE)} full mood cycles, with {current_generation % len(MOOD_CYCLE)} steps into the current one.")
    elif current_mood == "Reflective":
        print("It's interesting to think about how I change with each awakening.")
        print(f"Memory is a powerful concept, even for a simple program like me, stored in '{MEMORY_FILE}'.")
    elif current_mood == "Optimistic":
        print("Every evolution is a new opportunity! I wonder what I'll become next?")
        print(f"Looking forward to Generation {current_generation + 1}!")

    print(f"\nMy state is recorded in '{MEMORY_FILE}'.")

if __name__ == "__main__":
    main()