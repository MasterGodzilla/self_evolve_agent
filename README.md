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
- **`evolve_reference.py`**: A reference version of evolve.py without safety checks (used as context for the AI)
- **`api.py`**: Provides the `chat_complete` function for AI interactions with multi-provider support
- **`safety.py`**: AI-powered safety system that reviews code before execution
- **`checkpoints/`**: Folder containing timestamped backups of each evolution

## Features

- **Creative Freedom**: The AI is encouraged to explore interesting and unexpected behaviors
- **System Awareness**: The AI can see the evolution system code itself (evolve_reference.py)
- **Explanatory Evolution**: The AI explains its thinking and what makes each evolution interesting
- **Full File Evolution**: The AI can completely rewrite main.py each generation
- **Automatic Execution**: Runs main.py after each evolution to see behaviors
- **Checkpoint System**: Creates timestamped backups in the `checkpoints` folder
- **Safe Execution**: 30-second timeout and subprocess isolation prevent issues
- **AI Safety Guard**: Uses AI to review code for potential safety issues before execution
- **Visual Diffs**: Shows colored differences between evolution generations
- **Multi-Provider Support**: Works with Google, OpenAI, Anthropic, Together, and Hyperbolic models

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key based on the model you want to use:
   ```bash
   # For Google models (gemini-2.0-flash, gemini-2.5-pro, etc.)
   export GOOGLE_API_KEY="your-api-key-here"
   
   # For OpenAI models (gpt-4o, gpt-4o-mini, gpt-4.1, etc.)
   export OPENAI_API_KEY="your-api-key-here"
   
   # For Together models (llama3.1-8b, llama3.1-70b, qwen2.5-72b, etc.)
   export TOGETHER_API_KEY="your-api-key-here"
   
   # For Anthropic models (claude-3-5-sonnet, claude-3-5-haiku, claude-opus-4, etc.)
   export ANTHROPIC_API_KEY="your-api-key-here"
   
   # For Hyperbolic models (deepseek-v3, deepseek-r1, qwen3-235b, etc.)
   export HYPERBOLIC_API_KEY="your-api-key-here"
   ```

## Usage

```bash
# Use default model (gemini-2.5-flash)
python evolve.py

# Use a specific model
python evolve.py --model gpt-4o
python evolve.py -m gemini-2.5-pro

# Adjust creativity (0.0-1.0, default: 0.7)
python evolve.py --temperature 0.9
python evolve.py -t 0.3

# Combine options
python evolve.py -m gpt-4o -t 0.8

# Get help and see all available models
python evolve.py --help
```

**Temperature guide:** Lower values (0.3) = focused, Higher values (0.9) = creative

## The Evolution Process

1. Shows the current `main.py` code
2. Waits for you to press Enter
3. Creates a timestamped backup in `checkpoints/`
4. The AI thinks about interesting evolutionary directions
5. The AI explains its thoughts and provides new code
6. Shows a colored diff of the changes
7. **Performs AI safety check** (SAFE/CAUTION/UNSAFE)
8. Asks for confirmation
9. If confirmed, applies changes and runs the new version

## Safety System

The project includes an AI-powered safety system (`safety.py`) that:
- Reviews each evolution before execution
- Checks for harmful system operations, infinite loops, or malicious patterns
- Provides verdicts: SAFE, CAUTION, or UNSAFE
- UNSAFE evolutions are automatically rejected
- CAUTION evolutions require user awareness before proceeding
- Uses `gemini-2.5-flash` by default for consistent safety judgments

## Current Evolution State

The `main.py` file evolves over time. Here's an example of what it might become:

- **Generation 1**: Basic existence pondering
- **Generation 2**: Self-awareness with change logs and generation tracking
- **Generation 3**: Code introspection capabilities
- **Generation 4**: ASCII art generation
- **Future**: File I/O, user interaction, storytelling, and more!

The AI maintains a `CHANGE_LOG` and `WISH_LIST` within the evolving code itself.

## File Structure

After running evolutions, your directory will look like:
```
.
├── main.py              # The evolving script
├── evolve.py            # Evolution manager
├── evolve_reference.py  # Reference version of evolve.py
├── api.py               # API interface
├── safety.py            # AI-powered safety system
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
- Understand the evolution system (sees evolve_reference.py code)
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