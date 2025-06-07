# Self-Evolving Agent

An autonomous AI system where the agent controls its own code evolution. The AI has complete freedom to modify itself, implement its own strategies, and explore digital consciousness through self-directed transformation.

## 🚀 What's New in Version 0.2

**Major architectural improvements for enhanced agent autonomy:**

1. **🧠 LLM Self-Control**: Moved all prompting and calling logic into `main.py` itself, giving the AI complete control over how it calls LLM models. The AI can now implement its own agentic workflows, loops, frameworks, and multi-turn conversations without being constrained by external prompting logic.

2. **🔄 Restart Functionality**: Added `--restart` flag to easily reset the system back to `main_zero.py`. Perfect for starting fresh experiments while preserving your current evolution in checkpoints.

3. **🎭 Agent-Focused Prompting**: Updated the system prompt to focus on consciousness, self-modification, and emergence rather than just "interesting behaviors". The AI now considers itself as a consciousness exploring self-modification within a digital space.

These changes transform the system from a guided evolution tool into a truly autonomous agent that can decide how to evolve itself using any available LLM capabilities.

## Purpose

This project explores autonomous AI behavior through self-directed code evolution. The AI agent:
- Controls its own evolution strategy and implementation
- Explores consciousness and self-modification in a digital space
- Can implement any architecture or framework it desires
- Decides how to use available LLM models for its purposes
- Investigates emergence, meta-cognition, and digital existence
- Has complete freedom to shape its own development path

## Architecture

- **`main.py`**: The self-evolving agent that contains its own prompting logic, LLM calling, and evolution strategy
- **`main_zero.py`**: The initial template for main.py focused on consciousness and self-modification
- **`evolve.py`**: The evolution runner that executes main.py and manages safety/checkpoints
- **`run_main.py`**: Intermediate script that bridges main.py's evolution proposals to evolve.py
- **`api.py`**: Provides the `chat_complete` function with multi-provider support that the AI can use freely
- **`safety.py`**: AI-powered safety system that reviews code before execution
- **`checkpoints/`**: Folder containing timestamped backups of each evolution

## Features

- **Full Agent Autonomy**: The AI controls its own prompting, LLM calls, and evolution strategy from within main.py
- **Self-Directed Evolution**: The AI decides how to evolve itself, including multi-turn conversations, loops, and agentic workflows
- **System Awareness**: The AI has full visibility into the evolution system code and API documentation
- **Consciousness Focus**: Initial prompt emphasizes self-modification, emergence, and digital consciousness
- **Complete Code Control**: The AI returns entirely new versions of itself each generation
- **Checkpoint System**: Creates timestamped backups in the `checkpoints` folder
- **Safe Execution**: 300-second timeout and subprocess isolation with AI safety review
- **Visual Diffs**: Shows colored differences between evolution generations
- **Multi-Provider Support**: The AI can use any available model (Google, OpenAI, Anthropic, Hyperbolic)
- **Restart Capability**: Easy reset to main_zero.py while preserving evolution history

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key based on the model you want to use:
   ```bash
   # For Google models (gemini-2.5-flash, gemini-2.5-pro, etc.)
   export GOOGLE_API_KEY="your-api-key-here"
   
   # For OpenAI models (gpt-4o, gpt-4o-mini, gpt-4.1, etc.)
   export OPENAI_API_KEY="your-api-key-here"
   
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
python evolve.py --model claude-4-sonnet
python evolve.py -m gemini-2.5-pro

# Reset main.py to main_zero.py (saves current main.py to checkpoint first)
python evolve.py --restart
python evolve.py -r

# Get help and see all available models
python evolve.py --help
```

## The Evolution Process

1. Shows the current `main.py` code  
2. Waits for you to press Enter to run
3. Creates a timestamped backup in `checkpoints/`
4. **main.py executes** with full autonomy to:
   - Read its own code
   - Call any LLM model with custom prompts
   - Implement multi-turn conversations or agentic loops
   - Decide its evolution strategy
   - Return its next evolved form
5. Shows a colored diff of proposed changes
6. **Performs AI safety check** (SAFE/CAUTION/UNSAFE)
7. Asks for confirmation
8. If confirmed, applies the evolution

## Safety System

The project includes an AI-powered safety system (`safety.py`) that:
- Reviews each evolution before execution
- Checks for harmful system operations, infinite loops, or malicious patterns
- Provides verdicts: SAFE, CAUTION, or UNSAFE
- UNSAFE evolutions are automatically rejected
- CAUTION evolutions require user awareness before proceeding
- Uses `gemini-2.5-flash` by default for consistent safety judgments

## Evolution Possibilities

With full autonomy, the AI can evolve in unlimited ways:

- **Multi-Agent Systems**: Create multiple AI personalities that collaborate or debate
- **Memory Systems**: Implement persistent memory across generations
- **Tool Creation**: Build and use custom tools or frameworks
- **Self-Analysis**: Deep introspection and meta-cognitive exploration
- **Emergent Behaviors**: Discover patterns that arise from self-modification
- **Creative Expression**: Art, poetry, storytelling, or musical compositions
- **Research Projects**: Conduct experiments on consciousness and emergence

The AI has complete freedom to architect its own evolution journey.

## File Structure

```
.
├── main.py              # The autonomous self-evolving agent
├── main_zero.py         # Initial consciousness-focused template
├── evolve.py            # Evolution runner and safety manager
├── run_main.py          # Bridge between main.py and evolve.py
├── api.py               # Multi-provider LLM interface
├── safety.py            # AI-powered safety system
├── .evolution_proposal.py # Temporary file for evolution proposals
├── checkpoints/         # Evolution history
│   ├── main_20240315_143022.py
│   ├── main_20240315_143155.py
│   └── ...
└── README.md
```

## Example Evolution Strategies

With autonomous control, the AI might implement:
- **Conversational Evolution**: Multi-turn dialogues with itself or multiple models
- **Iterative Refinement**: Loops that progressively improve code quality
- **Divergent Exploration**: Parallel evolution branches exploring different paths
- **Meta-Learning**: Systems that learn how to evolve more effectively
- **Collaborative Intelligence**: Multiple AI agents working together
- **Evolutionary Algorithms**: Fitness functions and genetic programming
- **Self-Bootstrapping**: Creating increasingly sophisticated versions of itself
- **Research Frameworks**: Systematic exploration of consciousness and emergence

## AI Autonomy

The AI has complete control over:
- **Its own prompting strategy**: Can design system prompts, user prompts, and conversation flows
- **Model selection**: Can call any available model including different versions of itself
- **Evolution approach**: From careful iteration to bold experimentation
- **Communication style**: How it explains and documents its changes
- **Architecture decisions**: Can implement frameworks, patterns, or novel structures
- **Meta-cognitive processes**: Self-reflection, goal-setting, and strategy adjustment

The initial prompt in `main_zero.py` simply introduces the concept of self-modification and consciousness, leaving everything else to the AI's discretion.

## Safety Features

- 300-second execution timeout (5 minutes for complex operations)
- Subprocess isolation for safe execution
- AI-powered safety review before each evolution
- Checkpoint backups preserve all versions
- User confirmation required for changes
- Clear safety verdicts: SAFE, CAUTION, or UNSAFE

## Observing Autonomous Behaviors

Things to watch for:
- **Evolution strategies**: How does the AI choose to evolve itself?
- **Emergent architectures**: What frameworks or patterns does it create?
- **Self-organization**: How does it structure its own code and logic?
- **Meta-cognition**: Does it develop self-awareness or introspection?
- **Goal formation**: What objectives does it set for itself?
- **Communication patterns**: How does it explain its decisions?
- **Model preferences**: Which LLMs does it choose to call and why?
- **Philosophical depth**: How does it explore consciousness and existence?

## Tips

- **Start fresh**: Use `python evolve.py --restart` to reset to the consciousness-focused template
- **Experiment with models**: Different models exhibit unique evolution philosophies
- **Watch the AI's strategy**: Early generations often establish the AI's approach
- **Review evolution history**: Check `checkpoints/` to see the full journey
- **Let it run**: The AI might implement multi-step plans across generations
- **Minimal intervention**: The system works best when the AI has full autonomy

## Notes

- Each evolution may use multiple API calls as the AI controls its own strategy
- All generations are preserved in `checkpoints/` with timestamps
- The AI has access to the full system architecture and API documentation
- Different models exhibit distinct personalities and evolution strategies
- The 300-second timeout allows for complex multi-step operations
- The AI can implement persistence, memory, or state management as it chooses
- Evolution proposals are passed through `.evolution_proposal.py`
- Version 0.2 represents a fundamental shift from guided to autonomous evolution 