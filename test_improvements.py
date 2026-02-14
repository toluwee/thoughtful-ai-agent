"""
Test the improvements to question matching
"""

from pathlib import Path
from agent.knowledge_base import KnowledgeBase
from agent.responder import ThoughtfulAIResponder

# Initialize agent with new settings
kb_path = Path(__file__).parent / "data" / "knowledge_base.json"
kb = KnowledgeBase(str(kb_path))
responder = ThoughtfulAIResponder(kb, similarity_threshold=0.4)

print("=" * 60)
print("TESTING IMPROVEMENTS")
print("=" * 60)
print(f"\nKnowledge Base: {len(kb)} Q&A pairs (was 5)")
print(f"Threshold: 0.4 (was 0.6)\n")

# Test the problematic question
test_questions = [
    "Tell me about CAM",
    "Tell me about EVA",
    "Tell me about PHIL",
    "what is CAM",
]

for question in test_questions:
    print(f"\n{'-' * 60}")
    print(f"Question: \"{question}\"")
    response = responder.get_response(question)
    print(f"Source: {response['source']}")
    print(f"Confidence: {response['confidence']:.2%}")
    if response['matched_question']:
        print(f"Matched: \"{response['matched_question']}\"")
    status = "[PASS]" if response['source'] == 'predefined' else "[FALLBACK]"
    print(status)

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
