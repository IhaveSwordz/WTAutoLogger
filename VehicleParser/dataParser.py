import json

directory = "C:/Users/samue/PycharmProjects/Wt File Reader/War-Thunder-Datamine/char.vromfs.bin_u/config/unittags.blkx"
playz = {

}
'''
with open("battleData.json", "rb") as f:
    data: dict = json.load(f)['battles']
    for battle in data:
        players = battle["players"]
        for player in players:
            if playz.get(player["name"]) is None:
                playz.update({player["name"]: 1})
            else:
                playz[player["name"]] += 1
    print(playz)

with open("battleData.json", "rb") as f:
    data: dict = json.load(f)['battles']
    for battle in data:
        players = battle["players"]
        for player in players:
            print(player["vehicle"][1:-1])
'''
with open(directory, "rb") as f:
    data: dict = json.load(f)
    print(data.keys())