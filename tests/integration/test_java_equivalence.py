import unittest
import os
import sys
import random
import tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from models.game_level import GameLevel
from repositories.local_word_repository import LocalWordRepository


class TestJavaEquivalence(unittest.TestCase):
    """Tests to ensure Python implementation matches Java behavior exactly"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_files(self):
        """Create test files matching Java test data"""
        # Easy words (4 letters expected in Java)
        easy_words = ['BIRD', 'GAME', 'PLAY', 'CAKE', 'ROSE']
        
        # Medium words (6 letters expected in Java) 
        medium_words = ['ANIMAL', 'BAKERY', 'PYTHON', 'QUAINT', 'RHYTHM']
        
        # Hard words (8+ letters expected in Java)
        hard_words = ['STRENGTH', 'COMPUTER', 'KEYBOARD', 'FUNCTION', 'VARIABLE']
        
        for filename, words in [
            ('words-easy.txt', easy_words),
            ('words.txt', medium_words), 
            ('words-hard.txt', hard_words)
        ]:
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write('\n'.join(words))
    
    def test_game_level_constants_match_java(self):
        """Verify GameLevel constants match Java enum values"""
        # These values must match exactly with Java implementation
        self.assertEqual(GameLevel.EASY.word_length, 4)
        self.assertEqual(GameLevel.EASY.max_attempts, 8)
        
        self.assertEqual(GameLevel.MEDIUM.word_length, 6)
        self.assertEqual(GameLevel.MEDIUM.max_attempts, 6)
        
        self.assertEqual(GameLevel.HARD.word_length, 8)
        self.assertEqual(GameLevel.HARD.max_attempts, 4)
    
    def test_default_words_match_java(self):
        """Verify default fallback words match Java implementation"""
        repo = LocalWordRepository('/nonexistent/path')
        
        # These must match Java's getDefaultWordByLevel method
        self.assertEqual(repo._get_default_word_by_level(GameLevel.EASY), 'WORD')
        self.assertEqual(repo._get_default_word_by_level(GameLevel.MEDIUM), 'QWORDS')
        self.assertEqual(repo._get_default_word_by_level(GameLevel.HARD), 'STRENGTH')
    
    def test_file_loading_behavior_matches_java(self):
        """Test file loading produces same results as Java ClassPathResource"""
        self._create_test_files()
        repo = LocalWordRepository(self.temp_dir)
        
        # Verify case conversion (Java converts to uppercase)
        for word_list in [repo.easy_words, repo.medium_words, repo.hard_words]:
            for word in word_list:
                self.assertTrue(word.isupper(), f"Word '{word}' should be uppercase")
                self.assertTrue(word.isalpha(), f"Word '{word}' should be alphabetic")
    
    def test_random_selection_with_fixed_seed(self):
        """Test random selection behavior with controlled randomization"""
        self._create_test_files()
        repo = LocalWordRepository(self.temp_dir)
        
        # Test deterministic behavior
        random.seed(12345)
        words_run1 = [repo.get_random_word_by_level(GameLevel.MEDIUM) for _ in range(10)]
        
        random.seed(12345)  # Reset to same seed
        words_run2 = [repo.get_random_word_by_level(GameLevel.MEDIUM) for _ in range(10)]
        
        self.assertEqual(words_run1, words_run2, 
                        "Same seed should produce identical word sequences")
    
    def test_empty_file_handling_matches_java(self):
        """Test empty file handling matches Java behavior"""
        # Create empty files
        for filename in ['words-easy.txt', 'words.txt', 'words-hard.txt']:
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write('')  # Empty file
        
        repo = LocalWordRepository(self.temp_dir)
        
        # Should fall back to default words (same as Java)
        self.assertEqual(repo.get_random_word_by_level(GameLevel.EASY), 'WORD')
        self.assertEqual(repo.get_random_word_by_level(GameLevel.MEDIUM), 'QWORDS')
        self.assertEqual(repo.get_random_word_by_level(GameLevel.HARD), 'STRENGTH')
    
    def test_whitespace_handling_matches_java(self):
        """Test whitespace trimming matches Java's trim() behavior"""
        # Create file with various whitespace scenarios
        filepath = os.path.join(self.temp_dir, 'words.txt')
        with open(filepath, 'w') as f:
            f.write('  ANIMAL  \n')  # Leading/trailing spaces
            f.write('\tBAKERY\t\n')   # Tabs
            f.write('PYTHON\n')       # Normal
            f.write('   \n')          # Whitespace only
            f.write('\n')             # Empty line
        
        repo = LocalWordRepository(self.temp_dir)
        
        # Should match Java's behavior: trim whitespace, skip empty lines
        expected = ['ANIMAL', 'BAKERY', 'PYTHON']
        self.assertEqual(repo.medium_words, expected)
    
    def test_error_recovery_matches_java(self):
        """Test error recovery behavior matches Java exception handling"""
        # Test with completely invalid path (matches Java FileNotFoundException)
        repo = LocalWordRepository('/completely/invalid/path/that/does/not/exist')
        
        # Should gracefully fall back to defaults (same as Java catch block)
        word = repo.get_random_word_by_level(GameLevel.MEDIUM)
        self.assertEqual(word, 'QWORDS')
        
        # Verify all levels have fallbacks
        self.assertIsNotNone(repo.get_random_word_by_level(GameLevel.EASY))
        self.assertIsNotNone(repo.get_random_word_by_level(GameLevel.MEDIUM))
        self.assertIsNotNone(repo.get_random_word_by_level(GameLevel.HARD))


if __name__ == '__main__':
    unittest.main()
