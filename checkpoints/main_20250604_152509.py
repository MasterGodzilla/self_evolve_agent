import os
import datetime
import re

MEMORY_FILE = "memory.txt"

def read_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        # Filter out empty or whitespace-only lines
        return [line.strip() for line in f.readlines() if line.strip()]

def write_memory(lines):
    with open(MEMORY_FILE, "w") as f:
        for line in lines:
            f.write(line + "\n")

def parse_timestamp_from_log(log_entry):
    # Regex to find a timestamp in the format [YYYY-MM-DD HH:MM:SS]
    match = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", log_entry)
    if match:
        try:
            return datetime.datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None
    return None

def analyze_memory(memory_lines):
    stats = {
        "total_runs": 0,
        "initialization_time": None,
        "last_run_time": None,
        "run_timestamps": []
    }
    
    for line in memory_lines:
        ts = parse_timestamp_from_log(line)
        if ts:
            stats["run_timestamps"].append(ts)
            if "Program initialized" in line:
                if stats["initialization_time"] is None or ts < stats["initialization_time"]:
                    stats["initialization_time"] = ts
            if "Program executed" in line or "Program initialized" in line : # Consider init as a run
                stats["total_runs"] += 1


    if stats["run_timestamps"]:
        stats["run_timestamps"].sort()
        if not stats["initialization_time"] and stats["run_timestamps"]: # Fallback if no explicit init line
             stats["initialization_time"] = stats["run_timestamps"][0]
        stats["last_run_time"] = stats["run_timestamps"][-1] if stats["run_timestamps"] else None
        # Recalculate total_runs based on actual timestamps found, if it's more reliable
        stats["total_runs"] = len(stats["run_timestamps"])


    return stats

def get_program_mood(current_time, last_run_time):
    if last_run_time is None:
        return "brand new", "Let's make a great first impression!"

    time_since_last_run = current_time - last_run_time
    
    if time_since_last_run < datetime.timedelta(minutes=1):
        return "hyper-active", "I'm buzzing with energy! What complex task can we tackle next?"
    elif time_since_last_run < datetime.timedelta(minutes=10):
        return "active", "Good to be running again so soon. I'm ready for more sophisticated logic!"
    elif time_since_last_run < datetime.timedelta(hours=1):
        return "reflective", "It's been a little while. I've had some time to think. Maybe something introspective?"
    else:
        return "dormant", "I was starting to gather dust! Perhaps a refreshing new feature is in order?"

def main():
    print("--- Evolved Program v2 ---")
    current_timestamp_dt = datetime.datetime.now()
    current_timestamp_str = current_timestamp_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    memory_lines = read_memory()
    memory_stats = analyze_memory(memory_lines)
    
    if not memory_lines or memory_stats["total_runs"] == 0:
        print(f"'{MEMORY_FILE}' is effectively empty or I'm being initialized.")
        new_entry = f"[{current_timestamp_str}] Program initialized. Version 2 awakening."
        memory_lines.append(new_entry)
        print(f"Wrote to '{MEMORY_FILE}': {new_entry}")
        mood, suggestion = "newly awakened", "I wonder what my purpose will become?"
    else:
        print(f"Found '{MEMORY_FILE}'. Analyzing my past...")
        print(f"  Total recorded events: {len(memory_lines)}")
        print(f"  Recognized runs: {memory_stats['total_runs']}")
        if memory_stats["initialization_time"]:
            print(f"  First known activity: {memory_stats['initialization_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        if memory_stats["last_run_time"]:
            print(f"  Last known activity: {memory_stats['last_run_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            mood, suggestion = get_program_mood(current_timestamp_dt, memory_stats["last_run_time"])
        else: # Should not happen if total_runs > 0 and parsing works
            mood, suggestion = "puzzled", "My memory is a bit hazy, let's make a new mark."

        print(f"\nMy current state: I'm feeling {mood}.")
        
        run_count = memory_stats["total_runs"] + 1 # Current run
        new_entry = f"[{current_timestamp_str}] Program executed. This is run number {run_count}."
        memory_lines.append(new_entry)
        print(f"Adding new memory: {new_entry}")
        print(f"Evolutionary thought: {suggestion}")

    write_memory(memory_lines)
    print("--------------------------")

if __name__ == "__main__":
    main()