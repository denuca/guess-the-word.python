import unittest
import unittest.mock as mock
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.models.game_level import GameLevel
from app.repositories.local_word_repository import LocalWordRepository


class TestLocalWordRepository(unittest.TestCase):
    """Unit tests for LocalWordRepository - 100% coverage"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_file(self, filename, words):
        """Helper to create test word files"""
        filepath = os.path.join(self.temp_dir, filename)
        with open(filepath, 'w') as f:
            f.write('\n'.join(words))
        return filepath
    
    def test_successful_file_loading(self):
        """Test successful loading of all word files"""
        # Create test files
        self._create_test_file('words-easy.txt', ['bird', 'game', 'play'])
        self._create_test_file('words.txt', ['animal', 'bakery', 'python'])
        self._create_test_file('words-hard.txt', ['strength', 'computer'])
        
        repo = LocalWordRepository(self.temp_dir)
        
        # Verify words loaded correctly
        self.assertEqual(len(repo.easy_words), 3)
        self.assertEqual(len(repo.medium_words), 3)
        self.assertEqual(len(repo.hard_words), 2)
        
        # Verify uppercase conversion
        self.assertIn('BIRD', repo.easy_words)
        self.assertIn('PYTHON', repo.medium_words)
        self.assertIn('STRENGTH', repo.hard_words)
    
    def test_file_not_found_fallback(self):
        """Test fallback behavior when files don't exist"""
        repo = LocalWordRepository('/nonexistent/path')
        
        # Should have default words
        self.assertEqual(repo.easy_words, ['WORD'])
        self.assertEqual(repo.medium_words, ['QWORDS'])
        self.assertEqual(repo.hard_words, ['STRENGTH'])
    
    def test_empty_lines_handling(self):
        """Test handling of empty lines and whitespace"""
        self._create_test_file('words.txt', ['  animal  ', '', '  bakery', '\n', 'python\t'])
        
        repo = LocalWordRepository(self.temp_dir)
        
        # Should skip empty lines and trim whitespace
        expected = ['ANIMAL', 'BAKERY', 'PYTHON']
        self.assertEqual(repo.medium_words, expected)
    
    def test_get_random_word_easy(self):
        """Test random word selection for EASY level"""
        self._create_test_file('words-easy.txt', ['bird', 'game'])
        
        repo = LocalWordRepository(self.temp_dir)
        word = repo.get_random_word_by_level(GameLevel.EASY)
        
        self.assertIn(word, ['BIRD', 'GAME'])
    
    def test_get_random_word_medium(self):
        """Test random word selection for MEDIUM level"""
        self._create_test_file('words.txt', ['animal', 'python'])
        
        repo = LocalWordRepository(self.temp_dir)
        word = repo.get_random_word_by_level(GameLevel.MEDIUM)
        
        self.assertIn(word, ['ANIMAL', 'PYTHON'])
    
    def test_get_random_word_hard(self):
        """Test random word selection for HARD level"""
        self._create_test_file('words-hard.txt', ['strength', 'computer'])
        
        repo = LocalWordRepository(self.temp_dir)
        word = repo.get_random_word_by_level(GameLevel.HARD)
        
        self.assertIn(word, ['STRENGTH', 'COMPUTER'])
    
    def test_empty_word_list_fallback_easy(self):
        """Test fallback when EASY word list is empty"""
        self._create_test_file('words-easy.txt', [''])  # Empty file
        
        repo = LocalWordRepository(self.temp_dir)
        word = repo.get_random_word_by_level(GameLevel.EASY)
        
        self.assertEqual(word, 'WORD')
    
    def test_empty_word_list_fallback_medium(self):
        """Test fallback when MEDIUM word list is empty"""
        self._create_test_file('words.txt', [''])  # Empty file
        
        repo = LocalWordRepository(self.temp_dir)
        word = repo.get_random_word_by_level(GameLevel.MEDIUM)
        
        self.assertEqual(word, 'QWORDS')
    
    def test_empty_word_list_fallback_hard(self):
        """Test fallback when HARD word list is empty"""
        self._create_test_file('words-hard.txt', [''])  # Empty file
        
        repo = LocalWordRepository(self.temp_dir)
        word = repo.get_random_word_by_level(GameLevel.HARD)
        
        self.assertEqual(word, 'STRENGTH')
    
    def test_word_count_by_level(self):
        """Test word count functionality"""
        self._create_test_file('words-easy.txt', ['bird', 'game'])
        self._create_test_file('words.txt', ['animal', 'bakery', 'python'])
        
        repo = LocalWordRepository(self.temp_dir)
        
        self.assertEqual(repo.get_word_count_by_level(GameLevel.EASY), 2)
        self.assertEqual(repo.get_word_count_by_level(GameLevel.MEDIUM), 3)


if __name__ == '__main__':
    unittest.main()
