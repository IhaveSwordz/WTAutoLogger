
from PySide6.QtWidgets import QWidget, QCheckBox, QLabel, QTableWidgetItem, QTableWidget
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPalette, QTextItem
from src.signals import Signals
from src.DataManager.converter import DataGet, Vehicle


'''
LoggingDisplay is a QT QWidget which handles the displayment and parsing of data
does not generate any data, only parses data to be displayed

handles displaying of data related to the currently active battle
examples of data:
players
vehicles
who killed who
which nations
which vehicle types

'''


class Display(QWidget):
    def __init__(self, ):
        super().__init__()
        self.name = "Battle Logger"
        self.team1 = TeamDisplay(1, self)
        self.team2 = TeamDisplay(2, self)
        self.enableBox = QCheckBox(self)
        self.enableBoxText = QLabel(self)
        self.enableBoxText.setText("Enable / Disable Logging")
        self.enableBox.stateChanged.connect(self.send_data)
        Signals.signals.logs.connect(self.update_display)
        self.set_initial_pos()

    def set_initial_pos(self):
        self.team1.setGeometry(QRect(20, 50, 470, 400))
        self.team2.setGeometry(QRect(510, 50, 470, 400))

        self.enableBox.setGeometry(QRect(20, 15, 25, 25))
        self.enableBoxText.setGeometry(QRect(50, 15, 200, 25))

    def resize_event(self, width, height):
        pass

    def update_display(self, data: dict):
        self.team1.update_display(data["team1Tag"], [data["team1Players"], data["team2Players"]])
        self.team2.update_display(data["team2Tag"], [data["team2Players"], data["team1Players"]])



    def send_data(self, data: int):
        Signals.signals.data.emit(data)

class TeamDisplay(QWidget):
    font = QFont()
    font.setPixelSize(11)
    font.setBold(True)
    f_large = QFont()
    f_large.setBold(True)
    f_large.setPixelSize(16)

    nation_order = ("USA", "Germany", "Great Britain", "Japan", "China", "Italy", "France", "Sweden", "Israel")
    def __init__(self, team: int, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Dark)
        self.tag = QLabel(self)
        self.vehicle_text = QLabel(self)
        self.vehicle_text.setText("Vehicle Types:")
        self.vehicle = QLabel(self)
        self.nation_test = QLabel(self)
        self.nation_test.setText("Nations:")
        self.nation = QLabel(self)

        self.dataBox = QTableWidget(self)
        self.dataBox.setRowCount(8)
        self.dataBox.setColumnCount(4)
        self.dataBox.setHorizontalHeaderLabels(["Name", "Vehicle", "State", "Kills"])
        self.dataBox.horizontalHeader().setFont(self.font)
        self.dataBox.verticalHeader().setFixedWidth(56)
        self.dataBox.setColumnWidth(0, 135)
        self.dataBox.setColumnWidth(1, 135)
        self.dataBox.setColumnWidth(2, 50)
        self.dataBox.setColumnWidth(3, 75)
        self.dataBox.setVerticalHeaderLabels(
            [f"Player {str(i+8*(team-1))}" for i in range(1, 9)])
        self.dataBox.setFont(self.font)
        for x in range(4):
            for y in range(8):
                self.dataBox.setItem(y, x, self.item("womp"))
        self.set_initial_pos()

    def set_initial_pos(self):
        self.tag.setGeometry(QRect(210, 0, 50, 25))
        self.dataBox.setGeometry(QRect(8, 50, 455, 267))
        self.vehicle_text.setGeometry(QRect(8, 320, 100, 25))
        self.nation_test.setGeometry(QRect(8, 350, 100, 25))

    '''
    creates a QTableWidgetItem with a set name with flag ItemIsEditable set to false
    '''
    def item(self, val):
        payload = QTableWidgetItem()
        payload.setText(val)
        payload.setFlags(Qt.ItemFlag.ItemIsEditable)
        payload.setFont(self.font)
        return payload

    def resize_event(self, width, height):
        pass

    '''
    used to input data into the table and the threee QLabel items
    '''
    def update_display(self, squadron: str, player_info: list):
        self.tag.setText(squadron)
        # self.nation.setText(nations)
        # self.vehicle.setText(vehicle_types)
        for x, player in enumerate(player_info[0]):

            name, vehicle, is_dead, kills = player.name, player.vehicle[1:-1], player.dead, player.kills
            if not player.badPlayer:
                is_dead = "ALive" if is_dead is True else "Dead"
                temp = []
                for kill in kills:
                    if kill in player_info[0]:
                        temp.append(player_info[0].index(kill)+1)
                    elif kill in player_info[1]:
                        temp.append(player_info[1].index(kill)+9)
                    else:
                        # this is for when a drone or some shit gets into kills. I cant remember if thats possible or not
                        # but I know that a drone kill wont be in team comp but may get into player kills so this covers for that
                        temp.append(17)
                kills = ', '.join([str(z) for z in temp])
            for y, v in enumerate([name, vehicle, is_dead, kills]):
                if player.badPlayer:
                    v = ""
                item = self.item(v)
                if y == 2 and v == "Alive":
                    item.setFont(self.f_large)
                self.dataBox.setItem(y, x, item)


