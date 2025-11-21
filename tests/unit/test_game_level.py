import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app.models.game_level import GameLevel


class TestGameLevel(unittest.TestCase):
    """Test cases for GameLevel enum - 100% coverage"""
    
    def test_easy_level_properties(self):
        """Test EASY level has correct word length and max attempts"""
        level = GameLevel.EASY
        self.assertEqual(level.word_length, 4)
        self.assertEqual(level.max_attempts, 8)
    
    def test_medium_level_properties(self):
        """Test MEDIUM level has correct word length and max attempts"""
        level = GameLevel.MEDIUM
        self.assertEqual(level.word_length, 6)
        self.assertEqual(level.max_attempts, 6)
    
    def test_hard_level_properties(self):
        """Test HARD level has correct word length and max attempts"""
        level = GameLevel.HARD
        self.assertEqual(level.word_length, 8)
        self.assertEqual(level.max_attempts, 4)
    
    def test_all_levels_exist(self):
        """Test all expected difficulty levels exist"""
        levels = list(GameLevel)
        self.assertEqual(len(levels), 3)
        self.assertIn(GameLevel.EASY, levels)
        self.assertIn(GameLevel.MEDIUM, levels)
        self.assertIn(GameLevel.HARD, levels)
    
    def test_level_names(self):
        """Test enum names are correct"""
        self.assertEqual(GameLevel.EASY.name, 'EASY')
        self.assertEqual(GameLevel.MEDIUM.name, 'MEDIUM')
        self.assertEqual(GameLevel.HARD.name, 'HARD')
    
    def test_from_string_method(self):
        """Test from_string class method"""
        self.assertEqual(GameLevel.from_string('EASY'), GameLevel.EASY)
        self.assertEqual(GameLevel.from_string('easy'), GameLevel.EASY)
        self.assertEqual(GameLevel.from_string('INVALID'), GameLevel.MEDIUM)
    
    def test_to_dict_method(self):
        """Test to_dict method"""
        level_dict = GameLevel.EASY.to_dict()
        expected = {'name': 'EASY', 'word_length': 4, 'max_attempts': 8}
        self.assertEqual(level_dict, expected)


if __name__ == '__main__':
    unittest.main()
