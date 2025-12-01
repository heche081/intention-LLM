#!/usr/bin/env python3
"""Basic example demonstrating how to use the IntentionAnalyzer."""

from intention_llm import IntentionAnalyzer


def main():
    """Run basic intention analysis examples."""
    # Initialize the analyzer
    analyzer = IntentionAnalyzer()

    # Example queries to analyze
    queries = [
        "How do I make a website?",
        "What is machine learning?",
        "Why is the sky blue?",
        "Can you help me with my homework?",
        "Tell me about Python programming",
    ]

    print("=" * 60)
    print("Intention-LLM: Basic Usage Example")
    print("=" * 60)

    for query in queries:
        print(f"\nAnalyzing: '{query}'")
        print("-" * 40)

        result = analyzer.analyze(query)

        print(f"Intention: {result.intention}")
        print(f"Is Safe: {result.is_safe}")
        print(f"Confidence: {result.confidence:.2%}")
        print(f"\nFull Explanation:\n{result.explanation}")

    # Show how to get prompts for use with external LLM APIs
    print("\n" + "=" * 60)
    print("Generated Prompts for LLM Integration")
    print("=" * 60)

    sample_query = "How can I improve my code quality?"
    print(f"\nSample Query: '{sample_query}'")
    print("\n--- Intention Analysis Prompt ---")
    print(analyzer.get_intention_prompt(sample_query))
    print("\n--- Response Generation Prompt ---")
    print(analyzer.get_response_prompt())


if __name__ == "__main__":
    main()
