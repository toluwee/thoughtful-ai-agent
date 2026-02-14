# 🤖 Thoughtful AI Customer Support Agent

A conversational AI agent designed to answer questions about Thoughtful AI's healthcare automation agents. Built with intelligent question matching and graceful fallback handling.

## 📋 Overview

This application provides an interactive chat interface where users can ask questions about Thoughtful AI's suite of healthcare automation agents, including:

- **EVA** (Eligibility Verification Agent)
- **CAM** (Claims Processing Agent)
- **PHIL** (Payment Posting Agent)

The agent uses TF-IDF vectorization and cosine similarity to intelligently match user questions with predefined answers, providing accurate responses even when questions are phrased differently.

## ✨ Features

- **🎯 Intelligent Question Matching**: Uses TF-IDF and cosine similarity for semantic understanding
- **💬 Interactive Chat Interface**: Clean, modern web-based UI built with Streamlit
- **🔄 Fallback Handling**: Gracefully handles questions outside the knowledge base
- **📊 Confidence Scoring**: Displays match confidence for transparency
- **🛡️ Robust Error Handling**: Handles edge cases like empty inputs, special characters, and long texts
- **💡 Sample Questions**: Helpful suggestions to guide users
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔍 Conversation History**: Maintains chat context during the session

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**

```bash
cd thoughtful-ai-agent
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the application**

```bash
streamlit run app.py
```

4. **Open your browser**

The application will automatically open in your default browser at `http://localhost:8501`

## 📖 Usage

### Asking Questions

1. Launch the application using `streamlit run app.py`
2. Type your question in the chat input at the bottom
3. Press Enter or click the send button
4. The agent will respond with the most relevant answer

### Sample Questions to Try

- "What does the eligibility verification agent (EVA) do?"
- "Tell me about CAM"
- "How does PHIL work?"
- "What are the benefits of using Thoughtful AI's agents?"
- "Tell me about Thoughtful AI's Agents"

### Using Sidebar Features

- **Sample Questions**: Click any sample question button to auto-fill
- **Clear Chat**: Reset the conversation history
- **About Section**: Learn more about the agent's capabilities

## 🏗️ Architecture

```
thoughtful-ai-agent/
├── app.py                      # Main Streamlit application
├── agent/
│   ├── __init__.py            # Package initializer
│   ├── knowledge_base.py      # Knowledge base loader
│   ├── matcher.py             # Question matching engine
│   └── responder.py           # Response generation logic
├── data/
│   └── knowledge_base.json    # Predefined Q&A dataset
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Component Breakdown

#### 1. **Knowledge Base Layer** (`knowledge_base.py`)
- Loads and manages Q&A pairs from JSON
- Handles file I/O and data validation
- Provides clean interface for data access

#### 2. **Matcher Layer** (`matcher.py`)
- Implements TF-IDF vectorization
- Performs cosine similarity matching
- Includes exact match optimization
- Confidence scoring (threshold: 0.6)

#### 3. **Responder Layer** (`responder.py`)
- Orchestrates matching and response generation
- Implements fallback logic for low-confidence matches
- Handles edge cases and errors
- Formats responses for user display

#### 4. **UI Layer** (`app.py`)
- Streamlit-based chat interface
- Session state management
- Message rendering and styling
- User input handling

## 🔧 Customization

### Modifying the Knowledge Base

Edit `data/knowledge_base.json` to add, remove, or update Q&A pairs:

```json
{
    "questions": [
        {
            "question": "Your question here?",
            "answer": "Your answer here."
        }
    ]
}
```

**Important**: After modifying the knowledge base, restart the application for changes to take effect.

### Adjusting the Similarity Threshold

In `app.py`, modify the threshold parameter (line ~36):

```python
responder = ThoughtfulAIResponder(kb, similarity_threshold=0.6)  # Change 0.6 to your desired value
```

- **Higher threshold** (e.g., 0.8): More strict matching, fewer false positives
- **Lower threshold** (e.g., 0.4): More lenient matching, more results but potentially less accurate

### Customizing the UI

Modify the CSS in `app.py` (lines ~16-44) to change:
- Color schemes
- Message bubble styles
- Spacing and layout
- Font sizes

## 🧪 Testing

### Manual Testing Checklist

- [x] Exact question match returns correct answer
- [x] Similar phrasing returns relevant answer
- [x] Out-of-scope questions trigger fallback
- [x] Empty input shows appropriate message
- [x] Very long inputs are handled gracefully
- [x] Special characters don't break the app
- [x] Conversation history persists during session
- [x] Clear chat button works correctly
- [x] Sample questions populate correctly

### Test Cases

1. **Exact Match**: "What does the eligibility verification agent (EVA) do?"
   - Expected: EVA's predefined answer with 100% confidence

2. **Similar Question**: "Tell me what EVA does"
   - Expected: EVA's answer with >60% confidence

3. **Fallback**: "What's the weather today?"
   - Expected: Fallback response with sample questions

4. **Edge Cases**:
   - Empty string: Warning message
   - Special characters: Handled gracefully
   - Very long input (>500 chars): Truncated and processed

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Core programming language |
| Streamlit | 1.31.0+ | Web UI framework |
| scikit-learn | 1.3.0+ | TF-IDF and cosine similarity |
| NumPy | 1.24.0+ | Numerical computations |

## 🐛 Troubleshooting

### Port Already in Use

If port 8501 is already in use, specify a different port:

```bash
streamlit run app.py --server.port 8502
```

### Module Import Errors

Ensure you're in the correct directory and dependencies are installed:

```bash
pip install -r requirements.txt --upgrade
```

### Knowledge Base Not Found

Verify the file structure:

```bash
ls -la data/knowledge_base.json
```

The `data` folder should be in the same directory as `app.py`.

### Slow Initial Response

The first query may be slower as TF-IDF vectorizes the knowledge base. Subsequent queries will be faster.

## 📝 Code Quality

This project follows Python best practices:

- **PEP 8** compliant code formatting
- **Type hints** for better code clarity
- **Comprehensive docstrings** for all functions and classes
- **Error handling** for robust operation
- **Logging** for debugging and monitoring
- **Modular architecture** for maintainability

## 🚀 Future Enhancements

Potential improvements for future versions:

- [ ] Add persistent conversation storage (database)
- [ ] Implement user feedback mechanism
- [ ] Upgrade to sentence-transformers for better semantic understanding
- [ ] Add multi-language support
- [ ] Include analytics dashboard
- [ ] Add unit tests and CI/CD pipeline
- [ ] Deploy to cloud platform (Streamlit Cloud, Heroku, etc.)
- [ ] Add voice input/output capabilities
- [ ] Implement user authentication
- [ ] Add export conversation feature

## 📄 License

This project is created as a demonstration for Thoughtful AI.

## 🤝 Contributing

This is a demonstration project. For production use:

1. Add comprehensive unit tests
2. Implement CI/CD pipeline
3. Add database for conversation persistence
4. Enhance security measures
5. Add monitoring and analytics

## 👥 Authors

Built as a technical demonstration for Thoughtful AI's customer support automation capabilities.

## 📞 Support

For questions or issues:

1. Check the Troubleshooting section
2. Review the code comments and docstrings
3. Examine the console logs for error details

---

**Built with ❤️ for Thoughtful AI**
