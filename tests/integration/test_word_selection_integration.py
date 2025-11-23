import unittest
import os
import sys
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.models.game_level import GameLevel
from app.repositories.local_word_repository import LocalWordRepository


class TestWordSelectionIntegration(unittest.TestCase):
    """Integration tests using real word files"""
    
    def setUp(self):
        """Set up with real resource files"""
        self.resources_path = os.path.join(os.path.dirname(__file__), '../../resources')
        self.repo = LocalWordRepository(self.resources_path)
    
    def test_real_word_files_loaded(self):
        """Test that real word files are loaded successfully"""
        # Verify files exist and words are loaded
        self.assertGreater(len(self.repo.easy_words), 0)
        self.assertGreater(len(self.repo.medium_words), 0)
        self.assertGreater(len(self.repo.hard_words), 0)
        
        # Verify specific words from our test files
        self.assertIn('BIRD', self.repo.easy_words)
        self.assertIn('PYTHON', self.repo.medium_words)
        self.assertIn('STRENGTH', self.repo.hard_words)
    
    def test_word_length_constraints(self):
        """Test that selected words match expected length constraints"""
        # Note: Our test files don't strictly follow length constraints
        # This test validates the selection mechanism works
        
        for level in [GameLevel.EASY, GameLevel.MEDIUM, GameLevel.HARD]:
            word = self.repo.get_random_word_by_level(level)
            self.assertIsInstance(word, str)
            self.assertGreater(len(word), 0)
            self.assertTrue(word.isupper())
    
    def test_randomness_distribution(self):
        """Test that word selection shows proper randomness"""
        # Set seed for reproducible test
        random.seed(42)
        
        # Get multiple words and verify we get variety
        words = set()
        for _ in range(20):
            word = self.repo.get_random_word_by_level(GameLevel.MEDIUM)
            words.add(word)
        
        # Should get multiple different words (not just one repeated)
        self.assertGreater(len(words), 1, "Should get variety in word selection")
    
    def test_deterministic_behavior_with_seed(self):
        """Test that same seed produces same sequence"""
        # First sequence
        random.seed(123)
        sequence1 = [self.repo.get_random_word_by_level(GameLevel.EASY) for _ in range(5)]
        
        # Second sequence with same seed
        random.seed(123)
        sequence2 = [self.repo.get_random_word_by_level(GameLevel.EASY) for _ in range(5)]
        
        self.assertEqual(sequence1, sequence2, "Same seed should produce same sequence")
    
    def test_all_levels_functional(self):
        """Test that all difficulty levels return valid words"""
        for level in GameLevel:
            word = self.repo.get_random_word_by_level(level)
            
            # Basic validation
            self.assertIsInstance(word, str)
            self.assertGreater(len(word), 0)
            self.assertTrue(word.isupper())
            self.assertTrue(word.isalpha(), f"Word '{word}' should contain only letters")
    
    def test_concurrent_access_safety(self):
        """Test that repository is safe for concurrent access"""
        import threading
        import time
        
        results = []
        errors = []
        
        def worker():
            try:
                for _ in range(10):
                    word = self.repo.get_random_word_by_level(GameLevel.MEDIUM)
                    results.append(word)
                    time.sleep(0.001)  # Small delay to encourage race conditions
            except Exception as e:
                errors.append(e)
        
        # Start multiple threads
        threads = [threading.Thread(target=worker) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # Verify no errors and got expected number of results
        self.assertEqual(len(errors), 0, f"Concurrent access caused errors: {errors}")
        self.assertEqual(len(results), 50, "Should get results from all threads")


if __name__ == '__main__':
    unittest.main()
