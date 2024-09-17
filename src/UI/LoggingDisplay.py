import PySide6.QtGui
from PySide6.QtWidgets import QWidget, QCheckBox, QLabel, QTableWidgetItem, QTableWidget, QSplitter, QSizeGrip, \
    QPushButton
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPalette, QTextItem, QBrush
import re

import src.UI.DisplayMain
from src.Path import Path
from src.signals import Signals
from src.DataManager.converter import DataGet, Vehicle, BattleGroup
from src.DebugLogger import Debug
# from src.UI.DisplayMain import SVGClass


class Display_u(QWidget):
    def __init__(self):
        super().__init__()


# class that is a list with extra steps to allow for use in lambdas
class valTemp:
    def __init__(self):
        self.x = 0
        self.y = 0

    def set(self, x, y):
        self.x, self.y = x, y


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
    #TODO: make the team info windows resize correctly
    def __init__(self):
        super().__init__()
        self.name = "Battle Logger"
        self.t1_rect = [20, 50, 470, 470]
        self.t2_rect = [510, 50, 470, 470]
        self.team1 = TeamDisplay(1, self, self.t1_rect)
        self.team2 = TeamDisplay(2, self, self.t2_rect)
        self.enableBox = QCheckBox(self)
        self.enableBoxText = QLabel(self)
        self.enableBoxText.setText("Enable / Disable Logging")
        # this stores the reference to the class so that instances of it can be made


        self.winLossBox = QLabel(self)
        self.set_initial_pos()

    def set_signals(self):
        self.enableBox.stateChanged.connect(self.send_data)
        Signals.signals.winner.connect(self.winLossBox.setText)

        Signals.signals.logs.connect(self.update_display)



    def set_initial_pos(self):
        self.team1.setGeometry(QRect(*self.t1_rect))
        self.team2.setGeometry(QRect(*self.t2_rect))

        self.enableBox.setGeometry(QRect(20, 15, 25, 25))
        self.enableBoxText.setGeometry(QRect(50, 15, 200, 25))

        self.winLossBox.setGeometry(QRect(200, 0, 200, 25))

    def resize_event(self, width, height):
        pass

    def update_display(self, data: dict):
        self.team1.update_display(data["team1Tag"], [data["team1Players"], data["team2Players"]])
        self.team2.update_display(data["team2Tag"], [data["team2Players"], data["team1Players"]])

    def send_data(self, data: int):
        Signals.signals.data.emit(data)


class TeamDisplay(QWidget):
    converter = DataGet()
    path = Path.path
    pic_path = f"{path}\\VehicleParser\\War-Thunder-Datamine\\atlases.vromfs.bin_u\\gameuiskin"
    nation_order = ("USA", "Germany", "Ussr", "Britain", "Japan", "China", "Italy", "France", "Sweden", "Israel")
    MIN_SIZE = 0.4
    UNITS = 400
    ACTUAL = 395
    TABLE_RATIO = [135/UNITS, 135/UNITS, 45/UNITS, 85/UNITS]

    def __init__(self, team: int, parent, rect):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Dark)
        self.tag = QLabel(self) # current squadron tag
        self.vehicle_text = QLabel(self)
        self.vehicle_text.setText("Vehicle Types:")
        self.vehicle = QLabel(self) # label for vehicle types to be placed in
        self.svg_class = src.UI.DisplayMain.SVGClass(self, self.pic_path)

        self.team = team
        self.ratio = 1 # current box size ratio, used to tell stuff how big the box is currently to handle resizing

        self.Rect: list = rect
        self.rect_temp = []
        self.rect_temp_1 = []

        self.font = QFont()
        self.font.setPixelSize(11)
        self.font.setBold(True)
        self.f_large = QFont()
        self.f_large.setBold(True)
        self.f_large.setPixelSize(18)

        self.dataBox = QTableWidget(self)
        self.dataBox.setRowCount(8)
        self.dataBox.setColumnCount(4)
        self.dataBox.setHorizontalHeaderLabels(["Name", "Vehicle", "State", "Kills"])
        self.dataBox.horizontalHeader().setFont(self.font)
        self.dataBox.verticalHeader().setFixedWidth(56)
        self.dataBox.setColumnWidth(0, self.TABLE_RATIO[0]*self.ACTUAL)
        self.dataBox.setColumnWidth(1, self.TABLE_RATIO[1]*self.ACTUAL)
        self.dataBox.setColumnWidth(2, self.TABLE_RATIO[2]*self.ACTUAL)
        self.dataBox.setColumnWidth(3, self.TABLE_RATIO[3]*self.ACTUAL)
        self.dataBox.setVerticalHeaderLabels(
            [f"Player {str(i + 8 * (team - 1))}" for i in range(1, 9)])
        for x in range(4):
            for y in range(8):
                self.dataBox.setItem(y, x, self.item("womp", self.font))
        self.tag.setText("wompr")
        self.tag.setFont(self.f_large)

        self.moveBox = QPushButton(self)
        self.moveBox.resizeEvent = self.moveResizeEvent
        self.moveBox.setGeometry(QRect(0, 0, 15, 15))
        self.moveBox.mouseMoveEvent = self.moveResizeEvent
        self.moveBox.mousePressEvent = self.moveResizeEvent
        self.moveBox.hide()
        self.enlarge_box = QPushButton(self)
        self.enlarge_box.setGeometry(QRect(450, 380, 20, 20))
        self.enlarge_box.resizeEvent = self.boxResizeEvent
        self.enlarge_box.mouseMoveEvent = self.boxResizeEvent
        self.enlarge_box.mousePressEvent = self.boxResizeEvent
        self.enlarge_box.hide()
        self.tag_box = [10, 10, 65, 25]
        self.databox_box = [8, 50, 455, 267]
        self.vehicle_text_box = [8, 320, 100, 25]
        self.vehicle_box = [88, 320, 100, 25]
        self.nation_box_box = [100, 10, 360, 36]

        self.set_initial_pos()
        self.svg_render(self.nation_order)
        '''
        for index, nation in enumerate(self.nation_order):
            self.svgs[index].load(
                self.path + f"/VehicleParser/War-Thunder-Datamine/atlases.vromfs.bin_u/gameuiskin\\country_{nation.lower()}.svg")
            self.svgs[index].setGeometry(QRect(36 * index, 0, 30, 30))
            self.svgs[index].renderer()
            '''

    def set_initial_pos(self):
        self.tag.setGeometry(QRect(*self.tag_box))
        self.dataBox.setGeometry(QRect(*self.databox_box))
        self.vehicle_text.setGeometry(QRect(*self.vehicle_text_box))
        self.vehicle.setGeometry(QRect(*self.vehicle_box))
        self.svg_class.setGeometry(QRect(*self.nation_box_box))
        self.svg_class.r_event(self.svg_class.rect())

    # given a list of nation name, will get the svg pic and draw them with respect to box size
    def svg_render(self, nations):
        self.svg_class.svg_update(nations)

    # def svg_resize(self):
    #     for index in range(len(self.svgs)):
    #         self.svgs[index].setGeometry(QRect(36 * index * self.ratio, 0, 30 * self.ratio, 30 * self.ratio))

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent):
        self.ratio = event.size().width() / self.Rect[2]
        if self.ratio < self.MIN_SIZE:
            return
        self.enlarge_box.setGeometry(QRect(self.width() - 20, self.height() - 20, 20, 20))
        self.tag.setGeometry(QRect(*[x * self.ratio for x in self.tag_box]))
        self.dataBox.setGeometry(QRect(*[x * self.ratio for x in self.databox_box]))
        self.vehicle_text.setGeometry(QRect(*[x * self.ratio for x in self.vehicle_text_box]))
        self.svg_class.setGeometry(QRect(*[x * self.ratio for x in self.nation_box_box]))
        self.svg_class.r_event(self.svg_class.rect())

        self.font.setPixelSize(int(11*self.ratio+0.5))
        self.f_large.setPixelSize(int(18*self.ratio+0.5))
        self.tag.setFont(self.font)
        self.vehicle_text.setFont(self.font)
        self.vehicle.setFont(self.font)


        self.dataBox.setColumnWidth(0, self.ratio*self.TABLE_RATIO[0]*self.ACTUAL)
        self.dataBox.setColumnWidth(1, self.ratio*self.TABLE_RATIO[1]*self.ACTUAL)
        self.dataBox.setColumnWidth(2, self.ratio*self.TABLE_RATIO[2]*self.ACTUAL)
        self.dataBox.setColumnWidth(3, self.ratio*self.TABLE_RATIO[3]*self.ACTUAL)

    def moveResizeEvent(self, event):
        if type(event) is PySide6.QtGui.QMouseEvent:
            event: PySide6.QtGui.QMouseEvent = event
            if self.rect_temp == []:
                self.rect_temp = [event.globalX(), event.globalY()]
            else:

                off_x, off_y = event.globalX() - self.rect_temp[0], event.globalY() - self.rect_temp[1]
                self.setGeometry(self.x() + off_x, self.y() + off_y, self.width(), self.height())
                self.rect_temp = [event.globalX(), event.globalY()]
                self.raise_()
        elif True:
            pass

    def boxResizeEvent(self, event):

        if type(event) is PySide6.QtGui.QMouseEvent:
            event: PySide6.QtGui.QMouseEvent = event
            if event.isBeginEvent():
                self.rect_temp_1 = [event.globalX(), event.globalY()]
            else:
                ratio = self.Rect[2] / self.Rect[3]
                if self.width() >= 0 and self.height() >= 0:
                    off_x, off_y = event.globalX() - self.rect_temp_1[0], event.globalY() - self.rect_temp_1[1]
                    # This formula was such a fucking pain to come up with
                    # I have no actual idea how to handle this type of resizing
                    # so if someone comes through here please fucking fix this
                    # TODO
                    # also one thing to note is that floats given to any positional thing requiring ints are silently casted
                    e = abs(off_y+off_x)
                    if off_y+off_x != 0:
                        off_y = off_y/e
                        off_x = off_x/e
                        if self.width() / self.Rect[2] < self.MIN_SIZE and off_x < 0 and off_y < 0:
                            return
                        self.setGeometry(self.x(), self.y(), self.width() + off_x, self.height() + off_x)
                        self.setGeometry(self.x(), self.y(), self.width() + off_y, self.height() + off_y)

                        self.rect_temp_1 = [event.globalX(), event.globalY()]
                        self.raise_()
        elif True:
            pass

    '''
    creates a QTableWidgetItem with a set name with flag ItemIsEditable set to false
    '''

    def item(self, val, font: QFont = None):
        payload = QTableWidgetItem()
        payload.setText(val)
        if font is not None:
            payload.setFont(font)
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
        vehicles = []
        for x, player in enumerate(player_info[0]):

            name, vehicle, is_dead, kills = player.name, player.vehicle[1:-1], player.dead, player.kills
            # the getter we are using in DataCollector returns a Player object to represent a player
            if not player.badPlayer:
                is_dead = "Alive" if is_dead is True else "Dead"
                temp = []
                for kill in kills:
                    if kill in player_info[0]:
                        if self.team == 1:
                            temp.append(player_info[0].index(kill) + 1)
                        else:
                            temp.append(player_info[0].index(kill) + 9)
                    elif kill in player_info[1]:
                        if self.team == 1:
                            temp.append(player_info[1].index(kill) + 9)
                        else:
                            temp.append(player_info[1].index(kill) + 1)
                    else:
                        # this is for when a drone or some shit gets into kills. I cant remember if thats possible or not
                        # but I know that a drone kill wont be in team comp but may get into player kills so this covers for that
                        temp.append(17)
                kills = ', '.join([str(z) for z in temp])
            for y, v in enumerate([name, vehicle, is_dead, kills]):
                if player.badPlayer:
                    v = ""
                item = self.item(self.clean_vehicle_name(v))
                if y == 2 and v == "Alive":
                    # item.background().setColor("green")
                    back = QBrush()
                    back.setColor(PySide6.QtGui.qRgba(0, 255, 0, 120))
                    item.setBackground(back)
                    item.setData(Qt.ItemDataRole.DisplayRole.BackgroundRole, PySide6.QtGui.qRgba(0, 255, 0, 255))
                    item.setForeground(back)

                # self.dataBox.
                self.dataBox.setItem(x, y, item)
            vehicles.append(vehicle)
        team = BattleGroup(vehicles)
        self.svg_render(team.get_nations()[1])
        Debug.logger.log("Logger Display", team.get_vehicles_simple_shorthand())
        self.vehicle.setText(team.get_vehicles_simple_shorthand())
        # adds all the svgs for the current nation on each team


    def getNations(self, vehicles):
        payload = [{}, []]
        for vehicle in vehicles:
            if vehicle == '':
                continue
            internal = self.converter.query_name(vehicle)
            v = Vehicle(vehicle, internal[0:-2])
            if v.country in payload[0].keys():
                payload[0][v.country] += 1
            else:
                payload[0].update({v.country: 1})
        for nation in self.nation_order:
            if nation.lower() in payload[0].keys():
                payload[1].append(nation)

        return payload

    @staticmethod
    def clean_vehicle_name(name):
        if name is None:
            return ""
        name = re.sub(r'[▅▄◔◄␗▃▂▄▄◐▀␠◗◘◊○◌]', '', name)
        name = re.sub(r'\u00a0', ' ', name)  # Replace non-breaking spaces with regular spaces
        name = re.sub(r'\s+', ' ', name)  # Replace multiple spaces with a single space
        name = re.sub(r':flag_\w+:\s*', '', name).strip()  # Remove flags
        return name
