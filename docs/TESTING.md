# Testing Documentation

## Running Tests

### All Tests
```bash
# Run all tests
python tests/test_simple.py
python tests/test_improvements.py
python tests/test_agent.py
```

### Individual Tests
```bash
# Basic functionality
python tests/test_simple.py

# Improvement verification
python tests/test_improvements.py
```

## Test Coverage

### test_simple.py
- Exact match testing
- Semantic similarity testing
- Fallback handling
- Edge cases

### test_improvements.py
- Short query matching ("Tell me about CAM")
- Threshold optimization (0.4)
- Natural language variations

### test_agent.py
- Full integration testing
- All Q&A pairs
- Error handling

## Expected Results

All tests should pass with:
- 100% exact match accuracy
- 80-95% semantic match accuracy
- Graceful fallback for unknown questions

## Manual Testing

Test these questions in the UI:

**Exact Matches:**
- "What does the eligibility verification agent (EVA) do?"
- "Tell me about CAM"
- "Tell me about PHIL"

**Semantic Matches:**
- "what is CAM"
- "how does payment posting work"

**Fallback:**
- "What's the weather?"
