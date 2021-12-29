""" Database interface module for plotbot.py
"""
import os
import motor.motor_asyncio
from treelib import Tree
from fastapi.encoders import jsonable_encoder
from api.helpers import ConsoleDisplay
from bson.objectid import ObjectId
import datetime
import json
from api.models import UserDetails


MONGO_DETAILS = os.getenv(key="MONGO_DETAILS")
DEBUG = bool(os.getenv("DEBUG", "False") == "True")
USER_COLLECTION_NAME = os.getenv(key="USER_COLLECTION_NAME")


console_display = ConsoleDisplay()

# ----------------------------------------------------
#           Functions for loading users
# ----------------------------------------------------


class UserStorage:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        self.database = self.client.fabulator
        self.user_collection = self.database.get_collection(USER_COLLECTION_NAME)
        self.console_display = ConsoleDisplay()

    async def get_user_details_by_username(self, username: str):
        """return the a user's details given their username - used for log in"""
        self.username = username
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"get_user_details_by_username({self.username}) called"
            )
        try:
            user_deets = await self.user_collection.find_one(
                {"username": self.username}
            )
            if user_deets is not None:
                self.user_details = UserDetails(**user_deets)

            else:
                self.user_details = None
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving user details from the database username was: {self.username}"
            )
            print(exception_object)
            raise
        return self.user_details

    async def get_user_details_by_user_id(self, user_id):
        self.user_id = user_id
        """return the a user's details given their user_id"""
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"get_user_details_by_account({self.user_id}) called"
            )
        try:
            user_deets = await self.user_collection.find_one({"user_id": self.user_id})
            if user_deets is not None:
                self.user_details = UserDetails(**user_deets)
            else:
                self.user_details = None
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving user details from the database user_id was: {self.user_id}"
            )
            print(exception_object)
            raise
        return self.user_details
