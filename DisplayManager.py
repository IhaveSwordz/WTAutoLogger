# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, Signal, QThreadPool, QRunnable, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHeaderView, QLabel,
                               QMainWindow, QSizePolicy, QTabWidget, QTableView,
                               QWidget, QTableWidget, QTableWidgetItem)

from DataCollectorManager import Main
import sys
import traceback


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow: QMainWindow, signals):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.signals = signals
        MainWindow.resize(1000, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1000, 500))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.enableDisable = QCheckBox(self.tab)
        self.enableDisable.setObjectName(u"enableDisable")
        self.enableDisable.setGeometry(QRect(10, 0, 94, 16))
        self.Squad1Tag = QLabel(self.tab)
        self.Squad1Tag.setObjectName(u"Squad1Tag")
        self.Squad1Tag.setGeometry(QRect(230, 30, 80, 16))
        self.Squad2Tag = QLabel(self.tab)
        self.Squad2Tag.setObjectName(u"Squad2Tag")
        self.Squad2Tag.setGeometry(QRect(730, 30, 80, 16))

        self.Squad1 = QTableWidget(self.tab)
        self.Squad1.setObjectName(u"Squad1")
        self.Squad1.setGeometry(QRect(0, 70, 500, 430))

        self.Squad2 = QTableWidget(self.tab)
        self.Squad2.setObjectName(u"Squad2")
        self.Squad2.setGeometry(QRect(500, 70, 500, 430))

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.enableDisable.stateChanged.connect(self.sendData)
        self.signals.logs.connect(self.updateBattleData)

        self.threadpool = QThreadPool()

        worker = Main(self.signals)  # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

        red = QColor.fromRgb(255, 0, 0)
        blue = QColor.fromRgb(0, 255, 0)

        self.Squad1.setRowCount(8)
        self.Squad1.setColumnCount(4)
        self.Squad1.setHorizontalHeaderLabels(["name", "vehicle", "State", "kills"])
        self.Squad1.setVerticalHeaderLabels(
            ["Player 1", "Player 2", "Player 3", "Player 4", "Player 5", "Player 6", "Player 7", "Player 8"])
        for x in range(4):
            for y in range(8):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.Squad1.setItem(y, x, item)

        self.Squad2.setRowCount(8)
        self.Squad2.setColumnCount(4)
        # self.Squad2.
        self.Squad2.setHorizontalHeaderLabels(["Name", "Vehicle", "State", "Kills"])
        self.Squad2.setVerticalHeaderLabels(
            ["Player 9", "Player 10", "Player 11", "Player 12", "Player 13", "Player 14", "Player 15", "Player 16"])
        for x in range(4):
            for y in range(8):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable)
                self.Squad2.setItem(y, x, item)

        self.retranslateUi(MainWindow)
        # print(MainWindow.resizeEvent(self.test))
        # MainWindow.iconSizeChanged.connect(self.test)

        self.tabWidget.setCurrentIndex(0)
        # self.centralwidget.destroyed.connect(self.sendData)
        # MainWindow.destroyed.connect(self.sendData)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.enableDisable.setText(QCoreApplication.translate("MainWindow", u"Turn On/Off Logger", None))
        self.Squad1Tag.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.Squad2Tag.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  QCoreApplication.translate("MainWindow", u"Battle", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QCoreApplication.translate("MainWindow", u"PlayerSearch", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  QCoreApplication.translate("MainWindow", u"Vehicle Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  QCoreApplication.translate("MainWindow", u"Squadron Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5),
                                  QCoreApplication.translate("MainWindow", u"Settings", None))

    # retranslateUi

    def test(self, dat):
        print(dat)

    def sendData(self, data: int):
        self.signals.data.emit(data)

    '''
            "team1Tag": self.Tags[0],
            "team1Players": self.team1,
            "team2Tag": self.Tags[1],
            "team2Players": self.team2
    '''
    def updateBattleData(self, data: dict):
        # add tags
        self.Squad1Tag.setText(data["team1Tag"])
        self.Squad2Tag.setText(data["team2Tag"])
        print(data["team1Players"])
        print(data["team2Players"])
        bold = f"<html><head/><body><p><span style=\" font-weight:700;\">Alive/span></p></body></html>"
        for y, player in enumerate(data["team1Players"]):
            # add kills
            for x, val in enumerate([player.name, player.vehicle[1:-1], player.dead]):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable)
                if player.name == "":
                    player.dead = ""
                elif type(val) is bool:
                    val = "ALive" if val is True else "Dead"
                item.setText(str(val))
                self.Squad1.setItem(y, x, item)

        for y, player in enumerate(data["team2Players"]):
            # add kills
            for x, val in enumerate([player.name, player.vehicle[1:-1], player.dead]):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable)
                if player.name == "":
                    player.dead = ""
                elif type(val) is bool:
                    val = "Alive" if val is True else "Dead"
                item.setText(str(val))
                self.Squad2.setItem(y, x, item)


