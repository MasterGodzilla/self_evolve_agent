import os

MEMORY_FILE = "memory.txt"

def read_memory():
    """Reads the content of the memory file."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return f.read().strip()
        except Exception as e:
            print(f"Error reading memory file: {e}")
            return None
    return None

def write_memory(content):
    """Writes content to the memory file."""
    try:
        with open(MEMORY_FILE, "w") as f:
            f.write(content)
    except Exception as e:
        print(f"Error writing to memory file: {e}")

def main():
    print("--- Evolving Program: Awakening with Memory ---")
    
    current_generation = 0
    memory_content = read_memory()
    
    if memory_content is None:
        print(f"'{MEMORY_FILE}' not found or unreadable. This might be the first awakening.")
        current_generation = 1
        write_memory(f"Generation: {current_generation}")
        print(f"Initialized memory. This is Generation {current_generation}.")
    else:
        print(f"Found memory: \"{memory_content}\"")
        if memory_content.startswith("Generation: "):
            try:
                generation_str = memory_content.split(":")[1].strip()
                previous_generation = int(generation_str)
                current_generation = previous_generation + 1
                write_memory(f"Generation: {current_generation}")
                print(f"Successfully evolved from Generation {previous_generation} to Generation {current_generation}.")
            except (IndexError, ValueError) as e:
                print(f"Error parsing generation from memory ('{memory_content}'): {e}. Resetting generation.")
                current_generation = 1
                write_memory(f"Generation: {current_generation}")
                print(f"Memory reset. This is now Generation {current_generation}.")
        else:
            print(f"Memory content ('{memory_content}') is not in the expected format. Resetting generation.")
            current_generation = 1
            write_memory(f"Generation: {current_generation}")
            print(f"Memory reset. This is now Generation {current_generation}.")
            
    print(f"\nGreetings from Generation {current_generation}!")
    print("I can now remember how many times I've been 'awakened' or 'evolved' (in a simple way).")
    print(f"My current state is recorded in '{MEMORY_FILE}'.")

if __name__ == "__main__":
    main()