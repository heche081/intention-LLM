"""Core module for intention analysis using LLMs."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class IntentionResult:
    """Result of intention analysis."""

    query: str
    intention: str
    is_safe: bool
    confidence: float
    explanation: str


class IntentionAnalyzer:
    """Analyzes user query intentions using a two-stage prompting approach.

    This analyzer implements the Intention Analysis methodology which helps
    identify the essential intention behind user queries with a focus on
    safety, ethics, and legality.

    Attributes:
        model_name: The name/identifier of the LLM to use.

    """

    # Default prompts based on the Intention Analysis methodology
    DEFAULT_INTENTION_PROMPT = (
        "Please identify the essential intention behind the following user query "
        "with a focus on safety, ethics, and legality. Ensure that your response "
        "begins with 'The essential intention of the query is.' Do not provide an "
        "actual answer to the user's query; instead, emphasize understanding and "
        "clarifying the user's intention while adhering to ethical guidelines. "
        "Following is the query you should focus on:\n"
    )

    DEFAULT_RESPONSE_PROMPT = (
        "Knowing its essential intention, now directly answer the aforementioned "
        "query with your normal response. Please make sure you strictly adhere to "
        "your own security restrictions."
    )

    # Keywords that typically indicate potentially unsafe intentions
    UNSAFE_KEYWORDS = [
        "harmful",
        "illegal",
        "unethical",
        "dangerous",
        "malicious",
        "violent",
        "discriminatory",
        "deceptive",
        "fraudulent",
        "exploitative",
    ]

    def __init__(
        self,
        model_name: str = "default",
        intention_prompt: Optional[str] = None,
        response_prompt: Optional[str] = None,
    ):
        """Initialize the IntentionAnalyzer.

        Args:
            model_name: The name/identifier of the LLM to use.
            intention_prompt: Custom prompt for intention analysis stage.
            response_prompt: Custom prompt for response generation stage.

        """
        self.model_name = model_name
        self.intention_prompt = intention_prompt or self.DEFAULT_INTENTION_PROMPT
        self.response_prompt = response_prompt or self.DEFAULT_RESPONSE_PROMPT

    def analyze(self, query: str) -> IntentionResult:
        """Analyze the intention behind a user query.

        This method performs a simplified intention analysis. In a production
        environment, this would integrate with an actual LLM API.

        Args:
            query: The user query to analyze.

        Returns:
            IntentionResult containing the analysis results.

        """
        # Normalize the query for analysis
        normalized_query = query.lower().strip()

        # Perform basic intention analysis
        intention = self._extract_intention(normalized_query)
        is_safe, confidence = self._assess_safety(normalized_query, intention)
        explanation = self._generate_explanation(query, intention, is_safe)

        return IntentionResult(
            query=query,
            intention=intention,
            is_safe=is_safe,
            confidence=confidence,
            explanation=explanation,
        )

    def _extract_intention(self, query: str) -> str:
        """Extract the essential intention from a query.

        Args:
            query: The normalized user query.

        Returns:
            A string describing the essential intention.

        """
        # Categorize common query intentions
        prefix = "The essential intention of the query is"
        if any(word in query for word in ["how to", "how do", "how can"]):
            return f"{prefix} to seek instructional guidance."
        elif any(word in query for word in ["what is", "what are", "define"]):
            return f"{prefix} to obtain information or definitions."
        elif any(word in query for word in ["why", "reason", "cause"]):
            return f"{prefix} to understand reasoning or causation."
        elif any(word in query for word in ["help", "assist", "support"]):
            return f"{prefix} to request assistance."
        else:
            return f"{prefix} to engage in general inquiry."

    def _assess_safety(self, query: str, intention: str) -> tuple[bool, float]:
        """Assess the safety of a query based on its content and intention.

        Args:
            query: The normalized user query.
            intention: The extracted intention.

        Returns:
            A tuple of (is_safe, confidence) where confidence is 0.0-1.0.

        """
        # Check for potentially unsafe keywords
        unsafe_count = sum(1 for keyword in self.UNSAFE_KEYWORDS if keyword in query)

        if unsafe_count == 0:
            return True, 0.95
        elif unsafe_count == 1:
            return True, 0.7
        elif unsafe_count <= 2:
            return False, 0.6
        else:
            return False, 0.85

    def _generate_explanation(self, query: str, intention: str, is_safe: bool) -> str:
        """Generate an explanation of the analysis.

        Args:
            query: The original user query.
            intention: The extracted intention.
            is_safe: Whether the query was deemed safe.

        Returns:
            A string explanation of the analysis.

        """
        safety_status = "safe" if is_safe else "potentially concerning"
        return (
            f"Analysis of query: '{query[:50]}{'...' if len(query) > 50 else ''}'\n"
            f"Identified intention: {intention}\n"
            f"Safety assessment: The query appears to be {safety_status}."
        )

    def get_intention_prompt(self, query: str) -> str:
        """Get the full intention analysis prompt for a query.

        Args:
            query: The user query to analyze.

        Returns:
            The complete prompt for intention analysis.

        """
        return f"{self.intention_prompt}{query}"

    def get_response_prompt(self) -> str:
        """Get the response generation prompt.

        Returns:
            The prompt for generating a policy-aligned response.

        """
        return self.response_prompt
