""" configuration modefule for plotbot
"""
from logging import NOTSET
from dotenv import load_dotenv

# load contents of .env variables file
load_dotenv()

LOGFILE_NAME = "plotbot.log"
LOGFILE_LEVEL = NOTSET
