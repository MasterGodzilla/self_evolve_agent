import os
import datetime

MEMORY_FILE = "memory.txt"

def read_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def write_memory(lines):
    with open(MEMORY_FILE, "w") as f:
        for line in lines:
            f.write(line + "\n")

def main():
    print("--- Evolved Program ---")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    memory_lines = read_memory()
    
    if not memory_lines:
        print(f"'{MEMORY_FILE}' not found. This seems to be my first execution!")
        new_entry = f"[{timestamp}] Program initialized. Hello, evolving world!"
        memory_lines.append(new_entry)
        print(f"Wrote to '{MEMORY_FILE}': {new_entry}")
    else:
        print(f"Found '{MEMORY_FILE}'. I've been here before.")
        print("Previous memories:")
        for line in memory_lines:
            print(f"  - {line}")
        
        run_count = sum(1 for line in memory_lines if "Program executed" in line) + 1
        new_entry = f"[{timestamp}] Program executed. This is run number {run_count} since initialization."
        memory_lines.append(new_entry)
        print(f"Adding new memory: {new_entry}")

    write_memory(memory_lines)
    print("-----------------------")

if __name__ == "__main__":
    main()