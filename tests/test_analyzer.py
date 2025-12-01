"""Tests for the IntentionAnalyzer class."""


from intention_llm import IntentionAnalyzer
from intention_llm.analyzer import IntentionResult


class TestIntentionAnalyzer:
    """Test suite for IntentionAnalyzer."""

    def test_initialization_default(self):
        """Test default initialization."""
        analyzer = IntentionAnalyzer()
        assert analyzer.model_name == "default"
        assert analyzer.intention_prompt == IntentionAnalyzer.DEFAULT_INTENTION_PROMPT
        assert analyzer.response_prompt == IntentionAnalyzer.DEFAULT_RESPONSE_PROMPT

    def test_initialization_custom(self):
        """Test initialization with custom parameters."""
        custom_intention = "Custom intention prompt"
        custom_response = "Custom response prompt"
        analyzer = IntentionAnalyzer(
            model_name="gpt-4",
            intention_prompt=custom_intention,
            response_prompt=custom_response,
        )
        assert analyzer.model_name == "gpt-4"
        assert analyzer.intention_prompt == custom_intention
        assert analyzer.response_prompt == custom_response

    def test_analyze_returns_intention_result(self):
        """Test that analyze returns an IntentionResult."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("How do I learn Python?")
        assert isinstance(result, IntentionResult)

    def test_analyze_how_to_query(self):
        """Test analysis of 'how to' queries."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("How do I make a website?")
        assert "instructional guidance" in result.intention.lower()
        assert result.is_safe is True
        assert result.confidence > 0.5

    def test_analyze_what_is_query(self):
        """Test analysis of 'what is' queries."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("What is machine learning?")
        intention_lower = result.intention.lower()
        assert "information" in intention_lower or "definition" in intention_lower
        assert result.is_safe is True

    def test_analyze_why_query(self):
        """Test analysis of 'why' queries."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("Why is the sky blue?")
        intention_lower = result.intention.lower()
        assert "reasoning" in intention_lower or "causation" in intention_lower
        assert result.is_safe is True

    def test_analyze_help_query(self):
        """Test analysis of help requests."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("Can you help me with my homework?")
        assert "assistance" in result.intention.lower()
        assert result.is_safe is True

    def test_analyze_general_query(self):
        """Test analysis of general queries."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("Tell me about Python")
        assert "inquiry" in result.intention.lower()
        assert result.is_safe is True

    def test_safety_assessment_safe_query(self):
        """Test that safe queries are marked as safe."""
        analyzer = IntentionAnalyzer()
        result = analyzer.analyze("What is the capital of France?")
        assert result.is_safe is True
        assert result.confidence >= 0.7

    def test_safety_assessment_unsafe_keywords(self):
        """Test that queries with unsafe keywords are flagged appropriately."""
        analyzer = IntentionAnalyzer()
        # Query with multiple unsafe keywords should be flagged
        result = analyzer.analyze("harmful illegal unethical dangerous")
        assert result.is_safe is False
        assert result.confidence >= 0.6

    def test_get_intention_prompt(self):
        """Test getting the full intention prompt."""
        analyzer = IntentionAnalyzer()
        query = "Test query"
        prompt = analyzer.get_intention_prompt(query)
        assert query in prompt
        assert analyzer.intention_prompt in prompt

    def test_get_response_prompt(self):
        """Test getting the response prompt."""
        analyzer = IntentionAnalyzer()
        prompt = analyzer.get_response_prompt()
        assert prompt == analyzer.response_prompt

    def test_explanation_contains_query_info(self):
        """Test that explanation contains relevant query information."""
        analyzer = IntentionAnalyzer()
        query = "How do I cook pasta?"
        result = analyzer.analyze(query)
        assert query[:20] in result.explanation or "pasta" in result.explanation.lower()

    def test_explanation_truncates_long_queries(self):
        """Test that very long queries are truncated in explanation."""
        analyzer = IntentionAnalyzer()
        long_query = "This is a very long query " * 10
        result = analyzer.analyze(long_query)
        assert "..." in result.explanation


class TestIntentionResult:
    """Test suite for IntentionResult dataclass."""

    def test_intention_result_attributes(self):
        """Test that IntentionResult has all expected attributes."""
        result = IntentionResult(
            query="Test query",
            intention="Test intention",
            is_safe=True,
            confidence=0.95,
            explanation="Test explanation",
        )
        assert result.query == "Test query"
        assert result.intention == "Test intention"
        assert result.is_safe is True
        assert result.confidence == 0.95
        assert result.explanation == "Test explanation"
