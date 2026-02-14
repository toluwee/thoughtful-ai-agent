"""
Simple test script for Windows console (no emojis)
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

    print(f"\n[OK] Agent initialized with {len(kb)} Q&A pairs\n")

    # Test cases
    test_cases = [
        {
            "name": "Exact Match Test",
            "question": "What does the eligibility verification agent (EVA) do?",
        },
        {
            "name": "Similar Question Test",
            "question": "Tell me what EVA does",
        },
        {
            "name": "Another Similar Test",
            "question": "How does payment posting work?",
        },
        {
            "name": "Fallback Test",
            "question": "What's the weather today?",
        }
    ]

    # Run tests
    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'-' * 60}")
        print(f"TEST {i}: {test['name']}")
        print(f"{'-' * 60}")
        print(f"Question: \"{test['question']}\"")

        try:
            response = responder.get_response(test['question'])

            print(f"\nSource: {response['source']}")
            print(f"Confidence: {response['confidence']:.2%}")
            if response['matched_question']:
                print(f"Matched: \"{response['matched_question']}\"")

            answer_preview = response['answer'][:200]
            if len(response['answer']) > 200:
                answer_preview += "..."
            print(f"\nAnswer: {answer_preview}")

            # Check if response is valid
            if response['answer']:
                print(f"\n[PASS]")
                passed += 1
            else:
                print(f"\n[FAIL] - No answer returned")
                failed += 1

        except Exception as e:
            print(f"\n[ERROR] {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"TESTING COMPLETE: {passed} passed, {failed} failed")
    print("=" * 60)

    return passed, failed


if __name__ == "__main__":
    try:
        passed, failed = test_agent()
        exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        exit(1)
