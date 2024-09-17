from PySide6.QtWidgets import QWidget, QTextBrowser

'''
this file will purely handle the settings and documentation for users of SQBDotEXE

'''


class LoggingDisplay(QWidget):
    def __init__(self, ):
        super().__init__()
        self.name = "Settings"


class DebugDisplay(QTextBrowser):
    def __init__(self, parent):
        super().__init__(parent)
