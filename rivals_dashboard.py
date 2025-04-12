# --- START OF FILE rivals_dashboard.py ---

import sys
import json
import os
import re # Import regular expressions for parsing
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QScrollArea, QGroupBox, QTextEdit, QSizePolicy, QApplication,
    QPushButton, QLineEdit, QComboBox, QSpacerItem, QDialog, QFrame, QMessageBox
)
from PySide6.QtGui import (
    QPixmap, QPalette, QColor, QFont, QFontDatabase, QWheelEvent, QKeyEvent,
    QScreen, QTextOption, QIcon, QTextDocument, QMouseEvent
)
from PySide6.QtCore import Qt, QRect, QSize, Signal, Slot, QPoint, QStandardPaths, QTimer

# --- Helper Function for Resource Paths (Unchanged) ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        print(f"DEBUG resource_path: Running bundled (MEIPASS), base_path = {base_path}") # DEBUG
    except Exception:
        # Not bundled, use the directory of the current file
        base_path = os.path.abspath(os.path.dirname(__file__))
        print(f"DEBUG resource_path: Running as script (__file__), base_path = {base_path}") # DEBUG

    calculated_path = os.path.join(base_path, relative_path)
    print(f"DEBUG resource_path: Trying path: {calculated_path}") # DEBUG
    return calculated_path

# --- Configuration (Unchanged paths) ---
CHARACTER_DATA_FOLDER = resource_path('characters')
app_data_path = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
if not app_data_path: app_data_path = QStandardPaths.writableLocation(QStandardPaths.GenericDataLocation)
if app_data_path and not os.path.exists(app_data_path):
    try: os.makedirs(app_data_path); print(f"Created app data directory: {app_data_path}")
    except OSError as e: print(f"Warning: Could not create app data directory {app_data_path}: {e}"); app_data_path = resource_path('.')
if app_data_path: FAVORITES_FILE = os.path.join(app_data_path, 'rivals_dashboard_favorites.json'); print(f"Using favorites path: {FAVORITES_FILE}")
else: FAVORITES_FILE = resource_path('rivals_dashboard_favorites.json'); print(f"Warning: Could not get standard app data path. Using fallback: {FAVORITES_FILE}")
IMAGE_FOLDER = resource_path('images')
INFO_FOLDER = resource_path('info')
FONT_REGULAR = resource_path('BackIssuesBB_reg.otf')
FONT_ITALIC = resource_path('BackIssuesBB_ital.otf')
FONT_BOLDITALIC = resource_path('BackIssuesBB_boldital.otf')
FONT_FAMILY_NAME = "Back Issues BB"
DEFAULT_THEME_COLOR = "#888888"; DEFAULT_SECONDARY_THEME_COLOR = "#CCCCCC"
BASE_FONT_SIZE = 14; HEADER_FONT_SIZE = BASE_FONT_SIZE + 2; GROUP_TITLE_FONT_SIZE = BASE_FONT_SIZE + 3
CHARACTER_NAME_FONT_SIZE = 40; JUMP_BAR_ICON_SIZE = 60; JUMP_BAR_SPACING = 5
# --- STATIC JUMP BAR CONSTANTS ---
JUMP_BAR_FIXED_ICON_SIZE = 40 # New fixed size for icons
JUMP_BAR_FIXED_SPACING = 4
ABILITY_TITLE_STYLE_TEMPLATE = "font-size: 1.15em; text-decoration: underline; font-weight: bold; color: {color};"
DETAILS_COLOR = "#B8B8B8"; LORE_COLOR = "#C8C8C8"; PARTNER_STYLE_TEMPLATE = "font-weight: bold; color: {color};"
READING_LIST_TITLE_STYLE_TEMPLATE = "font-size: 1.1em; font-weight: bold; color: {color};"
SCROLL_PADDING_TOP = 20; MIN_SEARCH_LENGTH = 3
INFO_FILES = { "OVERVIEW": "overview.txt", "NEWS": "news.txt", "ANNOUNCEMENTS": "announcements.txt", "DEV DIARIES": "dev_diaries.txt", "GAME UPDATE": "game_update.txt", "BALANCE POST": "balance_post.txt", }
H1_COLOR = "#FBBF2C"; H2_COLOR = "#60A5FA"; H3_COLOR = "#F87171"
LIST_STYLE = "margin-left: 25px; margin-top: 5px; margin-bottom: 5px;"
INFO_POPUP_UNDERLINE_COLOR = "#FBBF2C"
BOLD_UNDERLINE_STYLE_TEMPLATE_POPUP = f"font-weight: bold; text-decoration: underline; color: {INFO_POPUP_UNDERLINE_COLOR};"
CHARACTER_IMAGE_MAP = { "Adam Warlock": "marvel-rivals-characters-adam-warlock--550x309.jpg", "Black Panther": "marvel-rivals-characters-black-panther--550x309.jpg", "Black Widow": "marvel-rivals-characters-black-widow--550x309.jpg", "Captain America": "marvel-rivals-characters-captain-america--550x309.jpg", "Cloak and Dagger": "marvel-rivals-characters-cloak-and-dagger--550x309.jpg", "Doctor Strange": "marvel-rivals-characters-doctor-strange--550x309.jpg", "Emma Frost": "marvel-rivals-characters-emma-frost.jpg", "Groot": "marvel-rivals-characters-groot--550x309.jpg", "Hawkeye": "marvel-rivals-characters-hawkeye--550x309.jpg", "Hela": "marvel-rivals-characters-hela--550x309.jpg", "Hulk": "marvel-rivals-characters-hulk-550x309.jpg", "Human Torch": "marvel-rivals-characters-human-torch--550x309.jpg", "Invisible Woman": "marvel-rivals-characters-invisible-woman-550x309.jpg", "Iron Fist": "marvel-rivals-characters-iron-fist--550x309.jpg", "Iron Man": "marvel-rivals-characters-iron-man--550x309.jpg", "Jeff the Land Shark": "marvel-rivals-characters-jeff--550x309.jpg", "Loki": "marvel-rivals-characters-loki--550x309.jpg", "Luna Snow": "marvel-rivals-characters-luna-snow--550x309.jpg", "Magik": "marvel-rivals-characters-magik--550x309.jpg", "Magneto": "marvel-rivals-characters-magneto--550x309.jpg", "Mantis": "marvel-rivals-characters-mantis--550x309.jpg", "Mister Fantastic": "marvel-rivals-characters-mr-fantastic-550x309.jpg", "Moon Knight": "marvel-rivals-characters-moon-knight--550x309.jpg", "Namor": "marvel-rivals-characters-namor--550x309.jpg", "Peni Parker": "marvel-rivals-characters-peni-parker--550x309.jpg", "Psylocke": "marvel-rivals-characters-psylocke--550x309.jpg", "Punisher": "marvel-rivals-characters-punisher--550x309.jpg", "Rocket Raccoon": "marvel-rivals-characters-rocket--550x309.jpg", "Scarlet Witch": "marvel-rivals-characters-scarlet-witch--550x309.jpg", "Spider-Man": "marvel-rivals-characters-spider-man--550x309.jpg", "Squirrel Girl": "marvel-rivals-characters-squirrel-girl--550x309.jpg", "Star-Lord": "marvel-rivals-characters-star-lord--550x309.jpg", "Storm": "marvel-rivals-characters-storm--550x309.jpg", "The Thing": "marvel-rivals-characters-the-thing--550x309.jpg", "Thor": "marvel-rivals-characters-thor--550x309.jpg", "Venom": "marvel-rivals-characters-venom--550x309.jpg", "Winter Soldier": "marvel-rivals-characters-winter-soldier--550x309.jpg", "Wolverine": "marvel-rivals-characters-wolverine--550x309.jpg" }
DARK_STYLESHEET = """ QMainWindow, QWidget { background-color: #282828; color: #E5E5E5; } QDialog#InfoPopupDialog { background-color: #333333; color: #E5E5E5; border: 2px solid #555555; border-radius: 8px; } QDialog#InfoPopupDialog QLabel#PopupTitleLabel { background-color: transparent; color: #E5E5E5; padding-top: 5px; padding-bottom: 5px; } QDialog#InfoPopupDialog ZoomableTextWidget { background-color: #2F2F2F; color: #E0E0E0; border: 1px solid #444444; border-radius: 4px; padding: 8px; } QDialog#InfoPopupDialog QPushButton#PopupCloseButton { background-color: rgba(200, 30, 30, 0.8); color: #FFFFFF; font-size: 18px; font-weight: bold; border: 1px solid #FF6060; border-radius: 13px; min-width: 26px; max-width: 26px; min-height: 26px; max-height: 26px; padding: 0px; margin: 4px; } QDialog#InfoPopupDialog QPushButton#PopupCloseButton:hover { background-color: rgba(220, 40, 40, 0.9); } QDialog#InfoPopupDialog QPushButton#PopupCloseButton:pressed { background-color: rgba(180, 20, 20, 0.9); } QScrollArea { border: none; background-color: #282828; } QScrollBar:vertical { border: 1px solid #444; background: #3a3a3a; width: 15px; margin: 15px 0 15px 0; border-radius: 2px; } QScrollBar::handle:vertical { background-color: #6a6a6a; min-height: 30px; border-radius: 7px; } QScrollBar::handle:vertical:hover { background-color: #7a7a7a; } QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { border: none; background: none; height: 15px; subcontrol-origin: margin; } QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background: none; } QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; } QGroupBox { color: #E5E5E5; border: 1px solid #555555; margin-top: 15px; padding: 10px 5px 5px 5px; border-radius: 5px; } QGroupBox#StaticInfoBox, QGroupBox#JumpBarGroupBox { padding-top: 25px; } QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; left: 10px; padding: 0 5px 0 5px; color: #CCCCCC; } QLabel { color: #E5E5E5; background-color: transparent; border: none; padding: 2px; } #CharacterNameLabel { margin-bottom: 8px; } #RoleLabel, #HealthLabel, #SpeedLabel { margin-bottom: 3px; } #ImageNotFoundLabel { font-style: italic; } #StaticInfoLabel a, #JumpBarLabel a { color: #77C4FF; text-decoration: none; } #StaticInfoLabel a:hover, #JumpBarLabel a:hover { color: #AADDFF; text-decoration: underline; } ZoomableTextWidget { color: #E0E0E0; background-color: rgba(0,0,0,0.15); border: none; padding: 6px; border-radius: 3px; margin-bottom: 4px; } QLineEdit { background-color: #3F3F3F; color: #E0E0E0; border: 1px solid #555555; border-radius: 4px; padding: 4px 8px; font-size: 14px; } QComboBox { background-color: #3F3F3F; color: #E0E0E0; border: 1px solid #555555; border-radius: 4px; padding: 4px 8px; } QComboBox::drop-down { border: none; width: 20px; } QComboBox QAbstractItemView { background-color: #3F3F3F; color: #E0E0E0; border: 1px solid #666666; selection-background-color: #5A5A5A; } QPushButton { background-color: #505050; color: #E0E0E0; border: 1px solid #656565; padding: 5px 10px; border-radius: 4px; min-height: 20px; } QPushButton:hover { background-color: #606060; border: 1px solid #757575; } QPushButton:pressed { background-color: #454545; } QPushButton#InfoButton { font-size: 13px; padding: 6px 12px; } QPushButton#FavoriteButton { background-color: transparent; border: none; padding: 2px; color: #AAAAAA; font-size: 20px; font-weight: bold; } QPushButton#FavoriteButton[favorited="true"] { color: #FFD700; } QPushButton#ExitButton { background-color: rgba(200, 30, 30, 0.8); color: #FFFFFF; font-size: 24px; font-weight: bold; border: 1px solid #FF6060; border-radius: 15px; min-width: 30px; max-width: 30px; min-height: 30px; max-height: 30px; padding: 0px; } QPushButton#ExitButton:hover { background-color: rgba(220, 40, 40, 0.9); } QPushButton#ExitButton:pressed { background-color: rgba(180, 20, 20, 0.9); } QLabel#JumpBarLabel { padding: 0px; margin: 1px; border-radius: 4px; } QLabel#JumpBarLabel:hover { background-color: rgba(255, 255, 255, 0.1); } QGroupBox#JumpBarGroupBox { background-color: #333333; border: 1px solid #444; padding: 25px 5px 5px 5px; } QGroupBox#JumpBarGroupBox > QWidget { background-color: transparent; border: none; padding: 0px; } """

# --- Global Font Variables ---
FONT_REG = QFont()
FONT_ITAL = QFont()
FONT_BOLDITAL = QFont()

# --- Helper Functions (Data Loading) ---
def load_character_data(data_folder=CHARACTER_DATA_FOLDER):
    all_character_data = {}; print(f"Loading character data from folder: {data_folder}"); loaded_count = 0; error_files = []
    if not os.path.isdir(data_folder): print(f"Error: Character data folder not found at '{data_folder}'"); return None
    for filename in os.listdir(data_folder):
        if filename.lower().endswith(".json"):
            file_path = os.path.join(data_folder, filename)
            try:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f: char_data = json.load(f)
                except UnicodeDecodeError:
                    print(f"Warning: UTF-8 decode failed for '{filename}'. Trying 'utf-8-sig'.")
                    with open(file_path, 'r', encoding='utf-8-sig') as f: char_data = json.load(f)
                char_name = char_data.get("name")
                if not char_name: print(f"Warning: Skipping file '{filename}'. Missing 'name'"); error_files.append(filename + " (Missing 'name')"); continue
                if char_name in all_character_data: print(f"Warning: Duplicate name '{char_name}' in '{filename}'. Overwriting."); error_files.append(filename + f" (Duplicate: {char_name})")
                all_character_data[char_name] = char_data; loaded_count += 1
            except Exception as e: print(f"Error loading '{filename}': {e}"); error_files.append(filename + f" (Load Error: {e})")
    if error_files: print("\n--- Issues loading files ---"); [print(f"- {err}") for err in error_files]; print("--------------------------\n")
    if loaded_count > 0: print(f"Successfully loaded data for {loaded_count} characters."); return all_character_data
    else: print("Error: No valid character data files loaded."); return None

def load_favorites(filename=FAVORITES_FILE):
    if not os.path.exists(filename): return set()
    try:
        with open(filename, 'r', encoding='utf-8') as f: data = json.load(f); return set(data.get("favorites", []))
    except Exception as e: print(f"Warning: Could not load favorites '{filename}'. Error: {e}"); return set()

def save_favorites(favorites_set, filename=FAVORITES_FILE):
    try:
        fav_dir = os.path.dirname(filename)
        if not os.path.exists(fav_dir):
            try: os.makedirs(fav_dir); print(f"Created directory for favorites: {fav_dir}")
            except OSError as e: print(f"Error creating directory for favorites '{fav_dir}'. Error: {e}"); return
        with open(filename, 'w', encoding='utf-8') as f: json.dump({"favorites": sorted(list(favorites_set))}, f, indent=2)
        print(f"Favorites saved to '{filename}'")
    except Exception as e: print(f"Error saving favorites to '{filename}'. Error: {e}")

# --- Zoomable Text Widget ---
class ZoomableTextWidget(QTextEdit):
    def __init__(self, initial_html="", base_font_size_pt=BASE_FONT_SIZE, parent=None):
        super().__init__(parent)
        self._base_font_size_pt = base_font_size_pt; self._current_font_size_pt = base_font_size_pt
        self.setReadOnly(True); self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff); self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff); self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere); self.setObjectName("ZoomableTextWidget")
        self.document().contentsChanged.connect(self.adjust_height); self._original_resizeEvent = self.resizeEvent; self.resizeEvent = self._custom_resizeEvent; self._update_font(); self.setHtmlWithBaseSize(initial_html)
        size_policy = self.sizePolicy(); size_policy.setVerticalPolicy(QSizePolicy.MinimumExpanding); size_policy.setHorizontalPolicy(QSizePolicy.Expanding); self.setSizePolicy(size_policy); self.adjust_height()
    def _custom_resizeEvent(self, event): self._original_resizeEvent(event); self.adjust_height()
    def _update_font(self): font = self.font(); font.setFamily(FONT_FAMILY_NAME); font.setPointSize(self._current_font_size_pt); self.setFont(font); self.adjust_height()
    def setHtmlWithBaseSize(self, html_text): styled_html = f"""<body style='font-family: "{FONT_FAMILY_NAME}"; font-size: {self._current_font_size_pt}pt;'>{html_text}</body>"""; self.document().blockSignals(True); super().setHtml(styled_html); self.document().blockSignals(False); self.document().setTextWidth(self.viewport().width() if self.viewport().width() > 0 else -1); self.adjust_height()
    def wheelEvent(self, event: QWheelEvent):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            delta = event.angleDelta().y(); new_size_pt = self._current_font_size_pt
            if delta > 0: new_size_pt += 1
            elif delta < 0: new_size_pt = max(7, self._current_font_size_pt - 1)
            if new_size_pt != self._current_font_size_pt:
                self._current_font_size_pt = new_size_pt; print(f"Zooming to base font size: {self._current_font_size_pt}pt")
                current_html_content = self.document().toHtml(); body_match = re.search(r"<body.*?>(.*)</body>", current_html_content, re.DOTALL | re.IGNORECASE); inner_html = body_match.group(1) if body_match else ""
                self._update_font(); self.setHtmlWithBaseSize(inner_html)
            event.accept()
        else:
            parent_scroll_area = self.parent()
            while parent_scroll_area is not None and not isinstance(parent_scroll_area, QScrollArea):
                 if isinstance(parent_scroll_area, InfoPopup): parent_scroll_area = parent_scroll_area.findChild(QScrollArea); break
                 parent_scroll_area = parent_scroll_area.parent()
            if isinstance(parent_scroll_area, QScrollArea): pos_in_parent = self.mapTo(parent_scroll_area.viewport(), event.position().toPoint()); global_pos = event.globalPosition(); new_event = QWheelEvent(pos_in_parent, global_pos, event.pixelDelta(), event.angleDelta(), event.buttons(), event.modifiers(), event.phase(), event.inverted(), event.source()); QApplication.sendEvent(parent_scroll_area.viewport(), new_event); event.accept()
            else: super().wheelEvent(event)
    @Slot()
    def adjust_height(self):
        current_width = self.viewport().width()
        self.document().setTextWidth(current_width if current_width > 0 else -1)
        calculated_height = self.document().size().height()
        margins = self.contentsMargins()
        padding = 8
        new_min_height = int(calculated_height + margins.top() + margins.bottom() + padding)
        if self.minimumHeight() != new_min_height:
             self.setMinimumHeight(new_min_height)

# --- Clickable Label for Jump Bar ---
class ClickableLabel(QLabel):
    clicked = Signal(str)
    def __init__(self, tooltip_text="", parent=None): super().__init__("", parent); self.setObjectName("JumpBarLabel"); self.setToolTip(tooltip_text)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.clicked.emit(self.toolTip())
        super().mousePressEvent(event)

# --- Character Card Widget ---
class CharacterCard(QWidget):
    favorite_toggled = Signal(str, bool)
    def __init__(self, character_name, character_data, is_favorite):
        super().__init__(); self.character_name = character_name; self.character_data = character_data; self._is_favorite = is_favorite; self.font_family = FONT_FAMILY_NAME; self.init_ui()
    def create_zoomable_widget(self, html_text): return ZoomableTextWidget(html_text, base_font_size_pt=BASE_FONT_SIZE)
    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setSpacing(12); primary_theme_color_str = self.character_data.get("color_theme", DEFAULT_THEME_COLOR); secondary_theme_color_str = self.character_data.get("color_theme_secondary", DEFAULT_SECONDARY_THEME_COLOR); primary_theme_color = QColor(primary_theme_color_str)
        self.setStyleSheet(f""" CharacterCard {{ border: 3px solid {primary_theme_color_str}; border-radius: 10px; padding: 15px; }} CharacterCard QGroupBox {{ border: 1px solid {primary_theme_color.darker(120).name()}; }} CharacterCard QGroupBox::title {{ color: {primary_theme_color_str}; }} """); self.setObjectName("CharacterCard")
        header_layout = QHBoxLayout(); header_layout.setSpacing(20); img_label = QLabel(); img_label.setObjectName("CharacterImageLabel"); img_label.setAlignment(Qt.AlignCenter); img_filename = CHARACTER_IMAGE_MAP.get(self.character_name); img_full_path = os.path.join(IMAGE_FOLDER, img_filename) if img_filename else None; img_found = False; max_height = 300
        if img_full_path and os.path.exists(img_full_path):
            full_pixmap = QPixmap(img_full_path)
            if not full_pixmap.isNull():
                # --- RESTORE ORIGINAL MAIN IMAGE CROP ---
                full_width = full_pixmap.width(); full_height = full_pixmap.height()
                target_crop_dim = max(1, full_height // 2)
                target_crop_dim = min(target_crop_dim, full_width) # Ensure fits width
                crop_x = max(0, (full_width - target_crop_dim) // 2)
                crop_y = 0
                crop_rect = QRect(crop_x, crop_y, target_crop_dim, full_height)
                cropped_pixmap = full_pixmap.copy(crop_rect)
                if not cropped_pixmap.isNull():
                    display_pixmap = cropped_pixmap.scaledToHeight(max_height, Qt.SmoothTransformation)
                    img_label.setPixmap(display_pixmap)
                    img_found = True
                else:
                    print(f"Warning: Main image cropping failed for {self.character_name}")
                # --- END RESTORED CROP ---
        if not img_found: fallback_text = f"Image Missing:\n{img_filename or 'Not Mapped'}"; img_label.setText(fallback_text); img_label.setObjectName("ImageNotFoundLabel"); img_label.setStyleSheet(f"color: {primary_theme_color_str};")
        img_label.setMinimumHeight(max_height); img_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed); header_layout.addWidget(img_label, 0)
        right_header_layout = QVBoxLayout(); right_header_layout.setAlignment(Qt.AlignTop); name_fav_layout = QHBoxLayout(); name_fav_layout.setSpacing(10); name_label = QLabel(self.character_name); name_font = QFont(self.font_family, CHARACTER_NAME_FONT_SIZE); name_label.setFont(name_font); name_label.setStyleSheet(f"color: {primary_theme_color_str};"); name_label.setObjectName("CharacterNameLabel"); name_fav_layout.addWidget(name_label, 1); self.fav_button = QPushButton(); self.fav_button.setObjectName("FavoriteButton"); self.fav_button.setCheckable(True); self.fav_button.setFixedSize(QSize(35, 35)); self.fav_button.setToolTip("Toggle Favorite"); self.fav_button.clicked.connect(self.toggle_favorite_button); self.update_favorite_button_style(); name_fav_layout.addWidget(self.fav_button, 0, Qt.AlignTop | Qt.AlignRight); right_header_layout.addLayout(name_fav_layout); stats_layout = QVBoxLayout(); stats_layout.setSpacing(5); role_label = QLabel(f"<b>Role:</b> {self.character_data.get('role', 'N/A')}"); role_font = QFont(self.font_family, BASE_FONT_SIZE + 1); role_label.setFont(role_font); role_label.setTextFormat(Qt.RichText); role_label.setObjectName("RoleLabel"); stats_layout.addWidget(role_label); health_label = QLabel(f"<b>Health:</b> {self.character_data.get('health', 'N/A')}"); health_label.setFont(QFont(self.font_family, BASE_FONT_SIZE + 1)); health_label.setTextFormat(Qt.RichText); health_label.setObjectName("HealthLabel"); stats_layout.addWidget(health_label); speed_label = QLabel(f"<b>Speed:</b> {self.character_data.get('speed', 'N/A')}"); speed_label.setFont(QFont(self.font_family, BASE_FONT_SIZE + 1)); speed_label.setTextFormat(Qt.RichText); speed_label.setObjectName("SpeedLabel"); stats_layout.addWidget(speed_label); right_header_layout.addLayout(stats_layout); header_layout.addLayout(right_header_layout, 1); main_layout.addLayout(header_layout)
        def create_section(title, data_list_or_str, secondary_color):
            group = QGroupBox(title); title_font = QFont(self.font_family, GROUP_TITLE_FONT_SIZE); title_font.setBold(True); group.setFont(title_font); layout = QVBoxLayout(group); layout.setSpacing(8); content_html = ""
            ability_title_style = ABILITY_TITLE_STYLE_TEMPLATE.format(color=secondary_color); partner_style = PARTNER_STYLE_TEMPLATE.format(color=secondary_color); reading_list_title_style = READING_LIST_TITLE_STYLE_TEMPLATE.format(color=secondary_color); title_span_style = f"style='{ability_title_style}'"; reading_title_span_style = f"style='{reading_list_title_style}'"; details_style = f"color: {DETAILS_COLOR}; font-size: 0.95em;"; lore_style = f"color: {LORE_COLOR}; font-style: italic; font-size: 1.0em;";
            if title == "Abilities":
                if not data_list_or_str: content_html = "<p><i>None listed.</i></p>"
                else:
                    for item in data_list_or_str: content_html += (f"<p><span {title_span_style}>{item.get('name', 'N/A')} ({item.get('keybind', '?')})</span><br/>"f"<i>Type:</i> {item.get('type', 'N/A')} | "f"<i>Damage:</i> {item.get('damage', 'N/A')} | "f"<i>Range:</i> {item.get('range', 'N/A')} | "f"<i>Cooldown:</i> {item.get('cooldown', 'N/A')}<br/>"f"<span style='{details_style}'>{item.get('details', '')}</i></span></p>")
            elif title == "Ultimate":
                 item = data_list_or_str[0] if isinstance(data_list_or_str, list) and data_list_or_str else {};
                 if not item: content_html = "<p><i>None listed.</i></p>"
                 else: content_html = (f"<p><span {title_span_style}>{item.get('name', 'N/A')} ({item.get('keybind', '?')})</span><br/>"f"<i>Damage:</i> {item.get('damage', 'N/A')} | "f"<i>Range/Effect:</i> {item.get('range', 'N/A')} / {item.get('effect', 'N/A')} | "f"<i>Charge Cost:</i> {item.get('charge_cost', 'N/A')}<br/>"f"<span style='{details_style}'>{item.get('details', '')}</i></span></p>")
            elif title == "Passives / Melee":
                if not data_list_or_str: content_html = "<p><i>None listed.</i></p>"
                else:
                    for item in data_list_or_str: content_html += (f"<p><span {title_span_style}>{item.get('name', 'N/A')} ({item.get('keybind', 'Passive')})</span><br/>"f"<span style='{details_style}'>{item.get('details', '')}</i></span></p>")
            elif title == "Teamups":
                if not data_list_or_str: content_html = "<p><i>None listed.</i></p>"
                else:
                    content_html = f"<p><span {title_span_style}>Synergies</span></p>";
                    for item in data_list_or_str: content_html += (f"<p><b style='{partner_style}'>Partner: {item.get('partner', 'N/A')}</b><br/>"f"<span style='{details_style}'>Effect: {item.get('effect', 'N/A')}</i></span></p>")
            elif title == "Lore":
                if not data_list_or_str: content_html = "<p><i>None listed.</i></p>"
                else: content_html = f"<p><span style='{lore_style}'>{data_list_or_str}</span></p>"
            elif title == "Relevant Comics":
                if not data_list_or_str: content_html = "<p><i>None listed.</i></p>"
                else:
                    content_html = f"<p><span {reading_title_span_style}>Reading List</span></p><ul>";
                    for comic in data_list_or_str: content_html += f"<li>{comic.get('title', 'N/A')}</li>"
                    content_html += "</ul>"
            if content_html: widget = self.create_zoomable_widget(content_html); layout.addWidget(widget)
            layout.addStretch(1); group.setLayout(layout); return group
        main_layout.addWidget(create_section("Abilities", self.character_data.get('abilities', []), secondary_theme_color_str)); ultimate_data = self.character_data.get('ultimate'); main_layout.addWidget(create_section("Ultimate", [ultimate_data] if ultimate_data else [], secondary_theme_color_str)); main_layout.addWidget(create_section("Passives / Melee", self.character_data.get('passives', []), secondary_theme_color_str)); main_layout.addWidget(create_section("Teamups", self.character_data.get('teamups', []), secondary_theme_color_str)); main_layout.addWidget(create_section("Lore", self.character_data.get('lore', ''), secondary_theme_color_str)); main_layout.addWidget(create_section("Relevant Comics", self.character_data.get('comics', []), secondary_theme_color_str))
    def update_favorite_button_style(self):
        if self._is_favorite: self.fav_button.setText("★"); self.fav_button.setProperty("favorited", True); self.fav_button.setToolTip("Remove from Favorites")
        else: self.fav_button.setText("☆"); self.fav_button.setProperty("favorited", False); self.fav_button.setToolTip("Add to Favorites")
        self.fav_button.style().unpolish(self.fav_button); self.fav_button.style().polish(self.fav_button)
    @Slot()
    def toggle_favorite_button(self): self._is_favorite = not self._is_favorite; self.update_favorite_button_style(); self.favorite_toggled.emit(self.character_name, self._is_favorite)
    def is_favorite(self): return self._is_favorite

# --- Info Popup Dialog ---
class InfoPopup(QDialog):
    def __init__(self, title, content_file_path, parent=None):
        super().__init__(parent); self.setWindowTitle(f"Info: {title}"); self.setModal(True); self.setObjectName("InfoPopupDialog"); self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint); self.setAttribute(Qt.WA_TranslucentBackground); self._drag_pos = QPoint()
        if parent: parent_size = parent.size(); self.resize(int(parent_size.width() * 0.8), int(parent_size.height() * 0.8))
        else: self.resize(800, 600)
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(2, 2, 2, 2); main_layout.setSpacing(0); title_bar_widget = QWidget(); title_bar_widget.setObjectName("PopupTitleBar"); title_bar_layout = QHBoxLayout(title_bar_widget); title_bar_layout.setContentsMargins(10, 0, 0, 0); title_bar_layout.setSpacing(5); title_label = QLabel(title); title_label.setObjectName("PopupTitleLabel"); title_font = QFont(FONT_FAMILY_NAME, GROUP_TITLE_FONT_SIZE + 2, QFont.Bold); title_label.setFont(title_font); title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft); close_button = QPushButton("X"); close_button.setObjectName("PopupCloseButton"); close_button.setToolTip("Close"); close_button.clicked.connect(self.reject); title_bar_layout.addWidget(title_label, 1); title_bar_layout.addWidget(close_button, 0, Qt.AlignTop | Qt.AlignRight); main_layout.addWidget(title_bar_widget); content_container = QWidget(); content_layout = QVBoxLayout(content_container); content_layout.setContentsMargins(10, 5, 10, 10); self.text_area = ZoomableTextWidget(base_font_size_pt=BASE_FONT_SIZE, parent=self); scroll_area = QScrollArea(); scroll_area.setWidgetResizable(True); scroll_area.setWidget(self.text_area); scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff); scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded); scroll_area.setFrameShape(QFrame.NoFrame); content_layout.addWidget(scroll_area, 1); main_layout.addWidget(content_container, 1); self.load_and_format_content(content_file_path); self.setLayout(main_layout)
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if event.position().y() < 40: self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft(); event.accept()
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and not self._drag_pos.isNull(): self.move(event.globalPosition().toPoint() - self._drag_pos); event.accept()
    def mouseReleaseEvent(self, event: QMouseEvent): self._drag_pos = QPoint(); event.accept()
    def markdown_to_html(self, markdown_text):
        lines = markdown_text.strip().split('\n'); html_lines = []; in_list = False; in_paragraph = False; bold_pattern = re.compile(r'\*\*(.+?)\*\*')
        def replace_bold_popup(match): return f"<span style='{BOLD_UNDERLINE_STYLE_TEMPLATE_POPUP}'>{match.group(1)}</span>"
        for line in lines:
            stripped_line = line.strip(); processed_line = bold_pattern.sub(replace_bold_popup, stripped_line)
            if not processed_line.startswith(('* ', '- ')) and in_list: html_lines.append("</ul>"); in_list = False
            if (processed_line.startswith(('# ', '## ', '### ', '* ', '- ')) or not stripped_line) and in_paragraph: html_lines.append("</p>"); in_paragraph = False
            if processed_line.startswith('# '): content = processed_line[2:]; html_lines.append(f"<h1 style='color: {H1_COLOR}; font-size: 1.4em; font-weight: bold; margin-bottom: 8px;'>{content}</h1>")
            elif processed_line.startswith('## '): content = processed_line[3:]; html_lines.append(f"<h2 style='color: {H2_COLOR}; font-size: 1.2em; font-weight: bold; margin-top: 10px; margin-bottom: 5px;'>{content}</h2>")
            elif processed_line.startswith('### '): content = processed_line[4:]; html_lines.append(f"<h3 style='color: {H3_COLOR}; font-size: 1.1em; font-weight: bold; margin-top: 8px; margin-bottom: 3px;'>{content}</h3>")
            elif processed_line.startswith(('* ', '- ')):
                if not in_list: html_lines.append(f"<ul style='{LIST_STYLE}'>"); in_list = True
                content = processed_line[2:]; html_lines.append(f"<li>{content}</li>")
            elif not stripped_line: pass
            else:
                if not in_paragraph: html_lines.append("<p style='margin-top: 4px; margin-bottom: 4px;'>"); in_paragraph = True; html_lines.append(processed_line)
                else: html_lines.append("<br/>"); html_lines.append(processed_line)
        if in_list: html_lines.append("</ul>")
        if in_paragraph: html_lines.append("</p>")
        inner_html = ''.join(html_lines); return inner_html.strip()
    def load_and_format_content(self, file_path):
        error_html = "";
        if not os.path.exists(file_path): error_html = f"<p>Error: Content file not found.<br/>Expected at: {file_path}</p>"; print(f"Error: Content file not found at '{file_path}'")
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f: markdown_content = f.read(); html_content = self.markdown_to_html(markdown_content); self.text_area.setHtmlWithBaseSize(html_content); return
            except Exception as e: error_html = f"<p>Error reading or formatting content file:<br/>{file_path}<br/><br/>{e}</p>"; print(f"Error reading/formatting content file '{file_path}': {e}")
        self.text_area.setHtmlWithBaseSize(error_html)

# --- Main Application Window ---
class MainWindow(QMainWindow):
    def __init__(self, character_data, target_screen, fullscreen):
        super().__init__()
        self.app = QApplication.instance()
        self.all_character_data = character_data if character_data else {}
        self.character_widgets = {} # For the main scroll area character cards
        self.favorites = load_favorites()
        self.font_family = FONT_FAMILY_NAME
        self.setWindowTitle("Marvel Rivals Dashboard")
        self._target_screen = target_screen
        self._fullscreen = fullscreen
        self.ASPECT_RATIO_THRESHOLD = 1.2
        self.jump_bar_icon_widgets: dict[str, ClickableLabel] = {}
        self.current_jump_bar_icon_size = 40 # Default/initial size

        # --- Debounce Timer for Jump Bar Icon Layout --- 
        self.jump_bar_layout_timer = QTimer(self)
        self.jump_bar_layout_timer.setSingleShot(True)
        self.jump_bar_layout_timer.setInterval(150) # milliseconds delay
        # Connect to method specifically for updating icon layout/size
        self.jump_bar_layout_timer.timeout.connect(self._update_jump_bar_layout)
        # -----------------------------------------

        self.init_ui()
        self.setup_fullscreen(target_screen, fullscreen)
        self.update_character_display()

        print(f"DEBUG __init__ END: jump_bar_icon_widgets in self.__dict__? {'jump_bar_icon_widgets' in self.__dict__}")

    def init_ui(self):
        print(f"DEBUG init_ui START: jump_bar_icon_widgets in self.__dict__? {'jump_bar_icon_widgets' in self.__dict__}") # DEBUG
        main_widget = QWidget(); self.setCentralWidget(main_widget); main_grid_layout = QGridLayout(main_widget); main_grid_layout.setContentsMargins(10, 10, 10, 10); main_grid_layout.setSpacing(10);
        content_widget = QWidget(); main_layout = QVBoxLayout(content_widget); main_layout.setContentsMargins(0, 0, 0, 0); main_layout.setSpacing(10);
        main_grid_layout.addWidget(content_widget, 0, 0, 1, 1); # Content in grid row 0, col 0, spans 1 col
        self.static_info_box = QGroupBox("Info & Links"); self.static_info_box.setObjectName("StaticInfoBox"); self.static_info_box.setFont(QFont(self.font_family, GROUP_TITLE_FONT_SIZE, QFont.Bold)); static_layout = QVBoxLayout(self.static_info_box); static_layout.setSpacing(8); info_button_layout = QHBoxLayout(); info_button_layout.setSpacing(10);
        self.info_buttons = {}; button_font = QFont(self.font_family, BASE_FONT_SIZE -1 )
        for btn_text in INFO_FILES.keys(): button = QPushButton(btn_text); button.setObjectName("InfoButton"); button.setFont(button_font); button.clicked.connect(self.show_info_popup); info_button_layout.addWidget(button); self.info_buttons[btn_text] = button

        # Add Spacer to push Exit button to the right
        info_button_layout.addStretch(1)

        # Add Exit Button Here
        self.exit_button = QPushButton("X")
        self.exit_button.setObjectName("ExitButton") # Use existing style
        self.exit_button.setToolTip("Close Application (ESC also works)")
        # Reuse existing style properties (size, font etc. defined in stylesheet)
        # self.exit_button.setFont(QFont(self.font_family, 18, QFont.Bold))
        self.exit_button.clicked.connect(self.close)
        info_button_layout.addWidget(self.exit_button)

        static_layout.addLayout(info_button_layout);
        self.static_info_box.setLayout(static_layout);
        self.static_info_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum);
        main_layout.addWidget(self.static_info_box)

        # --- STATIC JUMP BAR SETUP (MOVED HERE) ---
        self.jump_bar_groupbox = QGroupBox("Characters")
        self.jump_bar_groupbox.setObjectName("JumpBarGroupBox")
        self.jump_bar_groupbox.setFont(QFont(self.font_family, GROUP_TITLE_FONT_SIZE, QFont.Bold))
        groupbox_layout = QVBoxLayout(self.jump_bar_groupbox)
        groupbox_layout.setContentsMargins(5, 5, 5, 5)
        groupbox_layout.setSpacing(0)

        # Container Widget inside GroupBox (Will hold the rows vertically)
        self.jump_bar_icon_container = QWidget()
        # --- ADD CONTAINER SIZE POLICY --- Ensure it signals its preferred size
        self.jump_bar_icon_container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        # This container now needs a QVBoxLayout to stack the rows
        self.jump_bar_rows_layout = QVBoxLayout(self.jump_bar_icon_container)
        self.jump_bar_rows_layout.setContentsMargins(0, 0, 0, 0)
        self.jump_bar_rows_layout.setSpacing(JUMP_BAR_FIXED_SPACING) # Spacing between rows

        # --- Call helper to create icons and add rows to the VBox --- 
        print(f"DEBUG init_ui BEFORE _create_jump_bar_icons: jump_bar_icon_widgets in self.__dict__? {'jump_bar_icon_widgets' in self.__dict__}") # DEBUG
        self._create_jump_bar_icons() # Pass fixed size
        # -----------------------------------------------------

        self.jump_bar_icon_container.setLayout(self.jump_bar_rows_layout) # Set the VBox layout
        groupbox_layout.addWidget(self.jump_bar_icon_container) # Add container directly
        self.jump_bar_groupbox.setLayout(groupbox_layout)

        # Let GroupBox height be determined by its content (2 rows + padding)
        # Use Preferred policy vertically to allow shrinking if content allows (though it's fixed now)
        self.jump_bar_groupbox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        main_layout.addWidget(self.jump_bar_groupbox)

        # --- Toolbar Setup (Remains mostly unchanged) ---
        self.toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(self.toolbar_widget)
        toolbar_layout.setContentsMargins(0, 5, 0, 5)
        toolbar_layout.setSpacing(15)
        toolbar_layout.setAlignment(Qt.AlignLeft)
        search_label = QLabel("Search:")
        search_label.setFont(QFont(self.font_family, BASE_FONT_SIZE))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter by name (3+ chars)...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.textChanged.connect(self._handle_search_change)
        toolbar_layout.addWidget(search_label)
        toolbar_layout.addWidget(self.search_input)
        filter_label = QLabel("Role:")
        filter_label.setFont(QFont(self.font_family, BASE_FONT_SIZE))
        self.filter_combo = QComboBox()
        self.filter_combo.setFont(QFont(self.font_family, BASE_FONT_SIZE))
        self.populate_filter_combo()
        self.filter_combo.currentIndexChanged.connect(self.update_character_display)
        toolbar_layout.addWidget(filter_label)
        toolbar_layout.addWidget(self.filter_combo)
        sort_label = QLabel("Sort:")
        sort_label.setFont(QFont(self.font_family, BASE_FONT_SIZE))
        self.sort_combo = QComboBox()
        self.sort_combo.setFont(QFont(self.font_family, BASE_FONT_SIZE))
        self.sort_combo.addItem("★ + Name", "fav_name")
        self.sort_combo.addItem("Name (A-Z)", "name")
        self.sort_combo.addItem("Role", "role")
        self.sort_combo.addItem("Health (High-Low)", "health")
        self.sort_combo.currentIndexChanged.connect(self.update_character_display)
        toolbar_layout.addWidget(sort_label)
        toolbar_layout.addWidget(self.sort_combo)
        # RESTORED Jump Bar Toggle Button
        self.toggle_jump_bar_button = QPushButton("Hide") # Shortened initial text
        self.toggle_jump_bar_button.setToolTip("Show/Hide Character Icons")
        self.toggle_jump_bar_button.setCheckable(True)
        self.toggle_jump_bar_button.setChecked(True) # Start visible
        self.toggle_jump_bar_button.clicked.connect(self._toggle_jump_bar_manual)
        toolbar_layout.addWidget(self.toggle_jump_bar_button)
        toolbar_layout.addStretch(1)
        main_layout.addWidget(self.toolbar_widget)

        # --- Scroll Area for Character Cards (Remains Largely Unchanged) ---
        self.scroll_area = QScrollArea(); self.scroll_area.setWidgetResizable(True); self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff); self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded); self.scroll_content_widget = QWidget(); self.scroll_area.setWidget(self.scroll_content_widget); self.scroll_layout = QVBoxLayout(self.scroll_content_widget); self.scroll_layout.setSpacing(25); self.scroll_layout.setContentsMargins(10, 10, 10, 10); self.scroll_layout.setAlignment(Qt.AlignTop);
        # --- ADDED STRETCH FACTOR --- Allow scroll area to expand vertically
        main_layout.addWidget(self.scroll_area, 1)

        # --- Main Grid Layout Stretch (Adjusted) ---
        # Only one column now
        main_grid_layout.setColumnStretch(0, 1) # Content Area takes all space
        main_grid_layout.setRowStretch(0, 1)     # Let row 0 take vertical space

        # --- Trigger Initial Icon Sizing ---
        # Use a timer to ensure this runs after the window is shown and has a size
        QTimer.singleShot(0, self._update_jump_bar_layout)

    def setup_fullscreen(self, target_screen=None, fullscreen=True):
        """Sets the window geometry based on target screen and fullscreen mode."""
        if target_screen is None:
            target_screen = QApplication.primaryScreen()
        if not isinstance(target_screen, QScreen):
             print(f"Warning: Invalid target_screen provided ({target_screen}), falling back to primary.")
             target_screen = QApplication.primaryScreen()

        print(f"Targeting screen: {target_screen.name()}")
        print(f"Screen Geometry: {target_screen.geometry()}")
        print(f"Available Geometry: {target_screen.availableGeometry()}")

        if fullscreen:
            print("Setting to Fullscreen")
            self.setGeometry(target_screen.geometry())
            self.showFullScreen()
        else:
            print("Setting to Windowed (Fixed Size)")
            available_geo = target_screen.availableGeometry()
            # Use fixed target size
            target_width = 1130
            target_height = 1037

            # Ensure it fits on the screen, scale down if necessary maintaining aspect ratio
            if target_width > available_geo.width() or target_height > available_geo.height():
                print("  Warning: Target size too large for screen, scaling down.")
                width_scale = available_geo.width() / target_width
                height_scale = available_geo.height() / target_height
                scale = min(width_scale, height_scale) * 0.95 # Scale down slightly more just in case
                target_width = int(target_width * scale)
                target_height = int(target_height * scale)

            # Center the window
            window_x = available_geo.x() + (available_geo.width() - target_width) // 2
            window_y = available_geo.y() + (available_geo.height() - target_height) // 2

            self.setGeometry(window_x, window_y, target_width, target_height)
            self.show() # Use show() instead of showMaximized()

        # Allow the event loop to process the geometry changes immediately
        if self.app:
            self.app.processEvents()

        # Update responsive UI elements AFTER setting geometry/state
        self._update_responsive_ui()
        # Note: Initial jump bar layout is handled by QTimer in __init__ now

    def _create_jump_bar_icons(self):
        """Creates all jump bar icon widgets once and stores them."""
        print(f"DEBUG _create_jump_bar_icons START: jump_bar_icon_widgets in self.__dict__? {'jump_bar_icon_widgets' in self.__dict__}") # DEBUG
        if not self.all_character_data:
            return # No data

        character_names = sorted(self.all_character_data.keys())
        print(f"Creating {len(character_names)} jump bar icon widgets...") # Use fixed size constant

        # Clear any existing rows from the vertical layout
        while self.jump_bar_rows_layout.count() > 0:
            item = self.jump_bar_rows_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Create container widgets and HBoxLayouts for the two rows
        row1_widget = QWidget()
        row1_layout = QHBoxLayout(row1_widget)
        row1_layout.setContentsMargins(0, 0, 0, 0)
        row1_layout.setSpacing(JUMP_BAR_FIXED_SPACING)
        row1_layout.setAlignment(Qt.AlignLeft) # Align left within row

        row2_widget = QWidget()
        row2_layout = QHBoxLayout(row2_widget)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(JUMP_BAR_FIXED_SPACING)
        row2_layout.setAlignment(Qt.AlignLeft) # Align left within row

        icon_size = JUMP_BAR_FIXED_ICON_SIZE # Use the constant

        for i, name in enumerate(character_names):
            icon_label = ClickableLabel(name) # Tooltip is the name
            # DO NOT set fixed size or pixmap here - handled by _update_icon_visuals
            # icon_label.setFixedSize(icon_size, icon_size)
            icon_label.setAlignment(Qt.AlignCenter)

            # --- PIXMAP GENERATION REMOVED - Done in _update_icon_visuals ---
            # img_filename = ...
            # ... (pixmap logic removed) ...
            # --------------------------------------

            # Store the label reference
            print(f"  DEBUG: Checking self.jump_bar_icon_widgets exists for '{name}'? {hasattr(self, 'jump_bar_icon_widgets')}")
            if not hasattr(self, 'jump_bar_icon_widgets'):
                print("  FATAL DEBUG: self.jump_bar_icon_widgets lost!")
            self.jump_bar_icon_widgets[name] = icon_label
            # Connect the signal HERE during creation
            icon_label.clicked.connect(self.scroll_to_character)

            # --- ADD WIDGET TO THE CORRECT ROW LAYOUT ---
            if i < 19:
                row1_layout.addWidget(icon_label)
            elif i < 38:
                row2_layout.addWidget(icon_label)
            # else: Ignore characters beyond 38 for now

        # Add stretch to each row layout
        row1_layout.addStretch(1)
        row2_layout.addStretch(1)

        # Add the row widgets to the main vertical layout
        self.jump_bar_rows_layout.addWidget(row1_widget)
        self.jump_bar_rows_layout.addWidget(row2_widget)

        print("Finished creating icons.")

    def _update_responsive_ui(self):
        """Updates UI elements like button text based on current state."""
        # Check if elements exist - Safegaurd against calls before init_ui completes
        if not hasattr(self, 'jump_bar_groupbox'): # Removed check for toggle_jump_bar_button
            print("Warning: UI elements not ready for responsive update.")
            return
        # Removed aspect ratio check for visibility
        # The jump bar visibility is now controlled manually by the toggle button

        # Update button text based on current visibility state - RESTORED
        if hasattr(self, 'toggle_jump_bar_button'): # Check button exists
            self.toggle_jump_bar_button.setText("Hide" if self.jump_bar_groupbox.isVisible() else "Show") # Shortened text
        # Note: We removed the line that automatically sets the button's checked state based on aspect ratio.
        # The checked state is now purely determined by user interaction via _toggle_jump_bar_manual.
        # pass # No action needed currently for responsive UI with static jump bar

    # --- CORRECTED show_info_popup ---
    @Slot()
    def show_info_popup(self):
        sender_button = self.sender()
        if not sender_button:
            print("Error: Could not determine sender button for info popup.")
            return

        button_text = sender_button.text()
        content_filename = INFO_FILES.get(button_text)

        if not content_filename:
            print(f"Error: No info file configured for button '{button_text}'")
            QMessageBox.warning(self, "Info Error", f"No content file associated with '{button_text}'.")
            return

        content_path = os.path.join(INFO_FOLDER, content_filename)
        popup = InfoPopup(button_text, content_path, parent=self)
        popup.setStyleSheet(DARK_STYLESHEET)
        popup.exec()

    def populate_filter_combo(self): self.filter_combo.clear(); self.filter_combo.addItem("All Roles", "All"); roles = sorted(list(set(d.get("role", "Unknown") for d in self.all_character_data.values() if d.get("role")))); [self.filter_combo.addItem(role, role) for role in roles]; self.filter_combo.addItem("Unknown", "Unknown")
    @Slot()
    def handle_favorite_toggled(self, character_name, is_favorite):
        if is_favorite: self.favorites.add(character_name)
        else: self.favorites.discard(character_name)
        if self.sort_combo.currentData() == "fav_name" or "health" in self.sort_combo.currentData(): self.update_character_display()
        save_favorites(self.favorites)
    @Slot()
    def update_character_display(self):
        search_term=self.search_input.text().lower().strip(); filter_role=self.filter_combo.currentData(); sort_key=self.sort_combo.currentData(); effective_search_term = search_term
        if len(search_term) > 0 and len(search_term) < MIN_SEARCH_LENGTH: effective_search_term = ""
        filtered_names=[name for name, data in self.all_character_data.items() if (not effective_search_term or effective_search_term in name.lower()) and (filter_role == "All" or data.get("role", "Unknown") == filter_role)]
        def sort_logic(name):
            data = self.all_character_data[name]
            is_fav = name in self.favorites
            if sort_key == "fav_name":
                return (not is_fav, name.lower())
            elif sort_key == "name":
                return name.lower()
            elif sort_key == "role":
                return (data.get("role", "Unknown"), name.lower())
            elif sort_key == "health":
                health_str = str(data.get("health", 0))
                health = 0
                try:
                    match = re.search(r'\d+', health_str)
                    health = int(match.group(0)) if match else 0
                except Exception:
                    pass # Ignore conversion errors
                return (not is_fav, -health, name.lower())
            else:
                return (not is_fav, name.lower())

        sorted_names = sorted(filtered_names, key=sort_logic)
        current_widgets = {}
        stretch_item = None

        # Clear existing widgets, saving them for potential reuse
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget and isinstance(widget, CharacterCard):
                current_widgets[widget.character_name] = widget
                widget.setVisible(False)
                widget.setParent(None)
            elif widget:
                widget.deleteLater() # Delete non-card widgets
            elif item.spacerItem():
                stretch_item = item # Keep track of the stretch item

        # Add sorted widgets back
        insert_index = 0
        for name in sorted_names:
            if name in current_widgets:
                widget = current_widgets.pop(name) # Reuse existing widget
                widget.setParent(self.scroll_content_widget)
                widget.setVisible(True)
                self.scroll_layout.insertWidget(insert_index, widget)
                self.character_widgets[name] = widget
                insert_index += 1
            else:
                # Create new widget if not found
                data = self.all_character_data[name]
                is_fav = name in self.favorites
                card = CharacterCard(name, data, is_fav)
                card.favorite_toggled.connect(self.handle_favorite_toggled)
                self.scroll_layout.insertWidget(insert_index, card)
                self.character_widgets[name] = card
                insert_index += 1

        # Clean up unused widgets
        for name, widget in current_widgets.items():
            widget.deleteLater()
            self.character_widgets.pop(name, None)

        # Ensure stretch item is at the end
        last_item = self.scroll_layout.itemAt(self.scroll_layout.count() - 1)
        if not last_item or not last_item.spacerItem():
            # Remove existing stretch if it's not at the end
            for i in range(self.scroll_layout.count()):
                item = self.scroll_layout.itemAt(i)
                if item and item.spacerItem():
                    self.scroll_layout.takeAt(i)
                    break
            # Add the stretch item (recycled or new)
            if stretch_item:
                self.scroll_layout.addItem(stretch_item)
            else:
                self.scroll_layout.addStretch(1)
        elif not last_item and self.scroll_layout.count() == 0: # Handle empty layout case
            self.scroll_layout.addStretch(1)
    @Slot(str)
    def scroll_to_character(self, character_name):
        widget_to_scroll_to = self.character_widgets.get(character_name)
        if widget_to_scroll_to and widget_to_scroll_to.isVisible():
            # Calculate the top position of the widget relative to the viewport
            value = self.scroll_area.verticalScrollBar().value()
            widget_top_pos = widget_to_scroll_to.mapTo(self.scroll_content_widget, QPoint(0, 0)).y()
            # Set the scrollbar value to bring the widget's top to the viewport's top
            self.scroll_area.verticalScrollBar().setValue(widget_top_pos)
            # self.scroll_area.ensureWidgetVisible(widget_to_scroll_to, ymargin=0) # Doesn't guarantee top alignment
        elif character_name in self.all_character_data: print(f"Cannot scroll to {character_name}, it might be filtered out.")
        else: print(f"Character '{character_name}' not found in data.")
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape: print("Escape key pressed. Closing application."); self.close()
        else: super().keyPressEvent(event)
    def closeEvent(self, event): print("Saving favorites on close..."); save_favorites(self.favorites); super().closeEvent(event)

    @Slot(bool)
    def _toggle_jump_bar_manual(self, checked):
        print(f"--- _toggle_jump_bar_manual START (Checked: {checked}) ---") # DEBUG
        if not hasattr(self, 'jump_bar_groupbox'):
            print("  DEBUG: jump_bar_groupbox missing!") # DEBUG
            print("--- _toggle_jump_bar_manual END (ERROR) ---") # DEBUG
            return

        print(f"  DEBUG: Setting jump_bar_groupbox visible: {checked}") # DEBUG
        self.jump_bar_groupbox.setVisible(checked)
        # self.toggle_jump_bar_button.setText("Hide Characters" if checked else "Show Characters")

        # print("  DEBUG: GroupBox geometry BEFORE update trigger:", self.jump_bar_groupbox.geometry()) # DEBUG
        # If the jump bar was just made visible, force an update *after*
        # the event loop processes the visibility change and geometry update.
        if checked:
            # --- REVISED UPDATE TRIGGER --- Use processEvents + direct call
            # print("  DEBUG: Calling QApplication.processEvents()...") # DEBUG
            # QApplication.processEvents() # Try to force pending events processing
            # print("  DEBUG: Calling _update_jump_bar_layout() directly...") # DEBUG
            # self._update_jump_bar_layout() # Then update the layout immediately
            # QTimer.singleShot(0, self._update_jump_bar_layout)
            # print("  DEBUG: GroupBox geometry AFTER update trigger:", self.jump_bar_groupbox.geometry()) # DEBUG
            pass # No action needed when showing, layout is static
        print("--- _toggle_jump_bar_manual END ---") # DEBUG
        pass

    def resizeEvent(self, event: QKeyEvent):
        print(f"--- resizeEvent START (OldSize: {event.oldSize()}, NewSize: {event.size()}) ---") # DEBUG
        super().resizeEvent(event)
        self._update_responsive_ui() # RESTORED - Used for toggle button text
        # Instead of direct call, start/restart the debounce timer
        print("  DEBUG: Starting jump_bar_layout_timer...") # DEBUG
        self.jump_bar_layout_timer.start() # RESTORED - Trigger icon resize
        print("--- resizeEvent END ---") # DEBUG

    @Slot(str)
    def _handle_search_change(self, text):
        """Filters character display based on search input."""
        trimmed_text = text.strip()
        # Trigger update only if text is empty or meets minimum length
        if len(trimmed_text) == 0 or len(trimmed_text) >= MIN_SEARCH_LENGTH:
            self.update_character_display()

    def _update_jump_bar_layout(self):
        """Calculates required icon size based on width and updates visuals."""
        print("--- _update_jump_bar_layout START ---") # DEBUG
        if not hasattr(self, 'jump_bar_groupbox') or not self.jump_bar_groupbox.isVisible():
            print("  DEBUG: GroupBox not ready or visible, skipping layout.")
            return

        content_rect = self.jump_bar_groupbox.contentsRect()
        available_width = content_rect.width()
        print(f"  DEBUG: Available GroupBox Width: {available_width}")

        if available_width <= 0:
            print("  DEBUG: Zero width, skipping.")
            return

        # Calculate ideal size to fit 19 icons + spacing horizontally
        num_icons_per_row = 19
        spacing = JUMP_BAR_FIXED_SPACING
        # Width = 19 * icon_size + 18 * spacing => icon_size = (Width - 18*spacing) / 19
        calculated_size = (available_width - (num_icons_per_row - 1) * spacing) // num_icons_per_row
        new_icon_size = max(20, calculated_size) # Ensure a minimum size

        print(f"  DEBUG: Calculated icon size: {calculated_size} -> Final size: {new_icon_size}")

        # Update stored size only if it truly changes
        if new_icon_size != self.current_jump_bar_icon_size:
            print(f"  DEBUG: Icon size changed: {self.current_jump_bar_icon_size} -> {new_icon_size}. Updating visuals.")
            self.current_jump_bar_icon_size = new_icon_size
        # else: print("  DEBUG: Icon size unchanged.")

        # ALWAYS update visuals to ensure layout adjusts correctly when narrowing
        self._update_icon_visuals(new_icon_size)

        print("--- _update_jump_bar_layout END ---")

    def _update_icon_visuals(self, icon_size):
        """Updates the fixed size and pixmap for all existing jump bar icons."""
        print(f"--- _update_icon_visuals START (Size: {icon_size}) ---")
        if not self.jump_bar_icon_widgets: return # No icons to update

        for name, icon_label in self.jump_bar_icon_widgets.items():
            # 1. Update fixed size
            icon_label.setFixedSize(icon_size, icon_size)

            # 2. Re-generate Pixmap
            img_filename = CHARACTER_IMAGE_MAP.get(name)
            img_full_path = os.path.join(IMAGE_FOLDER, img_filename) if img_filename else None
            img_found = False
            final_pixmap = None # Initialize

            if img_full_path and os.path.exists(img_full_path):
                full_pixmap = QPixmap(img_full_path)
                if not full_pixmap.isNull():
                    # --- RESTORE ORIGINAL MAIN IMAGE CROP ---
                    full_width = full_pixmap.width()
                    full_height = full_pixmap.height()

                    # Determine crop dimension and Y offset based on character name
                    if name == "Jeff the Land Shark":
                        target_crop_dim = min(full_width, full_height) # Less zoom
                        crop_y = 0 # Top edge
                    elif name == "Spider-Man":
                        target_crop_dim = max(1, full_height // 2) # Zoomed
                        crop_y = max(0, full_height - target_crop_dim) # Bottom edge
                    elif name == "Peni Parker":
                        target_crop_dim = max(1, full_height // 2) # Zoomed
                        crop_y = max(0, (full_height - target_crop_dim) // 2) # Vertical center
                    else: # Default (Other characters)
                        target_crop_dim = max(1, full_height // 2) # Zoomed
                        crop_y = 0 # Top edge

                    # Ensure crop dim doesn't exceed width
                    target_crop_dim = min(target_crop_dim, full_width)

                    # Calculate X offset for horizontal centering
                    crop_x = max(0, (full_width - target_crop_dim) // 2)

                    # Final crop rectangle
                    crop_rect = QRect(crop_x, crop_y, target_crop_dim, target_crop_dim)
                    cropped_thumb = full_pixmap.copy(crop_rect)

                    if not cropped_thumb.isNull():
                        # Scale the *cropped* square thumbnail to the target icon size
                        final_pixmap = cropped_thumb.scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        img_found = True # Mark as found only if scaling succeeds

            # Set the final pixmap or fallback text
            if img_found and final_pixmap and not final_pixmap.isNull():
                 icon_label.setPixmap(final_pixmap)
            else:
                # Fallback text/style if image loading, cropping, or scaling failed
                icon_label.setText(name[0]) # First initial
                icon_label.setFont(QFont(FONT_FAMILY_NAME, max(8, icon_size // 3), QFont.Bold)) # Scale font roughly
                icon_label.setStyleSheet("background-color: #444; border-radius: 4px; color: #ccc;")
                icon_label.setPixmap(QPixmap()) # Clear any old pixmap

        # Force layout update after changing sizes
        print("  DEBUG: Forcing geometry updates after icon visual update...")
        if hasattr(self, 'jump_bar_icon_container'): self.jump_bar_icon_container.adjustSize()
        if hasattr(self, 'jump_bar_groupbox'): self.jump_bar_groupbox.adjustSize()
        # Force parent layout update
        if self.centralWidget() and self.centralWidget().layout(): self.centralWidget().layout().update()
        print("--- _update_icon_visuals END ---")

# --- run_dashboard function --- (Keep existing)
def run_dashboard(target_screen, fullscreen):
    app_instance = QApplication.instance();
    if not app_instance:
        # If no instance exists, create one (for direct run - though less likely now)
        print("INFO: QApplication instance not found, creating one.")
        app_instance = QApplication(sys.argv)

    # Target screen is now passed directly as an object
    if target_screen is None or not isinstance(target_screen, QScreen):
        print(f"Warning: Invalid target_screen object ({target_screen}), using primary.")
        target_screen = QApplication.primaryScreen()

    font_db = QFontDatabase(); font_id_reg = font_db.addApplicationFont(FONT_REGULAR); font_id_ital = font_db.addApplicationFont(FONT_ITALIC); font_id_boldital = font_db.addApplicationFont(FONT_BOLDITALIC)
    # --- DEBUG Font Loading ---
    print(f"DEBUG run_dashboard: Attempting to load REGULAR font from: {FONT_REGULAR}")
    print(f"DEBUG run_dashboard: Font ID Regular: {font_id_reg}")
    print(f"DEBUG run_dashboard: Attempting to load ITALIC font from: {FONT_ITALIC}")
    print(f"DEBUG run_dashboard: Font ID Italic: {font_id_ital}")
    print(f"DEBUG run_dashboard: Attempting to load BOLDITALIC font from: {FONT_BOLDITALIC}")
    print(f"DEBUG run_dashboard: Font ID BoldItalic: {font_id_boldital}")
    # --- END DEBUG ---
    global FONT_FAMILY_NAME; loaded_font_family = None
    if font_id_reg != -1:
        family_names = QFontDatabase.applicationFontFamilies(font_id_reg)
        if family_names: loaded_font_family = family_names[0]; print(f"Successfully loaded custom font family: '{loaded_font_family}' from ID {font_id_reg}")
        else: print(f"Warning: Font ID {font_id_reg} loaded, but no family names found for {FONT_REGULAR}.")
    else:
        print(f"Warning: Failed to load font {FONT_REGULAR} (ID: {font_id_reg}).")
        if font_id_ital == -1:
            print(f"Warning: Failed to load font {FONT_ITALIC} (ID: {font_id_ital}).")
        if font_id_boldital == -1:
            print(f"Warning: Failed to load font {FONT_BOLDITALIC} (ID: {font_id_boldital}).")

    if loaded_font_family:
        FONT_FAMILY_NAME = loaded_font_family
        app_instance.setFont(QFont(FONT_FAMILY_NAME, BASE_FONT_SIZE))
        print(f"Application font set to '{FONT_FAMILY_NAME}'")
    else:
        print("Warning: Using system default font.")
        FONT_FAMILY_NAME = app_instance.font().family()

    app_instance.setStyleSheet(DARK_STYLESHEET)
    if not os.path.exists(INFO_FOLDER):
        try:
            os.makedirs(INFO_FOLDER); print(f"Created info folder: '{INFO_FOLDER}'")
            for filename in INFO_FILES.values():
                filepath = os.path.join(INFO_FOLDER, filename)
                if not os.path.exists(filepath):
                    with open(filepath, 'w', encoding='utf-8') as f: f.write(f"# {filename.replace('.txt','').replace('_',' ').title()}\n\nContent coming soon...")
                    print(f"Created placeholder file: {filepath}")
        except Exception as e: print(f"Warning: Could not create info folder or placeholder files: {e}")
    all_data = load_character_data(CHARACTER_DATA_FOLDER)
    if all_data: main_window = MainWindow(all_data, target_screen, fullscreen); main_window.show(); return main_window # Show the window here
    else: msg_box = QMessageBox(); msg_box.setIcon(QMessageBox.Critical); msg_box.setWindowTitle("Data Load Error"); msg_box.setText(f"Fatal Error: Failed to load data from '{CHARACTER_DATA_FOLDER}' folder."); msg_box.setInformativeText("App cannot start. Ensure folder exists and contains valid JSON files."); msg_box.setStyleSheet("QMessageBox {{ background-color: #444; color: #EEE; }} QLabel {{ color: #EEE; }} QPushButton {{ background-color: #666; color: #EEE; border: 1px solid #888; padding: 5px; }}"); msg_box.exec(); raise RuntimeError("Failed to load character data.")