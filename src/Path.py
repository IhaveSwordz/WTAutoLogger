import sys
import os
class Path_u:
    def __init__(self):
        self.path = ""
        self.is_python = False
        self.is_pyinstaller = False
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            print('running in a PyInstaller bundle')
            self.path = '\\'.join(sys.path[0].split("\\")[:-2])
            self.is_pyinstaller = True
        else:
            print('running in a normal Python process')
            self.path = sys.path[0]
            self.is_python = True
        # print(self.path)


class NoFileError(Exception):
    def __init__(self, message, errors = None):
        super().__init__(message)

        self.errors = errors


class Path:
    path = Path_u().path
    settings = path + "/src/Output/settings.json"
    tags = path + "/src/tags.json"

    LOCATIONS_STEAM = [f"{x}SteamLibrary/steamapps/common/War Thunder" for x in os.listdrives()]
    LOCATIONS_STANDARD = []
    # print(LOCATIONS_STEAM)
    PATH = None
    for loc in LOCATIONS_STEAM:
        if os.path.exists(loc):
            PATH = loc

    if PATH is None:
        raise NoFileError(
            f"War Thunder Directory not Found! please put your war thunder directory, (...)/War Thunder, inside {settings}")

    wrpl_path = PATH + "//Replays"
    tag_path = path + "/src/tags.json"
