from time import time
import datetime
import sys

class Logger:
    NAME: str
    CMDS: str

    def __init__(self, name: str):
        self.NAME = f'[{bcolors.BOLD}{name}{bcolors.ENDC}]'
        if len(sys.argv) > 1:
            self.CMDS = sys.argv[1]
        else:
            self.CMDS = 'el'

    def get_name(self) -> None:
        print(self.NAME)

    def debug(self, text: str) -> None:
        if 'd' not in self.CMDS or 'n' in self.CMDS: return
        current = datetime.datetime.fromtimestamp(time())
        start = f'{self.NAME}{bcolors.WARNING}[{current}][DEBUG]:\t'
        print(f'{start}{text}{bcolors.ENDC}')

    def error(self, text: str) -> None:
        if 'n' in self.CMDS: return
        current = datetime.datetime.fromtimestamp(time())
        start = f'{self.NAME}{bcolors.FAIL}[{current}][ERROR]:\t'
        print(f'{start}{text}{bcolors.ENDC}')

    def log(self, text: str) -> None:
        if 'n' in self.CMDS: return
        current = datetime.datetime.fromtimestamp(time())
        start = f'{self.NAME}{bcolors.OKGREEN}[{current}][LOG]:\t'
        print(f'{start}{text}{bcolors.ENDC}')



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
