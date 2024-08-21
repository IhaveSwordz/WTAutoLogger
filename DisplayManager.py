# -*- coding: utf-8 -*-
import collections
import time

from multiprocessing.dummy import Pool as ThreadPool
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
                               QWidget, QTableWidget, QTableWidgetItem, QTextBrowser, QLineEdit, QPushButton,
                               QListWidget, QListView, QListWidgetItem)

from DataCollectorManager import Main
import PySide6.QtGui as qtg
import sys
import traceback
from converter import Vehicle, DataGet
from DatabaseManager import PlayerQuery
from rapidfuzz import process
from multiprocessing.dummy import Pool as ThreadPool

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

        self.nameEnterEnable = QCheckBox(self.tab_2)
        self.nameEnterEnable.setGeometry(QRect(90, 20, 20, 20))
        self.nameEnterText = QLabel(self.tab_2)
        self.nameEnterText.setGeometry(QRect(110, 20, 160, 20))
        self.nameEnterText.setText("Player Search")
        self.playerUpdateButton = QPushButton(self.tab_2)
        self.playerUpdateButton.setGeometry(QRect(20, 20, 60, 20))
        self.playerUpdateButton.setText("update")
        self.playerUpdateButton.clicked.connect(self.playerListUpdate)

        offset = 40+180
        self.vehicleEnterEnable = QCheckBox(self.tab_2)
        self.vehicleEnterEnable.setGeometry(QRect(offset+90, 20, 20, 20))
        self.vehicleEnterText = QLabel(self.tab_2)
        self.vehicleEnterText.setGeometry(QRect(offset+110, 20, 160, 20))
        self.vehicleEnterText.setText("Vehicle Search")
        self.vehicleUpdateButton = QPushButton(self.tab_2)
        self.vehicleUpdateButton.setGeometry(QRect(offset+20, 20, 60, 20))
        self.vehicleUpdateButton.setText("update")
        self.vehicleUpdateButton.clicked.connect(self.vehicleListUpdate)

        self.ActiveLookupName = QPushButton(self.tab_2)
        self.ActiveLookupName.setText("Lookup")
        self.ActiveLookupName.setGeometry(QRect(offset*2+20+150, 15, 75, 25))
        # connects Player lookup caller to button click
        self.ActiveLookupName.clicked.connect(self.data_lookup)



        # player box, hidden if nameEnterEnable not enabled
        self.playerBox = QWidget(self.tab_2)
        self.playerBox.hide()
        self.playerBox.setGeometry(QRect(20, 45, 200, 500))
        self.playerBox.setAutoFillBackground(True)
        self.NameEnterBox = QLineEdit(self.playerBox)
        self.NameEnterBox.setGeometry(QRect(10, 10, 180, 25))
        self.playerListing = QListWidget(self.playerBox)
        self.playerListing.setGeometry(QRect(10, 40, 180, 200))


        self.vehicleBox = QWidget(self.tab_2)
        self.vehicleBox.hide()
        self.vehicleBox.setGeometry(QRect(offset+20, 45, 200, 500))
        self.vehicleBox.setAutoFillBackground(True)
        self.vehicleEnterBox = QLineEdit(self.vehicleBox)
        self.vehicleEnterBox.setGeometry(QRect(10, 10, 180, 25))
        self.vehicleListing = QListWidget(self.vehicleBox)
        self.vehicleListing.setGeometry(QRect(10, 40, 180, 200))


        self.nameEnterEnable.stateChanged.connect(lambda inc: self.playerBox.show() if inc == 2 else self.playerBox.hide())
        self.vehicleEnterEnable.stateChanged.connect(lambda inc: self.vehicleBox.show() if inc == 2 else self.vehicleBox.hide())


        self.dataBox = QWidget(self.tab_2)
        self.dataBox.setAutoFillBackground(True)
        self.dataBox.setGeometry(QRect(offset*2+20, 45, 530, 500))

        self.playerNameTable = QTableWidget(self.dataBox)
        self.playerNameTable.setObjectName("Players")
        self.playerNameTable.setGeometry(QRect(190, 10, 330, 235))
        # self.Squad1.setRowCount(8)
        self.playerNameTable.setColumnCount(3)
        self.playerNameTable.setHorizontalHeaderLabels(["Player", "Count", "Squadron"])
        self.playerNameTable.setRowCount(1)

        self.vehicleNameTable = QTableWidget(self.dataBox)
        self.vehicleNameTable.setObjectName("Vehicles")
        self.vehicleNameTable.setGeometry(QRect(190, 255, 330, 235))
        self.vehicleNameTable.setColumnCount(3)
        self.vehicleNameTable.setHorizontalHeaderLabels(["Vehicle", "Count", "Type"])
        self.vehicleNameTable.setRowCount(1)

        #self.VehicleEnterBox = QLineEdit(self.tab_2)
        #self.VehicleEnterBox.setGeometry(QRect(210, 45, 180, 25))
        # self.ActiveLookupName = QPushButton(self.tab_2)
        #self.ActiveLookupName.setText("Lookup")
        #self.ActiveLookupName.setGeometry(QRect(190, 15, 75, 25))
        # connects Player lookup caller to button click
        # connects ui updater to player signal
        self.signals.dataSignal.connect(self.data_update)


        # self.dataBox.set
        self.playerName = QLabel(self.dataBox)
        self.playerName.setGeometry(QRect(85, 0, 150, 25))
        self.playerNameText = QLabel(self.dataBox)
        self.playerNameText.setGeometry(QRect(10, 0, 150, 25))
        self.playerNameText.setText("Player: ")

        self.playerVehicle = QLabel(self.dataBox)
        self.playerVehicleText = QLabel(self.dataBox)
        self.playerVehicle.setGeometry(QRect(85, 30, 150, 25))
        self.playerVehicleText.setGeometry(QRect(10, 30, 150, 25))
        self.playerVehicleText.setText("Vehicle: ")


        self.playerKDText = QLabel(self.dataBox)
        self.playerKDText.setText("K/D:")
        self.playerKD = QLabel(self.dataBox)

        self.playerKDText.setGeometry(QRect(10, 60, 200, 25))
        self.playerKD.setGeometry(QRect(85, 60, 200, 25))

        self.playerKillsText = QLabel(self.dataBox)
        self.playerKillsText.setText("Kills:")
        self.playerKills = QLabel(self.dataBox)

        self.playerKillsText.setGeometry(QRect(10, 90, 200, 25))
        self.playerKills.setGeometry(QRect(85, 90, 200, 25))

        self.playerDeathsText = QLabel(self.dataBox)
        self.playerDeathsText.setText("Deaths:")
        self.playerDeaths = QLabel(self.dataBox)

        self.playerDeathsText.setGeometry(QRect(10, 120, 200, 25))
        self.playerDeaths.setGeometry(QRect(85, 120, 200, 25))

        self.playerBattlesText = QLabel(self.dataBox)
        self.playerBattlesText.setText("Total Battles:")
        self.playerBattles = QLabel(self.dataBox)

        self.playerBattlesText.setGeometry(QRect(10, 180, 200, 25))
        self.playerBattles.setGeometry(QRect(85, 180, 200, 25))

        # self.playerTKsText = QLabel(self.dataBox)
        # self.playerTKs = QLabel(self.dataBox)

        # self.playerTKsText.setGeometry(QRect(0, 120, 200, 25))
        # self.playerTKs.setGeometry(QRect(75, 120, 200, 25))
        '''
        page 3
        '''
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.test2 = QListWidget(self.tab_3)
        items1 = [QListWidgetItem() for i in range(20)]
        [item.setText(f"item: {i}") for i, item in enumerate(items1)]
        [self.test2.insertItem(index, items) for index, items in enumerate(items1)]
        self.test2.setGeometry(QRect(25, 25, 100, 100))
        self.test2.show()
        self.test2.itemClicked.connect(self.item_clicked)


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
        '''
        page 1: the place where logging of battles happens
        page 2: the place where you look up the stats for a player in a vehicle (or just overall) or a vehicle stats
        page 3: look up names for players, vehicles, and squadrons to be used in page 2
        page 4: look up a squadron for stats or recent battle
        page 5: settings and info about all this
        '''
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.enableDisable.setText(QCoreApplication.translate("MainWindow", u"Turn On/Off Logger", None))
        self.Squad1Tag.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.Squad2Tag.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab),
                                  QCoreApplication.translate("MainWindow", u"Battle", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),
                                  QCoreApplication.translate("MainWindow", u"Stats Lookup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3),
                                  QCoreApplication.translate("MainWindow", u"Data Lookup", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4),
                                  QCoreApplication.translate("MainWindow", u"Squadron Search", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5),
                                  QCoreApplication.translate("MainWindow", u"Settings", None))

    # a tester function for fucking around with qListWidgets ands selecting
    def item_clicked(self, data: QListWidgetItem):
        print(data.text())

    def data_lookup(self):
        player = self.playerListing.selectedItems()
        vehicle = self.vehicleListing.selectedItems()
        if not player or player[0].text() == "Any":
            player = "%"
        else:
            player = player[0].text()
        if not vehicle or vehicle[0].text() == "Any":
            vehicle = "%"
        else:
            vehicle = vehicle[0].text()
        self.create_lookup_thread(self.signals.dataSignal, self.dataLookup.dataLookup, [player, vehicle])

    def squadron_lookup(self):
        self.create_lookup_thread(self.signals.SquadronSignal, self.dataLookup.squadLookup, None)

    '''
    called by playerUpdateButton button signal 
    given a name and puts it through a spell checker
    returns all possible names and puts them in playerListing, a QListWidget
    '''
    def playerListUpdate(self):
        name = self.NameEnterBox.text()
        all_names = self.dataLookup.getPlayerNames()
        self.playerListing.clear()
        if name != "":
            checker = process.extract(name, all_names, limit=1000, score_cutoff=50)
            # print(checker)
            for index, val in enumerate(checker):
                item = QListWidgetItem()
                item.setText(val[0])
                self.playerListing.insertItem(index, item)
        else:
            item = QListWidgetItem()
            item.setText("Any")
            self.playerListing.insertItem(0, item)
            for index, name in enumerate(all_names):
                item = QListWidgetItem()
                item.setText(name)
                self.playerListing.insertItem(index+1, item)

    def vehicleListUpdate(self):
        vehicle = self.vehicleEnterBox.text()
        # print(vehicle)
        all_vehicles = self.dataLookup.getVehicleNames(self.converter)
        self.vehicleListing.clear()
        if vehicle != "":
            checker = process.extract(vehicle, all_vehicles, limit=1000, score_cutoff=50)
            # print(checker)
            for index, val in enumerate(checker):
                item = QListWidgetItem()
                item.setText(val[0])
                self.vehicleListing.insertItem(index, item)
        else:
            item = QListWidgetItem()
            item.setText("Any")
            self.vehicleListing.insertItem(0, item)
            for index, name in enumerate(all_vehicles):
                item = QListWidgetItem()
                item.setText(name)
                self.vehicleListing.insertItem(index+1, item)

    '''
    called by signal PLayerSignal. 
    used to update player lookup display with relevant information
    totals kills
    total deaths
    k/d
    team kills
    all their played vehicles with count
    current squadron
    most recent vehicle
    '''
    def data_update(self, data):
        print(f"WOMP WOMP")
        if data[0] == -1:
            return
        pool = ThreadPool(16)
        with pool as p:
            clean_data = p.map(self.dataLookup.convert, data[2][1])
        print("data process inital")
        squadron = None
        deaths = 0
        teamkills = 0
        vehicles = {}
        players = {}
        kills = 0
        battles = len(clean_data)
        for index, battle_ids in enumerate(data[2][2]):
            for idz in battle_ids:
                battle = clean_data[idz]
                player, vehicle, death, kill = battle[index+6]
                if death == "0":
                    deaths += 1
                if kill[0] != '':
                    kills += len(kill)
                if vehicle in vehicles.keys():
                    vehicles[vehicle] += 1
                else:
                    vehicles.update({vehicle: 1})
                if player in players.keys():
                    players[player] += 1
                else:
                    players.update({player: 1})
        self.playerNameTable.clear()
        self.playerNameTable.setRowCount(len(players))
        self.playerNameTable.setHorizontalHeaderLabels(["Player", "Count", "Squadron"])

        stuff = {k: v for k, v in sorted(players.items(), key=lambda item: item[1])}
        player_sorted = collections.OrderedDict(stuff)
        for index, (player, count) in enumerate(list(player_sorted.items())[::-1]):
            name = QTableWidgetItem()
            name.setFlags(Qt.ItemFlag.ItemIsEditable)
            name.setText(player)

            co = QTableWidgetItem()
            co.setFlags(Qt.ItemFlag.ItemIsEditable)
            co.setText(str(count))
            self.playerNameTable.setItem(index, 0, name)
            self.playerNameTable.setItem(index, 1, co)


        self.vehicleNameTable.clear()
        self.vehicleNameTable.setRowCount(len(vehicles))
        self.vehicleNameTable.setHorizontalHeaderLabels(["Vehicle", "Count", "Type"])

        stuff = {k: v for k, v in sorted(vehicles.items(), key=lambda item: item[1])}
        vehicle_sorted = collections.OrderedDict(stuff)
        for index, (player, count) in enumerate(list(vehicle_sorted.items())[::-1]):
            name = QTableWidgetItem()
            name.setFlags(Qt.ItemFlag.ItemIsEditable)
            name.setText(player)

            co = QTableWidgetItem()
            co.setFlags(Qt.ItemFlag.ItemIsEditable)
            co.setText(str(count))
            self.vehicleNameTable.setItem(index, 0, name)
            self.vehicleNameTable.setItem(index, 1, co)
        name = data[1][0][0]
        name = "Any" if name == "%" else name
        vehicle = data[1][0][1]
        vehicle = "Any" if vehicle == "%" else vehicle
        self.playerName.setText(name)
        self.playerVehicle.setText(vehicle)
        self.playerKD.setText(str(round(kills/deaths, 5)))
        self.playerKills.setText(str(kills))
        self.playerDeaths.setText(str(deaths))
        self.playerBattles.setText(str(battles))
        print(players)
        print(vehicles)
        print(kills)
        print(deaths)
        print(battles)


    def create_lookup_thread(self, signal: Signal, func, data):
        if self.threadpool.activeThreadCount() < 2:
            lookup_worker = LookupThread(func, signal, data)
            self.threadpool.start(lookup_worker)
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
        print("THREADING")
        output = self.fn(self.data, self.signal)
        # print(output)

