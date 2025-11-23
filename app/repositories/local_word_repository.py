"""
Local file-based word repository for Guess The Word game.

This module provides the LocalWordRepository class which manages word data
loaded from local text files organized by difficulty level. It serves as
the data access layer for word retrieval in the game.

Example:
    >>> from app.repositories.local_word_repository import LocalWordRepository
    >>> from app.models.game_level import GameLevel
    >>> repo = LocalWordRepository('/path/to/resources')
    >>> word = repo.get_random_word_by_level(GameLevel.EASY)
    >>> print(f"Random easy word: {word}")
    Random easy word: BIRD

File Structure:
    The repository expects the following files in the resources directory:
    - words-easy.txt: 4-letter words for easy difficulty
    - words.txt: 6-letter words for medium difficulty  
    - words-hard.txt: 8-letter words for hard difficulty
"""

import random
import os
from typing import List, Optional
from app.models.game_level import GameLevel


class LocalWordRepository:
    """
    Repository for managing word data from local text files.
    
    This class loads words from different difficulty-specific files and provides
    random word selection functionality. It implements fallback mechanisms for
    missing files and empty word lists to ensure the game always has words available.
    
    Attributes:
        resources_path (str): Path to the directory containing word files
        easy_words (List[str]): List of words for easy difficulty
        medium_words (List[str]): List of words for medium difficulty
        hard_words (List[str]): List of words for hard difficulty
    
    Example:
        >>> repo = LocalWordRepository('/app/resources')
        >>> easy_count = repo.get_word_count_by_level(GameLevel.EASY)
        >>> print(f"Easy words available: {easy_count}")
        Easy words available: 37
    """
    
    def __init__(self, resources_path: str) -> None:
        """
        Initialize the repository and load words from files.
        
        Args:
            resources_path (str): Path to directory containing word files
                                 Expected files: words-easy.txt, words.txt, words-hard.txt
        
        Example:
            >>> repo = LocalWordRepository('/app/resources')
            >>> len(repo.easy_words) > 0
            True
        """
        self.resources_path = resources_path
        self.easy_words: List[str] = []
        self.medium_words: List[str] = []
        self.hard_words: List[str] = []
        self._load_words()
    
    def _load_words(self) -> None:
        """
        Load words from all difficulty-specific files into memory.
        
        This method is called during initialization to populate the word lists
        from the corresponding text files. It handles file loading errors gracefully
        by falling back to default words.
        """
        self.easy_words = self._load_words_from_file("words-easy.txt")
        self.medium_words = self._load_words_from_file("words.txt")
        self.hard_words = self._load_words_from_file("words-hard.txt")
    
    def _load_words_from_file(self, filename: str) -> List[str]:
        """
        Load words from a specific file in the resources directory.
        
        This method reads a text file line by line, processes each word by
        converting to uppercase and filtering out non-alphabetic entries,
        and returns a list of valid words.
        
        Args:
            filename (str): Name of the file to load (relative to resources_path)
            
        Returns:
            List[str]: List of words loaded from the file, or list with default
                      word if file loading fails
                      
        Example:
            >>> repo = LocalWordRepository('/app/resources')
            >>> words = repo._load_words_from_file('words-easy.txt')
            >>> all(word.isupper() and word.isalpha() for word in words)
            True
        """
        words = []
        file_path = os.path.join(self.resources_path, filename)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    word = line.strip().upper()
                    if word and word.isalpha():  # Skip empty lines and non-alphabetic
                        words.append(word)
        except FileNotFoundError:
            # Fallback words if file not found
            words.append(self._get_default_word(filename))
        except Exception as e:
            print(f"Error loading words from {filename}: {e}")
            words.append(self._get_default_word(filename))
        
        return words
    
    def get_random_word_by_level(self, level: GameLevel) -> str:
        """
        Retrieve a random word for the specified game difficulty level.
        
        This method selects a random word from the appropriate word list based
        on the difficulty level. If the word list is empty, it returns a default
        word to ensure the game can continue.
        
        Args:
            level (GameLevel): The game difficulty level (EASY, MEDIUM, or HARD)
            
        Returns:
            str: A random word appropriate for the specified level, guaranteed
                 to be non-empty and in uppercase
                 
        Example:
            >>> repo = LocalWordRepository('/app/resources')
            >>> word = repo.get_random_word_by_level(GameLevel.MEDIUM)
            >>> len(word) > 0 and word.isupper()
            True
        """
        if level == GameLevel.EASY:
            words = self.easy_words
        elif level == GameLevel.HARD:
            words = self.hard_words
        else:  # MEDIUM
            words = self.medium_words
        
        if not words:
            return self._get_default_word_by_level(level)
        
        return random.choice(words)
    
    def get_word_count_by_level(self, level: GameLevel) -> int:
        """
        Get the number of available words for a specific difficulty level.
        
        This method returns the count of words available for the given difficulty
        level, which can be useful for statistics or debugging purposes.
        
        Args:
            level (GameLevel): The game difficulty level
            
        Returns:
            int: Number of words available for the specified level
            
        Example:
            >>> repo = LocalWordRepository('/app/resources')
            >>> count = repo.get_word_count_by_level(GameLevel.EASY)
            >>> count >= 1  # At least default word available
            True
        """
        if level == GameLevel.EASY:
            return len(self.easy_words)
        elif level == GameLevel.HARD:
            return len(self.hard_words)
        else:
            return len(self.medium_words)
    
    def _get_default_word(self, filename: str) -> str:
        """
        Provide default words when file loading fails.
        
        This method determines an appropriate default word based on the filename
        to ensure the game has fallback words available even when files are missing.
        
        Args:
            filename (str): The name of the file that failed to load
            
        Returns:
            str: A default word appropriate for the file type
            
        Example:
            >>> repo = LocalWordRepository('/app/resources')
            >>> default = repo._get_default_word('words-easy.txt')
            >>> default == 'WORD'
            True
        """
        if "easy" in filename.lower():
            return "WORD"
        elif "hard" in filename.lower():
            return "STRENGTH"
        else:
            return "QWORDS"
    
    def _get_default_word_by_level(self, level: GameLevel) -> str:
        """
        Provide default words when word lists are empty.
        
        This method provides fallback words based on the game level to ensure
        the game can continue even when word lists are empty or corrupted.
        
        Args:
            level (GameLevel): The game difficulty level
            
        Returns:
            str: A default word appropriate for the specified level
            
        Example:
            >>> repo = LocalWordRepository('/app/resources')
            >>> default = repo._get_default_word_by_level(GameLevel.HARD)
            >>> default == 'STRENGTH'
            True
        """
        if level == GameLevel.EASY:
            return "WORD"
        elif level == GameLevel.HARD:
            return "STRENGTH"
        else:
            return "QWORDS"
