import pandas as pd
import json
import os
import sys
# C:/Users/samue/PycharmProjects/WarThunderBattleData/VehicleParser/War-Thunder-Datamine/aces.vromfs.bin_u
path = os.environ["PYTHONPATH"]
# print("SYS: ", sys.path)
tanks = f"{path}/VehicleParser/War-Thunder-Datamine/aces.vromfs.bin_u/gamedata/units/tankmodels"
planes = f"{path}/VehicleParser/War-Thunder-Datamine/aces.vromfs.bin_u/gamedata/flightmodels"
vehicleData = f"{path}/VehicleParser/War-Thunder-Datamine/char.vromfs.bin_u/config/unittags.blkx"
vehicleCost = f"{path}/VehicleParser/War-Thunder-Datamine/char.vromfs.bin_u/config/wpcost.blkx"


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
        # print(self.vData)
        # contains basic info about a vehicle like: type, country, vehicle type, release date
        # name you see in game
        self.name = name
        # internal name
        self.internalName = internal_name
        # directory to the vehicle specific file
        self.directory = None

        # gets the info from vData and vCost for the specific vehicle
        # print(name, internal_name)
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
        return payload

    def __str__(self):
        return f"name: {self.name}; internal name: {self.internalName}; type: {self.type}; vehicle type: {self.vehicleType}; release date: {self.releaseDate}; operator country: {self.country} BR: {self.num_to_BR(self.BR)}"


class DataGet:
    def __init__(self):
        self.nameToIGN = {}
        self.IGNtoname = {}
        with open(vehicleData, "rb") as f:
            dat: dict = json.load(f)
        keys = dat.keys()
        with open("VehicleParser/War-Thunder-Datamine/lang.vromfs.bin_u/lang/units.csv", "r", encoding="utf-8") as f:
            temp = f.read().split("\n")
            data = [[z[1:-1] for z in d.split(";")] for d in temp]
            d = pd.DataFrame(data)
            index = [i for i, val in enumerate(data[0]) if val == "<English>"][0]
            for i in range(1, len(d) - 3):
                if d[index][i] == "" or d[0][i] == "" or "_race_" in d[0][i] or d[0][i][-5:-1] == "_sho" or d[0][i][:11] == "shop/group/" or d[index][i] in ["Medium tank", "Heavy cruiser", "Subchaser", "Boat", "Light\xa0carrier", "Landing\xa0craft", "Light\xa0Cruiser", "Battleship", "Destroyer", "MBT", "SPAA", "Light cruiser", "Light tank", "Light\xa0tank", "SPG", "Infantry tank", "Carrier"] or "_missile_test" in d[0][i]:
                    continue
                if d[0][i][:-2] in keys:
                    self.nameToIGN.update({d[index][i]: d[0][i]})
                    self.IGNtoname.update({d[0][i][0:-2]: d[index][i]})

    '''
    given a vehicle name, will try to find the internal name
    '''
    def query_name(self, name: str):
        new_name = name
        if "\"" in name and name[0] != "\"":
            new_name = ""
            for letter in name:
                if letter == "\"":
                    new_name += "\""
                new_name += letter
        return self.nameToIGN[new_name]
        # return self.nameToIGN.get(new_name)

    '''
    given a internal name, will try and return the info about that vehicle 
    '''

    def query_id(self, name: str):
        return self.IGNtoname[name]


if "__main__" == __name__:
    d = DataGet()
    print(d.query_name("Type 90 (B) \"Fuji\""))
    print("starting")
    print(Vehicle("Tornado ", "tornado_gr1"))
    print(Vehicle("Leopard 2A7V", "germ_leopard_2a7v"))
    print(Vehicle("us_merkava_mk_1", "us_merkava_mk_1"))
