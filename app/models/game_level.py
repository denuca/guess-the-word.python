"""
Game difficulty levels for Guess The Word game.

This module defines the GameLevel enumeration which represents different difficulty
levels in the Guess The Word word-guessing game. Each level has specific constraints on
word length and maximum number of attempts allowed.

Example:
    >>> from app.models.game_level import GameLevel
    >>> level = GameLevel.MEDIUM
    >>> print(f"Level: {level.name}, Word Length: {level.word_length}")
    Level: MEDIUM, Word Length: 6

Attributes:
    EASY (GameLevel): 4-letter words with 8 attempts
    MEDIUM (GameLevel): 6-letter words with 6 attempts  
    HARD (GameLevel): 8-letter words with 4 attempts
"""

from enum import Enum
from typing import Dict, Any


class GameLevel(Enum):
    """
    Enumeration representing difficulty levels for the Guess The Word game.
    
    Each level defines the word length and maximum attempts allowed for that
    difficulty setting. The enum values are tuples of (word_length, max_attempts).
    
    Attributes:
        EASY: Beginner level with 4-letter words and 8 attempts
        MEDIUM: Intermediate level with 6-letter words and 6 attempts
        HARD: Expert level with 8-letter words and 4 attempts
    
    Example:
        >>> level = GameLevel.EASY
        >>> print(f"Word length: {level.word_length}")
        Word length: 4
        >>> print(f"Max attempts: {level.max_attempts}")
        Max attempts: 8
    """
    
    EASY = (4, 8)
    MEDIUM = (6, 6)
    HARD = (8, 4)
    
    def __init__(self, word_length: int, max_attempts: int) -> None:
        """
        Initialize a GameLevel with word length and maximum attempts.
        
        Args:
            word_length (int): Number of letters in words for this level
            max_attempts (int): Maximum number of guesses allowed
        """
        self.word_length = word_length
        self.max_attempts = max_attempts
    
    @classmethod
    def from_string(cls, level_str: str) -> 'GameLevel':
        """
        Create a GameLevel instance from a string representation.
        
        Args:
            level_str (str): String representation of the level (case-insensitive)
                           Valid values: 'EASY', 'MEDIUM', 'HARD'
        
        Returns:
            GameLevel: The corresponding GameLevel enum value
            
        Example:
            >>> level = GameLevel.from_string('easy')
            >>> level == GameLevel.EASY
            True
            >>> level = GameLevel.from_string('INVALID')
            >>> level == GameLevel.MEDIUM  # Default fallback
            True
        """
        try:
            return cls[level_str.upper()]
        except KeyError:
            return cls.MEDIUM  # Default fallback for invalid input
    
    def __str__(self) -> str:
        """
        Return string representation of the GameLevel.
        
        Returns:
            str: The name of the level (e.g., 'EASY', 'MEDIUM', 'HARD')
        """
        return self.name
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert GameLevel to dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary containing level information with keys:
                - name (str): Level name
                - word_length (int): Number of letters in words
                - max_attempts (int): Maximum attempts allowed
                
        Example:
            >>> level = GameLevel.MEDIUM
            >>> level.to_dict()
            {'name': 'MEDIUM', 'word_length': 6, 'max_attempts': 6}
        """
        return {
            'name': self.name,
            'word_length': self.word_length,
            'max_attempts': self.max_attempts
        }
