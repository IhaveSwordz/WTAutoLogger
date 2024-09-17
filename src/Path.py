import sys
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


class Path:
    path = Path_u().path
