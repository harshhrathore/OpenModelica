import datetime
import os
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap, QTextCursor
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.gui.styles import (
    ERROR_COLOR,
    INFO_COLOR,
    PROGRESS_BG,
    PROGRESS_FILL,
    SUCCESS_COLOR,
    STDOUT_COLOR,
    TIMESTAMP_COLOR,
)

_LOGO_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "logo.png"
)


class HeaderBanner(QWidget):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        logo_lbl = QLabel()
        logo_lbl.setFixedSize(48, 48)
        if os.path.isfile(_LOGO_PATH):
            pix = QPixmap(_LOGO_PATH).scaled(
                48, 48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl.setPixmap(pix)
        else:
            logo_lbl.setText("🔬")
            logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_lbl.setStyleSheet("font-size: 28px; background: transparent;")

        text_col = QVBoxLayout()
        text_col.setContentsMargins(0, 0, 0, 0)
        text_col.setSpacing(3)

        title = QLabel("OpenModelica Simulation Launcher")
        title.setObjectName("app_title")

        subtitle = QLabel(
            "Execute compiled TwoConnectedTanks simulations "
            "with configurable parameters"
        )
        subtitle.setObjectName("app_subtitle")
        subtitle.setWordWrap(True)

        text_col.addWidget(title)
        text_col.addWidget(subtitle)

        layout.addWidget(logo_lbl)
        layout.addLayout(text_col, stretch=1)


class PathSelectorWidget(QWidget):

    def __init__(
        self,
        placeholder: str = "Select compiled executable...",
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self._build_ui(placeholder)

    def _build_ui(self, placeholder: str) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setToolTip(
            "Path to the compiled OpenModelica executable.\n"
            "Type manually or click Browse to pick a file."
        )

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setObjectName("browse_btn")
        self.browse_btn.setFixedWidth(96)
        self.browse_btn.setToolTip("Open a file picker to select the executable")
        self.browse_btn.clicked.connect(self._on_browse)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.browse_btn)

    def _on_browse(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select OpenModelica Executable",
            "",
            "Executables (*.exe *.bat *)",
        )
        if path:
            self.line_edit.setText(path)

    def path(self) -> str:
        return self.line_edit.text().strip()

    def set_path(self, path: str) -> None:
        self.line_edit.setText(path)


class SectionCard(QFrame):

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("config_card")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self._inner = QVBoxLayout(self)
        self._inner.setContentsMargins(20, 16, 20, 16)
        self._inner.setSpacing(12)

    def inner_layout(self) -> QVBoxLayout:
        return self._inner


class LogPanel(QFrame):

    _STDOUT_COLOR = STDOUT_COLOR
    _STDERR_COLOR = ERROR_COLOR
    _SUCCESS_COLOR = SUCCESS_COLOR
    _INFO_COLOR = INFO_COLOR
    _TIMESTAMP_COLOR = TIMESTAMP_COLOR

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setObjectName("log_container")
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget()
        header.setObjectName("log_header")
        header_row = QHBoxLayout(header)
        header_row.setContentsMargins(0, 0, 0, 0)
        header_row.setSpacing(0)

        logs_lbl = QLabel("Logs")
        logs_lbl.setObjectName("logs_tab_label")

        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.setToolTip("Clear all log output")
        self.clear_btn.clicked.connect(self.clear)

        header_row.addWidget(logs_lbl)
        header_row.addStretch()
        header_row.addWidget(self.clear_btn)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 14, 16, 10)
        body_layout.setSpacing(8)

        out_lbl = QLabel("SIMULATION OUTPUT")
        out_lbl.setObjectName("section_output_label")

        self.text_edit = QTextEdit()
        self.text_edit.setObjectName("log_text")
        self.text_edit.setReadOnly(True)
        self.text_edit.setMinimumHeight(150)
        self.text_edit.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        body_layout.addWidget(out_lbl)
        body_layout.addWidget(self.text_edit)

        footer = QWidget()
        footer.setObjectName("log_footer")
        footer.setFixedHeight(18)
        footer_row = QHBoxLayout(footer)
        footer_row.setContentsMargins(14, 5, 14, 5)

        self._progress = QProgressBar()
        self._progress.setRange(0, 0)
        self._progress.setFixedHeight(4)
        self._progress.setTextVisible(False)
        self._progress.setStyleSheet(
            f"QProgressBar {{ background: {PROGRESS_BG}; border: none; "
            f"border-radius: 2px; }}"
            f"QProgressBar::chunk {{ background: {PROGRESS_FILL}; "
            f"border-radius: 2px; }}"
        )
        self._progress.hide()
        footer_row.addWidget(self._progress)

        root.addWidget(header)
        root.addWidget(body, stretch=1)
        root.addWidget(footer)

    def set_running(self, running: bool) -> None:
        self._progress.setVisible(running)

    def append_stdout(self, text: str) -> None:
        self._append_colored(text, self._STDOUT_COLOR)

    def append_stderr(self, text: str) -> None:
        self._append_colored(text, self._STDERR_COLOR)

    def append_success(self, text: str) -> None:
        self._append_colored(text, self._SUCCESS_COLOR)

    def append_info(self, text: str) -> None:
        self._append_colored(text, self._INFO_COLOR)

    def clear(self) -> None:
        self.text_edit.clear()

    def _append_colored(self, text: str, hex_color: str) -> None:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        ts_fmt = cursor.charFormat()
        ts_fmt.setForeground(QColor(self._TIMESTAMP_COLOR))
        cursor.setCharFormat(ts_fmt)
        cursor.insertText(f"[{timestamp}]  ")

        msg_fmt = cursor.charFormat()
        msg_fmt.setForeground(QColor(hex_color))
        cursor.setCharFormat(msg_fmt)
        cursor.insertText(f"{text}\n")

        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
