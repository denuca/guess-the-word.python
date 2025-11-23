"""
Home controller for Guess The Word application.
Handles the main landing page and navigation.
"""

from flask import Blueprint, render_template
from app.models.game_level import GameLevel

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """Display the home page with game level selection."""
    levels = [level.to_dict() for level in GameLevel]
    return render_template('index.html', levels=levels)


@home_bp.route('/about')
def about():
    """Display information about the Guess The Word game."""
    return render_template('about.html')
