from PySide6.QtCore import QObject, Signal


class Signals_u(QObject):
    # from bot
     # used to convey current state (waiting, game active, wt not running, error in bot)
    condition = Signal(int)
     # used to communicate internally that there has been an error
    error = Signal(list)
     # used to send data to be displayed
    logs = Signal(dict)
     # sends data to be logged in sql
    sql = Signal(dict)
    # sends data to ui saying current battle conditing (in game, you won, you lost)
    winner = Signal(str)

    # signals used in SquadronLookupDisplay
    # handles connection between the database query function and other shit
    squadron_list = Signal(list)

    # used in converter.py to signify that data has changed / been updated
    # the int signifies what has changed
    dataChange = Signal(int)
    # <English>";"<French>";"<Italian>";"<German>";"<Spanish>";"<Russian>";"<Polish>";"<Czech>";"<Turkish>";"<Chinese>";"<Japanese>";"<Portuguese>";"<Ukrainian>";"<Serbian>";"<Hungarian>";"<Korean>";"<Belarusian>";"<Romanian>";"<TChinese>";"<HChinese>";"<Vietnamese>"
    language = Signal(int)

    # to bot
    data = Signal(int)

    #From data fetcher
    dataSignal = Signal(list)
    SquadronSignal = Signal(list)

    #resizing
    # list containing size change
    sizeSignal = Signal(float, float)

    def __init__(self):
        super().__init__()

# done to make signals globally acessable by allowing everyone to import the initalized class to get signals
# makes it so no need to pass around a class for everyone to use
class Signals:
    signals = Signals_u()
