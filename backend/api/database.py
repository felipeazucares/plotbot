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
from api.models import UserDetails, Story


MONGO_DETAILS = os.getenv(key="MONGO_DETAILS")
DEBUG = bool(os.getenv("DEBUG", "False") == "True")
USER_COLLECTION_NAME = os.getenv(key="USER_COLLECTION_NAME")
STORY_COLLECTION_NAME = os.getenv(key="STORY_COLLECTION_NAME")


console_display = ConsoleDisplay()

# ----------------------------------------------------
#           Functions for loading users
# ----------------------------------------------------


class UserStorage:
    """Class providing user retrieval methods"""

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        self.database = self.client.plotbot
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


class StoryStorage:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
        self.database = self.client.fabulator
        self.story_collection = self.database.get_collection(STORY_COLLECTION_NAME)
        self.console_display = ConsoleDisplay()

    async def save_story(self, story: Story) -> str:
        """save the story provided to mongo db

        Args:
            user_id (str): salted hash id for user
            story (Story): wrapper containing userid, date time and tree object containing the story text and structure

        Returns:
            str: id of inserted mongodb document
        """
        self.story = story
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show="save_story(story) called"
            )
        try:
            self.save_response = await self.story_collection.insert_one(
                jsonable_encoder(self.story)
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show="Exception occured writing to the database"
            )
            print(exception_object)
            raise
        try:
            self.new_save = await self.story_collection.find_one(
                {"_id": ObjectId(self.save_response.inserted_id)}
            )
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retriving details for save operation to the database _id: {self.save_response.inserted_id}"
            )
            print(exception_object)
            raise
        return str(ObjectId(self.save_response.inserted_id))

    # async def create_tree(
    #     self, user_id: str, project_id: str, root_node_tag: str
    # ) -> str:
    #     """Create a new tree structure

    #     Args:
    #         user_id (str): salted hash id for user
    #         project_id (str): salted hash id for project
    #         root_node_tag (str): name for root node in the tree

    #     Returns:
    #         str: the id of the newly created tree
    #     """
    #     self.user_id = user_id
    #     self.project_id = project_id
    #     self.root_node_tag = root_node_tag
    #     self.console_display = ConsoleDisplay()
    #     # create the new tree object
    #     try:
    #         self.new_tree = Tree()
    #         self.new_tree.create_node(self.root_node_tag)
    #         self.new_tree.show()
    #     except Exception as e:
    #         self.console_display.show_exception_message(
    #             message_to_show=f"Exception occured creating new tree details for user_id: {self.user_id}"
    #         )
    #         print(e)
    #         raise
    #     # now save it
    #     try:
    #         self.save_response = await self.save_working_tree(
    #             user_id=self.user_id,
    #             project_id=self.project_id,
    #             tree=self.new_tree,
    #         )
    #     except Exception as e:
    #         self.console_display.show_exception_message(
    #             message_to_show=f"Exception occured saving new tree details for user_id: {self.user_id}"
    #         )
    #         print(e)
    #         raise
    #     if DEBUG:
    #         self.console_display.show_debug_message(
    #             message_to_show=f"new_tree_identifier:{self.new_tree.identifier}"
    #         )
    #     return self.new_tree.identifier

    # async def check_tree_exists(self, user_id: str, tree_id: str, project_id) -> bool:
    #     self.user_id = user_id
    #     self.project_id = project_id
    #     self.tree_id = tree_id
    #     self.console_display = ConsoleDisplay()
    #     # see if we can find an object in the tree collection that matchs the parameters
    #     try:
    #         self.last_save = await self.story_collection.find_one(
    #             {
    #                 "user_id": self.user_id,
    #                 "project_id": self.project_id,
    #                 "tree._identifier": tree_id,
    #             },
    #             sort=[("date_time", -1)],
    #         )
    #     except Exception as e:
    #         self.console_display.show_exception_message(
    #             message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
    #         )
    #         print(e)
    #         raise
    #     if self.last_save is not None:
    #         self.tree_was_found = True
    #     else:
    #         self.tree_was_found = False
    #     return self.tree_was_found

    async def list_all_saved_stories(self, user_id: str) -> dict:
        """return a dict of all the saves in the story_collection for supplied user_id"""
        self.user_id = user_id
        self.saves = []
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"list_all_saved_stories({self.user_id}) called"
            )
        try:
            async for save in self.story_collection.find({"user_id": self.user_id}):
                self.saves.append(saves_helper(save))
        except Exception as exception_object:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured reading all database saves to the database user_id {self.user_id}"
            )
            print(exception_object)
            raise
        return self.saves

    async def delete_all_saves(self, user_id: str) -> int:
        """delete all the saved documents in the story_collection for supplied user_id"""
        self.user_id = user_id
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"delete_all_saves({self.user_id}) called"
            )
        try:
            self.delete_result = await self.story_collection.delete_many(
                {"user_id": self.user_id}
            )
            # delete_result object contains a deleted_count & acknowledged properties
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured deleting a save from the database user_id was: {self.user_id}"
            )
            print(e)
            raise
        return self.delete_result.deleted_count

    # async def number_of_saves_for_account(self, user_id: str) -> int:
    #     """return count of save documents in the story_collection for supplied user_id"""
    #     self.user_id = user_id
    #     self.console_display = ConsoleDisplay()
    #     if DEBUG:
    #         self.console_display.show_debug_message(
    #             message_to_show=f"number_of_saves_for_account({self.user_id}) called"
    #         )
    #     try:
    #         self.save_count = await self.story_collection.count_documents(
    #             {"user_id": self.user_id}
    #         )
    #     except Exception as e:
    #         self.console_display.show_exception_message(
    #             message_to_show=f"Exception occured retrieving document count user_id was: {self.user_id}"
    #         )
    #         print(e)
    #         raise
    #     return self.save_count

    async def return_latest_save(self, user_id: str) -> dict:
        """return the latest save document from the story_collection for supplied user_id"""
        self.user_id = user_id
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_latest_save({self.user_id}) called"
            )
        try:
            self.last_save = await self.story_collection.find_one(
                {"user_id": self.user_id}, sort=[("date_time", -1)]
            )

        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
            )
            print(e)
            raise
        if self.last_save is None:
            return None
        else:
            return saves_helper(self.last_save)

    # async def return_latest_save_for_project(self, user_id: str, project_id) -> object:
    #     """Returns the latest save document filtered by user and project ids

    #     Args:
    #         user_id (str): user account id
    #         project_id (str): project identifier

    #     Returns:
    #         saves_helper: object containing the latest save
    #     """
    #     self.user_id = user_id
    #     self.project_id = project_id
    #     self.console_display = ConsoleDisplay()
    #     if DEBUG:
    #         self.console_display.show_debug_message(
    #             message_to_show=f"return_latest_save({self.user_id}) called"
    #         )
    #     try:
    #         self.last_save = await self.story_collection.find_one(
    #             {"user_id": self.user_id, "project_id": self.project_id},
    #             sort=[("date_time", -1)],
    #         )

    #     except Exception as e:
    #         self.console_display.show_exception_message(
    #             message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
    #         )
    #         print(e)
    #         raise
    #     if self.last_save is None:
    #         return None
    #     else:
    #         return saves_helper(self.last_save)

    # async def check_if_document_exists(self, save_id: str) -> int:
    #     """return count of save documents in the story_collection for supplied save_id"""
    #     self.save_id = save_id
    #     self.console_display = ConsoleDisplay()
    #     if DEBUG:
    #         self.console_display.show_debug_message(
    #             message_to_show=f"check_if_document_exists({self.save_id}) called"
    #         )
    #     try:
    #         self.save_count = await self.story_collection.count_documents(
    #             {"_id": ObjectId(self.save_id)}
    #         )
    #     except Exception as e:
    #         self.console_display.show_exception_message(
    #             message_to_show=f"Exception occured retrieving document count save_id was: {self.save_id}"
    #         )
    #         print(e)
    #         raise
    #     return self.save_count

    async def return_save(self, save_id: str) -> dict:
        """return save document from the story_collection for supplied save_id"""
        self.save_id = save_id
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"return_save({self.save_id}) called"
            )
        try:
            self.save = await self.story_collection.find_one(
                {"_id": ObjectId(self.save_id)}
            )
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving save from the database save_id was: {self.save_id}"
            )
            print(e)
            raise
        return saves_helper(self.save)

    async def load_save_into_working_tree(self, save_id: str) -> Tree:
        """return a tree containing the latest saved tree"""
        self.save_id = save_id
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"load_save_into_working_tree({self.save_id}) called"
            )
        try:
            self.save = await self.return_save(save_id=self.save_id)
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.save_id}"
            )
            print(e)
            raise
        # get the tree dict from the saved document
        try:
            self.save_tree = self.save["tree"]
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving tree structure from last save, last_save: {self.save}"
            )
            print(e)
            raise

        return self.build_tree_from_dict(tree_dict=self.save_tree)

    async def load_latest_into_working_tree(self, user_id: str) -> Tree:
        """return a tree containing the latest saved tree"""
        self.user_id = user_id
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"load_latest_into_working_tree({self.user_id}) called"
            )
        try:
            self.last_save = await self.return_latest_save(user_id=self.user_id)
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving latest save from the database user_id was: {self.user_id}"
            )
            print(e)
            raise
        # get the tree dict from the saved document
        if self.last_save:
            try:
                self.last_save_tree = self.last_save["tree"]
                self.tree = self.build_tree_from_dict(tree_dict=self.last_save_tree)
            except Exception as e:
                self.console_display.show_exception_message(
                    message_to_show=f"Exception occured retrieving tree structure from last save, last_save: {self.last_save}"
                )
                print(e)
                raise
        else:
            self.tree = Tree()
        return self.tree

    def build_tree_from_dict(self, tree_dict: dict) -> Tree:
        """return a tree built from provided dict structure"""
        self.tree_dict = tree_dict
        # Looks like there is no root in the subtree
        try:
            self.root_node = self.tree_dict["root"]
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured retrieving root object from dict, self.tree_dict: {self.tree_dict} {e}"
            )
            raise
        # create the root node
        try:
            self.new_tree = Tree(identifier=self.tree_dict["_identifier"])
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occured creating new tree with _identifier:{self.tree_dict['_identifier']} {e}"
            )
            raise

        self.final_tree = self.add_a_node(
            tree_id=self.tree_dict["_identifier"],
            loaded_tree=self.tree_dict,
            new_tree=self.new_tree,
            node_id=self.root_node,
        )
        return self.final_tree

    def add_a_node(self, tree_id, loaded_tree, new_tree, node_id) -> Tree:
        """Traverse the dict in mongo and rebuild the tree a node at a time (recursive)"""
        self.tree_id = tree_id
        self.loaded_tree = loaded_tree
        self.new_tree = new_tree
        self.node_id = node_id
        self.console_display = ConsoleDisplay()
        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"add_a_node() called"
            )

        # get name of node that's been passed to the routine
        try:
            self.name = self.loaded_tree["_nodes"][node_id]["_tag"]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"Current Node is: {self.name}"
                )
        except KeyError as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred unable to find _tag for {self.loaded_tree['_nodes'][node_id]}"
            )
            self.console_display.show_exception_message(
                message_to_show=f"loaded_tree['_nodes'][node_id]['_tag']: {self.loaded_tree['_nodes'][node_id]['_tag']}"
            )
            print(e)
            raise
        # get the id of the current node
        try:
            self.id = self.loaded_tree["_nodes"][node_id]["_identifier"]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"Current id is: {self.id}"
                )
        except KeyError as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred unable to find _identifier for {self.loaded_tree['_nodes'][node_id]}"
            )
            self.console_display.show_exception_message(
                message_to_show=f"loaded_tree['_nodes'][node_id]['_identifier']: {self.loaded_tree['_nodes'][node_id]['_identifier']}"
            )
            print(e)
            raise
        # set payload for new node to what's in the current node
        try:
            self.payload = self.loaded_tree["_nodes"][node_id]["data"]
        except KeyError as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred unable to get node data"
            )
            self.console_display.show_exception_message(
                message_to_show=f"loaded_tree['_nodes'][node_id]['data']: {self.loaded_tree['_nodes'][node_id]['data']}"
            )
            print(e)
            raise

        # for some reason the children of a node are stored under the tree_id key

        try:
            self.children = self.loaded_tree["_nodes"][node_id]["_successors"][tree_id]
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"{self.name}'s children: {self.children}"
                )
        except KeyError:
            # sometimes the _successors field has no key - so if we can't find it set to None
            self.children = None
            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"{self.name}'s children: None"
                )
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred retrieving the _successors field"
            )
            self.console_display.show_exception_message(
                message_to_show=f"id:{self.loaded_tree['_nodes'][node_id]['_identifier']}"
            )
            print(e)
            raise

        if DEBUG:
            self.console_display.show_debug_message(
                message_to_show=f"creating node with - name: {self.name}, identifier: {self.id}"
            )

        try:
            self.new_tree.create_node(
                tag=self.name,
                identifier=self.id,
                parent=self.loaded_tree["_nodes"][node_id]["_predecessor"][tree_id],
                data=self.payload,
            )
        except Exception as e:
            self.console_display.show_exception_message(
                message_to_show=f"Exception occurred adding a node to the working tree."
            )
            self.console_display.show_exception_message(
                message_to_show=f"name: {self.name}, identifier: {self.id}, data: {self.payload}"
            )
            print(e)
            raise

        if self.children != None:

            if DEBUG:
                self.console_display.show_debug_message(
                    message_to_show=f"recursive call"
                )
            for self.child_id in self.children:
                self.add_a_node(
                    tree_id=self.tree_id,
                    loaded_tree=self.loaded_tree,
                    new_tree=self.new_tree,
                    node_id=self.child_id,
                )

        else:
            if DEBUG:
                self.console_display.show_debug_message(message_to_show="base_case")

        return self.new_tree
