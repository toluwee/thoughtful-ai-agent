"""
Quick test script to verify agent functionality
"""

from pathlib import Path
from agent.knowledge_base import KnowledgeBase
from agent.responder import ThoughtfulAIResponder


def test_agent():
    """Test the agent with various inputs."""
    print("=" * 60)
    print("THOUGHTFUL AI AGENT - FUNCTIONALITY TEST")
    print("=" * 60)

    # Initialize agent
    kb_path = Path(__file__).parent / "data" / "knowledge_base.json"
    kb = KnowledgeBase(str(kb_path))
    responder = ThoughtfulAIResponder(kb, similarity_threshold=0.6)

    print(f"\n✅ Agent initialized with {len(kb)} Q&A pairs\n")

    # Test cases
    test_cases = [
        {
            "name": "Exact Match Test",
            "question": "What does the eligibility verification agent (EVA) do?",
            "expected": "predefined"
        },
        {
            "name": "Similar Question Test",
            "question": "Tell me what EVA does",
            "expected": "predefined"
        },
        {
            "name": "Another Similar Test",
            "question": "How does payment posting work?",
            "expected": "predefined"
        },
        {
            "name": "Fallback Test",
            "question": "What's the weather today?",
            "expected": "fallback"
        },
        {
            "name": "Empty Input Test",
            "question": "",
            "expected": "fallback"
        }
    ]

    # Run tests
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 60}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'─' * 60}")
        print(f"Question: \"{test['question']}\"")

        response = responder.get_response(test['question'])

        print(f"\nSource: {response['source']}")
        print(f"Confidence: {response['confidence']:.2%}")
        if response['matched_question']:
            print(f"Matched: \"{response['matched_question']}\"")
        print(f"\nAnswer: {response['answer'][:150]}...")

        # Verify expectation
        if response['source'] == test['expected']:
            print(f"\n✅ PASS - Got expected source: {test['expected']}")
        else:
            print(f"\n❌ FAIL - Expected {test['expected']}, got {response['source']}")

    print("\n" + "=" * 60)
    print("TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_agent()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
