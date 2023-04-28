from time import time
import datetime
import sys

from src.common.commons import BColors


class Logger:

    NAME: str
    """The name of the logger"""

    CMDS: str
    """The commands from the system arguments for the logger"""

    def __init__(self, name: str):
        self.NAME = f'[{BColors.BOLD}{name}{BColors.END_C}]'

        if len(sys.argv) > 1:
            self.CMDS = sys.argv[1]
        else:
            self.CMDS = 'el'

    def get_name(self) -> str:
        """
        Returns the name associated to the logger

        :return: The NAME of the logger
        """
        return self.NAME

    def get_commands(self) -> str:
        """
        Returns the commands associated to the logger

        :return: The CMDS of the logger
        """
        return self.CMDS

    def debug(self, text: str) -> None:
        """
        Given the debug format, displays in the terminal the text received

        :param text: The text to display
        """
        if 'd' not in self.CMDS or 'n' in self.CMDS:
            return

        current = datetime.datetime.fromtimestamp(time())
        start = f'{self.NAME}{BColors.WARNING}[{current}][DEBUG]:\t'

        try:
            print(f'{start}{str(text)}{BColors.END_C}')
        except TypeError:
            return

    def error(self, text: str) -> None:
        """
        Given the error format, displays in the terminal the text received

        :param text: The text to display
        """
        if 'n' in self.CMDS:
            return

        current = datetime.datetime.fromtimestamp(time())
        start = f'{self.NAME}{BColors.FAIL}[{current}][ERROR]:\t'

        try:
            print(f'{start}{str(text)}{BColors.END_C}')
        except TypeError:
            return

    def log(self, text: str) -> None:
        """
        Given the log format, displays in the terminal the text received

        :param text: The text to display
        """
        if 'n' in self.CMDS:
            return

        current = datetime.datetime.fromtimestamp(time())
        start = f'{self.NAME}{BColors.OK_GREEN}[{current}][LOG]:\t'

        try:
            print(f'{start}{str(text)}{BColors.END_C}')
        except TypeError:
            return


