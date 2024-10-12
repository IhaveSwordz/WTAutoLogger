import re
import os
import json
from datetime import datetime

import src.Path
from src.Path import Path_u


class Player:
    def __init__(self, player):
        self.playerId = player
        self.name = None
        self.tag = b''
        self.data = {}
        self.wl = None

    @staticmethod
    def get_players(players, pl):
        for p in players:
            if pl == p.playerId:
                return p
        p = Player(pl)
        players.append(p)
        return p

    def getPlayer(self):
        return self.bytes_to_int(self.data.get(29))

    def getTeam(self):
        return self.bytes_to_int(self.data.get(23))

    def __str__(self):
        ground_kills = self.data.get(8)
        air_kills = self.data.get(7)
        captures = self.data.get(16)
        deaths = self.data.get(15)
        score = self.data.get(18)
        extra = self.data.get(29)
        # print(self.bytes_to_int(extra))
        # print(ground_kills, air_kills, captures, deaths, score)
        self.name: bytes
        print()
        return f"player: {f"{self.name.decode("utf-8")}":20}; Ground K: {self.bytes_to_int(ground_kills):2}; Air K: {self.bytes_to_int(air_kills):3}; deaths: {self.bytes_to_int(deaths):2}; Caps: {self.bytes_to_int(captures):2}; score: {self.bytes_to_int(score):4}; tag: {self.tag.decode("utf-8")}, {self.name}"

    def getPid(self):
        return str(self.bytes_to_int(self.data.get(29))).encode("utf-8")

    @staticmethod
    def bytes_to_int(he):
        if he is None:
            return 0
        else:
            payload = 0
            for index, val in enumerate(he):
                payload += val * 16 ** (index * 2)
            return payload

    @staticmethod
    def purge(players):
        for pl in players:
            if len(list(pl.data)) != 29:
                players.remove(pl)


class Lookup:
    dir_letters = list(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_/.")
    BUFFER_SIZE = 128
    LEVEL_OFFSET = 0x00000008
    MAP_OFFSET = 0x00000088
    MAP_NAME_OFFSET = 0x0000018C
    BATTLE_ID_OFFSET = 0x000002DC
    BATTLE_BUFFER_SIZE = 12
    DATA_START = b"status"

    def __init__(self, file):
        self.file = file
        self.player_list: list[Player] = []
        # used to determine which team / squadron owns the battle as well as help with showing personal logs
        self.owner_id = None
        self.wl = None

    def get_id(self):
        with open(self.file, "rb") as f:
            x = bytes(f.read())
            data = x[self.BATTLE_ID_OFFSET: self.BATTLE_ID_OFFSET+self.BATTLE_BUFFER_SIZE][::-1]
            data = data.lstrip(b"\x00")
            info = ""
            for d in data:
                temp = str(hex(d))[2:]
                # print(temp, hex(d))
                if len(temp) == 1:
                    info += "0"
                info += temp
            return info
            # print(data)

    def get_time_unix(self):
        with open(self.file, "rb") as f:
            x = bytes(f.read())
            return int.from_bytes(x[0x38c:0x390], byteorder='little')

    def get_map(self):
        with open(self.file, "rb") as f:
            replay = bytes(f.read())
            mission_file = self._get_text(replay[0x88:0x18c], letters=self.dir_letters)
            mission_name = self._get_text(replay[0x18c:0x20c])
            return mission_file + ";" + mission_name

    @staticmethod
    def _get_text(bstring, letters=None):
        # print(bstring)
        """
        from a binary string, return a text string where only the allowed letters are in
        """

        if letters is None:
            letters = list(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_")

        text = ""
        idx = 0
        while (letter := bstring[idx]) in letters and idx < len(bstring):
            text += chr(letter)
            idx += 1
        return text

    @staticmethod
    def _get_info_from_bin(data: bytes):
        payload = {5: data[1:5]}
        data = data[5:]
        for i in range(0, len(data), 8):
            if data[i] > 37:
                return payload
            payload.update({data[i]: data[i+4:i+8]})
        return payload

    def _player_lookup(self, pid) -> Player:
        for player in self.player_list:
            if player.playerId == pid:
                return player
        p = Player(pid)
        self.player_list.append(p)
        return p

    def lookup(self):
        with open(self.file, "rb") as f:
            x = bytes(f.read())
            start = x.find(self.DATA_START)
            end = x[start:].find(b"\x00\x00\x00\x00") + start

            name_stuffs = x[start:end]
            important_stuffs = x[end:]
            if len(list(re.findall(b"__int_", name_stuffs))) != 16:
                return
            if b"fail" in name_stuffs:
                self.wl = 2
            elif b"success" in name_stuffs:
                self.wl = 1
            else:
                self.wl = 0
            important_names = name_stuffs.split(b"__int_")[16].split(b"\x00")
            split = 0
            if b"win64" in important_names and b"macosx" in important_names:
                if important_names.index(b"win64") > important_names.index(b"macosx"):
                    split = important_names.index(b"macosx")
                else:
                    split = important_names.index(b"win64")
            else:
                split = important_names.index(b"win64")
            important_names = important_names[:split][1:]
        data = important_stuffs.split(b"\x00\x00\x05\x00\x00")


        data = data[1:33]
        for d in data:
            out = self._get_info_from_bin(d)
            player = self._player_lookup(out[5])


            player.data.update(out)
        for d in self.player_list:
            print(len(d.data))
            print(d.data)
            if len(d.data) < 30:
                self.player_list.remove(d)
        # if len(self.player_list) > 16:
        #     return

        pids = [str(player.bytes_to_int(player.data.get(29))).encode("utf-8") for player in self.player_list]
        val = 0
        while important_names[val] not in pids:
            val += 1
        player1id = important_names[val]
        self.owner_id = player1id
        pids.remove(player1id)
        val += 1
        tag1 = important_names[val][:important_names[val].find(b" ")]
        player1Name = important_names[val][important_names[val].find(b" ")+1:]
        players = {player1id: [player1Name, tag1]}
        important_names = important_names[val + 1:]
        important_names.remove(tag1)
        important_names.remove(player1Name)
        player2id = None
        tag2 = None
        if __name__ == "__main__":
            src.Path.Path.tag_path = r"C:\Users\samue\PycharmProjects\WTAutoLogger\src\tags.json"
        with open(src.Path.Path.tag_path, "r") as f:
            js = json.load(f)
            for val1 in important_names:
                val = val1.decode("utf-8")
                for index, char in enumerate(js["front"].values()):
                    dec = chr(int(char, 16))
                    if len(val) > 0:
                        if val[0] == dec and chr(int(js["back"][str(index)], 16)) in val[1:]:
                            if 5 <= len(val1.decode("utf-8")) <= 7:
                                print(val1)
                                tag2 = val1
                                important_names.remove(val1)

        print(tag2)
        print(important_names)
        for val in pids:
            index = important_names.index(val)
            player_name = important_names[index-1]
            tag = None
            players.update({val: [player_name, tag]})
        important_1 = None
        important_2 = None
        for pl in self.player_list:
            dat = players[pl.getPid()]
            pl.name = dat[0]
            pl.tag = dat[1]
            if pl.getPid() == player1id:
                important_1 = pl
            elif pl.getPid() == player2id:
                important_2 = pl
        for pl in self.player_list:
            if pl.data.get(23) == important_1.data.get(23):
                pl.tag = important_1.tag
            else:
                pl.tag = tag2

    def get_json(self):
        payload = []
        for player in self.player_list:
            ground_kills = player.bytes_to_int(player.data.get(8))
            air_kills = player.bytes_to_int(player.data.get(7))
            captures = player.bytes_to_int(player.data.get(16))
            deaths = player.bytes_to_int(player.data.get(15))
            payload.append([player.name.decode("utf-8"), {
                "pid": player.getPid().decode("utf-8"),
                "ground_kills": ground_kills,
                "air_kills": air_kills,
                "captures": captures,
                "deaths": deaths,
                "tag": player.tag.decode("utf-8")[1:-1]
            }])
        return payload

    def get_dict(self):
        print(*self.player_list, sep=", ")
        payload = {}
        for player in self.player_list:
            ground_kills = player.bytes_to_int(player.data.get(8))
            air_kills = player.bytes_to_int(player.data.get(7))
            captures = player.bytes_to_int(player.data.get(16))
            deaths = player.bytes_to_int(player.data.get(15))
            payload.update({player.getPid().decode("utf-8"): {
                "name": player.name.decode("utf-8"),
                "ground_kills": ground_kills,
                "air_kills": air_kills,
                "captures": captures,
                "deaths": deaths,
                "tag": player.tag.decode("utf-8")[1:-1]
            }})
        return payload




if __name__ == "__main__":
    # dir = r"D:\SteamLibrary\steamapps\common\War Thunder\Replays\bad1.wrpl"
    # z = Lookup(dir)
    # print(z.get_id())
    # z.lookup()
    # for i in z.player_list:
    #     print(i)
    # 'input()

    base = "D:/SteamLibrary/steamapps/common/War Thunder/Replays"
    for file in os.listdir(base):
        f = base + f"/{file}"
        if f.endswith(".wrpl"):
            z = Lookup(f)
            # print(z.get_id())
            z.lookup()

            print(list(z.get_json()))
            print(z.get_id())
            input()
