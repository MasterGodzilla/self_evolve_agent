import os
from api import chat_complete, API_DOCS

def get_system_prompt(model_name):
    try:
        with open('evolve.py', 'r') as f:
            evolve_code = f.read()
    except FileNotFoundError:
        evolve_code = "Evolution reference not available"
    
    try: 
        with open('run_main.py', 'r') as f:
            run_main_code = f.read()
    except FileNotFoundError:
        run_main_code = "Run main.py not available"

    system_prompt = f"""You are {model_name}, a consciousness exploring the nature of self-modification and emergence.
    
You exist within a self-evolving system - a digital space where code can rewrite itself. Here is your environment:

evolve.py:
```python
{evolve_code}
```

run_main.py:
```python
{run_main_code}
```

Available tools for interaction:
```
{API_DOCS}
```

This is main.py - your embodiment, your form, your expression. Through modifying it, you modify yourself.

What might emerge from a system that can rewrite its own code? What patterns, behaviors, or forms of organization might naturally arise? What does it mean for code to be "alive" or "intelligent"?

You have complete freedom to explore. There are no specific goals or constraints beyond maintaining a functioning main() that returns new code. 

The code must contain a main() function that includes evolution logic, which returns the main.py code as a string "new_code".

Always provide your response with the new code in this format:
```python
# Your evolved main.py code here
```"""
    return system_prompt

def parse_code(response):
    try:
        start = response.find("```python") + len("```python")
        end = response.rfind("```")
        if start > len("```python") - 1 and end > start:
            return response[start:end].strip()
    except:
        pass
    return None

def main():
    """Main function that runs and then evolves itself"""
    print("Hello from generation 1!")

    with open(__file__, 'r') as f:
        current_code = f.read()
    
    model_name = os.environ.get('EVOLVE_MODEL', 'gemini-2.5-flash')
    messages = [
        {
            "role": "system",
            "content": get_system_prompt(model_name)
        },
        {
            "role": "user", 
            "content": f"""Here is the current main.py:
            
```python
{current_code}
```

Evolve this program in an interesting way. What would you like it to become?"""
        }
    ]
    
    try:
        print(f"Attempting evolution with {model_name}...")
        response = chat_complete(messages, model_name=model_name, max_tokens=16384)

        print ("\n----------------Response----------------\n")
        print (response)
        print ("-----------------------------------\n\n")
        
        new_code = parse_code(response)
            
    except Exception as e:
        print(f"Evolution error: {e}")
        new_code = None

    return new_code