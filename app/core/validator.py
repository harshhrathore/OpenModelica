import os
import platform
from dataclasses import dataclass


class ValidationError(ValueError):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


@dataclass
class SimulationConfig:
    exe_path: str
    start_time: int
    stop_time: int


TIME_MIN: int = 0
TIME_MAX_EXCLUSIVE: int = 5


class InputValidator:
    @staticmethod
    def validate(
        exe_path: str,
        start_time: int,
        stop_time: int,
    ) -> SimulationConfig:
        InputValidator._validate_exe_path(exe_path)
        InputValidator._validate_times(start_time, stop_time)
        return SimulationConfig(
            exe_path=exe_path,
            start_time=start_time,
            stop_time=stop_time,
        )

    @staticmethod
    def _validate_exe_path(exe_path: str) -> None:
        if not exe_path:
            raise ValidationError(
                "Executable path is empty.\n"
                "Please select or enter the path to the compiled simulation executable."
            )

        if not os.path.isfile(exe_path):
            raise ValidationError(
                f"Executable not found:\n{exe_path}\n\n"
                "Make sure the file exists and the path is correct."
            )

        if platform.system() != "Windows":
            if not os.access(exe_path, os.X_OK):
                raise ValidationError(
                    f"The file is not executable:\n{exe_path}\n\n"
                    "Run:  chmod +x <path>  to grant execute permission."
                )

    @staticmethod
    def _validate_times(start_time: int, stop_time: int) -> None:
        if start_time < TIME_MIN:
            raise ValidationError(
                f"Start time must be >= {TIME_MIN}. Got: {start_time}."
            )

        if stop_time >= TIME_MAX_EXCLUSIVE:
            raise ValidationError(
                f"Stop time must be < {TIME_MAX_EXCLUSIVE}. Got: {stop_time}."
            )

        if start_time >= stop_time:
            raise ValidationError(
                f"Start time ({start_time}) must be strictly less than "
                f"stop time ({stop_time}).\n"
                "Constraint: 0 <= startTime < stopTime < 5."
            )
