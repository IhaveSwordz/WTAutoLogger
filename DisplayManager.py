# -*- coding: utf-8 -*-
import time

import PySide6.QtGui
################################################################################
# Form generated from reading UI file 'mainwindow.ui'
#
# Created by: Qt User Interface Compiler version 6.7.2
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, Signal, QThreadPool, QRunnable, Slot)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform, QRawFont, QTextCharFormat)
from PySide6.QtWidgets import (QApplication, QCheckBox, QHeaderView, QLabel,
                               QMainWindow, QSizePolicy, QTabWidget, QTableView,
                               QWidget, QTableWidget, QTableWidgetItem, QTextBrowser, QLineEdit, QPushButton)

from DataCollectorManager import Main
import PySide6.QtGui as qtg
import sys
import traceback
from converter import Vehicle, DataGet
from DatabaseManager import PlayerQuery


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow: QMainWindow, signals):
        self.converter = DataGet()
        self.dataLookup = PlayerQuery()
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.signals = signals
        MainWindow.resize(1000, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1000, 600))
        self.tab = QWidget()

        self.threadpool = QThreadPool()
        self.lookup_thread_pool = QThreadPool()

        '''
        PAGE 1: 
        '''
        worker = Main(self.signals)  # Any other args, kwargs are passed to the run function

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
        self.Squad1.setGeometry(QRect(0, 70, 500, 330))

        self.Squad2 = QTableWidget(self.tab)
        self.Squad2.setObjectName(u"Squad2")
        self.Squad2.setGeometry(QRect(500, 70, 500, 330))

        self.enableDisable.stateChanged.connect(self.sendData)
        self.signals.logs.connect(self.updateBattleData)

        # textboxSize = lambda x, y: QRect(x, y, 500, 100)
        self.T1Vehicles = QLabel(self.tab)
        self.T1Vehicles.setObjectName("T1Vehicles")
        self.T1Vehicles.setGeometry(QRect(0, 400, 500, 25))
        self.T1Vehicles.setText("Nations: ")

        self.T1Nations = QLabel(self.tab)
        self.T1Nations.setObjectName("T1Nations")
        self.T1Nations.setGeometry(QRect(0, 425, 500, 25))
        self.T1Nations.setText("Vehicle Types: ")

        self.T2Vehicles = QLabel(self.tab)
        self.T2Vehicles.setObjectName("T2Vehicles")
        self.T2Vehicles.setGeometry(QRect(500, 400, 500, 25))
        self.T2Vehicles.setText("Nations: ")

        self.T2Nations = QLabel(self.tab)
        self.T2Nations.setObjectName("T2Nations")
        self.T2Nations.setGeometry(QRect(500, 425, 500, 25))
        self.T2Nations.setText("Vehicle Types: ")
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
        self.tabWidget.addTab(self.tab, "")
        '''
        tab 2
        '''

        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.NameEnterBox = QLineEdit(self.tab_2)
        self.NameEnterBox.setGeometry(QRect(15, 15, 175, 25))
        self.ActiveLookupName = QPushButton(self.tab_2)
        self.ActiveLookupName.setText("Lookup")
        self.ActiveLookupName.setGeometry(QRect(190, 15, 75, 25))
        self.ActiveLookupName.clicked.connect(self.player_lookup)
        self.signals.PlayerSignal.connect(self.player_update)
        # self.signals.caller.connect(self.doLookup(None, None))

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
        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)

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

    def player_lookup(self):
        self.create_lookup_thread(self.signals.PlayerSignal, self.dataLookup.playerLookup, self.NameEnterBox.text())

    def vehicle_lookup(self):
        self.create_lookup_thread(self.signals.VehicleSignal, self.dataLookup.vehicleLookup, None)

    def squadron_lookup(self):
        self.create_lookup_thread(self.signals.SquadronSignal, self.dataLookup.squadLookup, None)

    '''
    called by signal PLayerSignal. this signal provides data about a specific player in format
    '''
    def player_update(self, data):
        print(data)
        print("player update called")

    def create_lookup_thread(self, signal: Signal, func, data):
        if self.lookup_thread_pool.activeThreadCount() < 1:
            lookup_worker = LookupThread(func, signal, data)
            self.lookup_thread_pool.start(lookup_worker)
        else:
            print("bad boy")


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
        font = qtg.QFont()
        font.setBold(True)
        font.setPixelSize(16)
        t1: list = data["team1Players"]
        t2: list = data["team2Players"]
        for y, player in enumerate(data["team1Players"]):
            # add kills
            for x, val in enumerate([player.name, player.vehicle[1:-1], player.dead, player.kills]):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable)
                if player.badPlayer:
                    val = ""
                elif type(val) is bool:
                    if val is True:
                        item.setFont(font)
                    val = "ALive" if val is True else "Dead"

                if x == 3:
                    indexes = []
                    for kill in val:
                        if kill in t1:
                            indexes.append(t1.index(kill) + 1)
                        elif kill in t2:
                            indexes.append(t2.index(kill) + 9)
                        else:
                            indexes.append(17)
                    val = ', '.join([str(z) for z in indexes])
                item.setText(str(val))
                self.Squad1.setItem(y, x, item)

        for y, player in enumerate(data["team2Players"]):
            # add kills
            for x, val in enumerate([player.name, player.vehicle[1:-1], player.dead, player.kills]):
                item = QTableWidgetItem()
                item.setFlags(Qt.ItemFlag.ItemIsEditable)
                if player.badPlayer:
                    val = ""
                elif type(val) is bool:
                    if val is True:
                        item.setFont(font)
                    val = "ALive" if val is True else "Dead"
                if x == 3:
                    indexes = []
                    for kill in val:
                        if kill in t1:
                            indexes.append(t1.index(kill) + 1)
                        elif kill in t2:
                            indexes.append(t2.index(kill) + 9)
                        else:
                            indexes.append(17)
                    val = ', '.join([str(z) for z in indexes])

                item.setText(str(val))
                self.Squad2.setItem(y, x, item)
        t1_Nations = {}
        t1_Vehicles = {}
        t2_Nations = {}
        t2_Vehicles = {}

        for player in t1:
            if player.badPlayer:
                continue
            vehicle = player.vehicle
            if vehicle is not None or vehicle != "":
                internal = self.converter.query_name(vehicle[1:-1])
                v = Vehicle(vehicle, internal[0:-2])
                if t1_Nations.get(v.country) is None:
                    t1_Nations.update({v.country: 1})
                else:
                    t1_Nations[v.country] += 1
        print("team 1:")
        print(t1_Nations)
        for player in t2:
            if player.badPlayer:
                continue
            vehicle = player.vehicle
            if vehicle is not None or vehicle != "":
                internal = self.converter.query_name(vehicle[1:-1])
                # print(internal)
                v = Vehicle(vehicle, internal[0:-2])
                if t2_Nations.get(v.country) is None:
                    t2_Nations.update({v.country: 1})
                else:
                    t2_Nations[v.country] += 1
        print("team 2:")
        print(t2_Nations)
        self.T1Vehicles.setText(f"Nations: {', '.join([nat for nat in list(t1_Nations.keys())])}")
        self.T2Vehicles.setText(f"Nations: {', '.join([nat for nat in list(t2_Nations.keys())])}")


class LookupThread(QRunnable):
    def __init__(self, fn, signal, data, *args, **kwargs):
        super(LookupThread, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.data = data
        self.args = args
        self.kwargs = kwargs
        self.signal: Signal = signal

    @Slot()
    def run(self):
        output = self.fn(self.data, self.signal)
        # print(output)
