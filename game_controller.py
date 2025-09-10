"""
GAME CONTROLLER - Central Game Logic and State Management
========================================================

PURPOSE: Coordinate all game components and manage game progression
AUTHOR: Bomb Defuser Game
VERSION: 1.0

DESCRIPTION:
Central orchestrator for the bomb defusing game that handles:
- Level progression and difficulty scaling
- Code validation and error checking
- Timer management and hint system activation
- Win/lose logic and game state transitions
- Communication between UI components

DEPENDENCIES:
- level_manager: Level data and validation logic
- PyQt5.QtCore: Timer and signal management
- ast: Python code parsing and comparison
"""

import ast
import time
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from level_manager import LevelManager


class GameController(QObject):
    """
    CENTRAL GAME CONTROLLER
    
    PURPOSE: Orchestrate all game logic and component communication
    
    FUNCTIONALITY:
    - Manage game state and level progression
    - Coordinate timer, editor, and bomb widget interactions
    - Handle code validation and error detection
    - Control hint system and difficulty progression
    - Process win/lose conditions and state transitions
    
    SIGNALS:
    - level_completed: Emitted when level is successfully completed
    - game_over: Emitted when player fails (timer expires)  
    - game_won: Emitted when all levels are completed
    """
    
    # Qt signals for game events
    level_completed = pyqtSignal(int)  # Level number completed
    game_over = pyqtSignal(str)        # Game over with reason
    game_won = pyqtSignal()            # All levels completed
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.level_manager = LevelManager()
        self.init_game_state()
        
    def init_game_state(self):
        """
        INITIALIZE GAME STATE VARIABLES
        
        PURPOSE: Set up all game tracking and state management variables
        
        STATE VARIABLES:
        - Current level and progression tracking
        - Timer state and hint availability
        - Error tracking for wire cutting logic
        - Game completion and failure states
        """
        # Level and progression state
        self.current_level = 1
        self.max_level = 10
        self.levels_completed = 0
        
        # Timer and hint state
        self.level_start_time = None
        self.hint_available = False
        self.hint_shown = False
        
        # Error tracking for wire cutting
        self.errors_found = []
        self.errors_fixed = []
        self.total_errors_in_level = 0
        
        # Game state flags
        self.game_active = False
        self.level_completed_flag = False
        
        # UI component references (set during initialization)
        self.code_editor = None
        self.bomb_widget = None
        
    def initialize_game(self, code_editor, bomb_widget):
        """
        INITIALIZE GAME WITH UI COMPONENTS
        
        PURPOSE: Connect game controller to UI components and start first level
        
        INPUTS:
        - code_editor: CodeEditor widget instance
        - bomb_widget: BombWidget instance for timer and animations
        
        FUNCTIONALITY:
        - Store component references for communication
        - Connect signals between components
        - Load and start first level
        - Initialize all component states
        """
        # Store component references
        self.code_editor = code_editor
        self.bomb_widget = bomb_widget
        
        # Connect code editor signals
        self.code_editor.code_submitted.connect(self.validate_code)
        self.code_editor.syntax_error_found.connect(self.on_syntax_error)
        self.code_editor.restart_requested.connect(self.restart_level)
        
        # Connect bomb widget signals  
        self.bomb_widget.timer_expired.connect(self.on_timer_expired)
        self.bomb_widget.bomb_defused.connect(self.on_level_completed)
        
        # Start first level
        self.start_level(1)
        
    def start_level(self, level_number):
        """
        START NEW LEVEL
        
        PURPOSE: Initialize and begin a specific game level
        
        INPUTS:
        - level_number: Level to start (1-10)
        
        FUNCTIONALITY:
        - Load level data and broken code
        - Reset bomb widget and timer
        - Configure difficulty and time limits (doubled)
        - Update UI displays with level information
        - Start countdown timer
        - Set hint to appear 30 seconds before timer expires
        """
        self.current_level = level_number
        self.level_completed_flag = False
        self.hint_shown = False
        self.hint_available = False
        
        # Load level data
        level_data = self.level_manager.get_level(level_number)
        
        if not level_data:
            self.game_over.emit(f"Failed to load level {level_number}")
            return
            
        # Set level information
        self.total_errors_in_level = len(level_data['errors'])
        self.errors_found = []
        self.errors_fixed = []
        
        # Update UI components
        self.update_level_displays(level_data)
        
        # Set code in editor
        self.code_editor.set_code(level_data['broken_code'])
        
        # Reset and configure bomb widget
        self.bomb_widget.reset_bomb()
        
        # Start timer based on level difficulty (doubled)
        time_limit = self.calculate_time_limit(level_number)
        self.bomb_widget.start_timer(time_limit)
        self.level_start_time = time.time()
        
        # Set up hint timer
        if time_limit > 0:  
            hint_delay = int(time_limit * 0.8 * 1000)
            QTimer.singleShot(hint_delay, self.activate_hint_system)
        
        # Mark game as active
        self.game_active = True
        
        print(f"Started Level {level_number}: {level_data['title']}")
        print(f"Timer: {time_limit} seconds, Hint in: { time_limit * 0.8} seconds")
        
    def calculate_time_limit(self, level_number):
        """
        CALCULATE TIME LIMIT FOR LEVEL (DOUBLED DURATIONS)
        
        PURPOSE: Determine countdown time based on level difficulty with doubled timer
        
        INPUTS:
        - level_number: Current level (1-10)
        
        RETURNS:
        - Time limit in seconds (doubled from original)
        
        TIME SCALING (DOUBLED):
        - Level 1: 60 seconds (was 30)
        - Level 10: 600 seconds (was 300)
        - Progressive scaling between levels
        """
        # Base time: 60 seconds for level 1 (doubled from 30)
        # Max time: 600 seconds for level 10 (doubled from 300)
        # Linear scaling with slight curve for middle levels
        
        if level_number == 1:
            return 60  # Doubled from 30
        elif level_number <= 3:
            return 60 + (level_number - 1) * 30  # 60, 90, 120 (doubled from 30, 45, 60)
        elif level_number <= 6:
            return 120 + (level_number - 3) * 60  # 180, 240, 300 (doubled from 90, 120, 150)
        else:
            return 300 + (level_number - 6) * 75  # 375, 450, 525, 600 (doubled from 187.5, 225, 262.5, 300)
            
        # Ensure integer result
        return int(60 + (level_number - 1) * 60)  # Simplified doubled formula
        
    def update_level_displays(self, level_data):
        """
        UPDATE UI DISPLAYS WITH LEVEL INFORMATION
        
        PURPOSE: Update main window displays with current level info
        
        INPUTS:
        - level_data: Dictionary containing level information
        
        FUNCTIONALITY:
        - Update status labels with level number and title
        - Update mission description
        - Configure UI colors and styling for level theme
        """
        # Update main window status
        status_message = f"Defuse the Bomb! ({level_data['difficulty']})"
        self.main_window.update_status(self.current_level, status_message)
        
        # Update level information
        mission_text = f"{level_data['title']} - {level_data['description']}"
        self.main_window.update_level_info(mission_text)
        
    def validate_code(self, submitted_code):
        """
        VALIDATE SUBMITTED CODE
        
        PURPOSE: Check if submitted code fixes the errors and solves the problem
        
        INPUTS:
        - submitted_code: Code submitted by player
        
        FUNCTIONALITY:
        - Parse and validate Python syntax
        - Compare with expected solution patterns
        - Execute code with test cases
        - Track error fixing progress
        - Trigger wire cutting animations for fixed errors
        """
        if not self.game_active or self.level_completed_flag:
            return
            
        # Get current level data
        level_data = self.level_manager.get_level(self.current_level)
        
        if not level_data:
            return
            
        try:
            # First check: Syntax validation
            ast.parse(submitted_code)
            
            # Second check: Execute code with test cases
            validation_result = self.level_manager.validate_solution(
                self.current_level, submitted_code
            )
            
            if validation_result['valid']:
                # Solution is correct!
                self.on_correct_solution(validation_result)
            else:
                # Solution has issues
                self.on_incorrect_solution(validation_result)
                
        except SyntaxError as e:
            # Syntax error still present
            self.code_editor.update_status(
                f"✗ Syntax Error: {e.msg}", "error"
            )
        except Exception as e:
            # Runtime or other error
            self.code_editor.update_status(
                f"✗ Runtime Error: {str(e)}", "error"
            )
            
    def on_correct_solution(self, validation_result):
        """
        HANDLE CORRECT SOLUTION
        
        PURPOSE: Process successful level completion
        
        INPUTS:
        - validation_result: Dictionary with validation details
        
        FUNCTIONALITY:
        - Cut all remaining wires instantly
        - Update UI with success feedback
        - Trigger level completion sequence
        - Prepare for next level or game completion
        """
        print(f"Level {self.current_level} completed successfully!")
        
        # Cut all wires rapidly
        wire_names = ['red', 'blue', 'green', 'yellow']
        for i, wire in enumerate(wire_names):
            QTimer.singleShot(i * 200, lambda w=wire: self.bomb_widget.cut_wire(w))
            
        # Update editor status
        self.code_editor.update_status("✓ Solution Correct! Bomb Defused!", "success")
        
        # Mark level as completed
        self.level_completed_flag = True
        
        # Level completion will be handled by bomb_defused signal
        
    def on_incorrect_solution(self, validation_result):
        """
        HANDLE INCORRECT SOLUTION
        
        PURPOSE: Process failed solution attempt
        
        INPUTS:
        - validation_result: Dictionary with error details
        
        FUNCTIONALITY:
        - Provide feedback on remaining errors
        - Check for partial progress (some errors fixed)
        - Cut wires for fixed errors
        - Update UI with helpful feedback
        - Show restart option for difficult levels
        """
        errors_remaining = validation_result.get('errors', [])
        errors_fixed_count = validation_result.get('errors_fixed', 0)
        
        # Cut wires for errors that were fixed
        if errors_fixed_count > len(self.errors_fixed):
            newly_fixed = errors_fixed_count - len(self.errors_fixed)
            wire_names = ['red', 'blue', 'green', 'yellow']
            
            for i in range(newly_fixed):
                if len(self.errors_fixed) + i < len(wire_names):
                    wire = wire_names[len(self.errors_fixed) + i]
                    self.bomb_widget.cut_wire(wire)
                    
            # Update errors fixed list
            self.errors_fixed = list(range(errors_fixed_count))
            
        # Provide feedback
        if errors_remaining:
            error_msg = f"✗ {len(errors_remaining)} error(s) remaining"
            self.code_editor.update_status(error_msg, "warning")
            
            # Show restart button if user is struggling (more than 3 failed attempts could be tracked)
            # For now, show it after any incorrect solution
            self.code_editor.show_restart_button()
        else:
            self.code_editor.update_status("✗ Logic error in solution", "error")
            self.code_editor.show_restart_button()
            
    def on_syntax_error(self, error_message, line_number):
        """
        HANDLE SYNTAX ERROR DETECTION
        
        PURPOSE: Process real-time syntax error detection
        
        INPUTS:
        - error_message: Description of syntax error
        - line_number: Line number with error
        
        FUNCTIONALITY:
        - Track syntax error detection
        - Provide real-time feedback to player
        - No wire cutting for syntax errors (only for logical fixes)
        """
        # Real-time syntax errors don't trigger wire cutting
        # Only successful code execution cuts wires
        pass
        
    def activate_hint_system(self):
        """
        ACTIVATE HINT SYSTEM
        
        PURPOSE: Make hints available when 30 seconds remain on timer
        
        FUNCTIONALITY:
        - Mark hint as available
        - Generate hint showing actual error messages from level data
        - Display hint in code editor with specific bug information
        - Provide visual indication that help is available
        """
        if not self.game_active or self.level_completed_flag or self.hint_shown:
            return
            
        self.hint_available = True
        
        # Get level data for current level
        level_data = self.level_manager.get_level(self.current_level)
        
        if level_data and 'errors' in level_data:
            # Create hint text from actual error messages
            errors = level_data['errors']
            
            if len(errors) == 1:
                # Single error
                hint_text = f"🐛 BUG DETECTED: {errors[0]}"
            else:
                # Multiple errors
                hint_text = "🐛 BUGS DETECTED:\n"
                for i, error in enumerate(errors, 1):
                    hint_text += f"{i}. {error}\n"
            
            # Add encouraging message
            hint_text += "\n💡 Fix these issues to defuse the bomb!"
            
            self.code_editor.show_hint(hint_text)
            self.hint_shown = True
            
            print(f"Hint activated for level {self.current_level}: Showing {len(errors)} error(s)")
        
        elif level_data and 'hint' in level_data:
            # Fallback to generic hint if errors field is missing
            hint_text = f"💡 DEBUGGING HINT: {level_data['hint']}"
            self.code_editor.show_hint(hint_text)
            self.hint_shown = True
            
            print(f"Hint activated for level {self.current_level} (fallback to generic hint)")
        
        else:
            print(f"No hint data available for level {self.current_level}")
            
    def on_timer_expired(self):
        """
        HANDLE TIMER EXPIRATION
        
        PURPOSE: Process bomb explosion when countdown reaches zero
        
        FUNCTIONALITY:
        - Stop game activity
        - Trigger bomb explosion animation
        - Display game over message
        - Show restart button for retry option
        """
        self.game_active = False
        
        print(f"Timer expired on level {self.current_level}")
        
        # Update UI
        self.code_editor.update_status("💥 BOOM! Timer expired!", "error")
        
        # Show restart button so user can try again
        self.code_editor.show_restart_button()
        
        # Emit game over signal
        self.game_over.emit("Time expired - Bomb exploded!")
        
    def on_level_completed(self):
        """
        HANDLE LEVEL COMPLETION
        
        PURPOSE: Process successful level completion and advance game
        
        FUNCTIONALITY:
        - Stop current level timer
        - Update completion statistics
        - Check if game is fully completed
        - Advance to next level or trigger game completion
        """
        if not self.level_completed_flag:
            return
            
        self.game_active = False
        self.levels_completed += 1
        
        print(f"Level {self.current_level} completed! ({self.levels_completed}/{self.max_level})")
        
        # Emit level completion signal
        self.level_completed.emit(self.current_level)
        
        # Check if all levels completed
        if self.current_level >= self.max_level:
            # Game won!
            self.game_won.emit()
            print("🎉 All levels completed! Game won!")
        else:
            # Advance to next level after delay
            next_level = self.current_level + 1
            QTimer.singleShot(3000, lambda: self.start_level(next_level))
            
    def restart_level(self):
        """
        RESTART CURRENT LEVEL
        
        PURPOSE: Allow player to retry current level after failure
        
        FUNCTIONALITY:
        - Reset all level state
        - Reload level data and timer
        - Clear UI state and error tracking
        - Restart countdown and game activity
        """
        print(f"Restarting level {self.current_level}")
        self.start_level(self.current_level)
        
    def restart_game(self):
        """
        RESTART ENTIRE GAME
        
        PURPOSE: Reset game to beginning for new playthrough
        
        FUNCTIONALITY:
        - Reset all game state variables
        - Return to level 1
        - Clear all progress tracking
        - Reinitialize UI components
        """
        print("Restarting entire game")
        
        # Reset game state
        self.current_level = 1
        self.levels_completed = 0
        self.init_game_state()
        
        # Start from level 1
        self.start_level(1)
        
    def get_game_statistics(self):
        """
        GET GAME STATISTICS
        
        PURPOSE: Return current game progress and statistics
        
        RETURNS:
        - Dictionary with game statistics and progress
        
        STATISTICS:
        - Current level and completion status
        - Time spent on current level
        - Levels completed count
        - Overall game progress percentage
        """
        current_time = time.time() if self.level_start_time else 0
        time_on_level = current_time - self.level_start_time if self.level_start_time else 0
        
        return {
            'current_level': self.current_level,
            'levels_completed': self.levels_completed,
            'max_level': self.max_level,
            'progress_percent': (self.levels_completed / self.max_level) * 100,
            'time_on_current_level': time_on_level,
            'game_active': self.game_active,
            'hint_available': self.hint_available,
            'hint_shown': self.hint_shown
        }