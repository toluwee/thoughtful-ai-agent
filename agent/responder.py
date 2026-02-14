"""
Responder Module
Handles response generation with fallback logic for out-of-scope questions.
"""

from typing import Dict, List, Optional
import logging
from .matcher import QuestionMatcher
from .knowledge_base import KnowledgeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThoughtfulAIResponder:
    """
    Generates responses for user questions about Thoughtful AI.
    Uses predefined answers for known questions and fallback responses otherwise.
    """

    def __init__(self, knowledge_base: KnowledgeBase, similarity_threshold: float = 0.6):
        """
        Initialize the responder.

        Args:
            knowledge_base: KnowledgeBase instance with Q&A pairs
            similarity_threshold: Threshold for question matching (0.0-1.0)
        """
        self.kb = knowledge_base
        self.threshold = similarity_threshold

        # Extract questions and answers
        qa_pairs = self.kb.get_qa_pairs()
        questions = [qa['question'] for qa in qa_pairs]
        answers = [qa['answer'] for qa in qa_pairs]

        # Initialize matcher
        self.matcher = QuestionMatcher(questions, answers, threshold=similarity_threshold)

        # Fallback responses for different scenarios
        self.fallback_responses = {
            'no_match': (
                "I'm not sure about that specific question. I'm specialized in answering questions "
                "about Thoughtful AI's healthcare automation agents, including EVA (Eligibility Verification Agent), "
                "CAM (Claims Processing Agent), and PHIL (Payment Posting Agent).\n\n"
                "Here are some questions I can help with:\n{sample_questions}"
            ),
            'empty_input': "Please ask me a question about Thoughtful AI's agents!",
            'error': "I encountered an error processing your question. Please try again or rephrase your question."
        }

        logger.info(f"ThoughtfulAIResponder initialized with {len(questions)} Q&A pairs")

    def get_response(self, user_question: str) -> Dict[str, any]:
        """
        Generate a response for the user's question.

        Args:
            user_question: The question asked by the user

        Returns:
            Dictionary containing:
                - 'answer': The response text
                - 'confidence': Confidence score (0.0-1.0)
                - 'matched_question': The matched question if found
                - 'source': 'predefined' or 'fallback'
        """
        # Handle empty input
        if not user_question or not user_question.strip():
            logger.warning("Empty question received")
            return {
                'answer': self.fallback_responses['empty_input'],
                'confidence': 0.0,
                'matched_question': None,
                'source': 'fallback'
            }

        # Sanitize input
        user_question = user_question.strip()

        # Handle very long inputs (truncate with warning)
        max_length = 500
        if len(user_question) > max_length:
            logger.warning(f"Question truncated from {len(user_question)} to {max_length} characters")
            user_question = user_question[:max_length] + "..."

        try:
            # Try to find a match
            answer, confidence, matched_question = self.matcher.find_best_match(user_question)

            if answer:
                # Found a good match
                logger.info(f"Returning predefined answer with confidence {confidence:.3f}")
                return {
                    'answer': answer,
                    'confidence': confidence,
                    'matched_question': matched_question,
                    'source': 'predefined'
                }
            else:
                # No good match found - use fallback
                logger.info(f"No match found (confidence: {confidence:.3f}), using fallback")
                sample_questions = self._get_sample_questions(num_samples=3)
                fallback_answer = self.fallback_responses['no_match'].format(
                    sample_questions=sample_questions
                )
                return {
                    'answer': fallback_answer,
                    'confidence': confidence,
                    'matched_question': None,
                    'source': 'fallback'
                }

        except Exception as e:
            # Handle any unexpected errors
            logger.error(f"Error generating response: {e}")
            return {
                'answer': self.fallback_responses['error'],
                'confidence': 0.0,
                'matched_question': None,
                'source': 'error'
            }

    def _get_sample_questions(self, num_samples: int = 3) -> str:
        """
        Get formatted sample questions from the knowledge base.

        Args:
            num_samples: Number of sample questions to return

        Returns:
            Formatted string of sample questions
        """
        questions = self.matcher.get_all_questions()[:num_samples]
        return "\n".join([f"  • {q}" for q in questions])

    def get_all_sample_questions(self) -> List[str]:
        """
        Get all sample questions from the knowledge base.

        Returns:
            List of all predefined questions
        """
        return self.matcher.get_all_questions()

    def update_threshold(self, new_threshold: float) -> None:
        """
        Update the similarity matching threshold.

        Args:
            new_threshold: New threshold value (0.0-1.0)
        """
        self.threshold = new_threshold
        self.matcher.update_threshold(new_threshold)
        logger.info(f"Updated response threshold to {new_threshold}")
