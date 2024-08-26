import sys

import PySide6.QtGui
from src.Old.DisplayManager import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Signal, QObject


class WorkerSignals(QObject):
    # from bot
    finished = Signal()
    error = Signal(tuple)
    progress = Signal(int)
    logs = Signal(dict)

    # to bot
    data = Signal(int)

    #From data fetcher
    dataSignal = Signal(list)
    SquadronSignal = Signal(list)

    #resizing
    # list containing size change
    sizeSignal = Signal(list)


class MainWindow(QMainWindow):
    def __init__(self):
        self.signals = WorkerSignals()
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, self.signals)

    def closeEvent(self, event):
        self.signals.data.emit(5)
        event.accept()

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent):
        self.signals.sizeSignal.emit([event.size().width(), event.size().height()])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
