import os.path

from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget
from PySide6.QtCore import QRect
import datetime
from src.UI import LoggingDisplay
from src.UI import StatsLookup
from src.UI import PVSLookup
from src.UI import SquadronLookup
from src.UI import Settings
# from src.UI import LoggingDisplay, StatsLookup, PVSLookup, SquadronLookup, Settings
from src.signals import Signals
from src.DataManager.DatabaseManager import PlayerQuery
from PySide6.QtSvgWidgets import QSvgWidget


class Ui_MainWindow(QMainWindow):
    def __init__(self, main_window: QMainWindow):
        super().__init__()
        if not main_window.objectName():
            main_window.setObjectName(u"MainWindow")
        main_window.resize(1000, 600)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.central_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 1000, 600))
        self.tab_logging = LoggingDisplay.Display()
        self.tab_logging.set_signals()
        self.handler = DataHandler()
        self.tab_data_lookup = StatsLookup.Display(self.handler.players, self.handler.vehicles, self.handler.squadrons)
        self.tab_search = PVSLookup.LoggingDisplay()
        self.tab_squads = SquadronLookup.LoggingDisplay(self.handler.squadrons)
        self.tab_settings = Settings.LoggingDisplay()
        self.tabWidget.addTab(self.tab_logging, "")
        self.tabWidget.addTab(self.tab_data_lookup, "")
        self.tabWidget.addTab(self.tab_search, "")
        self.tabWidget.addTab(self.tab_squads, "")
        self.tabWidget.addTab(self.tab_settings, "")

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logging), self.tab_logging.name)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data_lookup), self.tab_data_lookup.name)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), self.tab_search.name)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_squads), self.tab_squads.name)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), self.tab_settings.name)
        self.tabWidget.setCurrentIndex(0)
        main_window.setCentralWidget(self.central_widget)

        Signals.signals.sizeSignal.connect(self.resize_event)

    def resize_event(self, width, height):
        self.tabWidget.setGeometry(QRect(0, 0, width, height))


'''
DataClass is a class to be passed to functions in StatsLookup that contain lists with useful info
when new data comes about

'''


class DataHandler:
    def __init__(self):
        self.players = DataClass(None)
        self.vehicles = DataClass(None)
        self.squadrons = DataClass(None)
        self.get = PlayerQuery()
        self.data_update(0)
        Signals.signals.dataChange.connect(self.data_update)

    def data_update(self, num):
        if num in [1, 0]:
            self.players.data = self.get.getPlayerNames()
        if num in [2, 0]:
            self.vehicles.data = self.get.getVehicleNames()
        if num in [3, 0]:
            self.squadrons.data = self.get.getAllSquads()


class DataClass:
    def __init__(self, l):
        self.data = l


class SVGClass(QWidget):
    nation_order = ("USA", "Germany", "Ussr", "Britain", "Japan", "China", "Italy", "France", "Sweden", "Israel")
    normal = [100, 10, 360, 30]
    widthRatio = 1/6

    def r_event(self, rect: QRect):
        dimensions = rect.size()
        width = dimensions.width()/10
        svg_width = width-width*self.widthRatio
        if dimensions.height() < 30:
            svg_width = dimensions.height()
        for index in range(len(self.svgs)):
            self.svgs[index].setGeometry(QRect(width * index, 0, svg_width, svg_width))

    def __init__(self, parent: QWidget, path):
        super().__init__(parent)
        self.svgs = [QSvgWidget(self) for i in range(10)]
        self.show()
        self.path = path
        self.svg_update(self.nation_order)

    def svg_update(self, nations):
        for index, nation in enumerate([*nations, *[None for x in range(10-len(nations))]]):
            svg = self.svgs[index]
            if nation is None:
                svg.hide()
            else:
                svg.load(self.path+f"/country_{nation.lower()}.svg")
                svg.renderer()
                svg.show()

