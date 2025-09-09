"""
BOMB DEFUSER GAME - Main Application Entry Point
================================================================

PURPOSE: Python debugging game where players defuse bombs by fixing code errors
AUTHOR: Coding Club Presentation Tool
VERSION: 1.0

DESCRIPTION:
A 10-level progressive difficulty game combining mathematical programming problems
with Python debugging skills. Players must fix errors to "cut wires" and defuse bombs.

DEPENDENCIES:
- PyQt5: GUI framework and widgets  
- Pygments: Python syntax highlighting
- ast: Code validation and parsing
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QSplitter, QLabel, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor

from game_controller import GameController
from code_editor import CodeEditor
from bomb_widget import BombWidget


class BombDefuserGame(QMainWindow):
    """
    MAIN APPLICATION WINDOW
    
    PURPOSE: Central coordinator for all game components and UI layout
    
    FUNCTIONALITY:
    - Creates split-panel layout with code editor and bomb visualization
    - Initializes game controller and manages application state  
    - Handles window styling and dark theme application
    - Coordinates communication between UI components
    """
    
    def __init__(self):
        super().__init__()
        self.game_controller = GameController(self)
        self.init_ui()
        self.apply_dark_theme()
        
    def init_ui(self):
        """
        INITIALIZE USER INTERFACE LAYOUT
        
        PURPOSE: Set up split-panel layout with code editor and bomb display
        
        LAYOUT STRUCTURE:
        Main Window
        ├── Central Widget (QSplitter)
        │   ├── Left Panel: Code Editor + Controls  
        │   └── Right Panel: Bomb Visualization + Timer
        """
        # Set window properties
        self.setWindowTitle("BOMB DEFUSER - Python Debugging Game")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1000, 600)
        
        # Create central widget with horizontal splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel: Code editor section
        self.left_panel = self.create_left_panel()
        splitter.addWidget(self.left_panel)
        
        # Right panel: Bomb visualization section  
        self.right_panel = self.create_right_panel()
        splitter.addWidget(self.right_panel)
        
        # Set initial splitter proportions (60% code, 40% bomb)
        splitter.setSizes([840, 560])
        
        # Initialize game controller with UI components
        self.game_controller.initialize_game(self.code_editor, self.bomb_widget)
        
    def create_left_panel(self):
        """
        CREATE LEFT PANEL - Code Editor Section
        
        PURPOSE: Container for code editing, controls, and game information
        
        COMPONENTS:
        - Game status header with level/timer info
        - Code editor with syntax highlighting  
        - Control buttons and hint display area
        """
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Game status header
        self.status_label = QLabel("LEVEL 1 - Defuse the Bomb!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #00ff00;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                border: 2px solid #444;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Code editor
        self.code_editor = CodeEditor()
        layout.addWidget(self.code_editor)
        
        # Set layout proportions (small header, large editor)
        layout.setStretchFactor(self.status_label, 0)
        layout.setStretchFactor(self.code_editor, 1)
        
        return panel
        
    def create_right_panel(self):
        """
        CREATE RIGHT PANEL - Bomb Visualization Section
        
        PURPOSE: Container for bomb display, timer, and game progress with club logo
        
        COMPONENTS:
        - Club logo display (persistent)
        - Level information display
        - Bomb widget with wire animations
        - Timer and progress indicators
        """
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # Club logo in top-right corner of game screen
        self.club_logo_label = QLabel("CODING CLUB")
        self.club_logo_label.setAlignment(Qt.AlignCenter)
        self.club_logo_label.setFixedSize(120, 60)
        self.club_logo_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #00ff00;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
                border: 2px solid #444;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.club_logo_label)
        
        # Level info header
        self.level_info = QLabel("MISSION: Debug the Algorithm")
        self.level_info.setAlignment(Qt.AlignCenter)
        self.level_info.setStyleSheet("""
            QLabel {
                background-color: #4a0000;
                color: #ffaa00;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border: 2px solid #aa0000;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.level_info)
        
        # Bomb visualization widget
        self.bomb_widget = BombWidget()
        layout.addWidget(self.bomb_widget)
        
        # Set layout proportions
        layout.setStretchFactor(self.club_logo_label, 0)  # Fixed size logo
        layout.setStretchFactor(self.level_info, 0)       # Fixed size header
        layout.setStretchFactor(self.bomb_widget, 1)      # Expandable bomb display
        
        return panel
        
    def show_game_screen(self):
        """Switch to game screen and initialize game"""
        self.stacked_widget.setCurrentWidget(self.game_screen)
        
        # Copy logo from start screen if available
        if (hasattr(self.start_screen, 'logo_label') and 
            self.start_screen.logo_label.pixmap() and 
            not self.start_screen.logo_label.pixmap().isNull()):
            scaled_pixmap = self.start_screen.logo_label.pixmap().scaled(
                110, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.club_logo_label.setPixmap(scaled_pixmap)
            self.club_logo_label.setText("")
        
        # Initialize game controller with UI components
        if hasattr(self, 'code_editor') and hasattr(self, 'bomb_widget'):
            self.game_controller.initialize_game(self.code_editor, self.bomb_widget)
        
    def apply_dark_theme(self):
        """
        APPLY DARK THEME STYLING
        
        PURPOSE: Create professional "hacker" aesthetic with dark colors
        
        THEME COLORS:
        - Background: Dark gray (#1e1e1e)
        - Text: Light colors (#ffffff, #00ff00)  
        - Accents: Green (#00ff00) and amber (#ffaa00)
        - Danger: Red (#ff0000)
        """
        # Set application-wide dark palette
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)
        
        # Set application stylesheet for additional styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #555;
            }
            QSplitter::handle {
                background-color: #555;
                width: 3px;
            }
            QSplitter::handle:hover {
                background-color: #00ff00;
            }
        """)
        
    def update_status(self, level, message):
        """
        UPDATE GAME STATUS DISPLAY
        
        PURPOSE: Update status label with current level and game information
        
        INPUTS:
        - level: Current level number (1-10)
        - message: Status message to display
        """
        self.status_label.setText(f"LEVEL {level} - {message}")
        
    def update_level_info(self, info_text):
        """
        UPDATE LEVEL INFORMATION DISPLAY
        
        PURPOSE: Update level info with current mission description
        
        INPUTS:
        - info_text: Mission description or level-specific information
        """
        self.level_info.setText(f"MISSION: {info_text}")


def main():
    """
    APPLICATION ENTRY POINT
    
    PURPOSE: Initialize PyQt5 application and start the game
    
    EXECUTION FLOW:
    1. Create QApplication instance
    2. Initialize main game window
    3. Display window and start event loop
    4. Handle clean application exit
    """
    # Create PyQt5 application
    app = QApplication(sys.argv)
    app.setApplicationName("Bomb Defuser")
    app.setApplicationVersion("1.0")
    
    # Set application font for consistency
    font = QFont("Consolas", 10)
    font.setStyleHint(QFont.Monospace)
    app.setFont(font)
    
    # Create and show main window
    game = BombDefuserGame()
    game.show()
    
    # Start application event loop
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nGame terminated by user")
        sys.exit(0)


if __name__ == "__main__":
    main()