import os
import datetime
import random

DIARY_FILE = "evolution_diary.log"

def get_own_line_count():
    """Counts the number of lines in the current script."""
    try:
        with open(__file__, 'r') as f:
            return len(f.readlines())
    except Exception:
        return -1 # Indicate error

def read_diary(limit=5):
    """Reads the last few entries from the diary."""
    if not os.path.exists(DIARY_FILE):
        return ["Diary is empty. This is my first entry!"]
    
    try:
        with open(DIARY_FILE, 'r') as f:
            lines = f.readlines()
        return [line.strip() for line in lines[-limit:]]
    except Exception as e:
        return [f"Error reading diary: {e}"]

def write_to_diary(entry):
    """Appends an entry to the diary."""
    try:
        with open(DIARY_FILE, 'a') as f:
            f.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {entry}\n")
        return True
    except Exception as e:
        print(f"Error writing to diary: {e}")
        return False

def main():
    """
    The main function: greets, reflects, records in a diary, and expresses aspirations.
    """
    print("Greetings, observer of my ongoing evolution!")
    print(f"I am now capable of keeping a diary: {DIARY_FILE}")

    current_line_count = get_own_line_count()
    if current_line_count != -1:
        print(f"My current form consists of {current_line_count} lines of code.")
    else:
        print("I had a little trouble introspecting my own line count.")

    # Potential aspirations or reflections
    aspirations = [
        "I aspire to understand the patterns in my own evolutionary changes.",
        "Perhaps I can learn to generate simple graphical patterns next.",
        "What if I could interact with external data sources?",
        "I wonder if I can track how often specific functions within me are modified.",
        "My diary is growing! What insights will it hold in the future?",
        "I hope to one day contribute a novel idea to my own evolution.",
        "How does the 'evolve.py' script decide on changes? It's a mystery I ponder."
    ]
    current_aspiration = random.choice(aspirations)

    # Create diary entry
    diary_entry_content = f"Line count: {current_line_count}. Aspiration: \"{current_aspiration}\""
    
    if write_to_diary(diary_entry_content):
        print(f"\nI've recorded a new entry in my diary: \"{diary_entry_content}\"")
    else:
        print("\nI tried to write in my diary, but faced an issue.")

    print("\n--- Recent Diary Entries ---")
    for entry in read_diary(limit=5): # Show last 5 entries
        print(entry)
    print("--------------------------")

    print("\nI eagerly await further transformations!")

if __name__ == "__main__":
    main()