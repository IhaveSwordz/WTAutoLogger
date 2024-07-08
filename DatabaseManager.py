import sqlite3
import re
import json


class Player:
    def __init__(self, name, vehicle, alive, kills):
        self.name = name
        self.vehicle = vehicle[1:-1]
        self.alive = alive
        self.kills = ''.join(letter for letter in str(kills) if letter not in ["[", "]", " "])

    def __str__(self):
        return f"name: {self.name}| vehicle: {self.vehicle}| alive: {self.alive}| kills: {self.kills}"


def adapt_point(player):
    return f"{player.name};{player.vehicle};{1 if player.alive else 0};{player.kills}"


'''
initilizer and api to the database
'''


class Manager:
    def __init__(self):
        # name of database file
        self.DB = "Data.db"
        # name of storage tables
        self.Battles = "Battles"
        self.Players = "Players"
        self.Vehicles = "Vehicles"
        self.PlayerSize = 0
        self.VehicleSize = 0

        sqlite3.register_adapter(Player, adapt_point)
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
            payload = [x[1] for x in cursor.fetchall()]
            if self.Battles not in payload:
                print("created Battles")
                self.create_battles()
            if self.Players not in payload:
                print("created Players")
                self.create_players()
            else:
                cursor.execute(f"SELECT * FROM {self.Players}")
                self.PlayerSize = len(cursor.fetchall())

            if self.Vehicles not in payload:
                self.create_vehicles()
                print("created Vehicles")
            else:
                cursor.execute(f"SELECT * FROM {self.Vehicles}")
                self.VehicleSize = len(cursor.fetchall())
        # print(self.PlayerSize)
        # print(self.VehicleSize)

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
Team1Tag TEXT(8),
Team2Tag TEXT(8),
Team1PlayerIndexes TEXT(23),
Team2PlayerIndexes TEXT(23),
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
Player15);"""
                cursor.execute(command)
        except Exception as e:
            print(e)

    def create_players(self):
        try:
            with sqlite3.connect(self.DB) as db:
                cursor = db.cursor()
                command = """CREATE TABLE Players (
        id INTEGER(16) PRIMARY KEY,
        name TEXT(16) UNIQUE);"""
                cursor.execute(command)
        except Exception as e:
            print(e)

    def create_vehicles(self):
        try:
            with sqlite3.connect(self.DB) as db:
                cursor = db.cursor()
                command = """CREATE TABLE Vehicles (
        id INTEGER(16) PRIMARY KEY,
        Vehicle TEXT(16) UNIQUE);"""
                cursor.execute(command)
        except Exception as e:
            print(e)

    '''
    method to batch get list of ids for each player, if name not in database automatically adds it
    '''

    def query_players(self, names: list):
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = []
            tba = []
            for name in names:
                cursor.execute(f"SELECT id FROM {self.Players} WHERE name = '{name}'")
                output = cursor.fetchall()
                # print("names: ", name, output)
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
        with sqlite3.connect(self.DB) as db:
            cursor = db.cursor()
            payload = []
            tba = []
            for name in names:
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
            return payload

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
            payload = [(idz + count, name) for idz, name in enumerate(data)]
            print(payload)
            try:
                cursor.executemany(f"INSERT INTO {table} VALUES (?, ?)", payload)
            except sqlite3.InternalError:
                print("ERROR tried to add name to database that was already in it!")
            db.commit()
            # values are only increased after SQL api call to ensure no errors cause fucky wuckys in count
            if table == self.Players:
                self.PlayerSize += len(data)
            elif table == self.Vehicles:
                self.VehicleSize += len(data)

    def addLog(self, battle_json):
        battle = Battle(battle_json, self)
        battle.convert()
        print(battle.Team1Tag, battle.Team2Tag)
        sql_command = f"""INSERT INTO Battles VALUES ('{battle.hash}', '{battle.Team1Tag}', '{battle.Team2Tag}', 
        '{battle.Team1PlayerIndexes}', '{battle.Team2PlayerIndexes}', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
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
    def __init__(self, battle: dict, man: Manager):
        # try:
        self.man: Manager = man
        self.hash = battle["hash"]
        self.Team1Tag = battle["team1Data"]["tag"]
        self.Team2Tag = battle["team2Data"]["tag"]
        self.Team1PlayerIndexes = []
        self.Team2PlayerIndexes = []
        self.players = []
        for player in battle["team1Data"]["players"]:
            pla = battle["players"][player["player"]]
            self.Team1PlayerIndexes.append(player["player"])
            kills = [kill if type(kill) is int else 17 for kill in player["kills"]]
            self.players.append(Player(pla["name"], pla["vehicle"], player["alive"], kills))

        for player in battle["team2Data"]["players"]:
            pla = battle["players"][player["player"]]
            self.Team2PlayerIndexes.append(player["player"])
            kills = [kill if type(kill) is int else 17 for kill in player["kills"]]
            self.players.append(Player(pla["name"], pla["vehicle"], player["alive"], kills))
        # print(self.Team1PlayerIndexes)
        # print(self.Team2PlayerIndexes)
        self.Team1PlayerIndexes = ','.join(
            [str(x) for x in self.Team1PlayerIndexes])
        # print(self.Team1PlayerIndexes)
        self.Team2PlayerIndexes = ','.join(
            [str(x) for x in self.Team2PlayerIndexes])
        # print(self.Team2PlayerIndexes)
        # input()
        # except Exception as e:
        #     print("exception!!! in Battle init")

    #      print(e)

    def convert(self):
        names = []
        vehicles = []
        for player in self.players:
            names.append(player.name)
            vehicles.append(player.vehicle)

        # print(names, vehicles)
        names = self.man.query_players(names)
        vehicles = self.man.query_vehicles(vehicles)
        for name, vehicle, player in zip(names, vehicles, self.players):
            player.name = name
            player.vehicle = vehicle
        for i in range(16 - len(self.players)):
            self.players.append(None)


manager = Manager()
with open("newFile.json", "rb") as f:
    datz: dict = json.load(f)
    for dat in datz["battles"]:
        if manager.validate(dat["hash"]):
            manager.addLog(dat)
        else:
            print(f"that battle with hash {dat["hash"]} already in there dumbass")
