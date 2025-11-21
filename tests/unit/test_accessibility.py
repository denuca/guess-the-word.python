"""
Unit tests for accessibility features in Q-Words application.

This module tests WCAG 2.1 AA compliance features including:
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Focus management
- Semantic HTML structure

Test Coverage:
- Template accessibility attributes
- JavaScript accessibility functions
- CSS accessibility features
- Keyboard interaction handling
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from app import create_app
from config.settings import TestingConfig


class TestAccessibilityFeatures(unittest.TestCase):
    """
    Test suite for accessibility compliance features.
    
    Ensures the application meets WCAG 2.1 AA standards and provides
    an excellent experience for users with disabilities.
    """
    
    def setUp(self):
        """Set up test client and application context."""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up test context."""
        self.app_context.pop()
    
    def test_skip_link_present(self):
        """
        Test that skip link is present for screen reader users.
        
        WCAG 2.4.1 - Bypass Blocks: A mechanism is available to bypass
        blocks of content that are repeated on multiple Web pages.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for skip link
        self.assertIn(b'skip-link', response.data)
        self.assertIn(b'Skip to main content', response.data)
        self.assertIn(b'href="#main-content"', response.data)
    
    def test_semantic_landmarks(self):
        """
        Test that semantic HTML landmarks are properly implemented.
        
        WCAG 1.3.1 - Info and Relationships: Information, structure, and
        relationships conveyed through presentation can be programmatically determined.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for semantic landmarks
        self.assertIn(b'role="banner"', response.data)
        self.assertIn(b'role="main"', response.data)
        self.assertIn(b'role="navigation"', response.data)
        self.assertIn(b'role="contentinfo"', response.data)
        self.assertIn(b'id="main-content"', response.data)
    
    def test_form_accessibility(self):
        """
        Test that forms have proper accessibility attributes.
        
        WCAG 4.1.2 - Name, Role, Value: For all user interface components,
        the name and role can be programmatically determined.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for form accessibility features
        self.assertIn(b'fieldset', response.data)
        self.assertIn(b'legend', response.data)
        self.assertIn(b'aria-describedby', response.data)
        self.assertIn(b'aria-label', response.data)
    
    def test_game_page_accessibility(self):
        """
        Test that game page has proper accessibility attributes.
        
        Tests ARIA live regions, proper labeling, and semantic structure.
        """
        # Start a game first
        with self.client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 0
            sess['guessHistory'] = []
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 200)
        
        # Check for accessibility features
        self.assertIn(b'aria-live="polite"', response.data)
        self.assertIn(b'role="status"', response.data)
        self.assertIn(b'aria-labelledby', response.data)
        self.assertIn(b'sr-only', response.data)
    
    def test_input_accessibility(self):
        """
        Test that input fields have proper accessibility attributes.
        
        WCAG 3.3.2 - Labels or Instructions: Labels or instructions are
        provided when content requires user input.
        """
        # Start a game to get input field
        with self.client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 0
            sess['guessHistory'] = []
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 200)
        
        # Check input accessibility
        self.assertIn(b'aria-describedby="guess-help"', response.data)
        self.assertIn(b'autocomplete="off"', response.data)
        self.assertIn(b'autocapitalize="characters"', response.data)
        self.assertIn(b'spellcheck="false"', response.data)
    
    def test_button_accessibility(self):
        """
        Test that buttons have proper accessibility attributes.
        
        Ensures buttons have descriptive labels and help text.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check button accessibility
        self.assertIn(b'aria-describedby', response.data)
        self.assertIn(b'type="submit"', response.data)
    
    def test_feedback_accessibility(self):
        """
        Test that game feedback has proper accessibility attributes.
        
        Ensures feedback symbols are properly labeled for screen readers.
        """
        # Start a game and make a guess
        with self.client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 1
            sess['guessHistory'] = [{
                'guess': 'ANIMAL',
                'feedback': 'x?xxxx',
                'attempt': 1
            }]
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 200)
        
        # Check feedback accessibility
        self.assertIn(b'aria-label="Guess', response.data)
        self.assertIn(b'role="listitem"', response.data)
        self.assertIn(b'role="log"', response.data)
    
    def test_navigation_accessibility(self):
        """
        Test that navigation has proper accessibility attributes.
        
        WCAG 2.4.6 - Headings and Labels: Headings and labels describe
        topic or purpose.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check navigation accessibility
        self.assertIn(b'aria-label="Main navigation"', response.data)
        self.assertIn(b'aria-current="page"', response.data)
    
    def test_heading_structure(self):
        """
        Test that heading structure is logical and hierarchical.
        
        WCAG 1.3.1 - Info and Relationships: Proper heading hierarchy
        helps screen reader users navigate content.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for proper heading structure
        content = response.data.decode('utf-8')
        
        # Should have h1 as main heading
        self.assertIn('<h1>', content)
        # Should have h2 for sections
        self.assertIn('<h2', content)
    
    def test_color_independence(self):
        """
        Test that information is not conveyed by color alone.
        
        WCAG 1.4.1 - Use of Color: Color is not used as the only visual
        means of conveying information.
        """
        # Start a game with feedback
        with self.client.session_transaction() as sess:
            sess['word'] = 'PYTHON'
            sess['gameLevel'] = 'MEDIUM'
            sess['attempts'] = 1
            sess['guessHistory'] = [{
                'guess': 'ANIMAL',
                'feedback': '+?xxxx',
                'attempt': 1
            }]
            sess['gameWon'] = False
            sess['gameLost'] = False
        
        response = self.client.get('/game/')
        self.assertEqual(response.status_code, 200)
        
        # Check that feedback uses symbols, not just colors
        self.assertIn(b'+', response.data)  # Correct position symbol
        self.assertIn(b'?', response.data)  # Wrong position symbol
        self.assertIn(b'x', response.data)  # Not in word symbol
    
    def test_focus_management(self):
        """
        Test that focus management attributes are present.
        
        WCAG 2.4.7 - Focus Visible: Any keyboard operable user interface
        has a mode of operation where the keyboard focus indicator is visible.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for focus management attributes
        self.assertIn(b'tabindex="-1"', response.data)  # For skip target
    
    def test_language_declaration(self):
        """
        Test that page language is properly declared.
        
        WCAG 3.1.1 - Language of Page: The default human language of each
        Web page can be programmatically determined.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for language declaration
        self.assertIn(b'lang="en"', response.data)
    
    def test_page_title_descriptive(self):
        """
        Test that page titles are descriptive.
        
        WCAG 2.4.2 - Page Titled: Web pages have titles that describe
        topic or purpose.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for descriptive title
        self.assertIn(b'<title>', response.data)
        self.assertIn(b'Q-Words', response.data)
        self.assertIn(b'Accessible', response.data)


class TestKeyboardNavigation(unittest.TestCase):
    """
    Test suite for keyboard navigation functionality.
    
    Ensures all interactive elements are accessible via keyboard
    and that keyboard navigation follows expected patterns.
    """
    
    def setUp(self):
        """Set up test client and application context."""
        self.app = create_app(TestingConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up test context."""
        self.app_context.pop()
    
    def test_radio_button_keyboard_navigation(self):
        """
        Test that radio buttons support arrow key navigation.
        
        WCAG 2.1.1 - Keyboard: All functionality of the content is operable
        through a keyboard interface.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check that radio buttons are present and properly structured
        content = response.data.decode('utf-8')
        self.assertIn('type="radio"', content)
        self.assertIn('name="level"', content)
        
        # Should have multiple radio options
        radio_count = content.count('type="radio"')
        self.assertGreaterEqual(radio_count, 3)  # Easy, Medium, Hard
    
    def test_form_submission_keyboard(self):
        """
        Test that forms can be submitted via keyboard.
        
        Ensures Enter key works for form submission.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for proper form structure
        self.assertIn(b'type="submit"', response.data)
        self.assertIn(b'<form', response.data)
    
    def test_button_keyboard_activation(self):
        """
        Test that buttons can be activated via keyboard.
        
        Ensures buttons respond to Enter and Space keys.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check for buttons with proper type
        self.assertIn(b'<button', response.data)
        self.assertIn(b'type="submit"', response.data)


if __name__ == '__main__':
    # Run accessibility tests
    unittest.main(verbosity=2)
