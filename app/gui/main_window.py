import os
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.core.runner import RESULT_FILE_SUFFIX, SimulationRunner
from app.core.validator import InputValidator, ValidationError
from app.gui.styles import MAIN_STYLESHEET
from app.gui.widgets import HeaderBanner, LogPanel, PathSelectorWidget, SectionCard
from app.utils.logger import AppLogger

WINDOW_MIN_WIDTH = 720
WINDOW_MIN_HEIGHT = 620
WINDOW_TITLE = "OpenModelica Simulation Launcher"


START_MIN, START_MAX, START_DEFAULT = 0, 4, 0
STOP_MIN, STOP_MAX, STOP_DEFAULT = 1, 4, 4


class MainWindow(QMainWindow):
    
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._logger = AppLogger.get_instance()
        self._runner: Optional[SimulationRunner] = None

        self.setWindowTitle(WINDOW_TITLE)
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.setStyleSheet(MAIN_STYLESHEET)

        self._build_ui()
        self._set_ready_state()

    def _build_ui(self) -> None:
        outer = QWidget()
        outer.setObjectName("outer_bg")
        self.setCentralWidget(outer)

        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(20, 20, 20, 0)
        outer_layout.setSpacing(0)

        card = QFrame()
        card.setObjectName("main_card")
        card.setFrameShape(QFrame.Shape.StyledPanel)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 16)
        card_layout.setSpacing(16)

        card_layout.addWidget(self._build_header())
        card_layout.addWidget(self._build_config_section())
        card_layout.addWidget(self._build_progress_bar())
        card_layout.addLayout(self._build_button_row())
        card_layout.addWidget(self._build_log_panel(), stretch=1)

        outer_layout.addWidget(card)

        self.setStatusBar(self._build_status_bar())

    def _build_header(self) -> HeaderBanner:
        return HeaderBanner()

    def _build_config_section(self) -> SectionCard:
        card = SectionCard()
        inner = card.inner_layout()

        heading = QLabel("SIMULATION CONFIGURATION")
        heading.setObjectName("section_label")
        inner.addWidget(heading)

        form = QFormLayout()
        form.setLabelAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        form.setHorizontalSpacing(16)
        form.setVerticalSpacing(10)
        form.setContentsMargins(0, 4, 0, 0)

        self._path_selector = PathSelectorWidget()
        form.addRow(self._make_field_label("Executable Path"), self._path_selector)

        self._start_spin, start_row = self._make_spin_row(
            START_MIN, START_MAX, START_DEFAULT,
            "Start time (s). Must satisfy: 0 ≤ startTime < stopTime < 5."
        )
        form.addRow(self._make_field_label("Start Time (s)"), start_row)

        self._stop_spin, stop_row = self._make_spin_row(
            STOP_MIN, STOP_MAX, STOP_DEFAULT,
            "Stop time (s). Must satisfy: 0 ≤ startTime < stopTime < 5."
        )
        form.addRow(self._make_field_label("Stop Time (s)"), stop_row)

        inner.addLayout(form)
        return card

    def _make_field_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("field_label")
        return lbl

    def _make_spin_row(
        self, min_val: int, max_val: int, default: int, tooltip: str
    ):
        minus = QPushButton("−")
        minus.setObjectName("spin_btn")
        minus.setFixedSize(44, 44)
        minus.setToolTip("Decrease")

        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spin.setToolTip(tooltip)

        plus = QPushButton("+")
        plus.setObjectName("spin_btn")
        plus.setFixedSize(44, 44)
        plus.setToolTip("Increase")

        minus.clicked.connect(spin.stepDown)
        plus.clicked.connect(spin.stepUp)

        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        row.addWidget(minus)
        row.addWidget(spin)
        row.addWidget(plus)
        row.addStretch()

        return spin, row

    def _build_progress_bar(self) -> QProgressBar:
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 0)
        self._progress_bar.setFixedHeight(6)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.hide()
        return self._progress_bar

    def _build_button_row(self) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(10)

        self._run_btn = QPushButton("▶  Run Simulation")
        self._run_btn.setObjectName("run_btn")
        self._run_btn.setToolTip(
            "Launch the simulation with the given start/stop times.\n"
            "Passes: -override=startTime=X,stopTime=Y"
        )
        self._run_btn.clicked.connect(self._on_run_clicked)

        self._stop_btn = QPushButton("■  Stop")
        self._stop_btn.setObjectName("stop_btn")
        self._stop_btn.setToolTip("Terminate the running simulation")
        self._stop_btn.setEnabled(False)
        self._stop_btn.clicked.connect(self._on_stop_clicked)

        row.addWidget(self._run_btn, stretch=1)
        row.addWidget(self._stop_btn)
        return row

    def _build_log_panel(self) -> LogPanel:
        self._log_panel = LogPanel()
        return self._log_panel

    def _build_status_bar(self) -> QStatusBar:
        self._status_bar = QStatusBar()
        self.setStatusBar(self._status_bar)
        return self._status_bar

    

    def _set_ready_state(self) -> None:
        self._run_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._progress_bar.hide()
        self._log_panel.set_running(False)
        self._status_bar.showMessage("Ready")

    def _set_running_state(self) -> None:
        self._run_btn.setEnabled(False)
        self._stop_btn.setEnabled(True)
        self._progress_bar.show()
        self._log_panel.set_running(True)
        self._status_bar.showMessage("Running…")

    def _set_finished_state(self, exit_code: int) -> None:
        self._run_btn.setEnabled(True)
        self._stop_btn.setEnabled(False)
        self._progress_bar.hide()
        self._log_panel.set_running(False)
        label = "Finished" if exit_code == 0 else "Failed"
        self._status_bar.showMessage(f"{label} (exit {exit_code})")

    def _on_run_clicked(self) -> None:
        exe = self._path_selector.path()
        start = self._start_spin.value()
        stop = self._stop_spin.value()

        try:
            config = InputValidator.validate(exe, start, stop)
        except ValidationError as exc:
            self._show_error("Validation Error", str(exc))
            self._logger.warning("Validation failed: %s", exc)
            return

        self._log_panel.append_info(
            f"Starting: {config.exe_path}  "
            f"startTime={config.start_time}  stopTime={config.stop_time}"
        )
        self._logger.info(
            "Launching: %s -override=startTime=%d,stopTime=%d",
            config.exe_path, config.start_time, config.stop_time,
        )

        self._runner = SimulationRunner(config)
        self._runner.output.connect(self._on_output)
        self._runner.error.connect(self._on_error)
        self._runner.finished.connect(self._on_finished)
        self._set_running_state()
        self._runner.start()

    def _on_stop_clicked(self) -> None:
        if self._runner and self._runner.isRunning():
            self._log_panel.append_stderr("User requested abort — terminating…")
            self._logger.warning("User aborted simulation.")
            self._runner.abort()
        self._set_ready_state()
        self._status_bar.showMessage("Aborted by user")

    def _on_output(self, line: str) -> None:
        self._log_panel.append_stdout(line)

    def _on_error(self, line: str) -> None:
        self._log_panel.append_stderr(line)

    def _on_finished(self, exit_code: int) -> None:
        self._set_finished_state(exit_code)
        if exit_code == 0:
            self._log_panel.append_success(
                f"Simulation finished successfully (exit {exit_code})."
            )
            exe = self._path_selector.path()
            exe_dir = os.path.dirname(os.path.abspath(exe))
            exe_name = os.path.splitext(os.path.basename(exe))[0]
            result = os.path.join(exe_dir, f"{exe_name}{RESULT_FILE_SUFFIX}")
            if os.path.isfile(result):
                self._log_panel.append_success(f"Output saved to: {result}")
            else:
                self._log_panel.append_info(f"Expected output file: {result}")
            self._logger.info("Simulation done (exit %d).", exit_code)
        else:
            self._log_panel.append_stderr(
                f"Simulation exited with non-zero code: {exit_code}."
            )
            self._logger.error("Simulation failed (exit %d).", exit_code)

    def _show_error(self, title: str, message: str) -> None:
        box = QMessageBox(self)
        box.setWindowTitle(title)
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.setStandardButtons(QMessageBox.StandardButton.Ok)
        box.exec()
