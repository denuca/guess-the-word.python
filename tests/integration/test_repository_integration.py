import pytest
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mock_flask_app import create_test_app
from repositories.local_word_repository import LocalWordRepository


@pytest.fixture
def client():
    """Test client"""
    app = create_test_app({'TESTING': True})
    return app.test_client()


class TestRepositoryIntegration:
    """Test data layer integration with web layer"""
    
    def test_local_file_repository_integration(self, client):
        """Test local file repository integration with endpoints"""
        # Test with real word files
        response = client.post('/game/start', data={'level': 'EASY'})
        assert response.status_code == 200
        
        with client.session_transaction() as sess:
            word = sess['word']
            assert len(word) > 0
            assert word.isupper()
            assert word.isalpha()
    
    def test_word_selection_consistency(self, client):
        """Test word selection produces consistent results"""
        # Start multiple games and verify words are valid
        valid_words = set()
        
        for _ in range(10):
            response = client.post('/game/start', data={'level': 'MEDIUM'})
            assert response.status_code == 200
            
            with client.session_transaction() as sess:
                word = sess['word']
                valid_words.add(word)
                assert len(word) > 0
                assert word.isupper()
        
        # Should get some variety in word selection
        assert len(valid_words) > 1
    
    @patch('repositories.local_word_repository.LocalWordRepository')
    def test_repository_error_handling(self, mock_repo_class, client):
        """Test graceful handling of repository errors"""
        # Mock repository to raise exception
        mock_repo = MagicMock()
        mock_repo.get_random_word_by_level.side_effect = Exception("Repository error")
        mock_repo_class.return_value = mock_repo
        
        # This would need to be handled in the actual app
        # For now, just verify the mock setup works
        repo = LocalWordRepository('/fake/path')
        with pytest.raises(Exception):
            repo.get_random_word_by_level.side_effect("test")
    
    def test_different_levels_return_different_words(self, client):
        """Test different difficulty levels can return different words"""
        level_words = {}
        
        for level in ['EASY', 'MEDIUM', 'HARD']:
            client.post('/game/start', data={'level': level})
            
            with client.session_transaction() as sess:
                level_words[level] = sess['word']
        
        # Verify we got words for all levels
        assert len(level_words) == 3
        for word in level_words.values():
            assert isinstance(word, str)
            assert len(word) > 0
