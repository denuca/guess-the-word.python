import pytest
import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from mock_flask_app import create_test_app


@pytest.fixture
def client():
    """Test client with session support"""
    app = create_test_app({'TESTING': True})
    return app.test_client()


class TestSessionManagement:
    """Test session state persistence and isolation"""
    
    def test_session_persistence_across_requests(self, client):
        """Test game state persists across HTTP requests"""
        # Start game
        client.post('/game/start', data={'level': 'MEDIUM'})
        
        # Make multiple guesses
        guesses = ['ANIMAL', 'BAKERY', 'PYTHON']
        for guess in guesses:
            client.post('/game/guess', data={'guess': guess})
        
        # Verify all guesses stored in session
        with client.session_transaction() as sess:
            assert len(sess['guessHistory']) == 3
            assert sess['attempts'] == 3
            stored_guesses = [g['guess'] for g in sess['guessHistory']]
            assert stored_guesses == guesses
    
    def test_session_isolation_between_games(self, client):
        """Test new game clears previous state"""
        # Play first game
        client.post('/game/start', data={'level': 'EASY'})
        client.post('/game/guess', data={'guess': 'BIRD'})
        client.post('/game/guess', data={'guess': 'GAME'})
        
        # Verify state exists
        with client.session_transaction() as sess:
            assert sess['attempts'] == 2
            assert len(sess['guessHistory']) == 2
        
        # Start new game
        client.post('/game/start', data={'level': 'HARD'})
        
        # Verify state reset
        with client.session_transaction() as sess:
            assert sess['attempts'] == 0
            assert len(sess['guessHistory']) == 0
            assert sess['gameWon'] is False
    
    def test_session_data_types_preserved(self, client):
        """Test session preserves correct data types"""
        client.post('/game/start', data={'level': 'MEDIUM'})
        
        with client.session_transaction() as sess:
            # Verify types are preserved
            assert isinstance(sess['word'], str)
            assert isinstance(sess['attempts'], int)
            assert isinstance(sess['guessHistory'], list)
            assert isinstance(sess['gameWon'], bool)
    
    def test_concurrent_session_isolation(self, client):
        """Test session isolation between concurrent requests"""
        # Simulate two different users/sessions
        client1 = client
        app = create_test_app({'TESTING': True})
        client2 = app.test_client()
        
        # Start different games
        client1.post('/game/start', data={'level': 'EASY'})
        client2.post('/game/start', data={'level': 'HARD'})
        
        # Make different guesses
        client1.post('/game/guess', data={'guess': 'BIRD'})
        client2.post('/game/guess', data={'guess': 'STRENGTH'})
        
        # Verify sessions are isolated
        with client1.session_transaction() as sess1:
            assert len(sess1['guessHistory']) == 1
            assert sess1['guessHistory'][0]['guess'] == 'BIRD'
        
        with client2.session_transaction() as sess2:
            assert len(sess2['guessHistory']) == 1
            assert sess2['guessHistory'][0]['guess'] == 'STRENGTH'
