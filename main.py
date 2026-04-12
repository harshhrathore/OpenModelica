import sys
from PyQt6.QtWidgets import QApplication
from app.gui.main_window import MainWindow
from app.utils.logger import AppLogger


def main() -> None:

    AppLogger.get_instance()
    app = QApplication(sys.argv)
    app.setApplicationName("OpenModelica Simulation Launcher")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
