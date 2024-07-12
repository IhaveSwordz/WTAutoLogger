import sys
from PySide6.QtCore import QFile
from DisplayManager import Ui_MainWindow
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget, QMainWindow, QApplication
from PySide6.QtCore import QTimer, QRunnable, Slot, Signal, QObject, QThreadPool


class WorkerSignals(QObject):
    # from bot
    finished = Signal()
    error = Signal(tuple)
    progress = Signal(int)
    logs = Signal(dict)

    # to bot
    data = Signal(int)


class MainWindow(QMainWindow):
    def __init__(self):
        self.signals = WorkerSignals()
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, self.signals)

    def closeEvent(self, event):
        self.signals.data.emit(5)
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
