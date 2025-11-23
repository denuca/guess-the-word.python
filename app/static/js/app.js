// Guess The Word Game - Accessible JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize accessibility features
    initializeAccessibility();
    
    // Auto-focus guess input on game page
    const guessInput = document.getElementById('guess-input');
    if (guessInput) {
        guessInput.focus();
        
        // Auto-uppercase input and validate
        guessInput.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
            validateInput(this);
        });
        
        // Prevent non-alphabetic characters
        guessInput.addEventListener('keypress', function(e) {
            const char = String.fromCharCode(e.which);
            if (!/[A-Za-z]/.test(char) && !isControlKey(e)) {
                e.preventDefault();
                announceToScreenReader('Only letters are allowed');
            }
        });
        
        // Handle paste events
        guessInput.addEventListener('paste', function(e) {
            setTimeout(() => {
                const value = this.value.replace(/[^A-Za-z]/g, '').toUpperCase();
                this.value = value.substring(0, this.maxLength);
                validateInput(this);
            }, 0);
        });
    }
    
    // Enhanced keyboard navigation for level selection
    const levelOptions = document.querySelectorAll('input[name="level"]');
    levelOptions.forEach((radio, index) => {
        radio.addEventListener('keydown', function(e) {
            handleRadioKeydown(e, levelOptions, index);
        });
    });
    
    // Form submission for guess
    const guessForm = document.querySelector('.guess-form');
    if (guessForm) {
        guessForm.addEventListener('submit', function(e) {
            const input = document.getElementById('guess-input');
            const guess = input.value.trim();
            
            // Basic validation
            if (!guess) {
                e.preventDefault();
                announceToScreenReader('Please enter a guess');
                input.focus();
                return;
            }
            
            if (!/^[A-Za-z]+$/.test(guess)) {
                e.preventDefault();
                announceToScreenReader('Please enter only letters');
                input.focus();
                return;
            }
            
            if (guess.length !== parseInt(input.maxLength)) {
                e.preventDefault();
                announceToScreenReader(`Please enter exactly ${input.maxLength} letters`);
                input.focus();
                return;
            }
            
            // Let form submit normally - page will refresh with updated state
        });
    }
    
    // Keyboard shortcuts with announcements
    document.addEventListener('keydown', function(e) {
        handleGlobalKeyboard(e);
    });
    
    // Add focus management for dynamic content
    manageFocusForDynamicContent();
    
    // Announce game state changes
    announceGameStateChanges();
});

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Create live region for announcements
    if (!document.getElementById('aria-live-region')) {
        const liveRegion = document.createElement('div');
        liveRegion.id = 'aria-live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);
    }
    
    // Add skip links functionality
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
        skipLink.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.focus();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }
    
    // Enhance button accessibility
    enhanceButtonAccessibility();
}

/**
 * Validate input and provide feedback
 */
function validateInput(input) {
    const value = input.value;
    const maxLength = parseInt(input.maxLength);
    const minLength = parseInt(input.minLength) || maxLength;
    
    // Remove invalid attribute if input is valid
    if (value.length === maxLength && /^[A-Z]+$/.test(value)) {
        input.removeAttribute('aria-invalid');
        input.setCustomValidity('');
    } else if (value.length > 0) {
        input.setAttribute('aria-invalid', 'true');
        if (value.length < minLength) {
            input.setCustomValidity(`Word must be exactly ${maxLength} letters`);
        } else if (!/^[A-Z]+$/.test(value)) {
            input.setCustomValidity('Only letters are allowed');
        }
    }
}

/**
 * Check if key is a control key
 */
function isControlKey(e) {
    return e.ctrlKey || e.metaKey || e.altKey || 
           [8, 9, 13, 27, 37, 38, 39, 40, 46].includes(e.keyCode);
}

/**
 * Handle radio button keyboard navigation
 */
function handleRadioKeydown(e, radios, currentIndex) {
    let newIndex = currentIndex;
    
    switch(e.key) {
        case 'ArrowDown':
        case 'ArrowRight':
            e.preventDefault();
            newIndex = (currentIndex + 1) % radios.length;
            break;
        case 'ArrowUp':
        case 'ArrowLeft':
            e.preventDefault();
            newIndex = currentIndex === 0 ? radios.length - 1 : currentIndex - 1;
            break;
        case 'Home':
            e.preventDefault();
            newIndex = 0;
            break;
        case 'End':
            e.preventDefault();
            newIndex = radios.length - 1;
            break;
        default:
            return;
    }
    
    radios[newIndex].checked = true;
    radios[newIndex].focus();
    announceToScreenReader(`Selected ${radios[newIndex].nextElementSibling.textContent.trim()}`);
}

/**
 * Handle global keyboard shortcuts
 */
function handleGlobalKeyboard(e) {
    // Escape key functionality
    if (e.key === 'Escape') {
        const resetButton = document.querySelector('.reset-button');
        if (resetButton && confirm('Are you sure you want to start a new game?')) {
            resetButton.click();
        }
    }
    
    // Enter key on home page
    if (e.key === 'Enter' && document.querySelector('.start-button')) {
        const startButton = document.querySelector('.start-button');
        if (startButton && document.activeElement !== startButton && 
            !document.activeElement.matches('input, button, a')) {
            startButton.focus();
        }
    }
}

/**
 * Enhance button accessibility
 */
function enhanceButtonAccessibility() {
    const buttons = document.querySelectorAll('button, .home-button');
    buttons.forEach(button => {
        // Ensure minimum touch target size
        if (!button.style.minHeight) {
            button.style.minHeight = '44px';
        }
        if (!button.style.minWidth) {
            button.style.minWidth = '44px';
        }
        
        // Add keyboard interaction
        button.addEventListener('keydown', function(e) {
            if (e.key === ' ' || e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
    });
}

/**
 * Manage focus for dynamic content
 */
function manageFocusForDynamicContent() {
    // Store focus before page changes
    let lastFocusedElement = null;
    
    document.addEventListener('focusin', function(e) {
        lastFocusedElement = e.target;
    });
    
    // Restore focus after dynamic updates
    window.addEventListener('beforeunload', function() {
        if (lastFocusedElement) {
            sessionStorage.setItem('lastFocusedElement', lastFocusedElement.id || lastFocusedElement.tagName);
        }
    });
}

/**
 * Announce game state changes
 */
function announceGameStateChanges() {
    // Monitor game state changes
    const gameInfo = document.querySelector('.game-info');
    if (gameInfo) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' || mutation.type === 'characterData') {
                    const text = gameInfo.textContent.trim();
                    if (text) {
                        announceToScreenReader(text);
                    }
                }
            });
        });
        
        observer.observe(gameInfo, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
}

/**
 * Announce message to screen readers
 */
function announceToScreenReader(message) {
    const liveRegion = document.getElementById('aria-live-region');
    if (liveRegion) {
        liveRegion.textContent = message;
        
        // Clear after announcement
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 1000);
    }
}

// Add visual feedback for keyboard users
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// Add CSS for keyboard navigation
const style = document.createElement('style');
style.textContent = `
    .keyboard-navigation *:focus {
        outline: 3px solid #0066cc !important;
        outline-offset: 2px !important;
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in-out forwards;
        opacity: 0;
    }
    
    @keyframes fadeIn {
        to {
            opacity: 1;
        }
    }
    
    @media (prefers-reduced-motion: reduce) {
        .fade-in {
            animation: none;
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
