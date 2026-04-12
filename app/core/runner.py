import os
import selectors
import subprocess
import time
from typing import List, Optional

from PyQt6.QtCore import QThread, pyqtSignal

from app.core.validator import SimulationConfig
from app.utils.logger import AppLogger

GRACEFUL_SHUTDOWN_TIMEOUT: float = 2.0
OVERRIDE_FLAG_TEMPLATE: str = "-override=startTime={start},stopTime={stop}"
RESULT_FILE_SUFFIX: str = "_res.mat"


class SimulationRunner(QThread):
    output: pyqtSignal = pyqtSignal(str)
    error: pyqtSignal = pyqtSignal(str)
    finished: pyqtSignal = pyqtSignal(int)

    def __init__(self, config: SimulationConfig) -> None:
        super().__init__()
        self._config = config
        self._process: Optional[subprocess.Popen] = None
        self._aborted: bool = False
        self._logger = AppLogger.get_instance()

    def run(self) -> None:
        cmd: List[str] = self._build_command()
        self._logger.info("Subprocess command: %s", " ".join(cmd))

        exe_dir: str = os.path.dirname(os.path.abspath(self._config.exe_path))

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                cwd=exe_dir,
            )
        except OSError as exc:
            self.error.emit(f"Failed to launch executable: {exc}")
            self._logger.error("Failed to launch executable: %s", exc)
            self.finished.emit(1)
            return

        self._stream_output()
        exit_code = self._process.wait()
        self._logger.info("Process exited with code %d.", exit_code)
        self.finished.emit(exit_code)

    def abort(self) -> None:
        self._aborted = True
        if self._process is None:
            return

        self._logger.warning(
            "Aborting simulation process (PID %d).", self._process.pid
        )
        self._process.terminate()

        deadline = time.monotonic() + GRACEFUL_SHUTDOWN_TIMEOUT
        while time.monotonic() < deadline:
            if self._process.poll() is not None:
                return
            time.sleep(0.1)

        if self._process.poll() is None:
            self._logger.warning(
                "Process did not terminate gracefully; sending SIGKILL."
            )
            self._process.kill()

    def _build_command(self) -> List[str]:
        override_flag = OVERRIDE_FLAG_TEMPLATE.format(
            start=self._config.start_time,
            stop=self._config.stop_time,
        )
        return [self._config.exe_path, override_flag]

    def _stream_output(self) -> None:
        if self._process is None:
            return

        stdout = self._process.stdout
        stderr = self._process.stderr

        if stdout is None or stderr is None:
            return

        sel = selectors.DefaultSelector()
        try:
            sel.register(stdout, selectors.EVENT_READ, data="stdout")
            sel.register(stderr, selectors.EVENT_READ, data="stderr")

            open_fds = 2
            while open_fds > 0 and not self._aborted:
                events = sel.select(timeout=0.1)
                for key, _ in events:
                    line = key.fileobj.readline()  # type: ignore[union-attr]
                    if line:
                        stripped = line.rstrip("\n")
                        if key.data == "stdout":
                            self.output.emit(stripped)
                        else:
                            self.error.emit(stripped)
                    else:
                        sel.unregister(key.fileobj)
                        open_fds -= 1

        except Exception as exc:
            self._logger.exception(
                "selectors-based stream reading failed (%s: %s); "
                "falling back to sequential drain.",
                type(exc).__name__,
                exc,
            )
            for line in stdout:
                self.output.emit(line.rstrip("\n"))
            for line in stderr:
                self.error.emit(line.rstrip("\n"))

        finally:
            sel.close()