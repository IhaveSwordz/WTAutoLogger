from PySide6.QtWidgets import QWidget, QLabel, QTableWidget, QTableWidgetItem, QTabWidget, QListWidget, QListWidgetItem, QPushButton
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtGui import QFont, QPalette
from PySide6.QtCore import QRect, Qt
import datetime


import src.UI.DisplayMain
from src.UI.StatsLookup import Lookup
from src.DataManager.DatabaseManager import PlayerQuery
from src.DataManager.converter import BattleGroup, DataGet
from src.QThreader import Thread
from src.signals import Signals
from src.Path import Path
from src.UI.LoggingDisplay import Display
from src.DataManager.DataCollector import Player
'''

This tab is to be used to look up squadrons to see previous battle info
'''


class LoggingDisplay(QWidget):
    def __init__(self, squadron_data_class):
        super().__init__()
        self.name = "Squadron Lookup"
        self.lookup = Lookup(squadron_data_class, "Squadron Lookup", self)
        self.lookup.enable_check.hide()
        self.lookup.checkHandler(2)
        self.lookup.dataList.itemClicked.connect(self.do_lookup)
        self.battle_list = QListWidget(self)
        self.normal_font = QFont("Consolas", 10)
        self.battle_list.itemActivated.connect(self.entered)
        self.popup_button = QPushButton(self)
        self.popup_button.setText("Show Full Battle")
        Signals.signals.squadron_list.connect(self.set_info)
        self.team1 = Team(self)
        self.team2 = Team(self)
        self.popup = None
        self.current_enter = None
        # self.popup.enableBox.hide()
        # self.popup.enableBoxText.hide()
        self.popup_button.pressed.connect(self.generate_popup)

        self.set_initial_pos()
        self.query = PlayerQuery()
        self.battles = []
        self.converter = DataGet()

    def entered(self, data: QListWidgetItem):
        self.current_enter = data
        raw = self.battles[self.battle_list.indexFromItem(self.current_enter).row()]
        data = self.query.convert(raw)
        t1tag = data[2]
        t2tag = data[3]
        t1players = [data[4+i] for i in range(8)]
        t2players = [data[4+i+8] for i in range(8)]
        if self.lookup.dataList.selectedItems()[0].text() == t2tag:
            self.team1.update_data(t2tag, [x[0] for x in t2players], [self.converter.query_id(x[1]) for x in t2players])
            self.team2.update_data(t1tag, [x[0] for x in t1players], [self.converter.query_id(x[1]) for x in t1players])
        else:
            self.team2.update_data(t2tag, [x[0] for x in t2players], [self.converter.query_id(x[1]) for x in t2players])
            self.team1.update_data(t1tag, [x[0] for x in t1players], [self.converter.query_id(x[1]) for x in t1players])

    def set_initial_pos(self):
        self.lookup.setGeometry(0, 0, 200, 260)
        self.battle_list.setGeometry(210, 25, 500, 235)
        self.team1.setGeometry(0, 270, 850, 150)
        self.team2.setGeometry(0, 420, 850, 150)
        self.popup_button.setGeometry(720, 240, 100, 25)

    def generate_popup(self):
        if self.current_enter is None:
            return
        raw = self.battles[self.battle_list.indexFromItem(self.current_enter).row()]
        data = self.query.convert(raw)
        self.popup = Display()

        self.popup.enableBox.hide()
        self.popup.enableBoxText.hide()

        t1tag = data[2]
        t2tag = data[3]
        t1players = [data[4+i] for i in range(8)]
        t2players = [data[4+i+8] for i in range(8)]
        box1 = self.popup.team1.dataBox
        box2 = self.popup.team2.dataBox
        vehicles = []
        for index, (player, vehicle, is_dead, kills) in enumerate(t1players):
            box1.item(index, 0).setText(player)
            out = self.converter.query_id(vehicle)
            vehicles.append(out)
            box1.item(index, 1).setText(out)
            box1.item(index, 2).setText("Alive" if is_dead == "1" else "Dead")
            box1.item(index, 3).setText(', '.join(kills))

        team = BattleGroup(vehicles)
        self.popup.team1.tag.setText(t1tag)
        self.popup.team1.svg_class.svg_update(team.get_nations()[1])
        self.popup.team1.vehicle.setText(team.get_vehicles_simple_shorthand())


        vehicles = []
        for index, (player, vehicle, is_dead, kills) in enumerate(t2players):
            box2.item(index, 0).setText(player)
            out = self.converter.query_id(vehicle)
            vehicles.append(out)
            box2.item(index, 1).setText(out)
            box2.item(index, 2).setText("Alive" if is_dead == "1" else "Dead")
            box2.item(index, 3).setText(', '.join(kills))

        team = BattleGroup(vehicles)
        self.popup.team2.tag.setText(t2tag)
        self.popup.team2.svg_class.svg_update(team.get_nations()[1])
        self.popup.team2.vehicle.setText(team.get_vehicles_simple_shorthand())

        self.popup.show()
        '''
        t1 = [*self.team1, *[Player("", "", "", badPlayer=True) for z in range(8 - len(self.team1))]]
        t2 = [*self.team2, *[Player("", "", "", badPlayer=True) for z in range(8 - len(self.team2))]]

        return {
            "team1Tag": t1tag,
            "team1Players": t1,
            "team2Tag": t2tag,
            "team2Players": t2
        }'''

    def do_lookup(self, item: QTableWidgetItem):
        payload = item.text()
        if payload == "Any":
            payload = "%"
        Thread.create_thread(Signals.signals.squadron_list, self.query.dataLookup, ["%", "%", payload])

    def set_info(self, data):
        self.battle_list.clear()
        battles = data[2][1][::-1]
        self.battles = battles
        for index, (hashz, time, s1, s2, *rest, wl, mapz) in enumerate(battles):
            delta_time = self.compare_time(time)
            day, hour, minute = delta_time.days, delta_time.seconds // 3600, (delta_time.seconds // 60) % 60
            if data[1][0][2] == s2:
                win = "N"
                if wl == 2:
                    win = "W"
                elif wl == 1:
                    win = "L"
                item = QListWidgetItem(
                    f"{win} : {s2:<5} vs {s1:<5} : {day} days, {hour} hours, and {minute} minutes ago")
            else:
                win = "N"
                if wl == 2:
                    win = "L"
                elif wl == 1:
                    win = "W"
                item = QListWidgetItem(
                    f"{win} : {s1:<5} vs {s2:<5} : {day} days, {hour} hours, and {minute} minutes ago")
            item.setFont(self.normal_font)
            self.battle_list.addItem(item)

    def compare_time(self, time: str):
        current = datetime.datetime.now(datetime.UTC)
        year, month, day, hour, minute = [int(x) for x in time.split(";")]
        old = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=datetime.UTC)
        return current - old


'''
Is Given a raw battle (raw as in directly from database) and parses and the information and makes a QWidget that
display the players, the vehicles, and the vehicle types
'''


class Team(QWidget):
    path = Path.path
    pic_path = f"{path}\\VehicleParser\\War-Thunder-Datamine\\atlases.vromfs.bin_u\\gameuiskin"
    nation_order = ("USA", "Germany", "Ussr", "Britain", "Japan", "China", "Italy", "France", "Sweden", "Israel")

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.converter = PlayerQuery()
        self.svg_box = src.UI.DisplayMain.SVGClass(self, self.pic_path)
        self.svg_box.svg_update(self.nation_order)
        self.tag = QLabel(self)
        self.tag.setText("WOMP")

        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Dark)

        self.vehicle_text = QLabel(self)
        self.vehicle_text.setText("Vehicle Types:")
        self.vehicle = QLabel(self) # label for vehicle types to be placed in

        self.team = QTableWidget(self)
        self.team.setColumnCount(8)
        self.team.setRowCount(2)

        self.team.setHorizontalHeaderLabels([f"Player {i+1}" for i in range(8)])
        self.team.setVerticalHeaderLabels(["Player", "Vehicle"])

        self.vehicle_text_box = [500, 10, 100, 25]
        self.vehicle_box = [588, 10, 100, 25]
        self.initial_pos()

    def initial_pos(self):
        self.svg_box.setGeometry(QRect(*[100, 10, 360, 36]))
        self.svg_box.r_event(self.svg_box.rect())
        self.tag.setGeometry(QRect(10, 10, 100, 25))
        self.team.setGeometry(QRect(0, 50, 850, 200))
        self.vehicle_text.setGeometry(QRect(*self.vehicle_text_box))
        self.vehicle.setGeometry(QRect(*self.vehicle_box))

    def update_data(self, tag, players, vehicles):
        self.tag.setText(tag)
        for index, player in enumerate(players):
            self.team.setItem(0, index, self.item(player))
        for index, vehicle in enumerate(vehicles):
            self.team.setItem(1, index, self.item(vehicle))
        parsed = BattleGroup(vehicles)
        self.svg_box.svg_update(parsed.get_nations()[1])
        self.vehicle.setText(parsed.get_vehicles_simple_shorthand())


    @staticmethod
    def item(val, font: QFont = None):
        payload = QTableWidgetItem()
        payload.setText(val)
        if font is not None:
            payload.setFont(font)
        payload.setFlags(Qt.ItemFlag.ItemIsEditable)
        # payload.setFont(self.font)
        return payload


