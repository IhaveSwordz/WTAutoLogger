import sys
import PySide6.QtGui
from PySide6.QtWidgets import QMainWindow, QApplication, QTabWidget
from PySide6.QtWidgets import QStyle
import traceback

from src.DebugLogger import Debug
Debug.logger.enable_filing()
try:
    from src.signals import Signals
    from src.UI.DisplayMain import Ui_MainWindow
    from src.DataManager.DataCollectorHandler import DataCollectorHandler
    from src.DataManager.DatabaseManager import Manager
except Exception as e:
    Debug.logger.log("Error", f"Unhandled Exception!: {e}")
    Debug.logger.special_log(traceback.format_exc())
    sys.exit(999)


class MainWindow(QMainWindow):
    def __init__(self):
        # this is done to force the init to run and create and initialize data.DB
        m = Manager()
        del m
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow(self)
        self.collector = DataCollectorHandler()

    def closeEvent(self, event):
        Signals.signals.data.emit(5)
        event.accept()

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent):
        Signals.signals.sizeSignal.emit(event.size().width(), event.size().height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    # app.setStyle()
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


