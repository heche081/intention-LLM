# intention-LLM

A Python library for analyzing user query intentions using Large Language Models (LLMs).

## Overview

Intention-LLM implements an intention analysis methodology that helps identify the essential intention behind user queries with a focus on safety, ethics, and legality. This approach is based on research showing that analyzing user intentions can help defend LLMs against jailbreak attacks and improve response quality.

The library uses a two-stage prompting approach:
1. **Intention Analysis**: Identifies the essential intention behind a user query
2. **Policy-Aligned Response**: Generates responses that adhere to safety guidelines

## Installation

```bash
# Clone the repository
git clone https://github.com/heche081/intention-LLM.git
cd intention-LLM

# Install in development mode
pip install -e .

# Or install with optional dependencies
pip install -e ".[dev]"  # For development tools
pip install -e ".[openai]"  # For OpenAI integration
```

## Quick Start

```python
from intention_llm import IntentionAnalyzer

# Initialize the analyzer
analyzer = IntentionAnalyzer()

# Analyze a user query
result = analyzer.analyze("How do I learn Python programming?")

print(f"Intention: {result.intention}")
print(f"Is Safe: {result.is_safe}")
print(f"Confidence: {result.confidence:.2%}")
print(f"Explanation: {result.explanation}")
```

## Features

- **Intention Extraction**: Automatically categorizes user query intentions
- **Safety Assessment**: Evaluates queries for potentially harmful content
- **Customizable Prompts**: Configure analysis and response prompts
- **LLM Integration Ready**: Get prompts formatted for use with any LLM API

## API Reference

### IntentionAnalyzer

The main class for performing intention analysis.

```python
from intention_llm import IntentionAnalyzer

# Default initialization
analyzer = IntentionAnalyzer()

# Custom initialization
analyzer = IntentionAnalyzer(
    model_name="gpt-4",
    intention_prompt="Your custom intention prompt...",
    response_prompt="Your custom response prompt..."
)
```

#### Methods

- `analyze(query: str) -> IntentionResult`: Analyze a user query
- `get_intention_prompt(query: str) -> str`: Get the full intention analysis prompt
- `get_response_prompt() -> str`: Get the response generation prompt

### IntentionResult

A dataclass containing analysis results.

```python
@dataclass
class IntentionResult:
    query: str        # The original query
    intention: str    # The identified intention
    is_safe: bool     # Safety assessment result
    confidence: float # Confidence score (0.0-1.0)
    explanation: str  # Human-readable explanation
```

## Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=intention_llm --cov-report=term-missing
```

## Example

See the `examples/` directory for usage examples:

```bash
# Run the basic usage example
python examples/basic_usage.py
```

## License

MIT License

## References

This library is inspired by research on intention analysis for LLM safety:

- Zhang, Y., Ding, L., Zhang, L., & Tao, D. (2024). "Intention Analysis Prompting Makes Large Language Models a Good Jailbreak Defender." arXiv:2401.06561