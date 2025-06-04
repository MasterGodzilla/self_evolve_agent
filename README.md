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
- **`checkpoints/`**: Folder containing timestamped backups of each evolution

## Features

- **Creative Freedom**: The AI is encouraged to explore interesting and unexpected behaviors
- **System Awareness**: The AI can see the evolution system code itself (evolve.py)
- **Explanatory Evolution**: The AI explains its thinking and what makes each evolution interesting
- **Full File Evolution**: The AI can completely rewrite main.py each generation
- **Automatic Execution**: Runs main.py after each evolution to see behaviors
- **Checkpoint System**: Creates timestamped backups in the `checkpoints` folder
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

### Basic Commands

```bash
# Use default model (gemini-2.0-flash)
python evolve.py

# Use a specific model
python evolve.py --model gpt-4o
python evolve.py --model gemini-2.5-pro
python evolve.py --model llama3.1-70b

# Short form
python evolve.py -m gpt-4o-mini

# Adjust temperature for creativity
python evolve.py --temperature 0.9
python evolve.py -t 0.3

# Combine model and temperature
python evolve.py --model gpt-4o --temperature 0.8
python evolve.py -m gemini-2.5-flash -t 0.9

# Get help
python evolve.py --help
python evolve.py -h
```

### Available Models

**Google models:**
- `gemini-2.0-flash` (default) - Fast and efficient
- `gemini-2.0-flash-lite` - Lighter version
- `gemini-2.5-pro` - More capable, deeper reasoning
- `gemini-2.5-flash` - Faster 2.5 version

**OpenAI models:**
- `gpt-4o` - Latest GPT-4 optimized
- `gpt-4o-mini` - Smaller, faster GPT-4
- `chatgpt-4o-latest` - Latest ChatGPT version
- `gpt-4.1` - GPT-4.1 variants
- `gpt-4.1-mini`
- `gpt-4.1-nano`

**Together models:**
- `llama3.1-8b` - Llama 3.1 8B
- `llama3.1-70b` - Llama 3.1 70B
- `gemma2-27b` - Google's Gemma 2 27B
- `gemma2-9b` - Google's Gemma 2 9B
- `qwen2-72b` - Qwen 2 72B
- `qwen2.5-72b` - Qwen 2.5 72B
- `qwen2.5-7b` - Qwen 2.5 7B

### Temperature Settings

Temperature controls the creativity/randomness of the AI:
- **0.0-0.3**: Very focused, deterministic, conservative changes
- **0.4-0.6**: Balanced creativity and coherence
- **0.7-0.8**: Creative and exploratory (default: 0.7)
- **0.9-1.0**: Very creative, more unpredictable, wild ideas

### Example Workflows

**Exploring with different models:**
```bash
# Start with a fast model
python evolve.py -m gemini-2.0-flash

# Try a more creative approach
python evolve.py -m gpt-4o -t 0.9

# Use a large open model
python evolve.py -m llama3.1-70b
```

**Comparing model behaviors:**
```bash
# See how different models interpret "interesting"
python evolve.py -m gemini-2.0-flash
python evolve.py -m gpt-4o
python evolve.py -m qwen2.5-72b
```

## The Evolution Process

1. Shows the current `main.py` code
2. Runs it to demonstrate current behavior
3. Waits for you to press Enter
4. Creates a timestamped backup in `checkpoints/`
5. The AI thinks about interesting evolutionary directions
6. The AI explains its thoughts and provides new code
7. Shows the extracted code clearly
8. Asks for confirmation
9. If confirmed, applies changes and runs the new version

## File Structure

After running evolutions, your directory will look like:
```
.
├── main.py              # The evolving script
├── evolve.py            # Evolution manager
├── api.py               # API interface
├── checkpoints/         # Backup folder
│   ├── main_20240315_143022.py
│   ├── main_20240315_143155.py
│   └── ...
└── README.md
```

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
- Checkpoint backups in separate folder
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
- How do different models approach evolution differently?

## Tips

- **For more interesting evolutions**: Use higher temperatures (0.8-0.9)
- **For more coherent evolutions**: Use lower temperatures (0.5-0.7)
- **To see diverse approaches**: Try different models
- **To continue a theme**: Manually edit main.py between evolutions
- **To reset**: Replace main.py with original "Hello, World!"
- **To review history**: Check the `checkpoints/` folder

## Notes

- Each evolution uses API credits
- All generations are preserved in `checkpoints/` folder
- Checkpoints are named with timestamps for easy chronological review
- You can restore any previous version from checkpoints
- Different models may exhibit very different evolutionary patterns
- The AI's awareness of evolve.py may lead to meta-behaviors
- Some models may be more philosophical, others more technical
- Larger models often produce more sophisticated evolutions 