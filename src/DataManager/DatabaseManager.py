import sqlite3
import json
import time
from venv import logger

from PySide6.QtCore import Signal
import datetime
import collections

import src.DataManager.DataCollector
from src.Path import Path
from src.signals import Signals
from src.DataManager import converter
from src.DebugLogger import Debug

path = Path.path


class Player:
    def __init__(self, name, pid, vehicle, alive, kills):
        self.name = name
        self.pid = pid
        self.vehicle = vehicle
        self.alive = alive
        self.kills = kills

    def update_kills(self, kills):
        for index, k in enumerate(kills):
            try:
                self.kills[index] = k
            except IndexError:
                self.kills.append(k*-1)
                Debug.logger.log("Database Error", f"Overflow of Kills for player {self.name}")

    def team_kill(self, kill):
        self.kills.append(kill)

    def __str__(self):
        return f"name: {self.name}| vehicle: {self.vehicle}| alive: {self.alive}| kills: {self.kills}"


class Time:
    def __init__(self):
        self.utc = datetime.datetime.now(datetime.UTC)
        self.year = self.utc.year
        self.month = self.utc.month
        self.day = self.utc.day
        self.hour = self.utc.hour
        self.minute = self.utc.minute


def adapt_point(player: Player):
    vehicle = player.vehicle if player is not None else -1
    kills = ','.join([str(x) for x in player.kills])
    return f"{player.name};{vehicle};{1 if player.alive else 0};{kills}"


def adapt_point_time(time: Time = None):
    if time is None:
        time = Time()
    return f"{time.year};{time.month};{time.day};{time.hour};{time.minute}"


'''
initilizer and api to the database
'''


class Manager:
    '''
    both of these are used to reduce processing times by being read before querying database
    for functions that need up-to-date name and vehicle info
    by starting it as true it forced the table to always initialize the first time
    '''
    playersUpdated = True
    DB = f"{path}/src/Output/Data.db"
    Debug.logger.log("SQL Manager", DB)

    def __init__(self, ):
        # name of database file
        # name of storage tables
        self.conv = converter.DataGet()
        self.Battles = "Battles"
        self.Players = "Players"
        self.Vehicles = "Vehicles"
        self.PlayerSize = 0
        self.VehicleSize = 0

        sqlite3.register_adapter(Player, adapt_point)
        sqlite3.register_adapter(Time, adapt_point_time)
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            payload = [x[1] for x in cursor.fetchall()]
            if self.Battles not in payload:
                Debug.logger.log("SQL Manager", "created Battles")
                self.create_battles()
            if self.Players not in payload:
                Debug.logger.log("SQL Manager", "created Players")
                self.create_players()
            else:
                cursor.execute(f"SELECT * FROM {self.Players}")
                self.PlayerSize = len(cursor.fetchall())

            if self.Vehicles not in payload:
                self.create_vehicles()
                Debug.logger.log("SQL Manager", "created Vehicles")
            else:
                cursor.execute(f"SELECT * FROM {self.Vehicles}")
                # fetched the current length of all vehicles, used for new vehicle assignment
                self.VehicleSize = len(cursor.fetchall())

    def delete_table(self):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute("DROP TABLE BATTLES")

    '''
    create_battles, create_players, and create_vehicle are core init function that should only execute on very
     first run through, automating creation and setting up of the database on new machines
    '''

    def create_battles(self):
        try:
            with sqlite3.connect(self.DB) as db:
                cursor = db.cursor()
                command = """CREATE TABLE Battles (
Hash TEXT(74) PRIMARY KEY UNIQUE,
Time TEXT(16),
Team1Tag TEXT(8),
Team2Tag TEXT(8),
Player0,
Player1,
Player2,
Player3,
Player4,
Player5,
Player6,
Player7,
Player8,
Player9,
Player10,
Player11,
Player12,
Player13,
Player14,
Player15,
Winner INT(1),
Map TEXT);"""
                cursor.execute(command)
        except Exception as e:
            Debug.logger.log("SQL Manager", f"Exception: {e}")

    def create_players(self):
        try:
            with sqlite3.connect(self.DB) as db:
                cursor = db.cursor()
                command = """CREATE TABLE Players (
        id INTEGER(16) PRIMARY KEY,
        name TEXT(16) UNIQUE,
        pid INTEGER UNIQUE,
        time INTEGER);"""
                cursor.execute(command)
        except Exception as e:
            Debug.logger.log("SQL Manager", f"Exception: {e}")

    def create_vehicles(self):
        try:
            with sqlite3.connect(self.DB) as db:
                cursor = db.cursor()
                command = """CREATE TABLE Vehicles (
        id INTEGER(16) PRIMARY KEY,
        Vehicle TEXT(16) UNIQUE);"""
                cursor.execute(command)
        except Exception as e:
            Debug.logger.log("SQL Manager", f"Exception: {e}")

    '''
    method to batch get list of ids for each player, if name not in database automatically adds it
    '''

    def query_players(self, names: list):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = []
            tba = []
            for name in names:
                if name[0] is None:
                    payload.append(None)
                    continue
                cursor.execute(f"SELECT id FROM {self.Players} WHERE name = '{name[0]}'")
                output = cursor.fetchall()
                if not output and name not in tba:
                    tba.append(name)
                    continue
                payload.extend(output[0])
            if len(tba) > 0:
                self.simple_batch_add(self.Players, tba)
                return self.query_players(names)
            return payload

    '''
    method to batch get player names based on id
    '''

    def query_players_id(self, ids: list):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = []
            for idz in ids:
                cursor.execute(f"SELECT name FROM {self.Players} WHERE id = '{idz}'")
                output = cursor.fetchall()
                payload.extend(output[0])
                if not output:
                    raise Exception(f"attempted to access id out of bounds. id: {idz}, global: {self.PlayerSize}")
            return payload

    '''
    method to batch get list of ids for each vehicle, if name not in database automatically adds it 
    '''

    def query_vehicles(self, names: list):
        # names = [self.conv.query_name(name[:-2]) for name in names] # translates any incoming name to internal name
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = []
            tba = []
            for name in names:
                if name is None:
                    payload.append(None)
                    continue
                cursor.execute(f"SELECT id FROM {self.Vehicles} WHERE Vehicle = '{name}'")
                output = cursor.fetchall()
                if not output:
                    if name not in tba:
                        tba.append(name)
                    continue
                payload.extend(output[0])
            if len(tba) > 0:
                self.simple_batch_add(self.Vehicles, tba)
                return self.query_vehicles(names)
            return payload

    '''
    method to batch get vehicle names based on id
    '''

    def query_vehicles_id(self, ids: list):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = []
            for idz in ids:
                cursor.execute(f"SELECT Vehicle FROM {self.Vehicles} WHERE id = '{idz}'")
                output = cursor.fetchall()
                payload.extend(output[0])
                if not output:
                    raise Exception(f"attempted to access id out of bounds. id: {idz}, global: {self.VehicleSize}")
            return [self.conv.query_id(x) for x in payload]

    """
    method to batch add simple data (player and vehicle) to the database
    @:param table: name of table
    @:param data: a list of items to be added, refers to the self.PlayerSize or self.VehicleSize to determine id
    """

    def simple_batch_add(self, table, data: list):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            count = 0
            if table == self.Players:
                count = self.PlayerSize
            elif table == self.Vehicles:
                count = self.VehicleSize
            try:
                if table == self.Players:
                    unix = time.time().__int__()
                    payload = [(idz + count, name, pid, unix) for idz, (name, pid) in enumerate(data)]
                    Debug.logger.log("SQL Manager", payload)
                    cursor.executemany(f"INSERT INTO {table} VALUES (?, ?, ?, ?)", payload)
                elif table == self.Vehicles:
                    payload = [(idz + count, name) for idz, name in enumerate(data)]
                    Debug.logger.log("SQL Manager", payload)
                    cursor.executemany(f"INSERT INTO {table} VALUES (?, ?)", payload)
                if table == self.Players:
                    self.playersUpdated = True
            except sqlite3.InternalError:

                Debug.logger.log("SQL Manager", "ERROR tried to add name to database that was already in it!")
            db.commit()
            # values are only increased after SQL api call to ensure no errors cause fucky wuckys in count
            if table == self.Players:
                self.PlayerSize += len(data)
                Signals.signals.dataChange.emit(1)
                Signals.signals.dataChange.emit(2)
            elif table == self.Vehicles:
                self.VehicleSize += len(data)
                Signals.signals.dataChange.emit(3)

    def addLog(self, battle_json, player_data):
        battle = Battle(battle_json, player_data, self, self.conv)
        battle.convert()
        sql_command = f"""INSERT INTO Battles VALUES ('{battle.hash}', '{battle.time}', '{battle.Team1Tag}', '{battle.Team2Tag}'
        , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, {battle.winner}, '{None}');
        """
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute(sql_command, battle.players)
            db.commit()

    '''
    checks if a given hash does not match any battle's hash
    returns true if hash not found, else false
    '''

    def validate(self, hash_):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT hash FROM {self.Battles}")
            fetch = [x[0] for x in cursor.fetchall()]
            return hash_ not in fetch


class Battle:
    def __init__(self, battle: dict, player_info, man: Manager, conv):
        # try:
        self.man: Manager = man
        self.hash = battle["hash"]
        self.time = battle["time"]
        self.winner = battle["winner"]
        self.conv = conv

        # year, month, day = self.hash[0:4], self.hash[4:6], self.hash[6:8]
        # self.time = f'{year};{month};{day};;'
        self.Team1Tag = battle["team1Tag"]
        self.Team2Tag = battle["team2Tag"]
        self.Team1PlayerIndexes = []
        self.Team2PlayerIndexes = []
        self.players1_temp = []
        self.players2_temp = []
        # player_list = [*battle["team1Players"], *battle["team2Players"]]
        self.players = []

        for player, p_dict in player_info:
            player: str
            if player.endswith("@live"):
                player = player.replace("@live", "")
            elif player.endswith("@psn"):
                player = player.replace("@psn", "")
            pl = Player(player, p_dict["pid"], None, p_dict["deaths"] == 0,
                        [18 for i in range(p_dict["ground_kills"] + p_dict["air_kills"])])
            if p_dict["tag"] == self.Team1Tag:
                self.players1_temp.append(pl)
            else:
                self.players2_temp.append(pl)

        for player in battle["team1Players"]:
            player: src.DataManager.DataCollector.Player
            pl = None
            if "⋇" in player.name:
                player.name = player.name.replace("⋇", "")
            for p in self.players1_temp:
                if p.name == player.name:
                    pl = p
            if pl is None:
                continue
            self.players1_temp.remove(pl)
            self.players.append(pl)
            name, vehicle, is_dead, kills = player.name, player.vehicle[1:-1], player.dead, player.kills
            if not player.badPlayer:
                team_kill = None
                temp = []
                for kill in kills:
                    if kill in battle["team1Players"]:
                        if kill == player:
                            team_kill = battle["team1Players"].index(kill)
                        else:
                            temp.append(battle["team1Players"].index(kill))

                    elif kill in battle["team2Players"]:
                        if kill == player:
                            team_kill = battle["team2Players"].index(kill)
                        else:
                            temp.append(battle["team2Players"].index(kill) + 8)
                    else:
                        temp.append(17)
                pl.update_kills(temp)

                if team_kill is not None:
                    pl.team_kill(team_kill)
                pl.vehicle = player.vehicle[1:-1]
        self.players.extend(self.players1_temp)
        if len(self.players) != 8:
            self.players.extend([None for i in range(8 - len(self.players))])

        for player in battle["team2Players"]:
            player: src.DataManager.DataCollector.Player

            if "⋇" in player.name:
                player.name = player.name.replace("⋇", "")
            pl = None
            for p in self.players2_temp:
                if p.name == player.name:
                    pl = p
            if pl is None:
                continue
            self.players2_temp.remove(pl)
            self.players.append(pl)
            name, vehicle, is_dead, kills = player.name, player.vehicle[1:-1], player.dead, player.kills
            if not player.badPlayer:
                team_kill = None
                temp = []
                for kill in kills:
                    if kill in battle["team2Players"]:
                        if kill == player:
                            team_kill = battle["team2Players"].index(kill)
                        else:
                            temp.append(battle["team2Players"].index(kill) + 8)
                    elif kill in battle["team1Players"]:
                        if kill == player:
                            team_kill = battle["team1Players"].index(kill)
                        else:
                            temp.append(battle["team1Players"].index(kill))
                    else:
                        temp.append(17)
                pl.update_kills(temp)
                if team_kill is not None:
                    pl.team_kill(team_kill)
                pl.vehicle = player.vehicle[1:-1]
        self.players.extend(self.players2_temp)
        if len(self.players) != 16:
            self.players.extend([None for i in range(16 - len(self.players))])
        return

    def convert(self):
        names = []
        vehicles = []
        for player in self.players:
            if player is None:
                names.append([None, None])
                vehicles.append(None)
                continue
            if player.name is not None:
                names.append([player.name, player.pid])
            else:
                names.append([None, None])
            if player.vehicle is not None:
                vehicles.append(self.conv.query_name(player.vehicle)[:-2])
            else:
                vehicles.append(None)
        if len(self.players) < 16:
            self.players.extend([None for i in range(16 - len(self.players))])

        names = self.man.query_players(names)
        vehicles = self.man.query_vehicles(vehicles)
        for name, vehicle, player in zip(names, vehicles, self.players):
            if player is None:
                continue
            player.name = name
            player.vehicle = vehicle
        # for i in range(16 - len(self.players)):
        #     self.players.append(None)


" a read only class whos use is to query data from the db to be used in UI info"


class PlayerQuery:
    def __init__(self):
        self.DB = Manager.DB
        self.conv = converter.DataGet()
        # name of storage tables
        self.Battles = "Battles"
        self.Players = "Players"
        self.Vehicles = "Vehicles"

    '''
    used as a backend proccess to access database for StatsLookup.py
    data: [player, vehicle, squadron]
    output: [state, [[input data], [pid], [vid]], [[battles hashes], [battles], [[battle index of specified player at i pos]*16]]]
    '''

    def dataLookup(self, data: str, signal: Signal):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            # gets id
            cursor.execute(f"SELECT id FROM {self.Players} WHERE name = '{data[0]}'")
            pid = cursor.fetchall()
            if data[1] == "%":
                vid = [["%"]]
            else:
                cursor.execute(f"SELECT id FROM {self.Vehicles} WHERE vehicle = '{self.conv.query_name(data[1])[:-2]}'")
                vid = cursor.fetchall()
                if len(vid) == 0:
                    signal.emit([-1])
                    return [-1]
            if data[0] == "%":
                pid = [["%"]]
            elif pid.__len__() == 0:
                signal.emit([-1])
                return [-1]


            Debug.logger.log("Lookup Data", f"looking up player: {pid[0][0]}, vehicle: {vid[0][0]}, {data[2]}")
            # this is done so that a players occurnace is place in the index of the list where that player
            # occured, used to help with faster parsing later
            occur = [[], [], [[] for _ in range(16)]]
            for i in range(16):
                cursor.execute(f"select * FROM {self.Battles} WHERE "
                               f"Player{i} LIKE '{pid[0][0]};{vid[0][0]};%;%'"
                               f"AND (Team1Tag LIKE '{data[2]}' or Team2Tag LIKE '{data[2]}')")
                for battle in cursor.fetchall():
                    if battle[0] not in occur[0]:
                        occur[0].append(battle[0])
                        occur[1].append(battle)
                        occur[2][i].append(occur[0].index(battle[0]))
                    else:
                        occur[2][i].append(occur[0].index(battle[0]))
                #reversed the order of the list so most recent battles are processed first
                occur[2][i] = occur[2][i][::-1]
            signal.emit([1, [data, pid, vid], occur])
            return [1, [data, pid, vid], occur]
    def squadLookup(self, squadron: str, signal: Signal):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = [[], []]
            for i in range(2):
                cursor.execute(f"select * FROM {self.Battles} WHERE Team{i + 1}Tag LIKE '{squadron}'")
                payload[i].extend(cursor.fetchall())
            return payload

    ''' 
    converts a db battle with uid and vid into a human readable format (give you the player and vehicle name)
    returns the inpputed battle in the same format with all id's replaced by their db value and semi colons and colons seperated
    '''

    def convert(self, battle):
        payload = []
        [payload.append(x.split(";") if ";" in x else x) for x in battle[0: 4]]
        # [payload.append([int(y) if y != "" else "" for y in x.split(",")]) for x in battle[4:6]]
        players = []
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            for player in battle[4:-2]:
                if player is None or player == "None":
                    players.append(None)
                    continue
                pid, vid, isDead, kills = player.split(";")

                cursor.execute(f"SELECT name FROM {self.Players} WHERE id = '{pid}'")
                player = cursor.fetchall()[0][0]
                if vid != "None":
                    cursor.execute(f"SELECT vehicle FROM {self.Vehicles} WHERE id = '{vid}'")
                    vehicle = cursor.fetchall()[0][0]
                else:
                    vehicle = None
                players.append([player, vehicle, isDead, kills.split(",")])
        payload.extend(players)
        return payload

    '''
    returns a dict containing all player names, only done for seamlessness
    '''

    def getPlayerNames(self):
        payload = {}
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT name FROM {self.Players}")
            temp = cursor.fetchall()
            player_list = {player[0]: 1 for player in temp}
        return player_list

    '''
    returns a list containing all vehicle names with the value equaling appearance
    '''

    def getVehicleNames(self):
        payload = {}
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT vehicle FROM {self.Vehicles}")
            temp = cursor.fetchall()
            vehicle_list = {self.conv.query_id(vehicle[0]): 1 for vehicle in temp}

        return vehicle_list

    '''
    WOMP WOMP
    used to get a list of all squadrons currently in bot
    '''

    def getAllSquads(self):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute((f"select Team1Tag, Team2Tag from {self.Battles}"))
            raw = cursor.fetchall()
        payload = {}
        for tags in raw:
            for tag in tags:
                if tag in payload.keys():
                    payload[tag] += 1
                else:
                    payload.update({tag: 1})
        stuff = {k: v for k, v in sorted(payload.items(), key=lambda item: item[1])}
        sort = collections.OrderedDict(stuff)
        return dict(list(sort.items())[::-1])


if __name__ == "__main__":
    p = PlayerQuery()
    # out = p.s("IhaveSwordz")
    print(p.getAllSquads())
    input()
    # occurs = p.vehicleLookup("2S38")
    # p.convert(occurs[0])
    data = p.squadLookup('%')
    squads = {}
    for dat in data[0]:
        s1, s2 = dat[2], dat[3]
        indz = squads.keys()
        for s in s1, s2:
            if s in indz:
                squads[s] += 1
            else:
                squads.update({s: 1})
    stuff = {k: v for k, v in sorted(squads.items(), key=lambda item: item[1])}

    input()
    with open("../Old/newFile.json", "rb") as f:
        manager = Manager()
        datz: dict = json.load(f)
        for dat in datz["battles"]:
            if manager.validate(dat["hash"]):
                manager.addLog(dat)
            else:
                print(f"that battle with hash {dat['hash']} already in there dumbass")
