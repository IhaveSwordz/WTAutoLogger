import pandas as pd
import json
import os
# C:/Users/samue/PycharmProjects/WarThunderBattleData/VehicleParser/War-Thunder-Datamine/aces.vromfs.bin_u
tanks = "C:/Users/samue/PycharmProjects/WarThunderBattleData/VehicleParser/War-Thunder-Datamine/aces.vromfs.bin_u/gamedata/units/tankmodels"
planes = "C:/Users/samue/PycharmProjects/WarThunderBattleData/VehicleParser/War-Thunder-Datamine/aces.vromfs.bin_u/gamedata/flightmodels"
vehicleData = "C:/Users/samue/PycharmProjects/WarThunderBattleData/VehicleParser/War-Thunder-Datamine/char.vromfs.bin_u/config/unittags.blkx"
vehicleCost = "C:/Users/samue/PycharmProjects/WarThunderBattleData/VehicleParser/War-Thunder-Datamine/char.vromfs.bin_u/config/wpcost.blkx"

# print("start")


class Vehicle:
    with open(vehicleData, "rb") as f:
        vData: dict = json.load(f)
    with open(vehicleCost, "rb") as f:
        vCost: dict = json.load(f)

    '''
    tags = []

    for key in vData.keys():
        for tag in vData[key]["tags"]:
            if tag not in tags:
                tags.append(tag)
    print(tags)
    '''
    def __init__(self, name, internal_name):
        # contains basic info about a vehicle like: type, country, vehicle type, release date
        # name you see in game
        self.name = name
        # internal name
        self.internalName = internal_name
        # directory to the vehicle specific file
        self.directory = None

        # gets the info from vData and vCost for the specific vehicle
        self.v_data: dict = self.vData[internal_name]
        self.v_cost: dict = self.vCost[internal_name]

        # ex: Fighter, Medium Tank, Bomber, etc...
        self.type = []
        # vehicle type
        self.vehicleType = self.v_data["type"]
        # release date (why is this in the files lmao)
        self.releaseDate = self.v_data.get("releaseDate")
        # operator country as in files
        self.country: str = self.v_cost["country"][8:]

        # battle rating
        self.BR = self.v_cost["economicRankHistorical"]

        for tag in self.v_data["tags"]:
            if self.vehicleType == "aircraft" \
                and tag in ['type_fighter', 'type_jet_fighter', 'type_naval_aircraft', 'type_assault', 'type_strike_ucav','type_strike_aircraft', 'type_interceptor', 'vtol_jet', 'type_utility_helicopter',
                       'type_attack_helicopter', 'type_bomber', 'type_frontline_bomber', 'type_light_bomber',
                       'type_hydroplane', 'type_jet_bomber', 'type_longrange_bomber','type_dive_bomber', 'type_aa_fighter',
                       'hydroplane','nuclear_bomber']:
                self.type.append(tag)
            elif self.vehicleType == "tank" \
                and tag in ['type_medium_tank', 'type_light_tank', 'scout',
                       'type_heavy_tank', 'type_tank_destroyer', 'has_aps', 'type_missile_tank', 'type_spaa']:
                self.type.append(tag)
            elif  self.vehicleType == "ship" \
                    and tag in [
                       'type_armored_boat',
                       'type_heavy_boat', 'type_boat', 'type_torpedo_boat', 'type_gun_boat', 'type_naval_ferry_barge',
                       'type_barge', 'type_torpedo_gun_boat', 'type_destroyer', 'type_minelayer', 'type_naval_aa_ferry',
                       'type_submarine_chaser', 'type_heavy_cruiser', 'type_light_cruiser', 'type_frigate',
                       'type_heavy_gun_boat', 'type_battleship', 'type_battlecruiser', 'light_cruiser']:
                self.type.append(tag)

    def num_to_BR(self, num: int):
        payload = str(int(num/3)+1)
        payload += {0: ".0", 1: ".3", 2 : ".7"}[num%3]
        print(num, payload)
        return payload

    def __str__(self):
        return f"name: {self.name}; internal name: {self.internalName}; type: {self.type}; vehicle type: {self.vehicleType}; release date: {self.releaseDate}; operator country: {self.country} BR: {self.num_to_BR(self.BR)}"


class DataGet:
    def __init__(self):
        self.nameToIGN = {}
        with open("VehicleParser/War-Thunder-Datamine/lang.vromfs.bin_u/lang/units.csv", "r", encoding="utf-8") as f:
            temp = f.read().split("\n")
            data = [[z[1:-1] for z in d.split(";")] for d in temp]
            d = pd.DataFrame(data)
            index = [i for i, val in enumerate(data[0]) if val == "<English>"][0]
            for i in range(1, len(d) - 3):
                # print(d[0][i][-5:-1])
                if d[0][i][-5:-1] == "_sho" or d[0][i][:11] == "shop/group/" or d[index][i] in ["Medium tank", "Heavy cruiser", "Subchaser", "Boat", "Light\xa0carrier", "Landing\xa0craft", "Light\xa0Cruiser", "Battleship", "Destroyer", "MBT", "SPAA", "Light cruiser", "Light tank", "Light\xa0tank", "SPG", "Infantry tank", "Carrier"]:
                    continue
                # print({d[index][i]: d[0][i]})
                self.nameToIGN.update({d[index][i]: d[0][i]})

    '''
    given a vehicle name, will try to find the internal name
    '''
    def query_name(self, name: str):
        return self.nameToIGN.get(name)

    '''
    given a internal name, will try and return the info about that vehicle
    '''


if "__main__" == __name__:
    print("starting")
    print(Vehicle("Tornado ", "tornado_gr1"))
    print(Vehicle("Leopard 2A7V", "germ_leopard_2a7v"))
    print(Vehicle("us_merkava_mk_1", "us_merkava_mk_1"))

'''
    with open("battleData.json", "rb") as z:
        data: dict = json.load(z)['battles']
        dat = DataGet()
        for battle in data:
            players = battle["players"]
            for player in players:
                ret = dat.query_name((player["vehicle"][1:-1]))
                if ret is not None:
                    print(ret[:-2])
                    # print(dat.getData(ret[:-2]))
                    # print(os.path.exists(tanks+f"/{ret[:-2]}.blkx"), " | ", os.path.exists(planes+f"/{ret[:-2]}.blkx"))
                    print(Vehicle(player["vehicle"][1:-1], ret[:-2]))
                else:
                    print(f"failure on query for vehicle name: {player["vehicle"]}")'''