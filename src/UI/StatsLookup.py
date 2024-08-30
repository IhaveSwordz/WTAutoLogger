
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QRect, Signal, Slot, Qt
from rapidfuzz import process
import collections

from src.DataManager.DatabaseManager import PlayerQuery
from src.QThreader import Thread
from src.signals import Signals
from multiprocessing.dummy import Pool as ThreadPool
from src.DataManager.converter import DataGet


class Display(QWidget):
    def __init__(self, player_data, vehicle_data, squadron_data):
        super().__init__()
        self.name = "Stats Lookup"
        self.player_lookup = Lookup(player_data, "Player Search", self)
        self.vehicle_lookup = Lookup(vehicle_data, "Vehicle Search", self)
        self.squadron_lookup = Lookup(squadron_data, "Squadron Search", self)
        self.activate_button = QPushButton(self)
        self.activate_button.setText("Lookup")
        self.data_lookup = PlayerQuery()
        self.lookup = InfoDisplay(self.data_lookup, self)
        self.activate_button.clicked.connect(self.data_send)
        self.set_initial_pos()

    def set_initial_pos(self):
        self.player_lookup.setGeometry(QRect(20, 20, 200, 260))
        self.vehicle_lookup.setGeometry(QRect(240, 20, 200, 260))
        self.squadron_lookup.setGeometry(QRect(20, 300, 200, 260))
        self.activate_button.setGeometry(QRect(500, 15, 75, 25))
        self.lookup.setGeometry(QRect(480, 50, 530, 500))

    @Slot()
    def pr(self, data, *args, **kwargs):
        print(data, args, kwargs)

    '''
    a function to be ran asynchronously that calculates info
    used to update lookup display with relevant information
    totals kills
    total deaths
    k/d
    team kills
    all their played vehicles with count
    current squadron
    most recent vehicle

    '''

    def data_send(self):
        try:
            player = self.player_lookup.dataList.selectedItems()[0].text()
        except IndexError:
            player = ""
        try:
            vehicle = self.vehicle_lookup.dataList.selectedItems()[0].text()
        except IndexError:
            vehicle = ""
        try:
            squadron = self.squadron_lookup.dataList.selectedItems()[0].text()
        except IndexError:
            squadron = ""
        if player in ["", "Any"]:
            player = "%"
        if vehicle in ["", "Any"]:
            vehicle = "%"
        if squadron in ["", "Any"]:
            squadron = "%"
        Thread.create_thread(Signals.signals.dataSignal, self.data_lookup.dataLookup, [player, vehicle, squadron])



class Lookup(QWidget):
    def __init__(self, data_class, title, parent):
        super().__init__(parent)
        self.parent: Display = parent
        self.data = data_class

        self.enable_check = QCheckBox(self)

        self.title = QLabel(self)
        self.title.setText(title)

        self.display_widget = QWidget(self)
        self.dataEnter = QLineEdit(self.display_widget)
        self.dataList = QListWidget(self.display_widget)

        self.dataEnter.textChanged.connect(self.lookup)
        self.lookup("")
        self.enable_check.stateChanged.connect(self.checkHandler)
        self.display_widget.setAutoFillBackground(True)
        self.display_widget.hide()

        self.set_initial_pos()

    def checkHandler(self, dat):
        if dat == 2:
            self.display_widget.show()
        elif dat == 0:
            self.display_widget.hide()
            self.dataEnter.setText("")


    def lookup(self, text):
        self.dataList.clear()
        if text != "":
            out = process.extract(text, self.data.data.keys(), limit=1000, score_cutoff=50)
            for index, val in enumerate(out):
                item = QListWidgetItem()
                item.setText(val[0])
                self.dataList.insertItem(index, item)
        else:
            for index, val in enumerate(["Any"]+list(self.data.data.keys())):
                item = QListWidgetItem()
                item.setText(val)
                self.dataList.insertItem(index, item)



    def set_initial_pos(self):
        # self.send_button.setGeometry(QRect(0, 0, 60, 20))
        self.enable_check.setGeometry(QRect(65, 0, 20, 20))
        self.title.setGeometry(QRect(85, 0, 160, 20))
        self.display_widget.setGeometry(QRect(0, 25, 200, 235))
        self.dataEnter.setGeometry(QRect(10, 10, 180, 25))
        self.dataList.setGeometry(QRect(10, 40, 180, 185))


class InfoDisplay(QWidget):
    def __init__(self, data_lookup: PlayerQuery, parent):
        super().__init__(parent)
        self.data_lookup = data_lookup
        self.conv = DataGet()
        self.setAutoFillBackground(True)

        self.playerNameTable = QTableWidget(self)
        self.playerNameTable.setObjectName("Players")
        self.playerNameTable.setColumnCount(3)
        self.playerNameTable.setHorizontalHeaderLabels(["Player", "Count", "Squadron"])
        self.playerNameTable.setRowCount(1)

        self.vehicleNameTable = QTableWidget(self)
        self.vehicleNameTable.setObjectName("Vehicles")
        self.vehicleNameTable.setColumnCount(3)
        self.vehicleNameTable.setHorizontalHeaderLabels(["Vehicle", "Count", "Type"])
        self.vehicleNameTable.setRowCount(1)
        self.vehicleNameTable.verticalHeader().setDefaultSectionSize(20)
        self.vehicleNameTable.setColumnWidth(0, 120)
        self.vehicleNameTable.setColumnWidth(1, 40)
        self.vehicleNameTable.setColumnWidth(2, 80)



        # self.dataBox.set
        self.playerName = QLabel(self)
        self.playerNameText = QLabel(self)
        self.playerNameText.setText("Player: ")

        self.squadron = QLabel(self)
        self.squadronText = QLabel(self)
        self.squadronText.setText("Squadron: ")

        self.playerVehicle = QLabel(self)
        self.playerVehicleText = QLabel(self)
        self.playerVehicleText.setText("Vehicle: ")


        self.playerKDText = QLabel(self)
        self.playerKDText.setText("K/D:")
        self.playerKD = QLabel(self)


        self.playerKillsText = QLabel(self)
        self.playerKillsText.setText("Kills:")
        self.playerKills = QLabel(self)

        self.teamKillsText = QLabel(self)
        self.teamKillsText.setText("Team Kills:")
        self.teamKills = QLabel(self)

        self.playerDeathsText = QLabel(self)
        self.playerDeathsText.setText("Deaths:")
        self.playerDeaths = QLabel(self)


        self.playerBattlesText = QLabel(self)
        self.playerBattlesText.setText("Total Battles:")
        self.playerBattles = QLabel(self)


        Signals.signals.dataSignal.connect(self.data_update)
        self.set_initial_pos()

    def set_initial_pos(self):
        self.playerNameTable.setGeometry(QRect(190, 10, 330, 235))
        self.vehicleNameTable.setGeometry(QRect(190, 255, 330, 235))

        self.playerName.setGeometry(QRect(85, 0, 150, 25))
        self.playerNameText.setGeometry(QRect(10, 0, 150, 25))
        self.squadron.setGeometry(QRect(85, 30, 150, 25))
        self.squadronText.setGeometry(QRect(10, 30, 150, 25))
        self.playerVehicle.setGeometry(QRect(85, 60, 150, 25))
        self.playerVehicleText.setGeometry(QRect(10, 60, 150, 25))
        self.playerKDText.setGeometry(QRect(10, 90, 200, 25))
        self.playerKD.setGeometry(QRect(85, 90, 200, 25))
        self.playerKillsText.setGeometry(QRect(10, 120, 200, 25))
        self.playerKills.setGeometry(QRect(85, 120, 200, 25))
        self.teamKillsText.setGeometry(QRect(10, 150, 200, 25))
        self.teamKills.setGeometry(QRect(85, 150, 200, 25))
        self.playerDeathsText.setGeometry(QRect(10, 180, 200, 25))
        self.playerDeaths.setGeometry(QRect(85, 180, 200, 25))
        self.playerBattlesText.setGeometry(QRect(10, 210, 200, 25))
        self.playerBattles.setGeometry(QRect(85, 210, 200, 25))

    '''
    [1, [data, pid, vid], occur]
    handles all the data created by dataLookup
    parses it into all the info we care about from the raw battle info
    '''
    #TODO: fix the teamkill checker

    def data_update(self, data):
        print(f"WOMP WOMP")
        if data[0] == -1:
            return
        pool = ThreadPool(16)
        with pool as p:
            clean_data = p.map(self.data_lookup.convert, data[2][1])
        print("data process inital")
        squadron = None
        deaths = 0
        # fix team kills not being counted correctly
        team_kills = 0
        vehicles = {}
        players = {}
        squadrons = {}
        kills = 0
        battles = len(clean_data)
        for index, battle_ids in enumerate(data[2][2]):
            for idz in battle_ids:
                battle = clean_data[idz]
                print(len(battle))
                if battle[index + 6] is None:
                    continue
                player, vehicle, death, kill = battle[index + 6]
                # print(player)
                squadron = None
                if index in battle[4]:
                    squadron = battle[2]
                    for k in kill:
                        if k == '':
                            continue
                        print(k, index)
                        k = int(k)
                        if k in battle[4] and k != index:
                            team_kills += 1
                else:
                    squadron = battle[3]
                    for k in kill:
                        if k == '':
                            continue

                        k = int(k)
                        if k in battle[5] and k != index:
                            team_kills += 1
                if data[1][0][2] != squadron and data[1][0][2] != "%":
                    # print("bad squadron: " + squadron)
                    continue
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

                if player not in squadrons.keys():
                    squadrons.update({player: squadron})

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

            squad = QTableWidgetItem()
            squad.setFlags(Qt.ItemFlag.ItemIsEditable)
            squad.setText(squadrons[player])
            self.playerNameTable.setItem(index, 0, name)
            self.playerNameTable.setItem(index, 1, co)
            self.playerNameTable.setItem(index, 2, squad)

        self.vehicleNameTable.clear()
        self.vehicleNameTable.setRowCount(len(vehicles))
        self.vehicleNameTable.setHorizontalHeaderLabels(["Vehicle", "Count", "Type"])

        stuff = {k: v for k, v in sorted(vehicles.items(), key=lambda item: item[1])}
        vehicle_sorted = collections.OrderedDict(stuff)
        for index, (player, count) in enumerate(list(vehicle_sorted.items())[::-1]):
            name = QTableWidgetItem()
            name.setFlags(Qt.ItemFlag.ItemIsEditable)
            name.setText(self.conv.query_id(player[:-2]))

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
        self.squadron.setText(data[1][0][2])
        self.playerKD.setText(str(round(kills / deaths, 5)))
        self.playerKills.setText(str(kills))
        self.playerDeaths.setText(str(deaths))
        self.teamKills.setText(str(team_kills))
        self.playerBattles.setText(str(battles))

        print(players)
        print(vehicles)
        print(kills)
        print(team_kills)
        print(deaths)
        print(battles)









'''
LoggingWidget is a QT QWidget which handles the looking up of stats for players
does not generate any data, only parses data to be displayed

handles displaying of data related to the currently active battle
examples of data:
players
vehicles
who killed who
which nations
which vehicle types

'''