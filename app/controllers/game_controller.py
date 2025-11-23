"""
Game controller for Guess The Word application.

This module handles all game-related HTTP endpoints including:
- Game initialization and level selection
- Word guessing and feedback processing
- Game state management (win/lose conditions)
- Session management for game persistence
- Debug mode functionality for development

The controller follows RESTful principles and supports both HTML form submissions
and AJAX requests for a responsive user experience.
"""

from flask import Blueprint, request, session, jsonify, render_template, current_app, redirect, url_for, make_response
from app.models.game_level import GameLevel
from app.models.word import Word
from app.repositories.local_word_repository import LocalWordRepository

# Create blueprint for game-related routes
game_bp = Blueprint('game', __name__)


def get_word_repository():
    """
    Factory function to get the appropriate word repository instance.
    
    Currently supports local file-based repository with future support
    for DynamoDB repository planned.
    
    Returns:
        LocalWordRepository: Repository instance for word operations
        
    Raises:
        NotImplementedError: If DynamoDB repository type is requested
    """
    repo_type = current_app.config.get('WORD_REPOSITORY_TYPE', 'local')
    
    if repo_type == 'local':
        resources_path = current_app.config.get('RESOURCES_PATH')
        return LocalWordRepository(resources_path)
    else:
        # Future enhancement: DynamoDB repository implementation
        raise NotImplementedError("DynamoDB repository not yet implemented")


@game_bp.route('/')
def game_page():
    """
    Display the main game page with current game state.
    
    This route serves the game interface showing:
    - Current game progress (attempts, level, word length)
    - Guess history with feedback
    - Input form for new guesses (if game is active)
    - Win/lose messages with action buttons
    - Debug information (if debug mode is enabled)
    
    Returns:
        Response: Rendered game.html template with cache-busting headers
        Redirect: To home page if no active game session exists
    """
    # Redirect to home if no active game
    if 'word' not in session:
        return redirect(url_for('home.index'))
    
    # Check if debug mode is enabled for development
    debug_mode = current_app.config.get('DEBUG', False)
    
    # Prepare game state data for template rendering
    game_state = {
        'level': GameLevel.from_string(session.get('gameLevel', 'MEDIUM')).to_dict(),
        'attempts': session.get('attempts', 0),
        'maxAttempts': GameLevel.from_string(session.get('gameLevel', 'MEDIUM')).max_attempts,
        'guessHistory': session.get('guessHistory', []),
        'gameWon': session.get('gameWon', False),
        'gameLost': session.get('gameLost', False),
        'wordLength': len(session.get('word', '')),
        'debugMode': debug_mode,
        'targetWord': session.get('word', '') if debug_mode else None
    }
    
    # Create response with cache-busting headers to prevent stale game state
    response = make_response(render_template('game.html', game=game_state))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@game_bp.route('/start', methods=['POST'])
def start_game():
    """
    Initialize a new game with the specified difficulty level.
    
    This route handles game initialization by:
    - Parsing the selected difficulty level from form data
    - Selecting a random word for the chosen level
    - Initializing clean session state
    - Redirecting to the game page
    
    Form Parameters:
        level (str): Game difficulty level ('EASY', 'MEDIUM', 'HARD')
        
    Returns:
        JSON: Game initialization data (if AJAX request)
        Redirect: To game page (if form submission)
        Redirect: To home page (if error occurs)
    """
    try:
        # Parse difficulty level from form, default to MEDIUM
        level_name = request.form.get('level', 'MEDIUM')
        level = GameLevel.from_string(level_name)
        
        # Get a random word for the selected difficulty level
        word_repo = get_word_repository()
        target_word = word_repo.get_random_word_by_level(level)
        
        # Initialize clean game session state
        session['word'] = target_word
        session['attempts'] = 0
        session['gameLevel'] = level.name
        session['guessHistory'] = []
        session['gameWon'] = False
        session['gameLost'] = False
        session.permanent = True
        session.modified = True
        
        # Return appropriate response based on request type
        if request.is_json:
            return jsonify({
                'status': 'started',
                'level': level.name,
                'maxAttempts': level.max_attempts,
                'wordLength': len(target_word)
            })
        else:
            return redirect(url_for('game.game_page'))
            
    except Exception as e:
        current_app.logger.error(f"Error starting game: {e}")
        if request.is_json:
            return jsonify({'error': 'Failed to start game'}), 500
        else:
            return redirect(url_for('home.index'))


@game_bp.route('/play-again', methods=['POST'])
def play_again():
    """
    Start a new game at the same difficulty level as the current game.
    
    This route is used when players want to play another round at the same
    difficulty without returning to level selection. It preserves the current
    level but resets all other game state.
    
    Returns:
        Redirect: To game page with new word (if successful)
        Redirect: To home page (if no active game or error)
    """
    try:
        # Ensure there's an active game with a level
        if 'gameLevel' not in session:
            current_app.logger.warning("Play again attempted without active game level")
            return redirect(url_for('home.index'))
        
        # Get current level and generate new word
        current_level = session.get('gameLevel', 'MEDIUM')
        level = GameLevel.from_string(current_level)
        
        word_repo = get_word_repository()
        target_word = word_repo.get_random_word_by_level(level)
        
        # Reset game state while preserving the difficulty level
        session['word'] = target_word
        session['attempts'] = 0
        session['gameLevel'] = level.name  # Preserve current level
        session['guessHistory'] = []
        session['gameWon'] = False
        session['gameLost'] = False
        session.permanent = True
        session.modified = True
        
        return redirect(url_for('game.game_page'))
        
    except Exception as e:
        current_app.logger.error(f"Error in play again: {e}")
        return redirect(url_for('home.index'))


@game_bp.route('/guess', methods=['POST'])
def submit_guess():
    """
    Process a word guess and return feedback.
    
    This route handles the core game logic by:
    - Validating the guess input
    - Evaluating the guess against the target word
    - Updating game state (attempts, history, win/lose status)
    - Returning appropriate feedback
    
    Form Parameters:
        guess (str): The player's word guess
        
    Returns:
        JSON: Guess result with feedback and game status
        Redirect: To game page (if form submission)
        JSON Error: If validation fails or game is over
    """
    # Ensure there's an active game
    if 'word' not in session:
        if request.is_json:
            return jsonify({'error': 'No active game'}), 400
        else:
            return redirect(url_for('home.index'))
    
    try:
        # Validate guess input
        guess = request.form.get('guess', '').strip()
        if not guess:
            return jsonify({'error': 'Guess cannot be empty'}), 400
        
        # Get current game state
        target_word = Word(session['word'])
        level = GameLevel.from_string(session.get('gameLevel', 'MEDIUM'))
        attempts = session['attempts']
        
        # Prevent guesses on finished games
        if session.get('gameWon') or session.get('gameLost'):
            return jsonify({'error': 'Game is already finished'}), 400
        
        # Evaluate the guess and get feedback
        feedback = target_word.evaluate_guess(guess)
        is_correct = target_word.is_correct_guess(guess)
        
        # Update game state
        attempts += 1
        session['attempts'] = attempts
        
        # Record the guess in history
        guess_result = {
            'guess': guess.upper(),
            'feedback': feedback,
            'attempt': attempts
        }
        session['guessHistory'].append(guess_result)
        
        # Check for win/lose conditions
        if is_correct:
            session['gameWon'] = True
        elif attempts >= level.max_attempts:
            session['gameLost'] = True
        
        # Prepare response data
        response_data = {
            'guess': guess.upper(),
            'feedback': feedback,
            'attempts': attempts,
            'maxAttempts': level.max_attempts,
            'won': session.get('gameWon', False),
            'lost': session.get('gameLost', False),
            'targetWord': target_word.word if session.get('gameWon') or session.get('gameLost') else None
        }
        
        # Return appropriate response based on request type
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify(response_data)
        else:
            return redirect(url_for('game.game_page'))
            
    except Exception as e:
        current_app.logger.error(f"Error processing guess: {e}")
        if request.is_json:
            return jsonify({'error': 'Failed to process guess'}), 500
        else:
            return redirect(url_for('game.game_page'))


@game_bp.route('/status')
def game_status():
    """
    Get current game status as JSON.
    
    This API endpoint provides the current game state for AJAX requests
    or external integrations. Useful for checking game progress without
    rendering the full HTML page.
    
    Returns:
        JSON: Complete game status including level, attempts, history, and win/lose state
        JSON: Empty status if no active game
        JSON Error: If status retrieval fails
    """
    try:
        has_active_game = 'word' in session
        
        if has_active_game:
            level = GameLevel.from_string(session.get('gameLevel', 'MEDIUM'))
            status = {
                'hasActiveGame': True,
                'level': level.to_dict(),
                'attempts': session.get('attempts', 0),
                'maxAttempts': level.max_attempts,
                'guessHistory': session.get('guessHistory', []),
                'gameWon': session.get('gameWon', False),
                'gameLost': session.get('gameLost', False),
                'wordLength': len(session.get('word', ''))
            }
        else:
            status = {'hasActiveGame': False}
        
        return jsonify(status)
        
    except Exception as e:
        current_app.logger.error(f"Error getting game status: {e}")
        return jsonify({'error': 'Failed to get game status'}), 500


@game_bp.route('/reset', methods=['POST'])
def reset_game():
    """
    Reset the current game session and return to level selection.
    
    This route completely clears the game session, effectively ending
    the current game and allowing the player to start fresh with a
    new difficulty level selection.
    
    Returns:
        JSON: Reset confirmation (if AJAX request)
        Redirect: To home page for level selection
        JSON Error: If reset operation fails
    """
    try:
        # Clear all game-related session data
        game_keys = ['word', 'attempts', 'gameLevel', 'guessHistory', 'gameWon', 'gameLost']
        for key in game_keys:
            session.pop(key, None)
        
        # Ensure session changes are persisted
        session.modified = True
        
        # Return appropriate response based on request type
        if request.is_json:
            return jsonify({'status': 'reset'})
        else:
            return redirect(url_for('home.index'))
            
    except Exception as e:
        current_app.logger.error(f"Error resetting game: {e}")
        if request.is_json:
            return jsonify({'error': 'Failed to reset game'}), 500
        else:
            return redirect(url_for('home.index'))
