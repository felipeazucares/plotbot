""" Helper module containing utility functions for plotbot application
"""
import logging
import datetime
from colorama import Fore, Style
import colorama
from api.config import LOGFILE_NAME, LOGFILE_LEVEL

logging.basicConfig(filename=LOGFILE_NAME, level=LOGFILE_LEVEL)


class ConsoleDisplay:
    """Utility class for logging messages to the console"""

    def __init__(self):
        # Initialise colorama if we're on Windows
        colorama.init()

    def __format_message(self, message_to_show, message_type):
        """format the message provided depending on message_type parameter"""
        self.__message_type = message_type
        self.__message_to_show = message_to_show
        self._dt_date = datetime.datetime.now().strftime("%d/%m/%y %I:%M %S %p")
        if self.__message_type == 1:
            self.__message_to_show = f"{Fore.GREEN}{Style.BRIGHT}{self._dt_date} : {self.__message_to_show} {Style.RESET_ALL}"
            logging.info(self.__message_to_show)
        elif self.__message_type == 2:
            self.__message_to_show = f"{Fore.CYAN}{Style.BRIGHT}{self._dt_date} : DEBUG :{self.__message_to_show} {Style.RESET_ALL}"
            logging.debug(self.__message_to_show)
        elif self.__message_type == 3:
            self.__message_to_show = f"{Fore.RED}{Style.BRIGHT}{self._dt_date} : EXCEPTION :{self.__message_to_show} {Style.RESET_ALL}"
            # self.__message_padding = Fore.RED + "-" * \
            #     (len(self.__message_to_show)-9) + Style.RESET_ALL
            logging.error(self.__message_to_show)
        print(self.__message_to_show)

    def show_message(self, message_to_show: str = None):
        """Format & output standard message along with timestamp"""
        self.__message_to_show = message_to_show
        self.__format_message(message_to_show=self.__message_to_show, message_type=1)

    def show_debug_message(self, message_to_show):
        self.__message_to_show = message_to_show
        """ Format & output debug message along with timestamp"""
        self.__message_to_show = message_to_show
        self.__format_message(message_to_show=self.__message_to_show, message_type=2)

    def show_exception_message(self, message_to_show: str = None):
        """Format & output exception message a long with timestamp"""
        self.__message_to_show = message_to_show
        self.__format_message(message_to_show=self.__message_to_show, message_type=3)
