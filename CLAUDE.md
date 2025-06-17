# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**FeynmanCraft ADK** is a multi-agent system for generating TikZ-Feynman diagrams from natural language descriptions, built on Google Agent Development Kit (ADK) v1.0.0.

### Core Architecture

```
User Request → OrchestratorAgent → Multi-Agent Pipeline → Validated TikZ Output
                    ↓
              ┌─────┴─────┬──────────┬───────────┬──────────┐
         PlannerAgent  KBRetriever  WebResearch  Generator  Validators
```

### Key Technologies
- **Framework**: Google ADK 1.0.0
- **Language Model**: Gemini 2.0 Flash
- **Knowledge Base**: BigQuery (production) / JSON (development)
- **Physics Engine**: Custom validation rules + particle data
- **Output Format**: TikZ-Feynman LaTeX code

## Directory Structure

```
feynmancraft-adk/
├── feynmancraft_adk/        # Main package (ADK entry point)
│   ├── __init__.py         # Package initialization
│   ├── agent.py            # Root agent definition
│   ├── sub_agents/         # Specialized agents
│   ├── tools/              # Agent tools
│   ├── shared_libraries/   # Shared utilities
│   └── data/              # Static data files
├── feyncore/               # Core physics and TikZ utilities
├── legacy/                 # Historical implementations (reference only)
├── test_runner.py         # Local test suite
├── requirements.txt       # Project dependencies
└── .env                   # Environment configuration
```

## Development Workflow

### Setting Up Environment

```bash
# Create conda environment
conda create --name fey python=3.11 -y
conda activate fey

# Install dependencies
cd feynmancraft-adk
pip install -r requirements.txt

# Configure environment
echo 'GOOGLE_API_KEY="your-key-here"' > .env
```

### Running the Application

```bash
# Start ADK Dev UI
adk run feynmancraft_adk

# Run with specific input (for testing)
python -m feynmancraft_adk.agent --input "Generate electron-positron annihilation diagram"

# Or run tests
python test_runner.py
```

### Common Tasks

1. **Adding a New Agent**
   - Create agent file in `feynmancraft_adk/sub_agents/`
   - Create corresponding prompt file `*_prompt.py`
   - Register in root agent's `sub_agents` list
   - Update `__init__.py` imports

2. **Modifying Agent Behavior**
   - Edit prompt in `*_prompt.py` files
   - Adjust agent parameters in agent definition
   - Test changes with `test_runner.py`

3. **Working with Knowledge Base**
   - Development: Edit `data/feynman_kb.json`
   - Production: Use BigQuery tools in `tools/`

## Agent System Details

### Core Agents

1. **OrchestratorAgent**: Main controller and router
2. **PlannerAgent**: Analyzes requests and creates execution plans
3. **KBRetrieverAgent**: Searches knowledge base for examples
4. **DiagramGeneratorAgent**: Generates TikZ code
5. **TikZValidatorAgent**: Validates LaTeX compilation
6. **PhysicsValidatorAgent**: Validates physics correctness
7. **FeedbackAgent**: Synthesizes final response

### Agent Communication Flow

```python
# Typical execution pattern
user_request → OrchestratorAgent.process()
    → PlannerAgent.create_plan(request)
    → KBRetrieverAgent.search(query)
    → DiagramGeneratorAgent.generate(prompt, examples)
    → TikZValidatorAgent.validate(tikz_code)
    → PhysicsValidatorAgent.check(process, particles)
    → FeedbackAgent.synthesize(all_results)
```

## Code Style Guidelines

### Python Code
- Use type hints for all functions
- Follow PEP 8 naming conventions
- Add docstrings to all public functions
- Use Pydantic models for data validation

### Agent Prompts
- Keep prompts focused and specific
- Include clear examples in prompts
- Use consistent terminology
- Test prompts with edge cases

### TikZ Output
- Always include necessary LaTeX packages
- Use TikZ-Feynman macros correctly
- Ensure proper vertex and particle naming
- Include comments for clarity

## Testing Guidelines

### Running Tests
```bash
# Run all tests
python test_runner.py

# Run specific test category
python test_runner.py --filter validation
```

### Writing Tests
- Place tests in appropriate test files
- Use descriptive test names
- Cover both success and failure cases
- Mock external dependencies

## Common Issues and Solutions

### Issue: ADK not finding the app
**Solution**: Ensure `app/agent.py` exists and imports from `feynmancraft_adk.agent`

### Issue: Import errors
**Solution**: Check that all `__init__.py` files are present and properly configured

### Issue: API key errors
**Solution**: Verify `.env` file exists with valid `GOOGLE_API_KEY`

### Issue: Knowledge base not found
**Solution**: Ensure `data/feynman_kb.json` exists or BigQuery credentials are configured

## Performance Optimization

### Best Practices
- Cache knowledge base queries
- Reuse compiled LaTeX results
- Batch similar requests
- Use appropriate model parameters

### Monitoring
- Check agent execution times in ADK UI
- Monitor token usage in responses
- Track compilation success rates
- Log physics validation results

## Security Considerations

- Never commit API keys or credentials
- Sanitize user inputs before processing
- Validate all generated LaTeX code
- Use environment variables for configuration

## Future Development Areas

### In Progress
- BigQuery integration for production KB
- WebResearchAgent for dynamic search
- Enhanced physics validation rules
- Performance metrics dashboard

### Planned
- Multi-language support
- Advanced diagram types (loops, corrections)
- Real-time collaboration features
- Export to various formats

## Useful Commands

```bash
# Format code
black feynmancraft_adk/
isort feynmancraft_adk/

# Check types
mypy feynmancraft_adk/

# Run linting
pylint feynmancraft_adk/

# Generate requirements
pip freeze > requirements.txt
```

## Resources

- [Google ADK Documentation](https://developers.google.com/agent-development-kit)
- [TikZ-Feynman Manual](http://tikz-feynman.readthedocs.io/)
- [Particle Data Group](https://pdg.lbl.gov/)
- [Project Repository](https://github.com/your-username/feynmancraft-adk)

## Contact

For questions or issues:
- Create an issue in the GitHub repository
- Check existing issues for similar problems
- Include relevant error messages and logs

---

Remember: This is an intelligent, self-learning system designed to continuously improve its diagram generation capabilities through the synergy of static knowledge, dynamic search, and creative generation.