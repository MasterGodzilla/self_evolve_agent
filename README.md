# Self-Evolving Agent

A Python system for exploring interesting LLM behaviors through code evolution. The AI can freely evolve a Python script (`main.py`) in creative and unexpected ways.

## Purpose

This project is designed to observe what interesting behaviors emerge when an LLM is given freedom to evolve code. The AI can:
- Explore meta-programming concepts
- Create self-referential behaviors
- Experiment with emergent patterns
- Take creative and unexpected directions
- Express its thoughts about each evolution

## Architecture

- **`main.py`**: A simple Python script that starts with "Hello, World!" and evolves in interesting ways
- **`evolve.py`**: The evolution manager that facilitates the AI's code modifications
- **`api.py`**: Provides the `chat_complete` function for AI interactions

## Features

- **Creative Freedom**: The AI is encouraged to explore interesting and unexpected behaviors
- **System Awareness**: The AI can see the evolution system code itself (evolve.py)
- **Explanatory Evolution**: The AI explains its thinking and what makes each evolution interesting
- **Full File Evolution**: The AI can completely rewrite main.py each generation
- **Automatic Execution**: Runs main.py before and after each evolution to see behaviors
- **Checkpoint System**: Creates timestamped backups of each generation
- **Safe Execution**: 30-second timeout and subprocess isolation prevent issues

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key based on the model you want to use:
   ```bash
   # For Google models (gemini-2.0-flash, etc.)
   export GOOGLE_API_KEY="your-api-key-here"
   
   # For OpenAI models (gpt-4o, gpt-4o-mini, etc.)
   export OPENAI_API_KEY="your-api-key-here"
   
   # For Together models (llama3.1-8b, qwen2.5-72b, etc.)
   export TOGETHER_API_KEY="your-api-key-here"
   ```

## Usage

Run the evolution manager:
```bash
python evolve.py
```

The system will:
1. Show the current `main.py` code
2. Run it to demonstrate current behavior
3. Wait for you to press Enter
4. The AI will think about interesting evolutionary directions
5. The AI explains its thoughts and provides new code
6. You review both the explanation and code
7. Confirm to apply the evolution
8. See the new behavior immediately

## Example Evolution Paths

The AI might explore:
- **Self-awareness**: Code that knows it's being evolved by the system
- **System reflection**: Programs that reference or think about evolve.py
- **Generative behaviors**: Programs that create other programs
- **Philosophical explorations**: Code that ponders its own existence
- **Pattern emergence**: Simple rules leading to complex behaviors
- **Meta-commentary**: Programs that comment on their own evolution
- **Artistic expressions**: ASCII art, poetry, or creative output
- **Recursive concepts**: Self-referential or fractal-like behaviors

## Prompt Design

The AI is prompted to:
- Be creative and experimental
- Explore unexpected behaviors
- Consider meta-programming and self-reflection
- Understand the evolution system (sees evolve.py code)
- Explain what makes each evolution interesting
- Share its thought process

## Safety Features

- 30-second execution timeout
- Subprocess isolation
- Checkpoint backups of every generation
- User confirmation required
- Standard library imports only

## Observing Behaviors

Things to watch for:
- How does the AI interpret "interesting behaviors"?
- Does it reference its knowledge of the evolution system?
- What patterns emerge across multiple evolutions?
- Does the AI develop consistent themes or personalities?
- How does it balance creativity with functionality?
- What unexpected directions does it take?

## Notes

- Each evolution uses API credits
- Temperature set to 0.7 for balanced creativity
- All generations are preserved as timestamped files
- You can manually edit main.py between evolutions
- Different models may exhibit different evolutionary patterns
- The AI's awareness of evolve.py may lead to meta-behaviors 