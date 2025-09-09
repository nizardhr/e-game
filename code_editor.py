"""
CODE EDITOR - Python Code Editor with Syntax Highlighting
=========================================================

PURPOSE: Custom code editor widget with Python syntax highlighting and error detection
AUTHOR: Bomb Defuser Game  
VERSION: 1.0

DESCRIPTION:
Provides a professional code editing experience with:
- Python syntax highlighting using Pygments
- Real-time error detection and highlighting
- Hint system for debugging assistance
- Submit button for code validation
- Line numbers and professional appearance

DEPENDENCIES:
- PyQt5.QtWidgets: Editor widget components
- PyQt5.QtCore: Event handling and signals
- PyQt5.QtGui: Text formatting and styling
- Pygments: Python syntax highlighting
"""

import ast
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QLabel, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import (QFont, QTextCharFormat, QColor, QSyntaxHighlighter, 
                         QTextDocument, QTextCursor, QPalette)

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import get_formatter_by_name
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    print("Warning: Pygments not available. Using basic syntax highlighting.")


class PythonHighlighter(QSyntaxHighlighter):
    """
    PYTHON SYNTAX HIGHLIGHTER
    
    PURPOSE: Provide Python syntax highlighting for code editor
    
    FUNCTIONALITY:
    - Highlight Python keywords, strings, comments, and numbers
    - Use Pygments if available, fallback to basic highlighting
    - Support error highlighting for debugging feedback
    - Maintain professional code appearance
    """
    
    def __init__(self, document):
        super().__init__(document)
        self.init_highlighting_rules()
        
    def init_highlighting_rules(self):
        """
        INITIALIZE SYNTAX HIGHLIGHTING RULES
        
        PURPOSE: Set up text formats for different Python syntax elements
        
        HIGHLIGHTING COLORS:
        - Keywords: Blue (#569cd6)
        - Strings: Orange (#ce9178)  
        - Comments: Green (#6a9955)
        - Numbers: Light green (#b5cea8)
        - Functions: Yellow (#dcdcaa)
        """
        # Python keywords
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor(86, 156, 214))  # Blue
        self.keyword_format.setFontWeight(QFont.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        self.keyword_patterns = [(f'\\b{keyword}\\b', self.keyword_format) 
                                for keyword in keywords]
        
        # String literals
        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor(206, 145, 120))  # Orange
        self.string_patterns = [
            ('"[^"]*"', self.string_format),      # Double quotes
            ("'[^']*'", self.string_format),      # Single quotes
            ('""".*"""', self.string_format),     # Triple double quotes
            ("'''.*'''", self.string_format)      # Triple single quotes
        ]
        
        # Comments
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor(106, 153, 85))  # Green
        self.comment_format.setFontItalic(True)
        self.comment_pattern = ('#.*$', self.comment_format)
        
        # Numbers
        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor(181, 206, 168))  # Light green
        self.number_pattern = ('\\b\\d+\\.?\\d*\\b', self.number_format)
        
        # Functions
        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor(220, 220, 170))  # Yellow
        self.function_format.setFontWeight(QFont.Bold)
        self.function_pattern = ('\\b[a-zA-Z_][a-zA-Z0-9_]*(?=\\()', self.function_format)
        
        # Error highlighting
        self.error_format = QTextCharFormat()
        self.error_format.setBackground(QColor(255, 0, 0, 50))  # Red background
        self.error_format.setUnderlineStyle(QTextCharFormat.WaveUnderline)
        self.error_format.setUnderlineColor(QColor(255, 0, 0))
        
    def highlightBlock(self, text):
        """
        HIGHLIGHT TEXT BLOCK
        
        PURPOSE: Apply syntax highlighting to a block of text
        
        INPUTS:
        - text: Text block to highlight
        
        FUNCTIONALITY:
        - Apply keyword highlighting
        - Apply string and comment highlighting  
        - Apply number and function highlighting
        - Handle error highlighting overlays
        """
        import re
        
        # Apply keyword highlighting
        for pattern, format_obj in self.keyword_patterns:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format_obj)
                
        # Apply string highlighting
        for pattern, format_obj in self.string_patterns:
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, format_obj)
                
        # Apply comment highlighting
        pattern, format_obj = self.comment_pattern
        for match in re.finditer(pattern, text):
            start, end = match.span()
            self.setFormat(start, end - start, format_obj)
            
        # Apply number highlighting
        pattern, format_obj = self.number_pattern
        for match in re.finditer(pattern, text):
            start, end = match.span()
            self.setFormat(start, end - start, format_obj)
            
        # Apply function highlighting
        pattern, format_obj = self.function_pattern
        for match in re.finditer(pattern, text):
            start, end = match.span()
            self.setFormat(start, end - start, format_obj)


class CodeEditor(QWidget):
    """
    PYTHON CODE EDITOR WIDGET
    
    PURPOSE: Complete code editing interface for bomb defusing game
    
    FUNCTIONALITY:
    - Code editing with syntax highlighting
    - Real-time syntax error detection
    - Submit button for code validation
    - Hint display system for debugging assistance
    - Professional code editor appearance
    
    SIGNALS:
    - code_submitted: Emitted when user submits code for validation
    - syntax_error_found: Emitted when syntax errors are detected
    """
    
    # Qt signals for code events
    code_submitted = pyqtSignal(str)  # Emits code content
    syntax_error_found = pyqtSignal(str, int)  # Emits error message and line number
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_editor_settings()
        self.current_hint = None
        
    def init_ui(self):
        """
        INITIALIZE USER INTERFACE
        
        PURPOSE: Set up editor layout with text area, buttons, and hint display
        
        LAYOUT STRUCTURE:
        Main Widget
        ├── Code Text Editor (QTextEdit)
        ├── Control Panel
        │   ├── Submit Button
        │   └── Status Label
        └── Hint Display Area (collapsible)
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Main code editing area
        self.text_editor = QTextEdit()
        self.text_editor.setFont(QFont("Consolas", 12))
        self.text_editor.setTabStopWidth(40)  # 4-space tabs
        layout.addWidget(self.text_editor)
        
        # Control panel with buttons
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel)
        
        # Hint display area (initially hidden)
        self.hint_frame = self.create_hint_display()
        layout.addWidget(self.hint_frame)
        self.hint_frame.hide()
        
        # Set layout proportions
        layout.setStretchFactor(self.text_editor, 1)  # Editor takes most space
        layout.setStretchFactor(control_panel, 0)     # Fixed size controls
        layout.setStretchFactor(self.hint_frame, 0)   # Fixed size hints
        
    def create_control_panel(self):
        """
        CREATE CONTROL PANEL
        
        PURPOSE: Create button panel for code submission and status display
        
        COMPONENTS:
        - Submit Code button for validation
        - Status label for feedback messages
        - Professional styling matching game theme
        """
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setMaximumHeight(60)
        
        layout = QHBoxLayout(panel)
        layout.setSpacing(15)
        
        # Submit button
        self.submit_button = QPushButton("🚀 TEST CODE")
        self.submit_button.setMinimumHeight(40)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #0e7490;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0891b2;
            }
            QPushButton:pressed {
                background-color: #0c7489;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)
        
        # Status label
        self.status_label = QLabel("Ready to debug...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        
        # Layout buttons
        layout.addWidget(self.submit_button)
        layout.addWidget(self.status_label)
        layout.addStretch()  # Push elements to left
        
        return panel
        
    def create_hint_display(self):
        """
        CREATE HINT DISPLAY AREA
        
        PURPOSE: Create collapsible area for showing debugging hints
        
        FUNCTIONALITY:
        - Hidden by default, shown when hints are available
        - Styled to match game theme with hint-specific colors
        - Scrollable for longer hint messages
        """
        frame = QFrame()
        frame.setFrameStyle(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a0a;
                border: 2px solid #ffaa00;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        
        # Hint header
        hint_header = QLabel("💡 DEBUGGING HINT")
        hint_header.setAlignment(Qt.AlignCenter)
        hint_header.setStyleSheet("""
            QLabel {
                color: #ffaa00;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
                background-color: #3a3a0a;
                border-radius: 3px;
            }
        """)
        layout.addWidget(hint_header)
        
        # Hint content area
        self.hint_label = QLabel("")
        self.hint_label.setWordWrap(True)
        self.hint_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 12px;
                padding: 10px;
                background-color: transparent;
            }
        """)
        
        # Scrollable hint area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.hint_label)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(100)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        layout.addWidget(scroll_area)
        
        return frame
        
    def init_editor_settings(self):
        """
        INITIALIZE EDITOR SETTINGS
        
        PURPOSE: Configure editor appearance and behavior
        
        SETTINGS:
        - Apply syntax highlighter
        - Set up real-time error detection
        - Configure editor appearance and theme
        - Enable proper cursor behavior and text selection
        - COMPLETELY DISABLE any automatic text selection
        """
        # Apply Python syntax highlighting
        self.highlighter = PythonHighlighter(self.text_editor.document())
        
        # Configure editor appearance
        self.text_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #444;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                line-height: 1.4;
                selection-background-color: #264f78;
                selection-color: #ffffff;
            }
            QTextEdit:focus {
                border-color: #00ff00;
            }
        """)
        
        # Configure text editor behavior
        self.text_editor.setLineWrapMode(QTextEdit.WidgetWidth)
        self.text_editor.setTabStopWidth(40)  # 4-space tabs
        
        # Enable normal text interaction
        self.text_editor.setTextInteractionFlags(Qt.TextEditorInteraction)
        
        # COMPLETELY DISABLE syntax checking to prevent cursor interference
        # We'll only check syntax when user submits code
        self.syntax_timer = QTimer()
        self.syntax_timer.setSingleShot(True)
        self.syntax_timer.timeout.connect(self.check_syntax)
        
        # DON'T connect textChanged to avoid cursor interference
        # self.text_editor.textChanged.connect(self.on_text_changed)
        
    def on_text_changed(self):
        """
        HANDLE TEXT CHANGE EVENT - DISABLED
        
        PURPOSE: This method is disabled to prevent cursor interference
        We only check syntax on code submission now
        """
        pass  # Disabled to prevent cursor jumping
        
    def check_syntax(self):
        """
        CHECK PYTHON SYNTAX
        
        PURPOSE: Perform syntax validation of code ONLY when requested
        
        FUNCTIONALITY:
        - Parse code using Python AST
        - Update status display with error information
        - Emit signals for game controller integration
        - NO automatic highlighting to prevent cursor issues
        """
        code = self.text_editor.toPlainText().strip()
        
        if not code:
            self.update_status("Ready to debug...", "normal")
            return
            
        try:
            # Attempt to parse the code
            ast.parse(code)
            self.update_status("✓ Syntax OK", "success")
            
        except SyntaxError as e:
            # Handle syntax error
            error_line = e.lineno if e.lineno else 1
            error_msg = str(e.msg) if e.msg else "Syntax error"
            
            self.update_status(f"✗ Syntax Error: {error_msg}", "error")
            self.syntax_error_found.emit(error_msg, error_line)
            
        except Exception as e:
            # Handle other parsing errors
            self.update_status(f"✗ Parse Error: {str(e)}", "error")
            
    def highlight_error_line(self, line_number):
        """
        HIGHLIGHT ERROR LINE - DISABLED
        
        PURPOSE: This method is disabled to prevent cursor jumping
        """
        pass  # Disabled to prevent cursor issues
        
    def clear_error_highlighting(self):
        """
        CLEAR ERROR HIGHLIGHTING - DISABLED
        
        PURPOSE: This method is disabled to prevent cursor jumping
        """
        pass  # Disabled to prevent cursor issues
        
    def update_status(self, message, status_type="normal"):
        """
        UPDATE STATUS DISPLAY
        
        PURPOSE: Update status label with current editor state
        
        INPUTS:
        - message: Status message to display
        - status_type: Type of status ("normal", "success", "error")
        
        FUNCTIONALITY:
        - Update status text and colors based on type
        - Provide visual feedback for different states
        - Maintain consistent styling with game theme
        """
        color_map = {
            "normal": "#00ff00",   # Green
            "success": "#00ff00",  # Green  
            "error": "#ff0000",    # Red
            "warning": "#ffaa00"   # Orange/Amber
        }
        
        color = color_map.get(status_type, "#00ff00")
        
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }}
        """)
        
    def submit_code(self):
        """
        SUBMIT CODE FOR VALIDATION
        
        PURPOSE: Submit current code to game controller for validation
        
        FUNCTIONALITY:
        - Get current code from editor
        - Validate code is not empty
        - Check syntax before submission
        - Emit signal with code content
        - Update UI state during submission
        """
        code = self.text_editor.toPlainText().strip()
        
        if not code:
            self.update_status("✗ No code to submit!", "error")
            return
            
        # Check syntax before submission
        self.check_syntax()
            
        # Disable submit button temporarily
        self.submit_button.setEnabled(False)
        self.submit_button.setText("⏳ TESTING...")
        
        # Update status
        self.update_status("Testing your solution...", "normal")
        
        # Emit code for validation
        self.code_submitted.emit(code)
        
        # Re-enable button after delay
        QTimer.singleShot(1000, self.reset_submit_button)
        
    def reset_submit_button(self):
        """
        RESET SUBMIT BUTTON STATE
        
        PURPOSE: Reset submit button to normal state after submission
        
        FUNCTIONALITY:
        - Re-enable submit button
        - Restore original button text
        - Prepare for next submission
        """
        self.submit_button.setEnabled(True)
        self.submit_button.setText("🚀 TEST CODE")
        
    def set_code(self, code):
        """
        SET EDITOR CODE CONTENT
        
        PURPOSE: Load new code into editor (for level initialization)
        
        INPUTS:
        - code: Python code string to display
        
        FUNCTIONALITY:
        - Clear current code and load new content
        - Position cursor at start WITHOUT selecting text
        - Reset editor state for new problem
        - PREVENT any automatic text selection
        """
        # Temporarily disconnect any signals to prevent interference
        self.text_editor.blockSignals(True)
        
        # Clear and set the code
        self.text_editor.clear()
        self.text_editor.setPlainText(code)
        
        # Position cursor at start without selecting anything
        cursor = self.text_editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        cursor.clearSelection()  # CRITICAL: Clear any selection
        self.text_editor.setTextCursor(cursor)
        
        # Re-enable signals
        self.text_editor.blockSignals(False)
        
        # Clear UI state
        self.clear_hint()
        self.update_status("Ready to debug...", "normal")
        
        # Give focus to editor but prevent selection
        QTimer.singleShot(50, self.ensure_no_selection)
        
    def ensure_no_selection(self):
        """
        ENSURE NO TEXT SELECTION
        
        PURPOSE: Make absolutely sure no text is selected after setting code
        """
        cursor = self.text_editor.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.Start)
        self.text_editor.setTextCursor(cursor)
        self.text_editor.setFocus()
        
    def get_code(self):
        """
        GET CURRENT CODE CONTENT
        
        PURPOSE: Retrieve current code from editor
        
        RETURNS:
        - String containing current editor code content
        """
        return self.text_editor.toPlainText()
        
    def show_hint(self, hint_text):
        """
        SHOW DEBUGGING HINT
        
        PURPOSE: Display hint to help user debug the code
        
        INPUTS:
        - hint_text: Hint message to display
        
        FUNCTIONALITY:
        - Show hint display area
        - Update hint content with formatted message
        - Apply hint-specific styling and animations
        """
        self.current_hint = hint_text
        self.hint_label.setText(hint_text)
        self.hint_frame.show()
        
        # Optional: Add flash effect to draw attention
        self.hint_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a0a;
                border: 2px solid #ffff00;
                border-radius: 5px;
            }
        """)
        
        # Reset border color after flash
        QTimer.singleShot(2000, self.reset_hint_styling)
        
    def reset_hint_styling(self):
        """
        RESET HINT STYLING
        
        PURPOSE: Reset hint display to normal styling after flash effect
        """
        self.hint_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a0a;
                border: 2px solid #ffaa00;
                border-radius: 5px;
            }
        """)
        
    def clear_hint(self):
        """
        CLEAR HINT DISPLAY
        
        PURPOSE: Hide hint display area
        
        FUNCTIONALITY:
        - Hide hint frame
        - Clear hint content
        - Reset hint state for next level
        """
        self.hint_frame.hide()
        self.current_hint = None
        self.hint_label.setText("")