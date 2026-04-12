BG_COLOR = "#E8EAF0"
SURFACE_COLOR = "#FFFFFF"
PANEL_BG = "#F9FAFB"
INPUT_BG = "#FFFFFF"

ACCENT_COLOR = "#6C63FF"
ACCENT_HOVER_COLOR = "#5A52E0"
ACCENT_PRESSED_COLOR = "#4A43C8"

RUN_COLOR = "#22C55E"
RUN_HOVER_COLOR = "#16A34A"
RUN_PRESSED_COLOR = "#15803D"

STOP_COLOR = "#EF4444"
STOP_HOVER_COLOR = "#DC2626"
STOP_PRESSED_COLOR = "#B91C1C"

TEXT_PRIMARY = "#1A1D23"
TEXT_SECONDARY = "#374151"
TEXT_MUTED = "#6B7280"
TEXT_HINT = "#9CA3AF"

BORDER_COLOR = "#D1D5DB"
BORDER_LIGHT = "#E2E6ED"

SUCCESS_COLOR = "#16A34A"
ERROR_COLOR = "#EF4444"
INFO_COLOR = "#6C63FF"
STDOUT_COLOR = "#1E293B"
TIMESTAMP_COLOR = "#9CA3AF"

PROGRESS_BG = "#E5E7EB"
PROGRESS_FILL = "#6C63FF"

FONT_FAMILY = '"Segoe UI", "Helvetica Neue", Arial, sans-serif'
MONO_FONT = '"Consolas", "Courier New", monospace'

MAIN_STYLESHEET = f"""
QMainWindow {{
    background-color: {BG_COLOR};
}}
QWidget {{
    font-family: {FONT_FAMILY};
    font-size: 13px;
    color: {TEXT_PRIMARY};
    background-color: transparent;
}}

QWidget#outer_bg {{
    background-color: {BG_COLOR};
}}

QFrame#main_card {{
    background-color: {SURFACE_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: 12px;
}}

QFrame#config_card {{
    background-color: {PANEL_BG};
    border: 1px solid {BORDER_LIGHT};
    border-radius: 10px;
}}

QLabel#app_title {{
    font-size: 18px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
}}
QLabel#app_subtitle {{
    font-size: 13px;
    color: {TEXT_MUTED};
}}
QLabel#section_label {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_HINT};
    letter-spacing: 1px;
}}
QLabel#field_label {{
    font-size: 14px;
    font-weight: 500;
    color: {TEXT_SECONDARY};
}}
QLabel#logs_tab_label {{
    font-size: 13px;
    font-weight: 700;
    color: {TEXT_PRIMARY};
    padding: 10px 18px 8px 18px;
    border-bottom: 2px solid {ACCENT_COLOR};
}}
QLabel#section_output_label {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_HINT};
    letter-spacing: 1px;
}}

QLineEdit {{
    background-color: {INPUT_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: {ACCENT_COLOR};
    selection-color: white;
}}
QLineEdit:focus {{
    border: 2px solid {ACCENT_COLOR};
}}

QSpinBox {{
    background-color: {INPUT_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 7px 6px;
    font-size: 14px;
    font-weight: 600;
    min-width: 50px;
    max-width: 50px;
}}
QSpinBox:focus {{
    border: 2px solid {ACCENT_COLOR};
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 0; height: 0;
}}

QPushButton#spin_btn {{
    background-color: {INPUT_BG};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    font-size: 18px;
    font-weight: 300;
    padding: 0px;
}}
QPushButton#spin_btn:hover {{
    background-color: {BORDER_LIGHT};
}}
QPushButton#spin_btn:pressed {{
    background-color: {BORDER_COLOR};
}}

QPushButton#browse_btn {{
    background-color: {ACCENT_COLOR};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 600;
    min-width: 90px;
}}
QPushButton#browse_btn:hover {{
    background-color: {ACCENT_HOVER_COLOR};
}}
QPushButton#browse_btn:pressed {{
    background-color: {ACCENT_PRESSED_COLOR};
}}

QProgressBar {{
    background-color: {PROGRESS_BG};
    border: none;
    border-radius: 3px;
}}
QProgressBar::chunk {{
    background-color: {PROGRESS_FILL};
    border-radius: 3px;
}}

QPushButton#run_btn {{
    background-color: {RUN_COLOR};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 0;
    font-size: 14px;
    font-weight: 700;
}}
QPushButton#run_btn:hover {{
    background-color: {RUN_HOVER_COLOR};
}}
QPushButton#run_btn:pressed {{
    background-color: {RUN_PRESSED_COLOR};
}}
QPushButton#run_btn:disabled {{
    background-color: {BORDER_COLOR};
    color: {TEXT_HINT};
}}

QPushButton#stop_btn {{
    background-color: {SURFACE_COLOR};
    color: {TEXT_SECONDARY};
    border: 1px solid {BORDER_COLOR};
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 14px;
    font-weight: 600;
    min-width: 100px;
}}
QPushButton#stop_btn:hover {{
    background-color: {STOP_COLOR};
    color: white;
    border-color: {STOP_COLOR};
}}
QPushButton#stop_btn:pressed {{
    background-color: {STOP_PRESSED_COLOR};
    color: white;
}}
QPushButton#stop_btn:disabled {{
    color: {TEXT_HINT};
    border-color: {BORDER_LIGHT};
    background-color: {SURFACE_COLOR};
}}

QFrame#log_container {{
    background-color: {SURFACE_COLOR};
    border: 1px solid {BORDER_LIGHT};
    border-radius: 10px;
}}
QWidget#log_header {{
    background-color: {PANEL_BG};
    border-bottom: 1px solid {BORDER_LIGHT};
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
}}
QPushButton#clear_btn {{
    background-color: transparent;
    color: {TEXT_MUTED};
    border: none;
    border-left: 1px solid {BORDER_LIGHT};
    border-radius: 0px;
    padding: 10px 16px;
    font-size: 13px;
}}
QPushButton#clear_btn:hover {{
    color: {TEXT_PRIMARY};
    background-color: {BORDER_LIGHT};
}}
QTextEdit#log_text {{
    background-color: {SURFACE_COLOR};
    color: {STDOUT_COLOR};
    border: none;
    padding: 4px 16px 12px 16px;
    font-family: {MONO_FONT};
    font-size: 13px;
    selection-background-color: {ACCENT_COLOR};
    selection-color: white;
}}
QWidget#log_footer {{
    background-color: {PANEL_BG};
    border-top: 1px solid {BORDER_LIGHT};
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
}}

QStatusBar {{
    background-color: {SURFACE_COLOR};
    color: {TEXT_HINT};
    border-top: 1px solid {BORDER_LIGHT};
    font-size: 12px;
    padding: 4px 8px;
}}
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER_COLOR};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QToolTip {{
    background-color: {TEXT_PRIMARY};
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}}
QMessageBox {{ background-color: {SURFACE_COLOR}; }}
QMessageBox QLabel {{ color: {TEXT_PRIMARY}; font-size: 13px; }}
QMessageBox QPushButton {{
    background-color: {ACCENT_COLOR};
    color: white;
    border: none;
    border-radius: 8px;
    min-width: 80px;
    padding: 8px 18px;
    font-weight: 600;
}}
QMessageBox QPushButton:hover {{ background-color: {ACCENT_HOVER_COLOR}; }}
"""
