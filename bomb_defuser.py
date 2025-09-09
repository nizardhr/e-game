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
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout, 
                             QVBoxLayout, QSplitter, QLabel, QFrame, QStackedWidget,
                             QPushButton)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap

from game_controller import GameController
from code_editor import CodeEditor
from bomb_widget import BombWidget


class StartScreen(QWidget):
    """
    START SCREEN WIDGET
    
    PURPOSE: Display welcome screen with logo and start game button
    
    FUNCTIONALITY:
    - Show coding-themed welcome interface
    - Display auto-detected logo image
    - Provide "Start Game" button to enter main game
    - Apply consistent dark theme styling
    """
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()
        
    def init_ui(self):
        """
        INITIALIZE START SCREEN UI
        
        PURPOSE: Create welcome screen with logo and start button
        """
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        
        # Main title - REMOVED text-shadow to fix CSS warning
        title_label = QLabel("BOMB DEFUSER")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                margin: 20px;
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 15px;
                background-color: rgba(0, 255, 0, 0.1);
            }
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Python Debugging Game")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ffaa00;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Courier New', monospace;
                margin: 10px;
            }
        """)
        layout.addWidget(subtitle_label)
        
        # Logo display area
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setMinimumSize(200, 150)
        self.logo_label.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                border: 2px solid #444;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        # Try to load logo image, fallback to text
        logo_loaded = self.load_logo_image()
        if not logo_loaded:
            self.logo_label.setText("CODING CLUB")
            self.logo_label.setStyleSheet("""
                QLabel {
                    background-color: #2b2b2b;
                    color: #00ff00;
                    font-size: 18px;
                    font-weight: bold;
                    border: 2px solid #444;
                    border-radius: 10px;
                    padding: 20px;
                }
            """)
        
        layout.addWidget(self.logo_label)
        
        # Start game button - REMOVED transform to fix CSS warning
        start_button = QPushButton("🚀 START GAME")
        start_button.setMinimumHeight(60)
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #0e7490;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                font-family: 'Courier New', monospace;
            }
            QPushButton:hover {
                background-color: #0891b2;
                border: 2px solid #00ff00;
            }
            QPushButton:pressed {
                background-color: #0c7489;
            }
        """)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)
        
        # Add some spacing at bottom
        layout.addStretch()
        
    def load_logo_image(self):
        """
        LOAD LOGO IMAGE WITH AUTO-DETECTION
        
        PURPOSE: Automatically detect and load logo.png or logo.jpg
        
        RETURNS:
        - True if image was loaded successfully
        - False if no image found (will use text fallback)
        """
        # Check for logo files in current directory
        for extension in ['png', 'jpg', 'jpeg']:
            logo_path = f"logo.{extension}"
            if os.path.exists(logo_path):
                try:
                    pixmap = QPixmap(logo_path)
                    if not pixmap.isNull():
                        # Scale image to fit the label while maintaining aspect ratio
                        scaled_pixmap = pixmap.scaled(
                            180, 130, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        self.logo_label.setPixmap(scaled_pixmap)
                        return True
                except Exception as e:
                    print(f"Error loading logo image {logo_path}: {e}")
                    continue
        
        return False
        
    def start_game(self):
        """
        START GAME TRANSITION
        
        PURPOSE: Switch from start screen to main game interface
        """
        self.main_window.show_game_screen()


class BombDefuserGame(QMainWindow):
    """
    MAIN APPLICATION WINDOW
    
    PURPOSE: Central coordinator for all game components and screen management
    
    FUNCTIONALITY:
    - Manages screen transitions using QStackedWidget
    - Creates start screen and game interface
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
        INITIALIZE USER INTERFACE WITH SCREEN MANAGEMENT
        
        PURPOSE: Set up stacked widget architecture for start screen and game
        
        LAYOUT STRUCTURE:
        Main Window
        ├── QStackedWidget (Central Widget)
        │   ├── Start Screen (Index 0)
        │   └── Game Screen (Index 1)
        │       ├── Left Panel: Code Editor + Controls  
        │       └── Right Panel: Bomb Visualization + Timer
        """
        # Set window properties
        self.setWindowTitle("BOMB DEFUSER - Python Debugging Game")
        self.setGeometry(100, 100, 1400, 800)
        self.setMinimumSize(1000, 600)
        
        # Create stacked widget for screen management
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create and add start screen
        self.start_screen = StartScreen(self)
        self.stacked_widget.addWidget(self.start_screen)
        
        # Create and add game screen
        self.game_screen = self.create_game_screen()
        self.stacked_widget.addWidget(self.game_screen)
        
        # Start with the start screen
        self.stacked_widget.setCurrentWidget(self.start_screen)
        
    def create_game_screen(self):
        """
        CREATE GAME SCREEN INTERFACE
        
        PURPOSE: Create the main game interface with code editor and bomb display
        
        RETURNS:
        - QWidget containing the complete game interface
        """
        game_widget = QWidget()
        
        main_layout = QHBoxLayout(game_widget)
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
        
        return game_widget
        
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
        
        # Club logo with auto-detected image
        self.club_logo_label = QLabel("CODING CLUB")
        self.club_logo_label.setAlignment(Qt.AlignCenter)
        self.club_logo_label.setFixedSize(120, 60)
        
        # Try to load logo image, fallback to text
        logo_loaded = self.load_game_logo()
        if not logo_loaded:
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
        
    def load_game_logo(self):
        """
        LOAD LOGO IMAGE FOR GAME INTERFACE
        
        PURPOSE: Load auto-detected logo for the game interface
        
        RETURNS:
        - True if image was loaded successfully
        - False if no image found (will use text fallback)
        """
        # Check for logo files in current directory
        for extension in ['png', 'jpg', 'jpeg']:
            logo_path = f"logo.{extension}"
            if os.path.exists(logo_path):
                try:
                    pixmap = QPixmap(logo_path)
                    if not pixmap.isNull():
                        # Scale image to fit the smaller game interface label
                        scaled_pixmap = pixmap.scaled(
                            110, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
                        )
                        self.club_logo_label.setPixmap(scaled_pixmap)
                        self.club_logo_label.setText("")  # Clear text when image loaded
                        self.club_logo_label.setStyleSheet("""
                            QLabel {
                                background-color: #2b2b2b;
                                padding: 5px;
                                border: 2px solid #444;
                                border-radius: 5px;
                            }
                        """)
                        return True
                except Exception as e:
                    print(f"Error loading game logo image {logo_path}: {e}")
                    continue
        
        return False
        
    def show_game_screen(self):
        """
        SHOW GAME SCREEN AND INITIALIZE GAME
        
        PURPOSE: Transition from start screen to game interface and initialize game
        """
        self.stacked_widget.setCurrentWidget(self.game_screen)
        
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