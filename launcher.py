import sys
import os
# import subprocess # REMOVED
# import argparse   # REMOVED
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QCheckBox, QPushButton, QSizePolicy, QSpacerItem, QSlider, QFrame
)
from PySide6.QtCore import Qt, QSize, Signal, Slot
from PySide6.QtGui import QScreen, QPixmap, QPainter, QColor, QPalette

# IMPORTANT: Import the function and potentially the main window class
# Assuming launcher.py is in the same directory as rivals_dashboard.py
try:
    # Use the resource_path function defined in the dashboard module
    # This ensures consistency, especially for packaged apps.
    from rivals_dashboard import (
        run_dashboard, MainWindow, resource_path,
        # Import constants needed for styling
        FONT_FAMILY_NAME, H1_COLOR, H2_COLOR, H3_COLOR
    )
except ImportError as e:
    print(f"Error importing from rivals_dashboard: {e}")
    print("Make sure launcher.py is in the same directory as rivals_dashboard.py")
    sys.exit(1)

# Define path for background image
LAUNCHER_BG_IMAGE = resource_path('images/marvel-rivals-bg-580x334.jpg')

class LauncherDialog(QDialog):
    def __init__(self, screens, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Marvel Rivals Dashboard - Launcher")
        self.setModal(True)
        # Make frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground, True) # Needed for custom shape/bg
        self._drag_pos = None # For dragging

        self.screens = screens
        self.selected_screen = None
        self.fullscreen_mode = False # Default to Windowed
        self.main_window_instance = None # To hold the dashboard window

        # Load background pixmap
        self.background_pixmap = QPixmap(LAUNCHER_BG_IMAGE)
        if self.background_pixmap.isNull():
            print(f"Warning: Could not load launcher background image at {LAUNCHER_BG_IMAGE}")

        self.init_ui()
        # Remove the old stylesheet application
        # self.setStyleSheet(DARK_STYLESHEET)

        # Set initial size based on background aspect ratio if desired, or fixed
        if not self.background_pixmap.isNull():
            # Optional: Base size on background aspect ratio
            # base_width = 580
            # self.setFixedSize(base_width, int(base_width * (self.background_pixmap.height() / self.background_pixmap.width())))
            self.setFixedSize(580, 334) # Fixed size based on image name
        else:
            self.setMinimumWidth(400)
            self.setFixedSize(self.sizeHint()) # Fallback fixed size

        # Apply Stylesheet AFTER widgets are created in init_ui
        self._apply_styles()

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background_pixmap.isNull():
            # Scale pixmap to fit the dialog size, keeping aspect ratio
            scaled_pixmap = self.background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            # Center the pixmap (optional, if scaling resulted in letter/pillarboxing)
            x = (self.width() - scaled_pixmap.width()) / 2
            y = (self.height() - scaled_pixmap.height()) / 2
            painter.drawPixmap(int(x), int(y), scaled_pixmap)
        else:
            # Fallback background color if image fails
            painter.fillRect(self.rect(), QColor("#282828"))
        # Important: Call superclass paintEvent if needed, though maybe not for a dialog background
        # super().paintEvent(event)
        # Let QPainter handle painting child widgets automatically on top

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Top Row: Title and Exit Button ---
        top_row_layout = QHBoxLayout()
        title_label = QLabel("LAUNCH OPTIONS") # Changed Title
        title_label.setObjectName("LauncherTitle")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.exit_button_launcher = QPushButton("X")
        self.exit_button_launcher.setObjectName("LauncherExitButton")
        self.exit_button_launcher.setToolTip("Close Launcher")
        self.exit_button_launcher.clicked.connect(self.reject) # Reject closes launcher

        top_row_layout.addWidget(title_label, 1) # Title takes stretch
        top_row_layout.addWidget(self.exit_button_launcher, 0)
        main_layout.addLayout(top_row_layout)

        # --- Monitor Selection --- 
        monitor_layout = QHBoxLayout()
        monitor_label = QLabel("Monitor:")
        monitor_label.setObjectName("LauncherLabel")
        self.monitor_combo = QComboBox()
        self.monitor_combo.setObjectName("LauncherComboBox")
        self.monitor_combo.setMinimumWidth(250) # Ensure enough space
        for i, screen in enumerate(self.screens):
            screen_name = screen.name()
            geo = screen.geometry()
            size_str = f"{geo.width()}x{geo.height()}"
            primary_str = " (Primary)" if screen == QApplication.primaryScreen() else ""
            display_text = f"Display {i+1}{primary_str}: [{size_str}]"
            # Define the tooltip text here
            tooltip_text = f"Screen {i+1}{primary_str}: {screen_name} [{size_str}]"
            self.monitor_combo.addItem(display_text, userData=screen) # Store QScreen object
            self.monitor_combo.setItemData(i, tooltip_text, Qt.ToolTipRole) # Add tooltip to item

        primary_screen_index = self.screens.index(QApplication.primaryScreen()) if QApplication.primaryScreen() in self.screens else 0
        self.monitor_combo.setCurrentIndex(primary_screen_index)

        monitor_layout.addWidget(monitor_label)
        monitor_layout.addWidget(self.monitor_combo, 1)
        main_layout.addLayout(monitor_layout)

        # --- Mode Selection --- 
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Display Mode:")
        mode_label.setObjectName("LauncherLabel")
        self.mode_combo = QComboBox()
        self.mode_combo.setObjectName("LauncherComboBox")
        self.mode_combo.addItem("Windowed", userData=False)
        self.mode_combo.addItem("Fullscreen", userData=True)
        self.mode_combo.setCurrentIndex(0) # Default to Windowed

        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo, 1)
        main_layout.addLayout(mode_layout)

        main_layout.addStretch(1) # Pushes controls down

        # --- Buttons --- 
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("LauncherButton")
        self.cancel_button.clicked.connect(self.reject)
        self.launch_button = QPushButton("Launch Dashboard")
        self.launch_button.setObjectName("LauncherButton")
        self.launch_button.setDefault(True)
        self.launch_button.clicked.connect(self.accept)

        button_layout.addStretch(1)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.launch_button)
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)

    # --- Window Dragging Methods ---
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Allow dragging by clicking anywhere on the dialog background
            # (Could refine to only drag by a specific title bar area if needed)
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    def _apply_styles(self):
        # Use imported theme colors and font
        font_family = FONT_FAMILY_NAME # Use imported font
        h1_color = H1_COLOR # Yellowish
        h2_color = H2_COLOR # Bluish
        h3_color = H3_COLOR # Reddish
        # Define some base colors derived from theme or common dark style
        bg_color = "rgba(40, 40, 40, 0.8)" # Semi-transparent dark gray
        text_color = "#FFFFFF" # White
        border_color = h2_color # Use blue for borders
        handle_color = h1_color # Use yellow for slider handle
        sub_page_color = handle_color # Yellow before handle
        add_page_color = h2_color # Blue after handle
        button_bg = "#555555"
        button_hover_bg = "#656565"
        button_pressed_bg = "#454545"
        red_exit_bg = "rgba(200, 30, 30, 0.8)"
        red_exit_hover_bg = "rgba(220, 40, 40, 0.9)"
        red_exit_pressed_bg = "rgba(180, 20, 20, 0.9)"
        red_exit_border = "#FF6060"

        style = f"""
        LauncherDialog {{
            font-family: '{font_family}';
            background-color: transparent; /* Let paintEvent handle bg */
        }}
        QFrame#LauncherFrame {{ /* Optional frame for better background separation */
             background-color: {bg_color};
             border-radius: 8px;
        }}
        #LauncherTitle {{
            color: {h1_color}; /* Yellow title */
            font-size: 24px;
            font-weight: bold;
            padding: 5px;
            margin-bottom: 15px;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 5px;
        }}
        #LauncherLabel {{
            color: {text_color};
            font-weight: bold;
            font-size: 16px;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 3px;
            padding: 4px 8px;
            margin-bottom: 3px;
        }}
        #LauncherValueLabel {{
            color: {text_color};
            font-size: 16px;
            font-weight: bold;
            background-color: rgba(0, 0, 0, 0.7);
            border: 1px solid {border_color};
            border-radius: 4px;
            padding: 5px;
            min-height: 20px; /* Ensure height */
            qproperty-alignment: 'AlignCenter';
        }}
        /* Remove Slider Styles */
        /* QSlider::groove:horizontal {{ ... }} */
        /* QSlider::handle:horizontal {{ ... }} */
        /* QSlider::add-page:horizontal {{ ... }} */
        /* QSlider::sub-page:horizontal {{ ... }} */
        /* QSlider::tick:horizontal {{ ... }} */

        /* Remove Checkbox Styles */
        /* #LauncherCheckbox {{ ... }} */
        /* #LauncherCheckbox::indicator {{ ... }} */
        /* #LauncherCheckbox::indicator:unchecked {{ ... }} */
        /* #LauncherCheckbox::indicator:checked {{ ... }} */

        /* Add/Adjust ComboBox Styles */
        #LauncherComboBox {{
            color: {text_color};
            background-color: {button_bg};
            border: 1px solid {border_color};
            border-radius: 4px;
            padding: 5px;
            min-height: 20px;
            font-size: 15px;
            font-weight: bold;
        }}
        #LauncherComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 20px;
            border-left-width: 1px;
            border-left-color: {border_color};
            border-left-style: solid;
            border-top-right-radius: 3px;
            border-bottom-right-radius: 3px;
            background-color: {button_bg};
        }}
        #LauncherComboBox::down-arrow {{
            /* You can use an image here, or keep it simple */
             border: 2px solid {handle_color}; /* Yellow arrow border */
             width: 8px;
             height: 8px;
             background: transparent;
             /* A simple triangle: */
             border-top-color: transparent;
             border-left-color: transparent;
             border-right-color: transparent;
        }}
        #LauncherComboBox::down-arrow:on {{ /* shift when dropdown is open */
            top: 1px; left: 1px;
        }}
        #LauncherComboBox QAbstractItemView {{
            color: {text_color};
            background-color: {button_pressed_bg}; /* Darker background for dropdown */
            border: 1px solid {border_color};
            selection-background-color: {h2_color}; /* Blue selection */
            padding: 4px;
            font-size: 14px;
        }}

        #LauncherButton {{
            background-color: {button_bg};
            color: {text_color};
            border: 1px solid {border_color};
            padding: 8px 18px;
            border-radius: 5px;
            min-height: 26px;
            font-size: 16px;
            font-weight: bold;
        }}
        #LauncherButton:hover {{
            background-color: {button_hover_bg};
            border: 1px solid {h1_color};
        }}
        #LauncherButton:pressed {{
            background-color: {button_pressed_bg};
        }}
        #LauncherButton:default {{
            border: 2px solid {h1_color}; /* Highlight default button with yellow */
        }}
        #LauncherExitButton {{
            background-color: {red_exit_bg};
            color: {text_color};
            font-size: 16px; /* Adjust size */
            font-weight: bold;
            border: 1px solid {red_exit_border};
            border-radius: 13px; /* Make round */
            min-width: 26px;
            max-width: 26px;
            min-height: 26px;
            max-height: 26px;
            padding: 0px;
            margin: 0px 4px; /* Add slight margin */
        }}
        #LauncherExitButton:hover {{ background-color: {red_exit_hover_bg}; }}
        #LauncherExitButton:pressed {{ background-color: {red_exit_pressed_bg}; }}
        """
        self.setStyleSheet(style)

    def accept(self):
        """Called when Launch is clicked."""
        monitor_index = self.monitor_combo.currentIndex()
        if 0 <= monitor_index < len(self.screens):
            self.selected_screen = self.screens[monitor_index]
        else:
            self.selected_screen = QApplication.primaryScreen() # Fallback
            print("Warning: Invalid monitor combo value, using primary screen.")

        self.fullscreen_mode = (self.mode_combo.currentData() == True)

        print(f"Launcher: Selected Screen: {self.selected_screen.name() if self.selected_screen else 'None'}")
        print(f"Launcher: Fullscreen Mode: {self.fullscreen_mode}")
        super().accept() # Close the dialog successfully

    def get_selection(self):
        """Returns the selected screen and fullscreen mode."""
        # Data is already processed in accept()
        return self.selected_screen, self.fullscreen_mode


if __name__ == "__main__":
    # Basic App setup needed for screen detection and dialog
    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    except AttributeError:
        pass # Ignore if not available
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)

    available_screens = QApplication.screens()
    if not available_screens:
        print("Error: No screens detected.")
        # Show a message box?
        sys.exit(1)

    launcher = LauncherDialog(available_screens)

    # --- Center Launcher on Primary Screen --- 
    primary_screen = QApplication.primaryScreen()
    if primary_screen:
        available_geo = primary_screen.availableGeometry()
        launcher_geo = launcher.frameGeometry()
        center_point = available_geo.center()
        launcher_geo.moveCenter(center_point)
        # Adjust if it goes off-screen (though centering on available should be safe)
        # Ensure top-left is within available bounds
        final_x = max(available_geo.left(), launcher_geo.left())
        final_y = max(available_geo.top(), launcher_geo.top())
        # Ensure bottom-right is within available bounds
        if final_x + launcher_geo.width() > available_geo.right():
            final_x = available_geo.right() - launcher_geo.width()
        if final_y + launcher_geo.height() > available_geo.bottom():
            final_y = available_geo.bottom() - launcher_geo.height()
        launcher.move(final_x, final_y)
    else:
        print("Warning: Could not get primary screen to center launcher.")

    result = launcher.exec() # Show the dialog modally

    if result == QDialog.Accepted:
        print("Launcher accepted, proceeding to dashboard...")
        selected_screen, fullscreen = launcher.get_selection()

        # --- Run dashboard directly in the same process ---
        try:
            main_window = run_dashboard(selected_screen, fullscreen)
            # Launcher dialog closes automatically via accept(), so just start main event loop
            sys.exit(app.exec()) # Start main app loop

        except RuntimeError as e:
            print(f"Dashboard failed to start: {e}")
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Launch Error", f"Dashboard failed to start:\n{e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred launching the dashboard: {e}")
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.critical(None, "Launch Error", f"Could not start the dashboard:\n{e}")
            sys.exit(1)

    else:
        print("Launcher cancelled by user.")
        sys.exit(0) # Clean exit