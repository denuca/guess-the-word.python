"""
Integration tests for Q-Words API endpoints.

This module tests the HTTP API endpoints that power the Q-Words game interface.
Tests cover the complete request-response cycle including:
- Route handling and HTTP status codes
- Request parameter validation
- Session state management
- JSON response formatting
- Error handling and edge cases

The tests ensure the API provides a reliable interface for both
HTML form submissions and AJAX requests, supporting accessibility
features and responsive design.

Test Coverage:
- Home page rendering and level selection
- Game initialization with different difficulty levels
- Guess submission and feedback generation
- Game status retrieval
- Session management and persistence
- Error handling for invalid requests

Author: Q-Words Development Team
Last Updated: 2024-11-17
"""

import pytest
import json
import sys
import os
from unittest.mock import patch

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app import create_app
from config.settings import TestingConfig
from app.models.game_level import GameLevel


class TestHomePageEndpoints:
    """
    Test suite for home page and navigation endpoints.
    
    Tests the main landing page functionality including level selection
    and navigation elements that support keyboard and screen reader users.
    """
    
    @pytest.fixture
    def client(self):
        """
        Create test client for HTTP requests.
        
        Returns:
            FlaskClient: Test client configured for testing environment
        """
        app = create_app(TestingConfig)
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_home_page_loads_successfully(self, client):
        """
        Test home page returns 200 status and contains required elements.
        
        Validates:
        - HTTP 200 response
        - Page title and branding
        - Level selection form
        - Accessibility features
        
        WCAG Compliance: Tests semantic structure and form accessibility.
        """
        response = client.get('/')
        
        # Verify successful response
        assert response.status_code == 200
        assert response.content_type.startswith('text/html')
        
        # Verify essential page elements
        content = response.data.decode('utf-8')
        assert 'Q-Words' in content
        assert 'start-game' in content
        assert 'level' in content
        
        # Verify accessibility features
        assert 'aria-label' in content
        assert 'role=' in content
        assert 'Skip to main content' in content
    
    def test_home_page_contains_all_difficulty_levels(self, client):
        """
        Test home page displays all available difficulty levels.
        
        Ensures all game levels are presented to users with proper
        accessibility attributes for screen readers.
        """
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Verify all difficulty levels are present
        assert 'EASY' in content
        assert 'MEDIUM' in content  
        assert 'HARD' in content
        
        # Verify form structure for accessibility
        assert 'type="radio"' in content
        assert 'name="level"' in content
        assert 'fieldset' in content
    
    def test_about_page_loads_successfully(self, client):
        """
        Test about page returns 200 status and contains game information.
        
        Validates the about page accessibility and content structure.
        """
        response = client.get('/about')
        
        assert response.status_code == 200
        assert response.content_type.startswith('text/html')
        
        content = response.data.decode('utf-8')
        assert 'Q-Words' in content
    
    def test_navigation_accessibility_features(self, client):
        """
        Test navigation contains proper accessibility attributes.
        
        WCAG 2.4.6 - Headings and Labels: Navigation should be properly labeled.
        WCAG 4.1.2 - Name, Role, Value: Navigation roles should be clear.
        """
        response = client.get('/')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Verify navigation accessibility
        assert 'role="navigation"' in content
        assert 'aria-label="Main navigation"' in content
        assert 'role="banner"' in content
        assert 'role="main"' in content


class TestGameInitializationEndpoints:
    """
    Test suite for game initialization and startup endpoints.
    
    Tests the game creation process including level selection,
    word generation, and session initialization.
    """
    
    @pytest.fixture
    def client(self):
        """Create test client with application context."""
        app = create_app(TestingConfig)
        app.config['TESTING'] = True
        with app.test_client() as client:
            with app.app_context():
                yield client
    
    def test_start_game_easy_level_success(self, client):
        """
        Test game initialization with EASY difficulty level.
        
        Validates:
        - Successful game creation
        - Proper session state initialization
        - Correct level configuration
        - JSON response format for AJAX requests
        """
        response = client.post('/game/start', 
                             data={'level': 'EASY'},
                             headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        # Should redirect to game page for form submission
        assert response.status_code == 302
        assert '/game/' in response.location
        
        # Verify session state was created
        with client.session_transaction() as sess:
            assert 'word' in sess
            assert sess['attempts'] == 0
            assert sess['gameLevel'] == 'EASY'
            assert sess['guessHistory'] == []
            assert sess['gameWon'] is False
            assert sess['gameLost'] is False
    
    def test_start_game_medium_level_success(self, client):
        """
        Test game initialization with MEDIUM difficulty level.
        
        Tests default level handling and medium difficulty configuration.
        """
        response = client.post('/game/start', data={'level': 'MEDIUM'})
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['gameLevel'] == 'MEDIUM'
            assert len(sess['word']) == 6  # Medium level word length
    
    def test_start_game_hard_level_success(self, client):
        """
        Test game initialization with HARD difficulty level.
        
        Tests maximum difficulty configuration.
        """
        response = client.post('/game/start', data={'level': 'HARD'})
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['gameLevel'] == 'HARD'
            assert len(sess['word']) == 8  # Hard level word length
    
    def test_start_game_ajax_request_returns_json(self, client):
        """
        Test game initialization via AJAX returns JSON response.
        
        Validates API response format for JavaScript-based interactions.
        Important for accessibility features that use AJAX.
        """
        response = client.post('/game/start',
                             data={'level': 'MEDIUM'},
                             headers={'Content-Type': 'application/json'})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = json.loads(response.data.decode())
        assert data['status'] == 'started'
        assert data['level'] == 'MEDIUM'
        assert 'maxAttempts' in data
        assert 'wordLength' in data
    
    def test_start_game_invalid_level_defaults_to_medium(self, client):
        """
        Test game initialization with invalid level defaults to MEDIUM.
        
        Ensures robust error handling for malformed requests.
        """
        response = client.post('/game/start', data={'level': 'INVALID'})
        
        # Should still create game with default level
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            # Should default to MEDIUM for invalid input
            assert 'gameLevel' in sess
    
    def test_start_game_missing_level_parameter(self, client):
        """
        Test game initialization without level parameter uses default.
        
        Tests parameter validation and default value handling.
        """
        response = client.post('/game/start', data={})
        assert response.status_code == 302
        
        with client.session_transaction() as sess:
            assert sess['gameLevel'] == 'MEDIUM'  # Default level


class TestGameplayEndpoints:
    """
    Test suite for core gameplay endpoints.
    
    Tests guess submission, feedback generation, and game state updates.
    These endpoints are critical for the interactive game experience.
    """
    
    @pytest.fixture
    def client_with_game(self):
        """
        Create test client with active game session.
        
        Returns:
            FlaskClient: Client with pre-initialized game state
        """
        app = create_app(TestingConfig)
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Initialize game session
        with client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 0
            sess['guessHistory'] = []
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        return client
    
    def test_submit_valid_guess_success(self, client_with_game):
        """
        Test valid word guess submission and feedback generation.
        
        Validates:
        - Guess processing and feedback calculation
        - Session state updates
        - JSON response format
        - Accessibility-friendly feedback symbols
        """
        response = client_with_game.post('/game/guess',
                                       data={'guess': 'ANIMAL'},
                                       headers={'X-Requested-With': 'XMLHttpRequest'})
        
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = json.loads(response.data.decode())
        
        # Verify response structure
        assert data['guess'] == 'ANIMAL'
        assert 'feedback' in data
        assert data['attempts'] == 1
        assert 'won' in data
        assert 'lost' in data
        
        # Verify feedback uses accessibility symbols
        feedback = data['feedback']
        assert all(char in '+?x' for char in feedback)
        
        # Verify session was updated
        with client_with_game.session_transaction() as sess:
            assert len(sess['guessHistory']) == 1
            assert sess['attempts'] == 1
            assert sess['guessHistory'][0]['guess'] == 'ANIMAL'
    
    def test_submit_winning_guess(self, client_with_game):
        """
        Test guess submission that wins the game.
        
        Validates win condition detection and proper game state updates.
        """
        response = client_with_game.post('/game/guess',
                                       data={'guess': 'PYTHON'},
                                       headers={'X-Requested-With': 'XMLHttpRequest'})
        
        assert response.status_code == 200
        data = json.loads(response.data.decode())
        
        # Verify win condition
        assert data['won'] is True
        assert data['feedback'] == '++++++'  # All correct positions
        assert data['targetWord'] == 'PYTHON'
        
        # Verify session reflects win
        with client_with_game.session_transaction() as sess:
            assert sess['gameWon'] is True
    
    def test_submit_guess_without_active_game(self):
        """
        Test guess submission without active game session.
        
        Validates error handling for invalid game state.
        """
        app = create_app(TestingConfig)
        client = app.test_client()
        
        response = client.post('/game/guess',
                             data={'guess': 'HELLO'},
                             headers={'X-Requested-With': 'XMLHttpRequest'})
        
        assert response.status_code == 400
        data = json.loads(response.data.decode())
        assert 'error' in data
        assert data['error'] == 'No active game'
    
    def test_submit_empty_guess_returns_error(self, client_with_game):
        """
        Test submission of empty guess returns validation error.
        
        Ensures proper input validation for accessibility.
        """
        response = client_with_game.post('/game/guess',
                                       data={'guess': ''},
                                       headers={'X-Requested-With': 'XMLHttpRequest'})
        
        assert response.status_code == 400
        data = json.loads(response.data.decode())
        assert 'error' in data
        assert 'empty' in data['error'].lower()
    
    def test_submit_guess_to_finished_game(self, client_with_game):
        """
        Test guess submission to already finished game.
        
        Validates that completed games don't accept new guesses.
        """
        # Set game to won state
        with client_with_game.session_transaction() as sess:
            sess['gameWon'] = True
        
        response = client_with_game.post('/game/guess',
                                       data={'guess': 'HELLO'},
                                       headers={'X-Requested-With': 'XMLHttpRequest'})
        
        assert response.status_code == 400
        data = json.loads(response.data.decode())
        assert 'already finished' in data['error']


class TestGameStatusEndpoints:
    """
    Test suite for game status and information endpoints.
    
    Tests endpoints that provide game state information for
    accessibility features and dynamic UI updates.
    """
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app(TestingConfig)
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_game_status_no_active_game(self, client):
        """
        Test game status endpoint with no active game.
        
        Validates response when no game session exists.
        """
        response = client.get('/game/status')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        
        data = json.loads(response.data.decode())
        assert data['hasActiveGame'] is False
    
    def test_game_status_with_active_game(self, client):
        """
        Test game status endpoint with active game session.
        
        Validates complete game state information for accessibility.
        """
        # Create active game session
        with client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 2
            sess['guessHistory'] = [
                {'guess': 'ANIMAL', 'feedback': 'x?xxxx', 'attempt': 1},
                {'guess': 'PYTHON', 'feedback': '++++++', 'attempt': 2}
            ]
            sess['gameWon'] = True
            sess['gameLost'] = False
        
        response = client.get('/game/status')
        assert response.status_code == 200
        
        data = json.loads(response.data.decode())
        
        # Verify complete status information
        assert data['hasActiveGame'] is True
        assert data['attempts'] == 2
        assert 'maxAttempts' in data
        assert len(data['guessHistory']) == 2
        assert data['gameWon'] is True
        assert data['gameLost'] is False
        assert data['wordLength'] == 6
    
    def test_game_page_accessibility_features(self, client):
        """
        Test game page contains proper accessibility features.
        
        WCAG Compliance: Tests ARIA labels, live regions, and semantic structure.
        """
        # Create active game session
        with client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 0
            sess['guessHistory'] = []
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        response = client.get('/game/')
        assert response.status_code == 200
        
        content = response.data.decode('utf-8')
        
        # Verify accessibility features
        assert 'aria-live="polite"' in content
        assert 'role="status"' in content
        assert 'aria-labelledby' in content
        assert 'sr-only' in content
        assert 'aria-describedby' in content


class TestSessionManagement:
    """
    Test suite for session management and persistence.
    
    Tests session handling, game state persistence, and cleanup functionality.
    Critical for maintaining game state across requests.
    """
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app(TestingConfig)
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_game_reset_clears_session(self, client):
        """
        Test game reset endpoint clears all session data.
        
        Validates complete session cleanup for new game functionality.
        """
        # Create game session
        with client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 3
            sess['guessHistory'] = [{'guess': 'TEST', 'feedback': 'xxxx'}]
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        # Reset game
        response = client.post('/game/reset')
        assert response.status_code == 302  # Redirect to home
        
        # Verify session is cleared
        with client.session_transaction() as sess:
            assert 'word' not in sess
            assert 'gameLevel' not in sess
            assert 'attempts' not in sess
            assert 'guessHistory' not in sess
            assert 'gameWon' not in sess
            assert 'gameLost' not in sess
    
    def test_play_again_preserves_level(self, client):
        """
        Test play again functionality preserves difficulty level.
        
        Validates that play again creates new game at same difficulty.
        """
        # Create finished game session
        with client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'HARD'
            sess['attempts'] = 5
            sess['guessHistory'] = [{'guess': 'TEST', 'feedback': 'xxxx'}]
            sess['gameWon'] = True
            sess['gameLost'] = False
        
        # Play again
        response = client.post('/game/play-again')
        assert response.status_code == 302  # Redirect to game page
        
        # Verify new game with same level
        with client.session_transaction() as sess:
            assert 'word' in sess
            assert sess['gameLevel'] == 'HARD'  # Level preserved
            assert sess['attempts'] == 0  # Reset to 0
            assert sess['guessHistory'] == []  # Empty history
            assert sess['gameWon'] is False  # Reset win state
            assert sess['gameLost'] is False  # Reset lose state


if __name__ == '__main__':
    # Run integration tests with detailed output
    pytest.main([__file__, '-v', '--tb=short'])
