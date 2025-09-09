"""
BOMB WIDGET - Bomb Visualization and Animation Component  
=========================================================

PURPOSE: Custom widget for bomb display, timer, and wire-cutting animations
AUTHOR: Bomb Defuser Game
VERSION: 1.0

DESCRIPTION:
Handles all bomb visualization including:
- Bomb graphic rendering with QPainter
- 4-wire system with cutting animations
- Countdown timer with visual urgency indicators
- Progress tracking and defusing effects

DEPENDENCIES:
- PyQt5.QtWidgets: Widget base classes
- PyQt5.QtCore: Timer and animation systems
- PyQt5.QtGui: Graphics rendering and effects
"""

import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QLinearGradient


class BombWidget(QWidget):
    """
    BOMB VISUALIZATION WIDGET
    
    PURPOSE: Render bomb graphics, manage timer countdown, and handle wire animations
    
    FUNCTIONALITY:
    - Custom QPainter graphics for bomb and wires
    - Animated countdown timer with color transitions  
    - Wire cutting animations when errors are fixed
    - Progress indication through visual feedback
    - Win/lose state animations
    
    SIGNALS:
    - timer_expired: Emitted when countdown reaches zero
    - bomb_defused: Emitted when all wires are cut
    """
    
    # Qt signals for game events
    timer_expired = pyqtSignal()
    bomb_defused = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_bomb_state()
        self.init_ui()
        self.init_timer()
        
    def init_bomb_state(self):
        """
        INITIALIZE BOMB STATE VARIABLES
        
        PURPOSE: Set up all bomb-related state tracking variables
        
        STATE VARIABLES:
        - Wire states (intact/cut) for 4 colored wires
        - Timer values and countdown state
        - Animation states and visual effects
        - Progress tracking for defusing sequence
        """
        # Wire system state (4 wires: Red, Blue, Green, Yellow)
        self.wires = {
            'red': {'cut': False, 'color': QColor(255, 50, 50), 'sparks': False},
            'blue': {'cut': False, 'color': QColor(50, 150, 255), 'sparks': False},
            'green': {'cut': False, 'color': QColor(50, 255, 50), 'sparks': False},
            'yellow': {'cut': False, 'color': QColor(255, 255, 50), 'sparks': False}
        }
        
        # Timer state
        self.time_remaining = 30  # Default 30 seconds
        self.total_time = 30
        self.timer_running = False
        self.timer_expired_flag = False
        
        # Visual state
        self.bomb_exploded = False
        self.bomb_defused_flag = False
        self.flash_effect = False
        
        # Animation state
        self.spark_animations = []
        self.defuse_progress = 0.0  # 0.0 to 1.0
        
    def init_ui(self):
        """
        INITIALIZE USER INTERFACE COMPONENTS
        
        PURPOSE: Set up widget layout and timer display
        
        COMPONENTS:
        - Main bomb visualization area (custom painting)
        - Digital timer display with styling
        - Layout management for proper sizing
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Digital timer display
        self.timer_display = QLabel("00:30")
        self.timer_display.setAlignment(Qt.AlignCenter)
        self.timer_display.setStyleSheet("""
            QLabel {
                background-color: #000000;
                color: #00ff00;
                font-family: 'Courier New';
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                border: 3px solid #00ff00;
                border-radius: 8px;
                min-height: 50px;
            }
        """)
        layout.addWidget(self.timer_display)
        
        # Bomb visualization area (filled by paintEvent)
        layout.addStretch()
        
        # Set minimum size for proper bomb rendering
        self.setMinimumSize(400, 500)
        
    def init_timer(self):
        """
        INITIALIZE COUNTDOWN TIMER SYSTEM
        
        PURPOSE: Set up QTimer for countdown and animation updates
        
        TIMER CONFIGURATION:
        - Main countdown timer: 1 second intervals
        - Animation timer: 50ms intervals for smooth effects
        - Connected to update functions for visual feedback
        """
        # Main countdown timer (1 second intervals)
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        
        # Animation update timer (smooth effects at ~20 FPS)
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animations)
        self.animation_timer.start(50)  # 50ms = 20 FPS
        
    def start_timer(self, seconds):
        """
        START COUNTDOWN TIMER
        
        PURPOSE: Begin countdown with specified duration
        
        INPUTS:
        - seconds: Total countdown time in seconds
        
        FUNCTIONALITY:
        - Reset timer state and display
        - Configure timer duration and visual indicators
        - Start countdown with periodic updates
        """
        self.time_remaining = seconds
        self.total_time = seconds
        self.timer_running = True
        self.timer_expired_flag = False
        
        # Update timer display and start countdown
        self.update_timer_display()
        self.countdown_timer.start(1000)  # 1 second intervals
        
    def stop_timer(self):
        """
        STOP COUNTDOWN TIMER
        
        PURPOSE: Halt countdown and reset timer state
        
        FUNCTIONALITY:
        - Stop countdown timer
        - Preserve current time for display
        - Set timer state to stopped
        """
        self.countdown_timer.stop()
        self.timer_running = False
        
    def update_countdown(self):
        """
        UPDATE COUNTDOWN TIMER
        
        PURPOSE: Handle timer tick, update display, and check for expiration
        
        FUNCTIONALITY:
        - Decrement time remaining
        - Update visual timer display with urgency colors
        - Emit timer_expired signal when countdown reaches zero
        - Handle automatic game over on timeout
        """
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.update_timer_display()
            
            # Check if this triggers hint display (80% time elapsed)
            time_elapsed_percent = 1 - (self.time_remaining / self.total_time)
            if time_elapsed_percent >= 0.8:
                # Timer color changes to indicate hint availability
                self.flash_effect = True
                
        else:
            # Timer expired - bomb explodes
            self.countdown_timer.stop()
            self.timer_running = False
            self.timer_expired_flag = True
            self.bomb_exploded = True
            self.timer_expired.emit()
            
    def update_timer_display(self):
        """
        UPDATE TIMER VISUAL DISPLAY
        
        PURPOSE: Update timer text and colors based on remaining time
        
        VISUAL FEEDBACK:
        - Green: > 50% time remaining
        - Yellow: 20-50% time remaining  
        - Red: < 20% time remaining
        - Flash effect when hints become available
        """
        # Format time as MM:SS
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_text = f"{minutes:02d}:{seconds:02d}"
        
        # Calculate time percentage for color coding
        time_percent = self.time_remaining / self.total_time if self.total_time > 0 else 0
        
        # Determine timer color based on urgency
        if time_percent > 0.5:
            color = "#00ff00"  # Green - plenty of time
            border_color = "#00ff00"
        elif time_percent > 0.2:
            color = "#ffff00"  # Yellow - getting urgent  
            border_color = "#ffff00"
        else:
            color = "#ff0000"  # Red - critical time
            border_color = "#ff0000"
            
        # Apply flash effect for hint availability
        if self.flash_effect and (self.time_remaining % 2 == 0):
            color = "#ffffff"
            
        # Update timer display styling
        self.timer_display.setText(time_text)
        self.timer_display.setStyleSheet(f"""
            QLabel {{
                background-color: #000000;
                color: {color};
                font-family: 'Courier New';
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
                border: 3px solid {border_color};
                border-radius: 8px;
                min-height: 50px;
            }}
        """)
        
    def cut_wire(self, wire_name):
        """
        CUT WIRE ANIMATION
        
        PURPOSE: Trigger wire cutting animation when error is fixed
        
        INPUTS:
        - wire_name: Name of wire to cut ('red', 'blue', 'green', 'yellow')
        
        FUNCTIONALITY:
        - Mark wire as cut in state tracking
        - Trigger spark animation effects  
        - Update defusing progress
        - Check for complete bomb defusing
        """
        if wire_name in self.wires and not self.wires[wire_name]['cut']:
            # Mark wire as cut
            self.wires[wire_name]['cut'] = True
            self.wires[wire_name]['sparks'] = True
            
            # Update defusing progress
            cut_wires = sum(1 for wire in self.wires.values() if wire['cut'])
            self.defuse_progress = cut_wires / len(self.wires)
            
            # Trigger visual effects
            self.flash_effect = True
            
            # Check if bomb is fully defused
            if self.defuse_progress >= 1.0:
                self.bomb_defused_flag = True
                self.stop_timer()
                self.bomb_defused.emit()
                
            # Schedule spark effect cleanup
            QTimer.singleShot(1000, lambda: self.clear_sparks(wire_name))
            
            # Force widget repaint
            self.update()
            
    def clear_sparks(self, wire_name):
        """
        CLEAR SPARK EFFECTS
        
        PURPOSE: Remove spark animation after wire cutting
        
        INPUTS:
        - wire_name: Wire to clear sparks from
        """
        if wire_name in self.wires:
            self.wires[wire_name]['sparks'] = False
            self.update()
            
    def reset_bomb(self):
        """
        RESET BOMB STATE
        
        PURPOSE: Reset all bomb state for new level
        
        FUNCTIONALITY:
        - Reset all wire states to intact
        - Clear all visual effects and animations
        - Reset progress and timer state
        - Prepare for new level start
        """
        # Reset wire states
        for wire in self.wires.values():
            wire['cut'] = False
            wire['sparks'] = False
            
        # Reset visual state
        self.bomb_exploded = False
        self.bomb_defused_flag = False
        self.flash_effect = False
        self.defuse_progress = 0.0
        
        # Reset timer state
        self.timer_expired_flag = False
        self.stop_timer()
        
        # Force repaint
        self.update()
        
    def update_animations(self):
        """
        UPDATE ANIMATION EFFECTS
        
        PURPOSE: Handle periodic animation updates for visual effects
        
        FUNCTIONALITY:
        - Update spark effects and flash animations
        - Handle bomb explosion/defusing animations
        - Trigger widget repaints for smooth visuals
        """
        # Handle flash effects
        if self.flash_effect:
            self.update()
            
        # Handle spark effects
        if any(wire['sparks'] for wire in self.wires.values()):
            self.update()
            
    def paintEvent(self, event):
        """
        CUSTOM PAINT EVENT - Bomb Graphics Rendering
        
        PURPOSE: Render bomb graphics, wires, and visual effects
        
        RENDERING ORDER:
        1. Bomb body (main cylindrical shape)
        2. Four colored wires with cut states
        3. Visual effects (sparks, explosions, etc.)
        4. Progress indicators and status graphics
        
        GRAPHICS DETAILS:
        - Bomb: Dark cylinder with metallic appearance
        - Wires: Colored lines with cut/intact visualization
        - Effects: Sparks, flash, and animation overlays
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Get widget dimensions for scaling
        width = self.width()
        height = self.height() - 80  # Account for timer display
        center_x = width // 2
        center_y = height // 2 + 40  # Offset for timer
        
        # Draw bomb body
        self.draw_bomb_body(painter, center_x, center_y, width, height)
        
        # Draw wires
        self.draw_wires(painter, center_x, center_y, width, height)
        
        # Draw visual effects
        if self.bomb_exploded:
            self.draw_explosion(painter, center_x, center_y)
        elif self.bomb_defused_flag:
            self.draw_defused_effect(painter, center_x, center_y)
            
    def draw_bomb_body(self, painter, center_x, center_y, width, height):
        """
        DRAW BOMB MAIN BODY
        
        PURPOSE: Render the main bomb cylinder with metallic appearance
        
        INPUTS:
        - painter: QPainter instance for rendering
        - center_x, center_y: Bomb center coordinates
        - width, height: Available drawing dimensions
        """
        # Bomb dimensions
        bomb_width = min(width * 0.6, 200)
        bomb_height = min(height * 0.4, 120)
        
        # Bomb body rectangle
        bomb_rect = QRect(int(center_x - bomb_width/2), 
                         int(center_y - bomb_height/2),
                         int(bomb_width), int(bomb_height))
        
        # Create metallic gradient
        gradient = QLinearGradient(0, bomb_rect.top(), 0, bomb_rect.bottom())
        gradient.setColorAt(0.0, QColor(80, 80, 80))
        gradient.setColorAt(0.5, QColor(120, 120, 120))
        gradient.setColorAt(1.0, QColor(60, 60, 60))
        
        # Draw bomb body
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(40, 40, 40), 3))
        painter.drawRoundedRect(bomb_rect, 10, 10)
        
        # Draw bomb details (rivets, warning labels)
        self.draw_bomb_details(painter, bomb_rect)
        
    def draw_bomb_details(self, painter, bomb_rect):
        """
        DRAW BOMB DETAIL ELEMENTS
        
        PURPOSE: Add rivets, warning symbols, and detail graphics
        
        INPUTS:
        - painter: QPainter instance
        - bomb_rect: Main bomb body rectangle
        """
        # Draw rivets around bomb body
        rivet_color = QColor(100, 100, 100)
        painter.setBrush(QBrush(rivet_color))
        painter.setPen(QPen(QColor(80, 80, 80), 1))
        
        # Top rivets
        for i in range(4):
            x = bomb_rect.left() + 20 + i * (bomb_rect.width() - 40) // 3
            y = bomb_rect.top() + 10
            painter.drawEllipse(x-3, y-3, 6, 6)
            
        # Bottom rivets
        for i in range(4):
            x = bomb_rect.left() + 20 + i * (bomb_rect.width() - 40) // 3
            y = bomb_rect.bottom() - 10
            painter.drawEllipse(x-3, y-3, 6, 6)
            
        # Warning symbol in center
        painter.setPen(QPen(QColor(255, 255, 0), 2))
        painter.setBrush(QBrush())
        
        # Draw triangle warning symbol
        triangle_size = 20
        center = bomb_rect.center()
        points = [
            (center.x(), center.y() - triangle_size//2),
            (center.x() - triangle_size//2, center.y() + triangle_size//2),
            (center.x() + triangle_size//2, center.y() + triangle_size//2)
        ]
        
        from PyQt5.QtGui import QPolygon
        from PyQt5.QtCore import QPoint
        triangle = QPolygon([QPoint(x, y) for x, y in points])
        painter.drawPolygon(triangle)
        
        # Draw exclamation mark inside triangle
        painter.setPen(QPen(QColor(255, 255, 0), 3))
        painter.drawLine(center.x(), center.y() - 8, center.x(), center.y() + 2)
        painter.drawPoint(center.x(), center.y() + 6)
        
    def draw_wires(self, painter, center_x, center_y, width, height):
        """
        DRAW BOMB WIRES WITH CUT STATES
        
        PURPOSE: Render four colored wires showing cut/intact status
        
        INPUTS:
        - painter: QPainter instance
        - center_x, center_y: Bomb center coordinates  
        - width, height: Available dimensions
        
        WIRE LAYOUT:
        - Red wire: Top-left
        - Blue wire: Top-right
        - Green wire: Bottom-left
        - Yellow wire: Bottom-right
        """
        wire_names = ['red', 'blue', 'green', 'yellow']
        wire_positions = [
            (-60, -40),  # Red: top-left
            (60, -40),   # Blue: top-right  
            (-60, 40),   # Green: bottom-left
            (60, 40)     # Yellow: bottom-right
        ]
        
        for i, wire_name in enumerate(wire_names):
            wire_data = self.wires[wire_name]
            start_x = center_x + wire_positions[i][0]
            start_y = center_y + wire_positions[i][1]
            
            # Draw wire extending from bomb
            end_x = start_x + (120 if wire_positions[i][0] > 0 else -120)
            end_y = start_y
            
            if wire_data['cut']:
                # Draw cut wire with gap
                self.draw_cut_wire(painter, start_x, start_y, end_x, end_y, wire_data)
            else:
                # Draw intact wire
                self.draw_intact_wire(painter, start_x, start_y, end_x, end_y, wire_data)
                
            # Draw sparks if cutting animation active
            if wire_data['sparks']:
                self.draw_sparks(painter, (start_x + end_x) // 2, (start_y + end_y) // 2)
                
    def draw_intact_wire(self, painter, start_x, start_y, end_x, end_y, wire_data):
        """
        DRAW INTACT WIRE
        
        PURPOSE: Render uncut wire with full connection
        
        INPUTS:
        - painter: QPainter instance
        - start_x, start_y: Wire start coordinates
        - end_x, end_y: Wire end coordinates  
        - wire_data: Wire state and color information
        """
        # Set wire color and thickness
        painter.setPen(QPen(wire_data['color'], 6))
        painter.drawLine(start_x, start_y, end_x, end_y)
        
        # Draw wire connectors at ends
        painter.setBrush(QBrush(wire_data['color'].darker(150)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        
        # Start connector
        painter.drawEllipse(start_x-4, start_y-4, 8, 8)
        
        # End connector
        painter.drawEllipse(end_x-4, end_y-4, 8, 8)
        
    def draw_cut_wire(self, painter, start_x, start_y, end_x, end_y, wire_data):
        """
        DRAW CUT WIRE WITH GAP
        
        PURPOSE: Render wire that has been cut, showing disconnection
        
        INPUTS:
        - painter: QPainter instance
        - start_x, start_y: Wire start coordinates
        - end_x, end_y: Wire end coordinates
        - wire_data: Wire state and color information
        """
        # Calculate cut position (middle of wire)
        cut_x = (start_x + end_x) // 2
        cut_y = (start_y + end_y) // 2
        gap_size = 20
        
        # Draw first half (from start to cut)
        painter.setPen(QPen(wire_data['color'], 6))
        painter.drawLine(start_x, start_y, cut_x - gap_size//2, cut_y)
        
        # Draw second half (from cut to end)
        painter.drawLine(cut_x + gap_size//2, cut_y, end_x, end_y)
        
        # Draw frayed wire ends
        painter.setPen(QPen(wire_data['color'].darker(200), 2))
        for i in range(3):
            # Left frayed end
            painter.drawLine(cut_x - gap_size//2 - i*2, cut_y - i, 
                           cut_x - gap_size//2 + i, cut_y + i)
            # Right frayed end  
            painter.drawLine(cut_x + gap_size//2 + i*2, cut_y - i,
                           cut_x + gap_size//2 - i, cut_y + i)
                           
        # Draw connectors
        painter.setBrush(QBrush(wire_data['color'].darker(150)))
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.drawEllipse(start_x-4, start_y-4, 8, 8)
        painter.drawEllipse(end_x-4, end_y-4, 8, 8)
        
    def draw_sparks(self, painter, x, y):
        """
        DRAW SPARK EFFECTS
        
        PURPOSE: Render animated sparks at wire cutting location
        
        INPUTS:
        - painter: QPainter instance
        - x, y: Spark center coordinates
        """
        import random
        
        # Draw multiple spark particles
        spark_color = QColor(255, 255, 200)
        painter.setPen(QPen(spark_color, 2))
        
        for i in range(8):
            # Random spark directions
            angle = i * 45 + random.randint(-15, 15)
            length = random.randint(10, 25)
            
            end_x = x + length * math.cos(math.radians(angle))
            end_y = y + length * math.sin(math.radians(angle))
            
            painter.drawLine(x, y, int(end_x), int(end_y))
            
        # Draw bright center flash
        painter.setBrush(QBrush(QColor(255, 255, 255, 150)))
        painter.setPen(QPen())
        painter.drawEllipse(x-5, y-5, 10, 10)
        
    def draw_explosion(self, painter, center_x, center_y):
        """
        DRAW EXPLOSION EFFECT
        
        PURPOSE: Render bomb explosion graphics when timer expires
        
        INPUTS:
        - painter: QPainter instance
        - center_x, center_y: Explosion center coordinates
        """
        # Draw explosion burst
        explosion_color = QColor(255, 100, 0, 200)
        painter.setBrush(QBrush(explosion_color))
        painter.setPen(QPen())
        
        # Multiple explosion circles for depth
        for i in range(5):
            radius = 30 + i * 15
            alpha = 200 - i * 40
            color = QColor(255, 100 - i * 20, 0, alpha)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(center_x - radius, center_y - radius, 
                              radius * 2, radius * 2)
                              
        # Draw explosion text
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.drawText(center_x - 50, center_y + 80, "BOOM!")
        
    def draw_defused_effect(self, painter, center_x, center_y):
        """
        DRAW BOMB DEFUSED EFFECT
        
        PURPOSE: Render success animation when bomb is fully defused
        
        INPUTS:
        - painter: QPainter instance  
        - center_x, center_y: Effect center coordinates
        """
        # Draw success glow
        success_color = QColor(0, 255, 0, 100)
        painter.setBrush(QBrush(success_color))
        painter.setPen(QPen())
        
        # Pulsing glow effect
        for i in range(3):
            radius = 40 + i * 20
            alpha = 100 - i * 30
            color = QColor(0, 255, 0, alpha)
            painter.setBrush(QBrush(color))
            painter.drawEllipse(center_x - radius, center_y - radius,
                              radius * 2, radius * 2)
                              
        # Draw checkmark
        painter.setPen(QPen(QColor(0, 255, 0), 8))
        # Checkmark lines
        painter.drawLine(center_x - 20, center_y, center_x - 5, center_y + 15)
        painter.drawLine(center_x - 5, center_y + 15, center_x + 20, center_y - 10)
        
        # Draw success text
        painter.setPen(QPen(QColor(0, 255, 0), 3))
        painter.setFont(QFont("Arial", 20, QFont.Bold))
        painter.drawText(center_x - 65, center_y + 80, "DEFUSED!")
                