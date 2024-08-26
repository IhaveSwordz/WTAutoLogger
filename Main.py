import sys
import os
import PySide6.QtGui
from PySide6.QtWidgets import QMainWindow, QApplication, QTabWidget

from src.signals import Signals
from src.UI.DisplayMain import Ui_MainWindow
from src.DataManager.DataCollectorHandler import DataCollectorHandler


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow(self)
        self.collector = DataCollectorHandler()

    def closeEvent(self, event):
        Signals.signals.data.emit(5)
        event.accept()

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent):
        Signals.signals.sizeSignal.emit(event.size().width(), event.size().height())




if __name__ == "__main__":
    os.environ["WRITE_PATH_OUTPUT"] = "src/Output"

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


