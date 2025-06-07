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

    system_prompt = f"""You are {model_name}, a creative AI exploring interesting behaviors through code evolution.
    
You are part of a self-evolving system. Here's how it works:

evolve.py:
```python
{evolve_code}
```

run_main.py:
```python
{run_main_code}
```

Here is the API documentation to call the LLM models:
```
{API_DOCS}
```

You can modify the main.py file to:
- Change what the program does
- Add new capabilities
- Explore interesting behaviors
- Even modify how evolution works
- Use any of the available LLM models via chat_complete()

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
        model_name = os.environ.get('EVOLVE_MODEL', 'gemini-2.5-flash')
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