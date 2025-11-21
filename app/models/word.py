"""
Word model with guess evaluation logic for Q-Words game.

This module contains the Word class which represents a target word in the game
and provides methods for evaluating player guesses against it. The evaluation
follows Wordle-style feedback rules.

Example:
    >>> from app.models.word import Word
    >>> word = Word("PYTHON")
    >>> feedback = word.evaluate_guess("ANIMAL")
    >>> print(feedback)  # 'x?xxxx' - only 'N' is in wrong position
    x?xxxx

Feedback Legend:
    '+': Correct letter in correct position (green in Wordle)
    '?': Correct letter in wrong position (yellow in Wordle)  
    'x': Letter not in the target word (gray in Wordle)
"""

from typing import List, Dict, Any


class Word:
    """
    Represents a target word in the Q-Words game with guess evaluation capabilities.
    
    This class encapsulates a target word and provides methods to evaluate player
    guesses against it, returning feedback in the form of symbols indicating
    correctness and position accuracy.
    
    Attributes:
        word (str): The target word in uppercase
        length (int): Length of the target word
    
    Example:
        >>> word = Word("HELLO")
        >>> word.word
        'HELLO'
        >>> word.length
        5
        >>> word.evaluate_guess("HELP")
        '+++x'
    """
    
    def __init__(self, word: str) -> None:
        """
        Initialize a Word instance with the target word.
        
        Args:
            word (str): The target word for the game (case-insensitive)
            
        Raises:
            ValueError: If word is empty or None
            
        Example:
            >>> word = Word("python")
            >>> word.word
            'PYTHON'
        """
        if not word:
            raise ValueError("Word cannot be empty")
        self.word = word.upper()
        self.length = len(self.word)
    
    def evaluate_guess(self, guess: str) -> str:
        """
        Evaluate a player's guess against the target word and return feedback.
        
        The evaluation follows these rules:
        1. '+' for correct letter in correct position
        2. '?' for correct letter in wrong position  
        3. 'x' for letter not in the target word
        
        The algorithm handles duplicate letters correctly by ensuring each letter
        in the target word can only be matched once.
        
        Args:
            guess (str): The player's guess (case-insensitive)
            
        Returns:
            str: Feedback string with same length as target word, containing
                 only '+', '?', and 'x' characters
                 
        Example:
            >>> word = Word("HELLO")
            >>> word.evaluate_guess("HELP")
            '+++x'
            >>> word.evaluate_guess("LLAMA")  # Handles duplicates correctly
            '?x?xx'
            >>> word.evaluate_guess("WORLD")
            'x?x?x'
        """
        if not guess:
            return 'x' * self.length
        
        guess = guess.upper()
        feedback = []
        target_chars = list(self.word)
        guess_chars = list(guess)
        
        # First pass: mark exact matches and remove them from consideration
        for i in range(min(len(guess_chars), len(target_chars))):
            if guess_chars[i] == target_chars[i]:
                feedback.append('+')
                target_chars[i] = None  # Mark as used
                guess_chars[i] = None   # Mark as processed
            else:
                feedback.append('?')    # Placeholder, will be updated in second pass
        
        # Pad with 'x' if guess is shorter than target
        while len(feedback) < self.length:
            feedback.append('x')
        
        # Second pass: check for wrong positions among remaining characters
        for i in range(len(feedback)):
            if feedback[i] == '?' and guess_chars[i] is not None:
                if guess_chars[i] in target_chars:
                    # Remove first occurrence from target_chars to handle duplicates
                    target_chars[target_chars.index(guess_chars[i])] = None
                    feedback[i] = '?'  # Correct letter, wrong position
                else:
                    feedback[i] = 'x'  # Letter not in word
        
        return ''.join(feedback[:self.length])
    
    def is_correct_guess(self, guess: str) -> bool:
        """
        Check if the guess matches the target word exactly.
        
        Args:
            guess (str): The player's guess (case-insensitive)
            
        Returns:
            bool: True if guess matches target word exactly, False otherwise
            
        Example:
            >>> word = Word("HELLO")
            >>> word.is_correct_guess("hello")
            True
            >>> word.is_correct_guess("HELP")
            False
        """
        return guess.upper() == self.word
    
    def __str__(self) -> str:
        """
        Return string representation of the Word.
        
        Returns:
            str: The target word in uppercase
        """
        return self.word
    
    def __eq__(self, other) -> bool:
        """
        Check equality with another Word instance or string.
        
        Args:
            other: Another Word instance or string to compare with
            
        Returns:
            bool: True if words are equal (case-insensitive), False otherwise
            
        Example:
            >>> word1 = Word("HELLO")
            >>> word2 = Word("hello")
            >>> word1 == word2
            True
            >>> word1 == "HELLO"
            True
        """
        if isinstance(other, Word):
            return self.word == other.word
        return self.word == str(other).upper()
    
    def __repr__(self) -> str:
        """
        Return detailed string representation for debugging.
        
        Returns:
            str: Detailed representation including class name and word
        """
        return f"Word('{self.word}')"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Word to dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: Dictionary containing word information with keys:
                - word (str): The target word
                - length (int): Length of the word
                
        Example:
            >>> word = Word("HELLO")
            >>> word.to_dict()
            {'word': 'HELLO', 'length': 5}
        """
        return {
            'word': self.word,
            'length': self.length
        }
