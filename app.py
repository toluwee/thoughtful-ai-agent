"""
Thoughtful AI Customer Support Agent
A conversational AI agent for answering questions about Thoughtful AI's healthcare automation agents.
"""

import streamlit as st
import os
from pathlib import Path
from agent.knowledge_base import KnowledgeBase
from agent.responder import ThoughtfulAIResponder

# Page configuration
st.set_page_config(
    page_title="Thoughtful AI Support Agent",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better chat appearance
st.markdown("""
    <style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .user-message {
        background-color: #e3f2fd;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .agent-message {
        background-color: #f5f5f5;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    .confidence-badge {
        background-color: #4caf50;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_agent():
    """Initialize the AI agent with knowledge base."""
    try:
        # Get the path to the knowledge base
        current_dir = Path(__file__).parent
        kb_path = current_dir / "data" / "knowledge_base.json"

        if not kb_path.exists():
            st.error(f"❌ Knowledge base not found at: {kb_path}")
            st.stop()

        # Load knowledge base and create responder
        kb = KnowledgeBase(str(kb_path))
        responder = ThoughtfulAIResponder(kb, similarity_threshold=0.4)

        return responder
    except Exception as e:
        st.error(f"❌ Error initializing agent: {str(e)}")
        st.stop()


def display_message(role: str, message: str, confidence: float = None):
    """
    Display a chat message with appropriate styling.

    Args:
        role: 'user' or 'agent'
        message: The message text
        confidence: Optional confidence score for agent responses
    """
    if role == "user":
        st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message}
            </div>
        """, unsafe_allow_html=True)
    else:
        confidence_badge = ""
        if confidence and confidence >= 0.6:
            confidence_badge = f'<span class="confidence-badge">{confidence:.0%} match</span>'

        st.markdown(f"""
            <div class="agent-message">
                <strong>🤖 Thoughtful AI Agent:</strong>{confidence_badge}<br>
                {message}
            </div>
        """, unsafe_allow_html=True)


def main():
    """Main application function."""

    # Header
    st.title("🤖 Thoughtful AI Support Agent")
    st.markdown("""
        Welcome! I'm here to answer your questions about **Thoughtful AI's healthcare automation agents**.
        Ask me anything about EVA, CAM, PHIL, and other agents!
    """)

    st.divider()

    # Initialize session state
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'responder' not in st.session_state:
        st.session_state.responder = initialize_agent()

    # Sidebar with sample questions
    with st.sidebar:
        st.header("💡 Sample Questions")
        st.markdown("Try asking:")

        sample_questions = st.session_state.responder.get_all_sample_questions()
        for i, question in enumerate(sample_questions[:5], 1):
            if st.button(f"❓ {question[:50]}...", key=f"sample_{i}", use_container_width=True):
                st.session_state.pending_question = question

        st.divider()

        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        # About section
        st.markdown("---")
        st.caption("**About**")
        st.caption("This agent uses AI-powered question matching to provide accurate information about Thoughtful AI's healthcare automation solutions.")

    # Display chat history
    if st.session_state.messages:
        st.subheader("💬 Conversation")
        for msg in st.session_state.messages:
            display_message(
                msg['role'],
                msg['content'],
                msg.get('confidence')
            )

    # Handle pending question from sidebar
    if hasattr(st.session_state, 'pending_question'):
        user_input = st.session_state.pending_question
        delattr(st.session_state, 'pending_question')
    else:
        user_input = None

    # Chat input
    st.divider()
    user_question = st.chat_input("Ask me about Thoughtful AI's agents...", key="chat_input")

    # Use sidebar question if available, otherwise use chat input
    if user_input or user_question:
        question = user_input or user_question

        # Validate input
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
            return

        # Add user message to history
        st.session_state.messages.append({
            'role': 'user',
            'content': question
        })

        # Get response from agent
        with st.spinner("🤔 Thinking..."):
            try:
                response_data = st.session_state.responder.get_response(question)

                # Add agent response to history
                st.session_state.messages.append({
                    'role': 'agent',
                    'content': response_data['answer'],
                    'confidence': response_data['confidence']
                })

                # Log for debugging (optional)
                if response_data['source'] == 'predefined':
                    st.toast(f"✅ Found answer with {response_data['confidence']:.0%} confidence", icon="✅")
                else:
                    st.toast("💡 Using fallback response", icon="💡")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.messages.append({
                    'role': 'agent',
                    'content': "I encountered an error processing your question. Please try again.",
                    'confidence': 0.0
                })

        # Rerun to update the display
        st.rerun()

    # Show welcome message if no conversation yet
    if not st.session_state.messages:
        st.info("👋 Ask me a question to get started! You can also try the sample questions in the sidebar.")


if __name__ == "__main__":
    main()
