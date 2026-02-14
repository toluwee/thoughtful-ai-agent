"""
Question Matcher Module
Implements intelligent question matching using TF-IDF and cosine similarity.
"""

from typing import Tuple, Optional
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuestionMatcher:
    """
    Matches user questions to predefined questions using TF-IDF and cosine similarity.
    """

    def __init__(self, questions: list, answers: list, threshold: float = 0.6):
        """
        Initialize the question matcher.

        Args:
            questions: List of predefined questions
            answers: List of corresponding answers
            threshold: Similarity threshold (0.0-1.0) for matching confidence

        Raises:
            ValueError: If questions and answers lists don't match in length
        """
        if len(questions) != len(answers):
            raise ValueError("Questions and answers must have the same length")

        if not questions:
            raise ValueError("Questions list cannot be empty")

        self.questions = questions
        self.answers = answers
        self.threshold = threshold
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')

        try:
            # Fit vectorizer on predefined questions
            self.question_vectors = self.vectorizer.fit_transform(questions)
            logger.info(f"Initialized matcher with {len(questions)} questions, threshold={threshold}")
        except Exception as e:
            logger.error(f"Error initializing TF-IDF vectorizer: {e}")
            raise

    def find_best_match(self, user_question: str) -> Tuple[Optional[str], float, Optional[str]]:
        """
        Find the best matching answer for a user question.

        Args:
            user_question: The question asked by the user

        Returns:
            Tuple of (answer, confidence_score, matched_question)
            Returns (None, 0.0, None) if no good match found
        """
        if not user_question or not user_question.strip():
            logger.warning("Empty question provided to matcher")
            return None, 0.0, None

        try:
            # First try exact match (case-insensitive) for perfect accuracy
            user_question_lower = user_question.lower().strip()
            for i, question in enumerate(self.questions):
                if question.lower().strip() == user_question_lower:
                    logger.info(f"Exact match found: '{question}'")
                    return self.answers[i], 1.0, question

            # If no exact match, use TF-IDF similarity
            user_vector = self.vectorizer.transform([user_question])
            similarities = cosine_similarity(user_vector, self.question_vectors)[0]

            # Find the highest similarity score
            best_match_idx = np.argmax(similarities)
            best_score = similarities[best_match_idx]

            logger.info(f"Best similarity match: score={best_score:.3f}, question='{self.questions[best_match_idx]}'")

            # Return match only if above threshold
            if best_score >= self.threshold:
                return self.answers[best_match_idx], float(best_score), self.questions[best_match_idx]
            else:
                logger.info(f"No match above threshold {self.threshold}")
                return None, float(best_score), None

        except Exception as e:
            logger.error(f"Error in question matching: {e}")
            return None, 0.0, None

    def get_all_questions(self) -> list:
        """Return all predefined questions."""
        return self.questions.copy()

    def update_threshold(self, new_threshold: float) -> None:
        """
        Update the similarity threshold.

        Args:
            new_threshold: New threshold value (0.0-1.0)

        Raises:
            ValueError: If threshold is not between 0 and 1
        """
        if not 0.0 <= new_threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")

        self.threshold = new_threshold
        logger.info(f"Updated threshold to {new_threshold}")
