"""
Knowledge Base Module
Handles loading and managing the predefined Q&A dataset for Thoughtful AI.
"""

import json
import os
from typing import List, Dict, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Manages the predefined question-answer pairs for Thoughtful AI agents."""

    def __init__(self, kb_path: str):
        """
        Initialize the knowledge base.

        Args:
            kb_path: Path to the JSON file containing Q&A pairs

        Raises:
            FileNotFoundError: If the knowledge base file doesn't exist
            json.JSONDecodeError: If the JSON file is malformed
        """
        self.kb_path = kb_path
        self.questions: List[Dict[str, str]] = []
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        """Load the knowledge base from JSON file."""
        try:
            if not os.path.exists(self.kb_path):
                raise FileNotFoundError(f"Knowledge base file not found: {self.kb_path}")

            with open(self.kb_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.questions = data.get('questions', [])

            if not self.questions:
                logger.warning("Knowledge base loaded but contains no questions")
            else:
                logger.info(f"Successfully loaded {len(self.questions)} questions from knowledge base")

        except FileNotFoundError as e:
            logger.error(f"Knowledge base file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in knowledge base: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading knowledge base: {e}")
            raise

    def get_all_questions(self) -> List[str]:
        """
        Get all questions from the knowledge base.

        Returns:
            List of question strings
        """
        return [q['question'] for q in self.questions]

    def get_answer(self, question: str) -> Optional[str]:
        """
        Get answer for an exact question match.

        Args:
            question: The question to look up

        Returns:
            The answer if found, None otherwise
        """
        for qa_pair in self.questions:
            if qa_pair['question'].lower() == question.lower():
                return qa_pair['answer']
        return None

    def get_qa_pairs(self) -> List[Dict[str, str]]:
        """
        Get all question-answer pairs.

        Returns:
            List of dictionaries containing 'question' and 'answer' keys
        """
        return self.questions

    def __len__(self) -> int:
        """Return the number of Q&A pairs in the knowledge base."""
        return len(self.questions)

    def __repr__(self) -> str:
        """String representation of the knowledge base."""
        return f"KnowledgeBase(questions={len(self.questions)}, path='{self.kb_path}')"
